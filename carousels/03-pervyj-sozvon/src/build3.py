"""Карусель 03: «Хотите 20 заявок, а канал даёт 2». Крупный шрифт для телефона."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *  # noqa

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
CSS3 = CSS + """
.body{font-size:46px;line-height:1.28}
.q{font-size:42px;line-height:1.25}
"""

def page3(cls, inner, glows=""):
    return f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS3}</style></head>
<body><div class="s {cls}">{glows}<div class="in">{inner}</div></div></body></html>"""

def photo(src, style, mask):
    return f'<img src="img/{src}" alt="" style="position:absolute;object-fit:cover;filter:saturate(.85) contrast(1.05);{style};-webkit-mask-image:{mask};-webkit-mask-composite:source-in">'

slides = {}

# 01 Обложка, синяя
slides[1] = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS3}</style></head><body>
<div class="s" style="background:linear-gradient(160deg,#081634 0%,#0B2763 55%,#1440A8 100%);color:#F3F5F4">
 <div class="glow" style="top:-300px;right:-260px;width:1000px;height:1000px;background:radial-gradient(circle,rgba(61,189,163,.45) 0%,rgba(8,22,52,0) 66%)"></div>
 <div class="glow" style="bottom:-300px;left:-300px;width:900px;height:900px;background:radial-gradient(circle,rgba(45,108,246,.55) 0%,rgba(8,22,52,0) 70%)"></div>
 <div class="in" style="gap:0">
  <div style="display:inline-flex;align-self:flex-start;align-items:center;gap:14px;background:rgba(243,245,244,.12);border:1px solid rgba(243,245,244,.28);border-radius:100px;padding:14px 28px">
   <span style="width:12px;height:12px;border-radius:50%;background:{TEAL}"></span>
   <span class="mono" style="font-size:30px;font-weight:500;letter-spacing:.08em;text-transform:uppercase">Первый созвон</span></div>
  <h1 class="osw" style="margin:64px 0 0;font-size:120px;line-height:1.05">Хотите 20&nbsp;заявок в&nbsp;день, а&nbsp;канал даёт <span style="display:inline-block;line-height:1;background:{ORANGE};color:#081634;padding:4px 18px 2px;border-radius:12px">2</span></h1>
  <p style="margin-top:44px;font-size:52px;line-height:1.24;color:rgba(243,245,244,.9);max-width:880px">Что я спрашиваю у собственника, прежде чем что-то обещать.</p>
  <div style="margin-top:auto;display:flex;flex-direction:column;gap:24px">
   <div style="background:rgba(8,22,52,.7);border:1px solid rgba(243,245,244,.2);border-radius:26px;padding:34px 38px;display:flex;flex-direction:column;gap:24px">
    <div style="display:flex;align-items:center;gap:24px"><span class="mono" style="font-size:32px;text-transform:uppercase;letter-spacing:.06em;color:rgba(243,245,244,.65);width:200px">Сейчас</span>
     <div style="flex:1;height:44px;display:flex"><div style="width:50%;background:{TEAL};border-radius:10px"></div></div>
     <span class="mono" style="font-weight:700;font-size:64px;width:100px;text-align:right">10</span></div>
    <div style="display:flex;align-items:center;gap:24px"><span class="mono" style="font-size:32px;text-transform:uppercase;letter-spacing:.06em;color:rgba(243,245,244,.65);width:200px">Хотим</span>
     <div style="flex:1;height:44px;border:3px dashed {ORANGE};border-radius:10px"></div>
     <span class="mono" style="font-weight:700;font-size:64px;width:100px;text-align:right;color:{ORANGE}">20</span></div>
   </div>
   <span style="font-size:40px;font-weight:600">Листайте →</span>
  </div>
 </div>
</div></body></html>"""

# 02 С чем приходят
def ch(name, ok):
    c = TEAL if ok else ORANGE
    st = "работает" if ok else "просел"
    bg = "rgba(10,22,19,.8)" if ok else "linear-gradient(135deg,rgba(255,138,91,.22),rgba(10,22,19,.9))"
    bd = "rgba(243,245,244,.16)" if ok else "rgba(255,138,91,.5)"
    return f'''<div style="display:flex;align-items:center;gap:24px;padding:30px 36px;border-radius:22px;background:{bg};border:1px solid {bd}">
      <span style="width:20px;height:20px;border-radius:50%;background:{c};flex:none"></span>
      <span style="font-size:44px;font-weight:600;flex:1">{name}</span>
      <span class="mono" style="font-size:34px;font-weight:700;color:{c}">{st}</span></div>'''
slides[2] = page3("dark", f"""{top('Ситуация', 2)}
<h2>Один канал<br>просел</h2>
<div style="display:flex;flex-direction:column;gap:16px">{ch('Контекстная реклама', True)}{ch('Карты', True)}{ch('SEO', True)}{ch('Авито', False)}</div>
<p class="body" style="margin-top:auto">С этой болью и&nbsp;приходят. Поэтому я&nbsp;считаю конкретный канал, а&nbsp;не&nbsp;всё вместе.</p>""", DARK_GLOWS)

# 03 Вопрос 1. Канал
def qcard(n, t, light=True):
    return f'''<div class="card" style="display:flex;align-items:center;gap:30px;padding:50px 44px">
      <span class="mono" style="font-weight:700;font-size:72px;line-height:1;color:{'#0F7F6B' if light else TEAL};width:70px">{n}</span>
      <span style="font-size:52px;line-height:1.18;font-weight:600">{t}</span></div>'''
slides[3] = page3("light", f"""{top('Вопрос 1', 3)}
<h2>Канал</h2>
<div style="display:flex;flex-direction:column;gap:20px">
 {qcard('$','Бюджет на канал в&nbsp;месяц')}{qcard('#','Сколько заявок он&nbsp;даёт')}{qcard('=','Сколько стоит клиент именно с&nbsp;него')}
</div>
<p class="body" style="margin-top:auto">Без этих цифр спорить, работает канал или нет, бесполезно.</p>""", LIGHT_GLOWS)

# 04 Вопрос 2. Воронка
def fbar(label, num, w, bg, fg="#F3F5F4"):
    return f'''<div style="width:{w}%;min-width:440px;background:{bg};color:{fg};border-radius:18px;padding:24px 32px;display:flex;justify-content:space-between;align-items:center">
      <span style="font-size:40px;font-weight:600">{label}</span><span class="mono" style="font-weight:700;font-size:58px">{num}</span></div>'''
def conv(p):
    return f'<span class="mono" style="font-size:34px;font-weight:700;color:{TEAL};padding-left:32px">↓ {p}</span>'
slides[4] = page3("dark", f"""{top('Вопрос 2', 4)}
<div style="display:flex;align-items:baseline;gap:28px"><h2>Воронка</h2><span class="cap" style="color:rgba(243,245,244,.6)">на примере</span></div>
<div style="display:flex;flex-direction:column;gap:10px">
 {fbar('Переходы','1 240',100,'rgba(243,245,244,.14)')}{conv('3,7%')}
 {fbar('Заявки','46',78,'rgba(45,108,246,.55)')}{conv('41%')}
 {fbar('Целевые','19',62,'#0F7F6B')}{conv('37%')}
 {fbar('Договоры','7',50,TEAL,'#07100E')}
</div>
<p class="body" style="margin-top:auto">Сразу видно, где теряются люди: в&nbsp;рекламе, на&nbsp;сайте или в&nbsp;продажах.</p>""", DARK_GLOWS)

# 05 Вопрос 3. Деньги
def mcard(t, d):
    return f'''<div class="card" style="display:flex;flex-direction:column;gap:8px;padding:32px 44px">
      <span class="osw" style="font-size:76px;color:#0F7F6B">{t}</span>
      <span style="font-size:46px;line-height:1.22;color:#1B2725">{d}</span></div>'''
slides[5] = page3("light", f"""{top('Вопрос 3', 5)}
<h2>Деньги</h2>
<div style="display:flex;flex-direction:column;gap:20px">
 {mcard('Средний чек','Сколько платит один клиент')}{mcard('Маржа','Сколько из чека остаётся вам')}{mcard('LTV','Сколько клиент приносит за&nbsp;всё время')}
</div>
<p class="body" style="margin-top:auto">Без них непонятно, сколько можно платить за&nbsp;клиента.</p>""", LIGHT_GLOWS)

# 06 Вопрос 4. Учёт, фото
def chk(t):
    return f'''<div style="display:flex;align-items:center;gap:24px">
      <span style="width:66px;height:66px;border-radius:16px;border:3px solid {TEAL};flex:none"></span>
      <span style="font-size:44px;line-height:1.2;font-weight:600">{t}</span></div>'''
P6 = photo("suit.jpg", "right:-80px;top:300px;width:620px;height:760px;object-position:50% 15%",
           "linear-gradient(to right,transparent 0%,#000 45%),linear-gradient(to bottom,transparent 0%,#000 18%,#000 60%,transparent 100%)")
slides[6] = page3("dark", f"""{top('Вопрос 4', 6)}
<h2>Учёт</h2>
<div style="display:flex;flex-direction:column;gap:34px;max-width:560px;margin-top:10px">
 {chk('CRM-система')}{chk('Сквозная аналитика')}{chk('Как продажи работают с&nbsp;заявками канала')}
</div>
<div class="card" style="margin-top:auto;background:rgba(10,22,19,.92)">
 <p style="font-size:44px;line-height:1.26">Без CRM ответы на&nbsp;первые три вопроса будут оценкой на&nbsp;глаз.</p>
</div>""", DARK_GLOWS + P6)

# 07 Вопрос 5. Ёмкость
def big(num, unit, t, c):
    return f'''<div class="card" style="display:flex;flex-direction:column;gap:12px;padding:36px 40px;border-top:6px solid {c}">
      <div style="display:flex;align-items:baseline;gap:14px"><span class="mono" style="font-weight:700;font-size:130px;line-height:1;color:{c}">{num}</span><span style="font-size:40px;color:#35423F">{unit}</span></div>
      <span style="font-size:42px;line-height:1.22;font-weight:600">{t}</span></div>'''
slides[7] = page3("light", f"""{top('Вопрос 5', 7)}
<h2>Ёмкость</h2>
<div style="display:flex;flex-direction:column;gap:22px">
 {big('10','в день','Столько заявок приходит сейчас со&nbsp;всех каналов','#0F7F6B')}
 {big('?','в день','Столько продажи могут обработать без&nbsp;потерь','#B8401F')}
</div>
<p class="body" style="margin-top:auto">Если отдел продаж тянет 12, то&nbsp;20 заявок просто сгорят.</p>""", LIGHT_GLOWS)

# 08 Математика, фото
P8 = photo("tee.jpg", "right:-60px;top:120px;width:560px;height:640px;object-position:50% 20%",
           "linear-gradient(to right,transparent 0%,#000 45%),linear-gradient(to bottom,transparent 0%,#000 15%,#000 55%,transparent 100%)")
def seg(w, bg, t, fg="#07100E", dashed=False):
    b = f"border:3px dashed {ORANGE};" if dashed else f"background:{bg};"
    return f'<div style="width:{w}%;{b}border-radius:12px;height:84px;display:flex;align-items:center;justify-content:center;font-family:JBM,monospace;font-weight:700;font-size:44px;color:{fg}">{t}</div>'
slides[8] = page3("dark", f"""{top('Математика', 8)}
<h2 style="max-width:560px">Даже вдвое лучше не&nbsp;даст 20</h2>
<div style="display:flex;flex-direction:column;gap:14px;margin-top:auto">
 <span class="cap" style="color:rgba(243,245,244,.7)">Сейчас</span>
 <div style="display:flex;gap:8px">{seg(40,'rgba(243,245,244,.25)','8','#F3F5F4')}{seg(10,TEAL,'2')}</div>
 <span class="cap" style="color:rgba(243,245,244,.7);margin-top:10px">Канал вдвое лучше</span>
 <div style="display:flex;gap:8px">{seg(40,'rgba(243,245,244,.25)','8','#F3F5F4')}{seg(20,TEAL,'4')}</div>
 <span class="cap" style="color:{ORANGE};margin-top:10px">Хотим</span>
 <div style="display:flex;gap:8px">{seg(40,'rgba(243,245,244,.25)','8','#F3F5F4')}{seg(20,TEAL,'4')}{seg(40,'','+8',ORANGE,True)}</div>
</div>
<p class="body">Восемь заявок даст только новый канал. Об&nbsp;этом договариваемся на&nbsp;первом созвоне, а&nbsp;не&nbsp;через месяц.</p>""", DARK_GLOWS + P8)

# 09 Что сделать до созвона
def step(n, t):
    return f'''<div style="display:flex;gap:28px;align-items:flex-start;padding:28px 0;border-bottom:1px solid rgba(11,20,18,.12)">
      <span class="mono" style="font-weight:700;font-size:56px;line-height:1;color:#0F7F6B;width:70px">{n}</span>
      <span style="font-size:44px;line-height:1.22;font-weight:500">{t}</span></div>'''
slides[9] = page3("light", f"""{top('До созвона', 9)}
<h2>Один лист<br>вместо часа</h2>
<div style="display:flex;flex-direction:column">
 {step('01','Выпишите ответы на&nbsp;пять вопросов')}
 {step('02','Цель ставьте по&nbsp;каналу, а&nbsp;не&nbsp;по&nbsp;бизнесу целиком')}
 {step('03','Нет CRM? Начинайте с&nbsp;аналитики, реклама подождёт')}
 {step('04','Пришлите лист в&nbsp;бот, скажу, что с&nbsp;ним делать')}
</div>""", LIGHT_GLOWS)

# 10 Финал
def fact(n, t):
    return f'''<div style="background:rgba(10,22,19,.75);border:1px solid rgba(243,245,244,.14);border-radius:20px;padding:28px;display:flex;flex-direction:column;gap:10px">
      <span class="mono" style="font-weight:700;font-size:82px;line-height:1;color:{TEAL}">{n}</span>
      <span style="font-size:36px;line-height:1.2;color:rgba(243,245,244,.85)">{t}</span></div>'''
slides[10] = f"""<!doctype html><html lang="ru"><head><meta charset="utf-8"><style>{CSS3}</style></head><body>
<div class="s dark">
 <div class="glow" style="bottom:-300px;right:-240px;width:960px;height:960px;background:radial-gradient(circle,rgba(61,189,163,.5) 0%,rgba(61,189,163,.15) 40%,rgba(7,16,14,0) 72%)"></div>
 <div class="glow" style="top:-260px;left:-220px;width:760px;height:760px;background:radial-gradient(circle,rgba(45,108,246,.45) 0%,rgba(7,16,14,0) 70%)"></div>
 <img src="img/office.jpg" alt="" style="position:absolute;right:58px;top:110px;width:360px;height:360px;border-radius:50%;object-fit:cover;object-position:52% 22%;border:3px solid rgba(61,189,163,.5);box-shadow:0 24px 70px rgba(0,0,0,.6)">
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
        # минимальный кегль видимого текста
        mn = pg.evaluate("""(()=>{let m=999,w='';document.querySelectorAll('.s *').forEach(e=>{if(![...e.childNodes].some(n=>n.nodeType===3&&n.textContent.trim()))return;const f=parseFloat(getComputedStyle(e).fontSize);if(f<m){m=f;w=e.textContent.trim().slice(0,30)}});return m+' '+w})()""")
        pg.screenshot(path=os.path.join(OUT, f"{n:02d}.png"))
        print(n, "overflow", ov, "min font", mn)
    b.close()
