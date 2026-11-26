"""Карусель 02: генерация HTML-слайдов в стиле карусели 01 и рендер в JPEG."""
import os, sys
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
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

