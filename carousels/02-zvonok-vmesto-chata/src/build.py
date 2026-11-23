"""Карусель 02: генерация HTML-слайдов в стиле карусели 01 и рендер в JPEG."""
import os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
os.makedirs(OUT, exist_ok=True)

TEAL = "#3DBDA3"
BLUE = "#2D6CF6"
ORANGE = "#FF8A5B"

CSS = f"""
@font-face{{font-family:Oswald;src:url(fonts/Oswald.ttf);font-weight:200 700}}
@font-face{{font-family:Golos;src:url(fonts/Golos.ttf);font-weight:400 900}}
@font-face{{font-family:JBM;src:url(fonts/JBMono.ttf);font-weight:100 800}}
*{{box-sizing:border-box}}
body{{margin:0}}
.s{{position:relative;width:1080px;height:1350px;overflow:hidden;font-family:Golos,sans-serif}}
.dark{{background:#07100E;color:#F3F5F4}}
.light{{background:linear-gradient(170deg,#FFFFFF 0%,#EAF4F1 60%,#DCEDE8 100%);color:#0B1412}}
.glow{{position:absolute;border-radius:50%}}
.in{{position:relative;height:100%;padding:72px;display:flex;flex-direction:column;gap:38px}}
.mono{{font-family:JBM,monospace;font-variant-numeric:tabular-nums}}
.osw{{font-family:Oswald,sans-serif;font-weight:700;text-transform:uppercase}}
h2{{margin:0;font-family:Oswald,sans-serif;font-weight:700;font-size:90px;line-height:.96;text-transform:uppercase}}
.top{{display:flex;align-items:center;justify-content:space-between}}
.cnt{{font-family:JBM,monospace;font-size:34px;font-weight:700;letter-spacing:.06em}}
.dark .cnt{{color:rgba(243,245,244,.55)}}
.light .cnt{{color:#4C5C58}}
.lab{{font-family:Oswald,sans-serif;font-weight:700;font-size:44px;letter-spacing:.04em;text-transform:uppercase;padding:14px 30px;border-radius:12px}}
.dark .lab{{background:{TEAL};color:#07100E}}
.light .lab{{background:#0B1412;color:#fff}}
p{{margin:0}}
.body{{font-size:44px;line-height:1.28}}
.dark .body{{color:rgba(243,245,244,.88)}}
.light .body{{color:#1B2725}}
.card{{border-radius:26px;padding:36px 40px}}
.dark .card{{background:rgba(10,22,19,.8);border:1px solid rgba(243,245,244,.16)}}
.light .card{{background:#fff;box-shadow:0 20px 50px rgba(11,20,18,.1)}}
.blk{{background:#0B1412;color:#F3F5F4;border-radius:26px;padding:36px 40px}}
.cap{{font-family:JBM,monospace;font-size:30px;font-weight:700;letter-spacing:.08em;text-transform:uppercase}}
"""

def page(cls, inner, glows=""):
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head>
<body><div class="s {cls}">{glows}<div class="in">{inner}</div></div></body></html>"""

DARK_GLOWS = f"""
<div class="glow" style="top:-300px;right:-240px;width:900px;height:900px;background:radial-gradient(circle,rgba(61,189,163,.42) 0%,rgba(7,16,14,0) 68%)"></div>
<div class="glow" style="bottom:-380px;left:-280px;width:900px;height:900px;background:radial-gradient(circle,rgba(45,108,246,.36) 0%,rgba(7,16,14,0) 70%)"></div>"""
LIGHT_GLOWS = """<div class="glow" style="top:-220px;right:-180px;width:700px;height:700px;background:radial-gradient(circle,rgba(61,189,163,.5) 0%,rgba(234,244,241,0) 70%)"></div>"""

def top(label, n):
    return f'<div class="top"><span class="lab">{label}</span><span class="cnt">{n:02d} / 10</span></div>'

PHONE = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.8 19.8 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6A19.8 19.8 0 0 1 2.12 4.18 2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.13.96.36 1.9.7 2.81a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45c.91.34 1.85.57 2.81.7A2 2 0 0 1 22 16.92z"/></svg>'
CHAT = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>'
CHECK = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6 9 17l-5-5"/></svg>'
SEARCH = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="{c}" stroke-width="2.5" stroke-linecap="round" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>'

def ico(t, s, c):
    return t.replace("{s}", str(s)).replace("{c}", c)

slides = {}

# 01 Обложка: светлая, интерфейс вместо портрета
bubbles = ""
offs = [(0, 1.0), (70, .7), (24, .42)]
for i, (dx, op) in enumerate(offs):
    bubbles += f'''<div style="align-self:flex-start;margin-left:{dx}px;opacity:{op};display:flex;align-items:center;gap:16px;background:#fff;border-radius:28px 28px 28px 8px;padding:20px 30px;box-shadow:0 14px 34px rgba(11,20,18,.1)">
      {ico(CHAT,34,'#8A9894')}<span style="font-size:36px;color:#35423F;white-space:nowrap">Сколько стоит?</span></div>'''
slides[1] = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="s light">
 <div class="glow" style="top:-260px;right:-260px;width:1000px;height:1000px;background:radial-gradient(circle,rgba(61,189,163,.55) 0%,rgba(234,244,241,0) 68%)"></div>
 <div class="glow" style="bottom:-340px;left:-300px;width:900px;height:900px;background:radial-gradient(circle,rgba(45,108,246,.22) 0%,rgba(234,244,241,0) 70%)"></div>
 <div style="position:absolute;right:60px;top:640px;width:440px;display:flex;flex-direction:column;gap:18px">{bubbles}</div>
 <div style="position:absolute;right:120px;bottom:150px;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(61,189,163,.55) 0%,rgba(61,189,163,0) 70%)"></div>
 <div style="position:absolute;right:170px;bottom:200px;width:200px;height:200px;border-radius:50%;background:{TEAL};display:flex;align-items:center;justify-content:center;box-shadow:0 30px 70px rgba(15,127,107,.45),0 0 0 18px rgba(61,189,163,.22),0 0 0 40px rgba(61,189,163,.1)">{ico(PHONE,92,'#07100E')}</div>
 <div class="in" style="gap:0">
  <div style="display:inline-flex;align-self:flex-start;align-items:center;gap:14px;background:#0B1412;color:#fff;border-radius:100px;padding:14px 28px">
    <span style="width:12px;height:12px;border-radius:50%;background:{TEAL}"></span>
    <span class="mono" style="font-size:30px;font-weight:500;letter-spacing:.08em;text-transform:uppercase">Разбор</span></div>
  <h1 class="osw" style="margin:56px 0 0;font-size:96px;line-height:1.12">Заявки подорожали<br><span style="display:inline-block;line-height:1.02;background:{TEAL};color:#07100E;padding:4px 16px 2px;border-radius:12px">втрое</span>, а&nbsp;реклама<br>окупилась</h1>
  <p style="margin-top:40px;font-size:46px;line-height:1.24;color:#1B2725;max-width:430px">Одна правка в объявлении. Бюджет тот же.</p>
  <div style="margin-top:auto;display:flex;flex-direction:column;align-items:flex-start;gap:22px">
   <div style="background:#0B1412;color:#F3F5F4;border-radius:24px;padding:26px 34px;box-shadow:0 24px 60px rgba(11,20,18,.3);display:flex;flex-direction:column;gap:16px">
    <div style="display:flex;align-items:center;gap:22px"><span class="mono" style="font-size:30px;letter-spacing:.06em;text-transform:uppercase;color:rgba(243,245,244,.6);width:150px">Заявка</span>
     <span class="mono" style="font-weight:700;font-size:60px;line-height:1;color:{ORANGE}">$2,8</span><span class="mono" style="font-size:44px;color:rgba(243,245,244,.5)">→</span><span class="mono" style="font-weight:700;font-size:60px;line-height:1;color:{ORANGE}">$8,9</span></div>
    <div style="height:1px;background:rgba(243,245,244,.16)"></div>
    <div style="display:flex;align-items:center;gap:22px"><span class="mono" style="font-size:30px;letter-spacing:.06em;text-transform:uppercase;color:rgba(243,245,244,.6);width:150px">ROMI</span>
     <span class="mono" style="font-weight:700;font-size:60px;line-height:1;color:{TEAL}">150%</span></div>
   </div>
   <span style="font-size:38px;font-weight:600;color:#1B2725">Листайте →</span>
  </div>
 </div>
</div></body></html>"""

# 02 Ситуация, с фото
def stat(num, txt, color):
    return f'''<div class="card" style="display:flex;align-items:center;gap:22px;padding:24px 30px;backdrop-filter:blur(8px)">
      <span class="mono" style="font-weight:700;font-size:72px;line-height:1;color:{color};min-width:170px">{num}</span>
      <span style="font-size:34px;line-height:1.2;color:rgba(243,245,244,.85)">{txt}</span></div>'''
PHOTO2 = f"""
<img src="img/chin.jpg" alt="" style="position:absolute;right:-60px;top:420px;width:640px;height:760px;object-fit:cover;object-position:50% 18%;filter:saturate(.85) contrast(1.05);-webkit-mask-image:linear-gradient(to right,transparent 0%,#000 45%),linear-gradient(to bottom,transparent 0%,#000 22%,#000 62%,transparent 100%);-webkit-mask-composite:source-in;mask-composite:intersect">"""
slides[2] = page("dark", f"""{top('Ситуация', 2)}
<h2>Всё выглядит<br>нормально</h2>
<p class="body" style="max-width:560px">Люди пишут, спрашивают про услугу и&nbsp;цену. Объявления живые.</p>
<div style="display:flex;flex-direction:column;gap:16px;width:540px">
 {stat('$2,8','за заявку, ниже рынка',TEAL)}{stat('80','сообщений в месяц',TEAL)}{stat('1/20','доходит до&nbsp;сервиса',ORANGE)}
</div>
<div class="card" style="margin-top:auto;display:flex;gap:28px;align-items:center;background:linear-gradient(135deg,rgba(255,138,91,.2),rgba(10,22,19,.92));border-color:rgba(255,138,91,.4)">
 <span class="mono" style="font-weight:700;font-size:96px;line-height:1;color:{ORANGE}">5%</span>
 <span style="font-size:42px;line-height:1.25">заявок превращаются в приход клиента</span>
</div>""", DARK_GLOWS + PHOTO2)

# 03 Воронка до
def bar(label, num, w, bg, fg="#fff"):
    return f'''<div style="width:{w}%;background:{bg};color:{fg};border-radius:18px;padding:26px 32px;display:flex;justify-content:space-between;align-items:center">
      <span style="font-size:38px;font-weight:600">{label}</span><span class="mono" style="font-weight:700;font-size:56px">{num}</span></div>'''
def money(num, lab, color, sub):
    return f'''<div class="card" style="display:flex;flex-direction:column;gap:10px;padding:30px 34px;border-top:6px solid {color}">
      <span class="mono" style="font-weight:700;font-size:96px;line-height:1;color:{color}">{num}</span>
      <span style="font-size:36px;color:#35423F">{lab}</span>{sub}</div>'''
slides[3] = page("light", f"""{top('До', 3)}
<h2>На $222<br>в месяц</h2>
<div style="display:flex;flex-direction:column;gap:16px">
 {bar('Сообщений', '80', 100, '#0B1412')}
 {bar('Пришли', '4', 34, '#B8401F')}
</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px">
 {money('$2,8','за заявку','#0F7F6B','')}{money('$55','за клиента','#B8401F','')}
</div>
<p class="body" style="margin-top:auto">Подрядчик отчитывается про <b>$2,8</b>, а&nbsp;собственник платит <b style="color:#B8401F">$55</b>.</p>""", LIGHT_GLOWS)

# 04 Где искали
def row_ok(t):
    return f'''<div class="card" style="display:flex;align-items:center;gap:26px;padding:28px 34px">
      <span style="width:62px;height:62px;border-radius:16px;background:rgba(61,189,163,.16);display:flex;align-items:center;justify-content:center;flex:none">{ico(CHECK,36,TEAL)}</span>
      <span style="font-size:40px">{t}</span></div>'''
slides[4] = page("dark", f"""{top('Поиск причины', 4)}
<h2>Проверили всё,<br>кроме главного</h2>
<div style="display:flex;flex-direction:column;gap:16px">
 {row_ok('Объявления живые')}{row_ok('Цена по рынку')}{row_ok('Менеджеры отвечают быстро')}
</div>
<div style="margin-top:auto;border-radius:26px;padding:40px;background:linear-gradient(135deg,rgba(61,189,163,.22),rgba(45,108,246,.18));border:1px solid rgba(243,245,244,.2);display:flex;flex-direction:column;gap:20px">
 <div style="display:flex;align-items:center;gap:18px">{ico(SEARCH,44,TEAL)}<span class="cap" style="color:{TEAL}">Сведение рекламы с CRM</span></div>
 <p style="font-size:46px;line-height:1.25;font-weight:600">Почти все заявки были сообщениями в&nbsp;чат.</p>
</div>""", DARK_GLOWS)

# 05 Причина
firms = ["Сервис на Лесной", "Автотехцентр 24", "Мастерская у дома", "Сервис «Гараж»", "Бокс №7", "Ремзона"]
rows = ""
for i, f in enumerate(firms):
    rows += f'''<div style="display:flex;align-items:center;gap:22px;padding:14px 26px;background:#fff;border-radius:20px;box-shadow:0 10px 26px rgba(11,20,18,.08)">
      <span style="width:58px;height:58px;border-radius:50%;background:#DCEDE8;color:#0B5F50;display:flex;align-items:center;justify-content:center;font-weight:700;font-size:28px;flex:none">{f.replace('Сервис «','').replace('Сервис ','')[0] if False else f[0]}</span>
      <div style="display:flex;flex-direction:column;gap:2px;min-width:0"><span style="font-size:30px;font-weight:600;color:#0B1412">{f}</span><span style="font-size:28px;color:#4C5C58">Вы: Сколько стоит?</span></div>
      <span class="mono" style="margin-left:auto;font-size:24px;color:#4C5C58">12:0{i}</span></div>'''
slides[5] = page("light", f"""{top('Причина', 5)}
<h2>Написать стоит<br>пять секунд</h2>
<div style="display:flex;flex-direction:column;gap:10px">{rows}</div>
<p class="body" style="margin-top:auto;font-size:40px">Человек отправляет «сколько стоит?» в&nbsp;шесть мест сразу и&nbsp;ждёт, кто ответит дешевле. Записываться он пока не&nbsp;собирается.</p>""", LIGHT_GLOWS)

# 06 Что сделали
slides[6] = page("dark", f"""{top('Решение', 6)}
<h2>Убрали кнопку<br>«Написать»</h2>
<div style="display:flex;flex-direction:column;gap:26px;margin-top:20px">
 <div style="position:relative;display:flex;align-items:center;justify-content:center;gap:24px;height:150px;border-radius:28px;border:3px dashed rgba(243,245,244,.25);color:rgba(243,245,244,.35)">
  {ico(CHAT,56,'rgba(243,245,244,.35)')}<span class="osw" style="font-size:60px;font-weight:500">Написать</span>
  <div style="position:absolute;left:60px;right:60px;top:50%;height:6px;background:{ORANGE};border-radius:3px;transform:rotate(-6deg)"></div>
 </div>
 <div style="display:flex;align-items:center;justify-content:center;gap:26px;height:190px;border-radius:28px;background:{TEAL};color:#07100E;box-shadow:0 30px 80px rgba(61,189,163,.35),0 0 0 14px rgba(61,189,163,.14)">
  {ico(PHONE,72,'#07100E')}<span class="osw" style="font-size:78px">Позвонить</span>
 </div>
</div>
<div class="card" style="margin-top:auto;display:flex;flex-direction:column;gap:14px">
 <span class="cap" style="color:{TEAL}">Не трогали</span>
 <p style="font-size:44px;line-height:1.25">Бюджет, объявления и&nbsp;цены остались прежними.</p>
</div>""", DARK_GLOWS)

# 07 После
slides[7] = page("light", f"""{top('После', 7)}
<h2>Те же $222</h2>
<div style="display:flex;flex-direction:column;gap:16px">
 {bar('Звонков', '25', 100, '#0B1412')}
 {bar('Записались', '10', 66, '#0F7F6B')}
 {bar('Уже пришли', '6', 46, TEAL, '#07100E')}
</div>
<div style="display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:24px">
 {money('$8,9','за звонок','#B8401F','')}{money('$37','за клиента','#0F7F6B','<span style="font-size:30px;color:#4C5C58">было $55</span>')}
</div>
<p class="body" style="margin-top:auto">Ещё <b>4 человека</b> записаны на&nbsp;следующие даты.</p>""", LIGHT_GLOWS)

# 08 Итог, с фото
GLOWS8 = """
<div class="glow" style="top:-200px;left:-260px;width:1000px;height:900px;background:radial-gradient(circle,rgba(61,189,163,.32) 0%,rgba(7,16,14,0) 66%)"></div>
<div class="glow" style="bottom:-380px;left:-280px;width:900px;height:900px;background:radial-gradient(circle,rgba(45,108,246,.36) 0%,rgba(7,16,14,0) 70%)"></div>"""
def cmp(lab, a, b):
    return f'''<div style="display:flex;align-items:center;gap:20px;padding:24px 0;border-top:1px solid rgba(243,245,244,.14)">
      <span style="font-size:38px;color:rgba(243,245,244,.8);flex:1">{lab}</span>
      <span class="mono" style="font-size:46px;color:rgba(243,245,244,.45)">{a}</span><span class="mono" style="font-size:40px;color:rgba(243,245,244,.4)">→</span>
      <span class="mono" style="font-weight:700;font-size:56px;color:{TEAL}">{b}</span></div>'''
PHOTO8 = f"""
<img src="img/arms.jpg" alt="" style="position:absolute;right:-40px;top:140px;width:600px;height:700px;object-fit:cover;object-position:50% 20%;filter:saturate(.85) contrast(1.05);-webkit-mask-image:linear-gradient(to right,transparent 0%,#000 48%),linear-gradient(to bottom,transparent 0%,#000 18%,#000 55%,transparent 100%);-webkit-mask-composite:source-in;mask-composite:intersect">"""
slides[8] = page("dark", f"""{top('Итог', 8)}
<div style="display:flex;flex-direction:column;gap:8px;margin-top:10px">
 <span class="cap" style="color:{TEAL}">ROMI по чистой прибыли</span>
 <span class="mono" style="font-weight:700;font-size:220px;line-height:1;color:{TEAL};letter-spacing:-.03em;text-shadow:0 10px 40px rgba(7,16,14,.9)">150%</span>
</div>
<p class="body" style="max-width:520px;text-shadow:0 2px 20px rgba(7,16,14,.95)">И&nbsp;это до того, как приедут оставшиеся четыре.</p>
<div style="margin-top:auto;display:flex;flex-direction:column">
 {cmp('Доходимость до прихода', '5%', '24%')}
 {cmp('Цена клиента', '$55', '$37')}
 {cmp('Диалогов у менеджера', '80', '25')}
</div>""", GLOWS8 + PHOTO8)

# 09 Кому поможет
niches = ["Эвакуатор и техпомощь", "Вскрытие замков", "Ремонт техники на дому", "Замер окон и потолков",
          "Стоматология и клиники", "Автосервис и шиномонтаж", "Рестораны и банкетные залы",
          "Ветклиники", "Юристы по ДТП и долгам", "Клининг и химчистка мебели"]
li = "".join(f'''<div style="display:flex;align-items:center;gap:24px;padding:9px 0;border-bottom:1px solid rgba(11,20,18,.1)">
   <span class="mono" style="font-weight:700;font-size:30px;color:#0F7F6B;width:48px">{i+1:02d}</span>
   <span style="font-size:38px;font-weight:500">{n}</span></div>''' for i, n in enumerate(niches))
slides[9] = page("light", f"""{top('Кому подойдёт', 9)}
<h2>Где звонок<br>сильнее чата</h2>
<div style="display:flex;flex-direction:column;margin-top:-6px">{li}</div>
<div class="blk" style="margin-top:auto;display:flex;flex-direction:column;gap:12px;padding:30px 36px">
 <span class="cap" style="color:{ORANGE}">Не подойдёт</span>
 <p style="font-size:34px;line-height:1.26">Интернет-магазину и&nbsp;аудитории до&nbsp;25 лет. Там оставьте чат, но&nbsp;сделайте телефон обязательным полем.</p>
</div>""", LIGHT_GLOWS)

# 10 Финал, новое фото
def fact(n, t):
    return f'''<div style="background:rgba(10,22,19,.75);border:1px solid rgba(243,245,244,.14);border-radius:20px;padding:28px;display:flex;flex-direction:column;gap:10px">
      <span class="mono" style="font-weight:700;font-size:82px;line-height:1;color:{TEAL}">{n}</span>
      <span style="font-size:34px;line-height:1.2;color:rgba(243,245,244,.8)">{t}</span></div>'''
slides[10] = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS}</style></head><body>
<div class="s dark">
 <div class="glow" style="bottom:-300px;right:-240px;width:960px;height:960px;background:radial-gradient(circle,rgba(61,189,163,.5) 0%,rgba(61,189,163,.15) 40%,rgba(7,16,14,0) 72%)"></div>
 <div class="glow" style="top:-260px;left:-220px;width:760px;height:760px;background:radial-gradient(circle,rgba(45,108,246,.45) 0%,rgba(7,16,14,0) 70%)"></div>
 <img src="img/final.jpg" alt="" style="position:absolute;right:58px;top:110px;width:360px;height:360px;border-radius:50%;object-fit:cover;object-position:38% 30%;border:3px solid rgba(61,189,163,.5);box-shadow:0 24px 70px rgba(0,0,0,.6)">
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
        # проверка переполнения
        ov = pg.evaluate("(()=>{const r=document.querySelector('.in');return r?r.scrollHeight-r.clientHeight:0})()")
        pg.screenshot(path=os.path.join(OUT, f"{n:02d}.png"))
        print(n, "overflow", ov)
    b.close()
