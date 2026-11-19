#!/usr/bin/env python3
"""Публикация карусели в Telegram-канал альбомом (sendMediaGroup).

  python3 publisher/publish_tg.py check   carousels/01-proverka-podryadchika
  python3 publisher/publish_tg.py publish carousels/01-proverka-podryadchika [--force]

Настройки: TG_BOT_TOKEN и TG_CHAT_ID (например @veselovpro_marketing) в publisher/.env
или в окружении. Файлы уходят в Telegram напрямую, хостинг не нужен.
"""
import argparse
import json
import mimetypes
import os
import sys
import uuid
import urllib.error
import urllib.request
from datetime import datetime, timezone

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from publish_ig import ROOT, env, load_env, load_post  # noqa: E402

CAPTION_LIMIT = 1024  # подпись к альбому в Telegram
PHOTO_LIMIT = 10 * 1024 * 1024


def api(method, fields=None, files=None):
    token = env("TG_BOT_TOKEN", required=True)
    url = f"https://api.telegram.org/bot{token}/{method}"
    boundary = uuid.uuid4().hex
    body = bytearray()
    for k, v in (fields or {}).items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n".encode()
        body += str(v).encode() + b"\r\n"
    for name, path in (files or {}).items():
        ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{name}\"; "
                 f"filename=\"{os.path.basename(path)}\"\r\nContent-Type: {ctype}\r\n\r\n").encode()
        with open(path, "rb") as f:
            body += f.read()
        body += b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=bytes(body), method="POST",
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.loads(r.read())
    except urllib.error.HTTPError as e:
        data = json.loads(e.read() or b"{}")
    if not data.get("ok"):
        sys.exit(f"Telegram {method}: {data.get('error_code')} {data.get('description')}")
    return data["result"]


def validate(abs_folder, post, caption):
    errors = []
    if not 2 <= len(post["slides"]) <= 10:
        errors.append(f"{len(post['slides'])} слайдов, альбом Telegram принимает от 2 до 10")
    if len(caption) > CAPTION_LIMIT:
        errors.append(f"Подпись {len(caption)} символов, у альбома лимит {CAPTION_LIMIT}. "
                      f"Сократи или положи текст для Telegram в caption_tg.txt")
    for s in post["slides"]:
        p = os.path.join(abs_folder, s)
        if not os.path.exists(p):
            errors.append(f"{s}: файла нет")
        elif os.path.getsize(p) > PHOTO_LIMIT:
            errors.append(f"{s}: больше 10 МБ")
    return errors


def tg_caption(abs_folder, caption):
    alt = os.path.join(abs_folder, "caption_tg.txt")
    if os.path.exists(alt):
        with open(alt, encoding="utf-8") as f:
            return f.read().strip()
    return caption


def cmd_check(args):
    abs_folder, rel, post, caption = load_post(args.folder)
    caption = tg_caption(abs_folder, caption)
    errors = validate(abs_folder, post, caption)
    me = api("getMe")
    chat_id = env("TG_CHAT_ID", required=True)
    chat = api("getChat", {"chat_id": chat_id})
    member = api("getChatMember", {"chat_id": chat_id, "user_id": me["id"]})
    can_post = member.get("status") == "creator" or member.get("can_post_messages")
    print(f"Бот @{me['username']}, канал «{chat.get('title')}», статус бота: {member.get('status')}")
    if not can_post:
        errors.append("Бот не может публиковать в канал: сделай его админом с правом «Публикация сообщений»")
    print(f"Слайдов: {len(post['slides'])}, подпись: {len(caption)} символов")
    if errors:
        sys.exit("Ошибки:\n - " + "\n - ".join(errors))
    print("Всё готово к публикации.")


def cmd_publish(args):
    abs_folder, rel, post, caption = load_post(args.folder)
    caption = tg_caption(abs_folder, caption)
    log_path = os.path.join(abs_folder, "published_tg.json")
    if os.path.exists(log_path) and not args.force:
        with open(log_path, encoding="utf-8") as f:
            prev = json.load(f)
        sys.exit(f"Уже опубликовано {prev.get('published_at')}: {prev.get('link')}\nПовторно только с --force")
    errors = validate(abs_folder, post, caption)
    if errors:
        sys.exit("Ошибки:\n - " + "\n - ".join(errors))

    media, files = [], {}
    for i, s in enumerate(post["slides"]):
        key = f"p{i:02d}"
        files[key] = os.path.join(abs_folder, s)
        item = {"type": "photo", "media": f"attach://{key}"}
        if i == 0 and caption:
            item["caption"] = caption
        media.append(item)
    chat_id = env("TG_CHAT_ID", required=True)
    msgs = api("sendMediaGroup", {"chat_id": chat_id, "media": json.dumps(media, ensure_ascii=False)}, files)
    first = msgs[0]
    username = first.get("chat", {}).get("username")
    link = f"https://t.me/{username}/{first['message_id']}" if username else None
    record = {
        "chat_id": chat_id,
        "message_ids": [m["message_id"] for m in msgs],
        "link": link,
        "published_at": datetime.now(timezone.utc).isoformat(),
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Опубликовано: {link or record['message_ids']}")


def main():
    load_env()
    p = argparse.ArgumentParser(description="Публикация карусели в Telegram-канал")
    sub = p.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("check")
    sp.add_argument("folder")
    sp = sub.add_parser("publish")
    sp.add_argument("folder")
    sp.add_argument("--force", action="store_true")
    args = p.parse_args()
    {"check": cmd_check, "publish": cmd_publish}[args.cmd](args)


if __name__ == "__main__":
    main()
