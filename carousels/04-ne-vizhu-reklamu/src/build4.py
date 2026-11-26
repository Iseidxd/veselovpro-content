"""Карусель 04: «Я не вижу свою рекламу». Крупный шрифт для телефона."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
CSS4 = CSS + """
.body{font-size:46px;line-height:1.28}
"""
BLUE_BG = "linear-gradient(160deg,#081634 0%,#0B2763 55%,#1440A8 100%)"


def page4(cls, inner, glows="", style=""):
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS4}</style></head>
<body><div class="s {cls}" style="{style}">{glows}<div class="in">{inner}</div></div></body></html>"""


def photo(src, style, mask):
    return (f'<img src="img/{src}" alt="" style="position:absolute;object-fit:cover;filter:saturate(.85) contrast(1.05);'
            f'{style};-webkit-mask-image:{mask};-webkit-mask-composite:source-in">')


slides = {}

# 01 Обложка: тёмная, фото справа
P1 = photo("cover.jpg", "right:-60px;top:0;width:660px;height:1350px;object-position:50% 8%",
           "linear-gradient(to right,transparent 0%,#000 42%),linear-gradient(to bottom,transparent 0%,#000 14%,#000 70%,transparent 100%)")
slides[1] = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS4}</style></head><body>
<div class="s dark">
 <div class="glow" style="top:-280px;left:-260px;width:900px;height:900px;background:radial-gradient(circle,rgba(61,189,163,.38) 0%,rgba(7,16,14,0) 68%)"></div>
 <div class="glow" style="bottom:-360px;left:-200px;width:900px;height:900px;background:radial-gradient(circle,rgba(45,108,246,.34) 0%,rgba(7,16,14,0) 70%)"></div>
 {P1}
 <div class="in" style="gap:0">
  <div style="display:inline-flex;align-self:flex-start;align-items:center;gap:14px;background:rgba(243,245,244,.1);border:1px solid rgba(243,245,244,.25);border-radius:100px;padding:14px 28px">
   <span style="width:12px;height:12px;border-radius:50%;background:{TEAL}"></span>
   <span class="mono" style="font-size:30px;font-weight:500;letter-spacing:.08em;text-transform:uppercase">Разговор с клиентом</span></div>
  <div class="osw" style="margin-top:70px;font-size:200px;line-height:.7;color:{TEAL}">«</div>
  <h1 class="osw" style="margin:0;font-size:116px;line-height:1.02;max-width:640px;text-shadow:0 6px 30px rgba(7,16,14,.8)">Я не вижу свою рекламу</h1>
  <p style="margin-top:44px;font-size:48px;line-height:1.24;color:rgba(243,245,244,.9);max-width:560px;text-shadow:0 2px 20px rgba(7,16,14,.95)">Три фразы, которые я слышу от собственников каждую неделю, и что на них отвечаю.</p>
  <span style="margin-top:auto;font-size:40px;font-weight:600">Листайте →</span>
 </div>
</div></body></html>"""


# Слайды-фразы: одинаковый синий стиль
def quote_slide(n, k, q, sub):
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS4}</style></head><body>
<div class="s" style="background:{BLUE_BG};color:#F3F5F4">
 <div class="glow" style="top:-300px;right:-260px;width:1000px;height:1000px;background:radial-gradient(circle,rgba(61,189,163,.4) 0%,rgba(8,22,52,0) 66%)"></div>
 <div class="in">
  <div class="top"><span class="lab" style="background:{ORANGE};color:#081634">Фраза {k} из 3</span><span class="cnt" style="color:rgba(243,245,244,.6)">{n:02d} / 10</span></div>
  <div style="margin-top:auto;display:flex;flex-direction:column;gap:10px">
   <div class="osw" style="font-size:240px;line-height:.6;color:{ORANGE}">«</div>
   <h2 style="font-size:112px;line-height:1.02">{q}</h2>
  </div>
  <p class="body" style="margin-bottom:auto;color:rgba(243,245,244,.9);margin-top:20px">{sub}</p>
 </div>
</div></body></html>"""


slides[2] = quote_slide(2, 1, "Я вбиваю запрос, а&nbsp;меня нет",
                        "Клиент искал себя вчера, даже в&nbsp;режиме инкогнито, и&nbsp;ничего не&nbsp;нашёл. Значит, реклама не&nbsp;работает?")
slides[5] = quote_slide(5, 2, "Хочу всегда быть первым",
                        "Можно. Только сначала посчитаем, сколько это стоит.")
slides[7] = quote_slide(7, 3, "Конкурент дешевле вдвое и&nbsp;всегда первый",
                        "Клиенты уходят к&nbsp;нему, он везде выше нас.")

# 03 Почему так
def step(n, t, c="#0F7F6B"):
    return f'''<div class="card" style="display:flex;align-items:center;gap:28px;padding:32px 38px">
      <span class="mono" style="font-weight:700;font-size:60px;color:{c};width:60px">{n}</span>
      <span style="font-size:44px;line-height:1.2;font-weight:600">{t}</span></div>'''
slides[3] = page4("light", f"""{top('Почему так', 3)}
<h2>Поисковик (Яндекс и&nbsp;Гугл) прячет вас от&nbsp;вас же</h2>
<div style="display:flex;flex-direction:column;gap:16px">
 {step('1','Вы видите своё объявление')}
 {step('2','И&nbsp;не&nbsp;кликаете, потому что зачем')}
 {step('3','Система решает, что вам не&nbsp;интересно', '#B8401F')}
</div>
<p class="body" style="margin-top:auto">Собственник ищет себя по&nbsp;десять раз в&nbsp;день и&nbsp;первым выпадает из&nbsp;показов.</p>""", LIGHT_GLOWS)

# 04 Что показали, фото с камерой
P4 = photo("camera.jpg", "right:-80px;top:120px;width:620px;height:720px;object-position:55% 30%",
           "linear-gradient(to right,transparent 0%,#000 45%),linear-gradient(to bottom,transparent 0%,#000 15%,#000 60%,transparent 100%)")
slides[4] = page4("dark", f"""{top('Что показали', 4)}
<h2 style="max-width:600px">Первое место по&nbsp;главному запросу</h2>
<div style="display:flex;flex-direction:column;gap:16px;margin-top:auto">
 <div class="card" style="display:flex;align-items:baseline;gap:24px;background:rgba(10,22,19,.9)">
  <span class="mono" style="font-weight:700;font-size:110px;line-height:1;color:{TEAL}">190</span>
  <span style="font-size:42px;line-height:1.2">показов в&nbsp;день</span></div>
 <div class="card" style="display:flex;align-items:baseline;gap:24px;background:rgba(10,22,19,.9)">
  <span class="mono" style="font-weight:700;font-size:110px;line-height:1;color:{TEAL}">85–90%</span>
  <span style="font-size:42px;line-height:1.2">всего спроса</span></div>
</div>
<p class="body">Проверять нужно через диагностику объявлений, а&nbsp;не&nbsp;своим поиском.</p>""", DARK_GLOWS + P4)

# 06 Математика первого места
def mrow(lab, a, b, c):
    return f'''<div style="display:flex;align-items:center;gap:20px;padding:26px 0;border-bottom:1px solid rgba(11,20,18,.12)">
      <span style="font-size:42px;flex:1;font-weight:600">{lab}</span>
      <span class="mono" style="font-size:46px;color:#4C5C58">{a}</span><span class="mono" style="font-size:40px;color:#4C5C58">→</span>
      <span class="mono" style="font-weight:700;font-size:56px;color:{c}">{b}</span></div>'''
slides[6] = page4("light", f"""{top('Математика', 6)}
<h2>Сколько стоит первое место</h2>
<div style="display:flex;flex-direction:column">
 {mrow('Цена клика','×1','×2','#B8401F')}
 {mrow('Конверсия сайта','10%','10%','#0F7F6B')}
 {mrow('Цена заявки','×1','дороже','#B8401F')}
 {mrow('Бюджет на +20–30% заявок','×1','×2','#B8401F')}
</div>
<div class="blk" style="margin-top:auto">
 <p style="font-size:44px;line-height:1.25">Мы предлагаем расти постепенно и&nbsp;держать цену заявки.</p>
</div>""", LIGHT_GLOWS)

# 08 Что мы знаем о конкуренте
def opt(n, t):
    return f'''<div class="card" style="display:flex;gap:26px;align-items:flex-start;padding:34px 38px">
      <span class="mono" style="font-weight:700;font-size:56px;line-height:1;color:{TEAL}">{n}</span>
      <span style="font-size:44px;line-height:1.24">{t}</span></div>'''
slides[8] = page4("dark", f"""{top('Конкурент', 8)}
<h2>Видим только выдачу</h2>
<p class="body">Кабинета и&nbsp;продаж конкурента у&nbsp;нас нет. Обычно за&nbsp;таким стоит одно из&nbsp;двух:</p>
<div style="display:flex;flex-direction:column;gap:16px">
 {opt('А','Тратит фиксированные $5&nbsp;500 в&nbsp;месяц и&nbsp;не&nbsp;считает окупаемость')}
 {opt('Б','Отбивает дорогую заявку повторными продажами за&nbsp;год')}
</div>
<div style="margin-top:auto;border-radius:26px;padding:36px 40px;background:linear-gradient(135deg,rgba(61,189,163,.25),rgba(45,108,246,.18));border:1px solid rgba(243,245,244,.2)">
 <p style="font-size:44px;line-height:1.25;font-weight:600">Работаем от&nbsp;своих цифр, а&nbsp;не&nbsp;от&nbsp;чужой позиции.</p>
</div>""", DARK_GLOWS)

# 09 Свои цифры за день
def num(v, t, c="#0F7F6B"):
    return f'''<div class="card" style="display:flex;flex-direction:column;gap:8px;padding:30px 34px">
      <span class="mono" style="font-weight:700;font-size:76px;line-height:1;color:{c}">{v}</span>
      <span style="font-size:38px;line-height:1.2;color:#1B2725">{t}</span></div>'''
slides[9] = page4("light", f"""{top('Свои цифры', 9)}
<h2>Один день рекламы</h2>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px">
 {num('$67','расход за&nbsp;день')}{num('2','заявки')}
 {num('$0,18','клик в&nbsp;баннерах')}{num('$2,2–3,3','клик в&nbsp;поиске')}
 {num('10%','конверсия сайта')}{num('$28','цена заявки', '#B8401F')}
</div>
<p class="body" style="margin-top:auto">Рабочий коридор заявки $17–33. Вот на&nbsp;что смотреть вместо своей позиции в&nbsp;выдаче.</p>""", LIGHT_GLOWS)

# 10 Финал
def fact(n, t):
    return f'''<div style="background:rgba(10,22,19,.75);border:1px solid rgba(243,245,244,.14);border-radius:20px;padding:28px;display:flex;flex-direction:column;gap:10px">
      <span class="mono" style="font-weight:700;font-size:82px;line-height:1;color:{TEAL}">{n}</span>
      <span style="font-size:36px;line-height:1.2;color:rgba(243,245,244,.85)">{t}</span></div>'''
slides[10] = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS4}</style></head><body>
<div class="s dark">
 <div class="glow" style="bottom:-300px;right:-240px;width:960px;height:960px;background:radial-gradient(circle,rgba(61,189,163,.5) 0%,rgba(61,189,163,.15) 40%,rgba(7,16,14,0) 72%)"></div>
 <div class="glow" style="top:-260px;left:-220px;width:760px;height:760px;background:radial-gradient(circle,rgba(45,108,246,.45) 0%,rgba(7,16,14,0) 70%)"></div>
 <img src="img/final.jpg" alt="" style="position:absolute;right:58px;top:110px;width:360px;height:360px;border-radius:50%;object-fit:cover;object-position:50% 25%;border:3px solid rgba(61,189,163,.5);box-shadow:0 24px 70px rgba(0,0,0,.6)">
 <div class="in" style="justify-content:space-between">
  <div style="display:flex;flex-direction:column;gap:22px;max-width:540px">
   <span class="cap" style="color:{TEAL};font-weight:500;letter-spacing:.1em">Кто это писал</span>
   <h2 style="font-size:86px;line-height:.94">Владимир<br>Веселов</h2>
   <p style="font-size:44px;line-height:1.25;color:rgba(243,245,244,.86)">Разбираю, куда утекает бюджет и&nbsp;почему заявки не&nbsp;превращаются в&nbsp;деньги.</p>
  </div>
  <div style="display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px">{fact('7','лет в перформансе')}{fact('150+','бизнесов через руки')}{fact('9','спецов в команде')}</div>
  <div style="background:linear-gradient(135deg,rgba(61,189,163,.22),rgba(45,108,246,.18));border:1px solid rgba(243,245,244,.18);border-radius:26px;padding:40px;display:flex;flex-direction:column;gap:26px">
   <p style="font-size:44px;line-height:1.25">Разберу вашу ситуацию в&nbsp;телеграме. Ссылка в&nbsp;шапке профиля.</p>
   <div style="display:flex;align-items:center;justify-content:space-between;gap:20px">
    <span class="mono" style="font-size:36px;color:{TEAL}">vveselov.pro</span>
    <span style="background:{TEAL};color:#07100E;font-weight:700;font-size:36px;padding:20px 38px;border-radius:12px;white-space:nowrap">@vv_marketing_bot</span>
   </div>
  </div>
 </div>
</div></body></html>"""

only = [int(a) for a in sys.argv[1:]] or sorted(slides)
with sync_playwright() as p:
    b = p.chromium.launch(executable_path="/usr/bin/google-chrome", args=["--no-sandbox"])
    pg = b.new_page(viewport={"width": 1080, "height": 1350}, device_scale_factor=1)
    for n in only:
        path = os.path.join(HERE, f"s{n:02d}.html")
        open(path, "w", encoding="utf-8").write(slides[n])
        pg.goto("file://" + path)
        pg.evaluate("document.fonts.ready")
        pg.wait_for_timeout(300)
        ov = pg.evaluate("(()=>{const r=document.querySelector('.in');return r?r.scrollHeight-r.clientHeight:0})()")
        pg.screenshot(path=os.path.join(OUT, f"{n:02d}.png"))
        print(n, "overflow", ov)
    b.close()
