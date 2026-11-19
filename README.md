# veselovpro-content

Контент блога @veselovpro и публикатор каруселей в Instagram через Graph API.

## Структура

```
carousels/
  01-proverka-podryadchika/
    slides/01.jpg … 10.jpg   1080×1350, JPEG
    caption.txt               текст под постом
    post.json                 порядок слайдов
    published.json            появляется после публикации, защищает от дубля
publisher/
  publish_ig.py               публикатор, только стандартный Python
  .env.example
.github/workflows/publish-instagram.yml   публикация кнопкой на GitHub
```

Instagram не принимает файлы, он сам скачивает слайды по ссылке. Ссылки идут через jsDelivr с привязкой к коммиту:

```
https://cdn.jsdelivr.net/gh/Iseidxd/veselovpro-content@<коммит>/carousels/01-proverka-podryadchika/slides/01.jpg
```

Привязка к коммиту нужна, чтобы правка слайда задним числом не подменила картинку в уже собранном контейнере.

## Новая карусель

1. Папка `carousels/NN-slug/` с `slides/*.jpg`, `caption.txt` и `post.json` по образцу первой.
2. Коммит и push.
3. `python3 publisher/publish_ig.py check carousels/NN-slug` проверит, что все ссылки отдают JPEG.

## Подключение Instagram, один раз

1. developers.facebook.com → My Apps → Create App → тип Business → продукт Instagram → «API setup with Instagram login».
2. В разделе «Generate access tokens» добавить @veselovpro, войти, выдать права `instagram_business_basic` и `instagram_business_content_publish`. Получится токен на 60 дней.
3. `cp publisher/.env.example publisher/.env`, вставить токен в `IG_ACCESS_TOKEN`.
4. `python3 publisher/publish_ig.py whoami` покажет `IG_USER_ID`, вписать его в `.env`.
5. Для публикации с GitHub: Settings → Secrets and variables → Actions → секреты `IG_ACCESS_TOKEN` и `IG_USER_ID`.

Пока приложение в режиме разработки, публиковать можно только в аккаунты, добавленные в него как тестировщики. Для своего @veselovpro этого достаточно, App Review не нужен.

## Публикация

С ноутбука:

```
python3 publisher/publish_ig.py check   carousels/01-proverka-podryadchika
python3 publisher/publish_ig.py publish carousels/01-proverka-podryadchika --dry-run
python3 publisher/publish_ig.py publish carousels/01-proverka-podryadchika
```

С GitHub: Actions → Publish to Instagram → Run workflow, папка и режим `check`, `dry-run` или `publish`. После публикации workflow сам закоммитит `published.json`.

`--dry-run` создаёт контейнеры у Instagram, но не публикует. Так проверяется, что Meta приняла все 10 картинок и подпись.

## Токен

Живёт 60 дней. Продлевать не реже раза в 50 дней:

```
python3 publisher/publish_ig.py refresh-token
```

Новый токен вставить в `publisher/.env` и в секрет на GitHub. Лимит публикаций в сутки: `python3 publisher/publish_ig.py limit`.
