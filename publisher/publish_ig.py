#!/usr/bin/env python3
"""Публикатор каруселей veselovpro в Instagram через Graph API.

Только стандартная библиотека Python 3.9+, ставить ничего не нужно.

Команды:
  python3 publisher/publish_ig.py links   carousels/01-proverka-podryadchika
  python3 publisher/publish_ig.py check   carousels/01-proverka-podryadchika
  python3 publisher/publish_ig.py publish carousels/01-proverka-podryadchika [--force]
  python3 publisher/publish_ig.py whoami
  python3 publisher/publish_ig.py limit
  python3 publisher/publish_ig.py refresh-token

Настройки берутся из переменных окружения или файла publisher/.env (см. .env.example).
"""
import argparse
import json
import os
import struct
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone

REPO = "Iseidxd/veselovpro-content"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAX_ITEMS = 10
MAX_BYTES = 8 * 1024 * 1024


# ---------- настройки ----------

def load_env():
    path = os.path.join(ROOT, "publisher", ".env")
    if os.path.exists(path):
        with open(path, encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def env(name, default=None, required=False):
    val = os.environ.get(name, default)
    if required and not val:
        sys.exit(f"Не задана переменная {name} (publisher/.env или окружение)")
    return val


def api_base():
    host = env("IG_HOST", "graph.instagram.com")
    version = env("IG_API_VERSION", "v26.0")
    return f"https://{host}/{version}"


# ---------- ссылки на слайды ----------

def git_ref():
    ref = env("CONTENT_REF")
    if ref:
        return ref
    try:
        return subprocess.check_output(
            ["git", "-C", ROOT, "rev-parse", "HEAD"], text=True).strip()
    except Exception:
        return "main"


def public_url(rel_path, ref):
    """Ссылка на файл в репозитории.

    По умолчанию jsDelivr: отдаёт image/jpeg и кэширует по коммиту,
    поэтому правка слайда в новом коммите не подменит уже опубликованный пост.
    URL_STYLE=raw переключает на raw.githubusercontent.com.
    """
    rel_path = urllib.parse.quote(rel_path)
    if env("URL_STYLE", "jsdelivr") == "raw":
        return f"https://raw.githubusercontent.com/{REPO}/{ref}/{rel_path}"
    return f"https://cdn.jsdelivr.net/gh/{REPO}@{ref}/{rel_path}"


def load_post(folder):
    folder = os.path.normpath(folder)
    abs_folder = folder if os.path.isabs(folder) else os.path.join(ROOT, folder)
    with open(os.path.join(abs_folder, "post.json"), encoding="utf-8") as f:
        post = json.load(f)
    caption = ""
    if post.get("caption_file"):
        with open(os.path.join(abs_folder, post["caption_file"]), encoding="utf-8") as f:
            caption = f.read().strip()
    rel_folder = os.path.relpath(abs_folder, ROOT).replace(os.sep, "/")
    return abs_folder, rel_folder, post, caption


def jpeg_size(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        length = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + length
    return None


def validate_local(abs_folder, post, caption):
    errors = []
    slides = post.get("slides", [])
    if not 2 <= len(slides) <= MAX_ITEMS:
        errors.append(f"В карусели {len(slides)} слайдов, API принимает от 2 до {MAX_ITEMS}")
    if len(caption) > 2200:
        errors.append(f"Подпись {len(caption)} символов, лимит 2200")
    if caption.count("#") > 30:
        errors.append("Больше 30 хэштегов")
    first_ratio = None
    for s in slides:
        p = os.path.join(abs_folder, s)
        if not os.path.exists(p):
            errors.append(f"{s}: файла нет")
            continue
        if not s.lower().endswith((".jpg", ".jpeg")):
            errors.append(f"{s}: нужен JPEG")
        size = os.path.getsize(p)
        if size > MAX_BYTES:
            errors.append(f"{s}: {size // 1024} КБ, лимит 8 МБ")
        wh = jpeg_size(p)
        if not wh:
            errors.append(f"{s}: не читается как JPEG")
            continue
        ratio = wh[0] / wh[1]
        if not 0.8 - 0.005 <= ratio <= 1.91 + 0.005:
            errors.append(f"{s}: {wh[0]}×{wh[1]}, соотношение вне диапазона 4:5–1,91:1")
        if first_ratio is None:
            first_ratio = ratio
        elif abs(ratio - first_ratio) > 0.01:
            errors.append(f"{s}: соотношение сторон отличается от первого слайда, Instagram обрежет")
    return errors


# ---------- HTTP ----------

def http(method, url, params=None, retries=3):
    data = None
    if params:
        encoded = urllib.parse.urlencode(params)
        if method == "GET":
            url = f"{url}{'&' if '?' in url else '?'}{encoded}"
        else:
            data = encoded.encode()
    for attempt in range(retries):
        req = urllib.request.Request(url, data=data, method=method)
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read()
                return r.status, dict(r.headers), body
        except urllib.error.HTTPError as e:
            body = e.read()
            if e.code >= 500 and attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            return e.code, dict(e.headers), body
        except urllib.error.URLError:
            if attempt < retries - 1:
                time.sleep(3 * (attempt + 1))
                continue
            raise


def graph(method, path, params=None):
    params = dict(params or {})
    params["access_token"] = env("IG_ACCESS_TOKEN", required=True)
    status, _, body = http(method, f"{api_base()}/{path}", params)
    try:
        data = json.loads(body)
    except ValueError:
        data = {"raw": body[:500].decode("utf-8", "replace")}
    if status >= 400 or "error" in data:
        err = data.get("error", data)
        msg = err.get("error_user_msg") or err.get("message") or err
        sys.exit(f"Graph API {method} {path}: {status} {msg}\n{json.dumps(err, ensure_ascii=False)}")
    return data


def wait_finished(container_id, label, timeout=300):
    started = time.time()
    while True:
        st = graph("GET", container_id, {"fields": "status_code,status"})
        code = st.get("status_code")
        if code == "FINISHED":
            return
        if code in ("ERROR", "EXPIRED"):
            sys.exit(f"{label}: контейнер {container_id} в статусе {code}: {st.get('status')}")
        if time.time() - started > timeout:
            sys.exit(f"{label}: контейнер {container_id} не дошёл до FINISHED за {timeout} с")
        time.sleep(3)


# ---------- команды ----------

def cmd_links(args):
    abs_folder, rel, post, _ = load_post(args.folder)
    ref = git_ref()
    for s in post["slides"]:
        print(public_url(f"{rel}/{s}", ref))


def cmd_check(args):
    abs_folder, rel, post, caption = load_post(args.folder)
    errors = validate_local(abs_folder, post, caption)
    ref = git_ref()
    print(f"Коммит: {ref}")
    for s in post["slides"]:
        url = public_url(f"{rel}/{s}", ref)
        try:
            status, headers, body = http("GET", url)
        except Exception as e:
            errors.append(f"{s}: {url} недоступен ({e})")
            continue
        ctype = {k.lower(): v for k, v in headers.items()}.get("content-type", "")
        ok = status == 200 and ctype.startswith("image/jpeg") and body[:2] == b"\xff\xd8"
        print(f"{'OK ' if ok else 'ERR'} {status} {ctype:<12} {len(body) // 1024:>5} КБ  {url}")
        if not ok:
            errors.append(f"{s}: по ссылке не JPEG (HTTP {status}, {ctype}). Коммит запушен?")
    print(f"Подпись: {len(caption)} символов")
    if errors:
        print("\nОшибки:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("\nВсё готово к публикации.")


def cmd_publish(args):
    abs_folder, rel, post, caption = load_post(args.folder)
    log_path = os.path.join(abs_folder, "published.json")
    if os.path.exists(log_path) and not args.force:
        with open(log_path, encoding="utf-8") as f:
            prev = json.load(f)
        sys.exit(f"Уже опубликовано {prev.get('published_at')}: {prev.get('permalink')}\n"
                 f"Повторно только с --force")
    errors = validate_local(abs_folder, post, caption)
    if errors:
        sys.exit("Локальная проверка не прошла:\n - " + "\n - ".join(errors))

    ig_user = env("IG_USER_ID", required=True)
    ref = git_ref()
    urls = [public_url(f"{rel}/{s}", ref) for s in post["slides"]]
    print(f"Публикую «{post.get('title', rel)}», {len(urls)} слайдов, коммит {ref[:10]}")

    children = []
    for i, url in enumerate(urls, 1):
        res = graph("POST", f"{ig_user}/media", {"image_url": url, "is_carousel_item": "true"})
        children.append(res["id"])
        print(f"  слайд {i:02d} -> контейнер {res['id']}")
    for i, cid in enumerate(children, 1):
        wait_finished(cid, f"слайд {i:02d}")

    parent = graph("POST", f"{ig_user}/media", {
        "media_type": "CAROUSEL",
        "children": ",".join(children),
        "caption": caption,
    })["id"]
    print(f"  карусель -> контейнер {parent}")
    wait_finished(parent, "карусель")

    if args.dry_run:
        print("--dry-run: контейнеры созданы, media_publish не вызывался. "
              "Контейнер живёт 24 часа и потом удаляется сам.")
        return

    media_id = graph("POST", f"{ig_user}/media_publish", {"creation_id": parent})["id"]
    info = graph("GET", media_id, {"fields": "permalink,timestamp"})
    record = {
        "media_id": media_id,
        "permalink": info.get("permalink"),
        "published_at": info.get("timestamp") or datetime.now(timezone.utc).isoformat(),
        "commit": ref,
        "slides": urls,
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Опубликовано: {record['permalink']}")
    print(f"Лог: {os.path.relpath(log_path, ROOT)} (закоммить, чтобы не опубликовать дважды)")


def cmd_whoami(args):
    if "graph.facebook.com" in api_base():
        data = graph("GET", "me/accounts", {"fields": "name,instagram_business_account{id,username}"})
        for page in data.get("data", []):
            iba = page.get("instagram_business_account")
            if iba:
                print(f"Страница «{page['name']}»: IG_USER_ID={iba['id']} (@{iba.get('username')})")
    else:
        data = graph("GET", "me", {"fields": "user_id,username,account_type"})
        print(f"@{data.get('username')} ({data.get('account_type')}): IG_USER_ID={data.get('user_id')}")


def cmd_limit(args):
    ig_user = env("IG_USER_ID", required=True)
    data = graph("GET", f"{ig_user}/content_publishing_limit", {"fields": "config,quota_usage"})
    print(json.dumps(data, ensure_ascii=False, indent=2))


def cmd_refresh(args):
    token = env("IG_ACCESS_TOKEN", required=True)
    if "graph.facebook.com" in api_base():
        params = {
            "grant_type": "fb_exchange_token",
            "client_id": env("FB_APP_ID", required=True),
            "client_secret": env("FB_APP_SECRET", required=True),
            "fb_exchange_token": token,
        }
        status, _, body = http("GET", f"{api_base()}/oauth/access_token", params)
    else:
        params = {"grant_type": "ig_refresh_token", "access_token": token}
        status, _, body = http("GET", "https://graph.instagram.com/refresh_access_token", params)
    data = json.loads(body)
    if status >= 400 or "access_token" not in data:
        sys.exit(f"Не удалось продлить токен: {data}")
    days = int(data.get("expires_in", 0)) // 86400
    print(f"Новый токен, живёт {days} дн. Вставь в publisher/.env и в секрет IG_ACCESS_TOKEN на GitHub:")
    print(data["access_token"])


def main():
    load_env()
    p = argparse.ArgumentParser(description="Публикатор каруселей veselovpro в Instagram")
    sub = p.add_subparsers(dest="cmd", required=True)
    for name in ("links", "check"):
        sp = sub.add_parser(name)
        sp.add_argument("folder")
    sp = sub.add_parser("publish")
    sp.add_argument("folder")
    sp.add_argument("--force", action="store_true", help="публиковать, даже если есть published.json")
    sp.add_argument("--dry-run", action="store_true", help="создать контейнеры, но не публиковать")
    sub.add_parser("whoami")
    sub.add_parser("limit")
    sub.add_parser("refresh-token")
    args = p.parse_args()
    {
        "links": cmd_links, "check": cmd_check, "publish": cmd_publish,
        "whoami": cmd_whoami, "limit": cmd_limit, "refresh-token": cmd_refresh,
    }[args.cmd](args)


if __name__ == "__main__":
    main()
