"""Генератор SVG-секций для профиля GitHub.

Запуск:  python scripts/build.py   → файлы появятся в assets/
Тексты, услуги, стек и контакты — в константах ниже.
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

SANS = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Courier New', monospace"
ACC = "#EB4B1F"
INK = "#151515"
GREY = "#8A8A8A"
BG = "#EDEDED"

# ───────────────────────── КОНТЕНТ ─────────────────────────
NICK = "ZEDKODEX"

TELEGRAM = "https://t.me/fkskrrkdjs"

# Услуги — как на сайте (CODIX-WEB/front/.../Services/typeServices.ts)
# (название, описание, пункты, иконка lucide, цвет плитки)
SERVICES = [
    ("Сайты",
     "Лендинги, интернет-магазины, SaaS и админки — быстрые, адаптивные и на своей кодовой базе, без конструкторов.",
     ["Лендинг и корпоративный сайт", "Интернет-магазин с оплатой", "SaaS и личный кабинет", "Админка и CRM"],
     "globe", "#111111"),
    ("Telegram-боты",
     "Боты и MiniApp для продаж, поддержки и рассылок — с админкой, оплатой и статистикой.",
     ["MiniApp внутри Telegram", "Оплата и подписки", "Рассылки и автоворонки", "Парсеры и чат-поддержка"],
     "send", "#2AABEE"),
    ("Приложения",
     "Десктопные и мобильные приложения с офлайн-режимом и синхронизацией — одна кодовая база на несколько платформ.",
     ["Windows и macOS", "iOS и Android", "Офлайн-режим", "Синхронизация данных"],
     "app-window-mac", "#5B5BD6"),
    ("Интеграция ИИ",
     "Встраиваю нейросети в продукт: ассистенты, поиск по документам компании, обработка заявок и генерация контента.",
     ["Поиск по базе знаний", "ИИ-ассистент в чате", "Разбор и классификация заявок", "Генерация контента"],
     "brain-circuit", "#E5484D"),
    ("Автоматизация",
     "Связываю CRM, почту, склад и таблицы в один сценарий — ручные выгрузки и копипаст уходят, процессы работают сами.",
     ["Интеграция CRM и сервисов", "Вебхуки и расписания", "Отчёты и выгрузки", "Мониторинг процессов"],
     "calendar-sync", "#30A46C"),
]
WORK_FORMATS = ["Под ключ", "Под ключ + деплой и домен", "Доработка чужого проекта", "Поддержка после запуска"]

# Стек — как на сайте (CODIX-WEB/front/.../Stats/typeStats.ts)
# (название, иконка simpleicons или URL, цвет иконки, цвет плитки, позиция x/y)
LANGS = [
    ("React", "react", "61DAFB", "#20232A", (-0.36, -0.3)),
    ("TypeScript", "typescript", "FFFFFF", "#3178C6", (-0.2, -0.25)),
    ("Vue", "vuedotjs", "4FC08D", "#FFFFFF", (0.0, -0.33)),
    ("JavaScript", "javascript", "000000", "#F7DF1E", (0.22, -0.31)),
    ("C#", "https://api.iconify.design/mdi/language-csharp.svg", "FFFFFF", "#68217A", (0.38, -0.27)),
    ("Redis", "redis", "FFFFFF", "#FF4438", (-0.4, -0.02)),
    ("Python", "python", "3776AB", "#FFFFFF", (0.39, 0.03)),
    ("Rust", "rust", "FFFFFF", "#111111", (-0.37, 0.28)),
    ("PostgreSQL", "postgresql", "FFFFFF", "#4169E1", (-0.2, 0.34)),
    ("SQLite", "sqlite", "FFFFFF", "#003B57", (0.0, 0.4)),
    ("FastAPI", "fastapi", "FFFFFF", "#009688", (0.19, 0.33)),
    ("Docker", "docker", "FFFFFF", "#2496ED", (0.37, 0.29)),
    ("Go", "go", "00ADD8", "#FFFFFF", (-0.28, 0.12)),
]

# (подпись, значение) — вся секция ведёт в Telegram
CONTACTS = [
    ("Telegram", "@fkskrrkdjs"),
    ("GitHub", "@KUZURAKI"),
]

ICON_CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons")


def fetch_icon(key, url):
    """Скачивает SVG иконки один раз и кладёт в scripts/icons/."""
    import urllib.request
    os.makedirs(ICON_CACHE, exist_ok=True)
    path = os.path.join(ICON_CACHE, key.replace("/", "_") + ".svg")
    if not os.path.exists(path):
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req) as r, open(path, "wb") as f:
            f.write(r.read())
    with open(path, encoding="utf-8") as f:
        return f.read()


def svg_inner(src):
    import re
    return re.sub(r"^.*?<svg[^>]*>|</svg>\s*$", "", src.strip(), flags=re.S)


def lucide(name):
    return svg_inner(fetch_icon("lucide-" + name, f"https://unpkg.com/lucide-static@latest/icons/{name}.svg"))


def brand_icon(slug):
    url = slug if slug.startswith("http") else f"https://cdn.simpleicons.org/{slug}"
    import re
    paths = re.findall(r'<path[^>]*\sd="([^"]+)"', fetch_icon(slug.split("/")[-1], url))
    return "".join(f'<path d="{d}"/>' for d in paths)

# 5x7 пиксельный шрифт для LED-матрицы
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "F": ["11111", "10000", "10000", "11110", "10000", "10000", "10000"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    " ": ["00000"] * 7,
}


def led(text, x, y, p, color, r=None):
    r = r or p * 0.4
    dots, cx = [], x
    for ch in text:
        for ri, row in enumerate(FONT[ch]):
            for ci, b in enumerate(row):
                if b == "1":
                    dots.append(f'<circle cx="{cx + ci * p + p / 2:.1f}" cy="{y + ri * p + p / 2:.1f}" r="{r:.2f}"/>')
        cx += 6 * p
    return f'<g fill="{color}">{"".join(dots)}</g>'


def t(x, y, s, size, color=INK, weight=400, anchor="start", font=SANS, extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" '
            f'fill="{color}" text-anchor="{anchor}" {extra}>{s}</text>')


def lines(x, y, items, size, color=INK, lh=None, **kw):
    lh = lh or size * 1.5
    return "".join(t(x, y + i * lh, s, size, color, **kw) for i, s in enumerate(items))


def wrap(s, n):
    out, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = f"{cur} {w}".strip()
    return out + [cur]


def pills(x, y, items, size=11.5):
    out = []
    for s in items:
        w = len(s) * size * 0.62 + 20
        out.append(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="24" rx="12" fill="none" stroke="#CFCFCF"/>')
        out.append(t(x + w / 2, y + 16, s, size, "#444", 500, "middle", MONO))
        x += w + 8
    return "".join(out)


def header(y, label, title, subtitle=None, x=600, anchor="middle"):
    out = [t(x, y, label, 13, ACC, 600, anchor, MONO, 'letter-spacing="1"'),
           t(x, y + 54, title, 44, INK, 400, anchor, extra='letter-spacing="-1"')]
    if subtitle:
        out.append(t(x, y + 92, subtitle, 16, "#444", 400, anchor))
    return "".join(out)


def svg(name, w, h, body, defs=""):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs>{COMMON_DEFS}{defs}</defs>{body}</svg>')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(doc)
    print(name, len(doc) // 1024, "KB")


COMMON_DEFS = """
<filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">
  <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="0.10"/>
</filter>
<filter id="glow" x="-10%" y="-30%" width="120%" height="160%">
  <feGaussianBlur stdDeviation="3.5"/>
</filter>
<filter id="soft" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="12"/></filter>
<linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FAFAFA"/><stop offset="1" stop-color="#D2D2D2"/>
</linearGradient>
"""


# ───────────────────────── HERO ─────────────────────────
def hero():
    W, H = 1200, 700
    defs = """
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#F7F7F7"/><stop offset="1" stop-color="#E4E4E4"/>
</linearGradient>
<radialGradient id="spot" cx="0.5" cy="0.35" r="0.5">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.9"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</radialGradient>
<pattern id="dots" x="292" y="238" width="9" height="9" patternUnits="userSpaceOnUse">
  <circle cx="4.5" cy="4.5" r="1.9" fill="#1E1E1E"/>
</pattern>
"""
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>',
         f'<rect width="{W}" height="540" rx="24" fill="url(#spot)"/>']

    top = []  # всё, что над полосой фич, поднимаем на место убранной навигации
    # устройство
    top.append('<ellipse cx="600" cy="372" rx="370" ry="16" fill="#000" opacity="0.28" filter="url(#soft)"/>')
    top.append('<rect x="330" y="146" width="540" height="46" rx="12" fill="#FCFCFC" stroke="#D6D6D6"/>')
    top.append(t(600, 176, "idea → release", 17, "#3A3A3A", 500, "middle", MONO))
    top.append('<circle cx="372" cy="169" r="15" fill="#F4F4F4" stroke="#CFCFCF"/>'
             f'<circle cx="372" cy="169" r="9" fill="{ACC}"/>')
    top.append(f'<circle cx="826" cy="169" r="15" fill="{ACC}"/><circle cx="826" cy="169" r="9" fill="none" stroke="#fff" stroke-width="1.5" opacity="0.7"/>')
    top.append('<rect x="240" y="180" width="720" height="182" rx="42" fill="url(#body)" stroke="#C9C9C9"/>')
    top.append('<rect x="262" y="198" width="676" height="146" rx="24" fill="#0A0A0A"/>')
    top.append('<rect x="262" y="198" width="676" height="146" rx="24" fill="url(#dots)"/>')
    red = led(NICK, 292, 238, 9, "#FF2A1A", 3.7)
    top.append(f'<g filter="url(#glow)" opacity="0.85">{red}</g>')
    top.append(f'<g>{red}<animate attributeName="opacity" values="1;0.82;1;1" dur="3s" repeatCount="indefinite"/></g>')
    white = led("FULL", 790, 226, 4.5, "#F4F4F4", 1.9) + led("STACK", 790, 270, 4.5, "#F4F4F4", 1.9)
    top.append(f'<g filter="url(#glow)" opacity="0.5">{white}</g>{white}')

    # текст
    top.append(t(600, 434, f"{NICK} — fullstack-разработчик", 30, INK, 500, "middle", extra='letter-spacing="-0.5"'))
    top.append(lines(600, 474, ["Сайты, Telegram-боты, приложения, интеграция ИИ и автоматизация.",
                                "Беру задачу целиком — от идеи и дизайна до запуска и поддержки.",
                                "Код и доступы остаются у вас."], 16, "#555", 26, anchor="middle"))
    top.append(f'<rect x="452" y="566" width="140" height="44" rx="4" fill="{ACC}"/>')
    top.append(t(522, 593, "НАПИСАТЬ", 14, "#fff", 600, "middle", extra='letter-spacing="1"'))
    top.append(f'<rect x="608" y="566" width="140" height="44" rx="4" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    top.append(t(678, 593, "ПРОЕКТЫ", 14, INK, 600, "middle", extra='letter-spacing="1"'))
    b.append(f'<g transform="translate(0 -100)">{"".join(top)}</g>')

    # полоса фич
    y0 = 546
    b.append(f'<line x1="0" y1="{y0}" x2="1200" y2="{y0}" stroke="#D3D3D3"/>')
    b.append(f'<line x1="400" y1="{y0}" x2="400" y2="{H}" stroke="#D3D3D3"/><line x1="800" y1="{y0}" x2="800" y2="{H}" stroke="#D3D3D3"/>')
    ic = 'fill="none" stroke="#5A5A5A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    cy = y0 + 54
    icons = [
        f'<g {ic}><rect x="42" y="{cy - 17}" width="40" height="28" rx="3"/><path d="M54 {cy + 17} h16 M62 {cy + 11} v6"/></g>',
        f'<g {ic}><rect x="444" y="{cy - 16}" width="13" height="13"/><rect x="463" y="{cy - 16}" width="13" height="13"/>'
        f'<rect x="444" y="{cy + 3}" width="13" height="13"/><path d="M469.5 {cy + 3} v13 M463 {cy + 9.5} h13"/></g>',
        f'<g {ic}><path d="M858 {cy - 16} l10 6 v12 l-10 6 l-10-6 v-12 z"/><circle cx="858" cy="{cy - 4}" r="3.5"/>'
        f'<path d="M872 {cy + 2} l7 4 v8 l-7 4 l-7-4 v-8 z"/></g>',
    ]
    cols = [("Под ключ", ["От идеи и дизайна интерфейса", "до деплоя и поддержки"]),
            ("Любая часть", ["Фронтенд, бэкенд, бот или", "интеграция — отдельно"]),
            ("Без рутины", ["Автоматизирую всё, что можно", "не делать руками"])]
    for i, (title, desc) in enumerate(cols):
        x = i * 400 + 104
        b.append(icons[i])
        b.append(t(x, cy - 4, title, 16))
        b.append(lines(x, cy + 20, desc, 13, GREY, 19))
    svg("hero.svg", W, H, "".join(b), defs)


# ───────────────────────── 01 УСЛУГИ ─────────────────────────
def services():
    W, H = 1200, 990
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
         header(70, "01 — УСЛУГИ", "Что я делаю", "Выберите то, что вам подходит.")]
    check = (f'<path d="M0 5 l3.5 3.5 l7-8" fill="none" stroke="{ACC}" stroke-width="2" '
             'stroke-linecap="round" stroke-linejoin="round"/>')
    for i, (title, desc, points, icon, tile) in enumerate(SERVICES):
        x, y = 60 + (i % 3) * 370, 210 + (i // 3) * 390
        b.append(f'<rect x="{x}" y="{y}" width="340" height="360" rx="16" fill="#fff" filter="url(#shadow)"/>')
        b.append(t(x + 314, y + 42, f"{i + 1:02d}", 13, ACC, 700, "end", MONO))
        b.append(f'<rect x="{x + 26}" y="{y + 26}" width="52" height="52" rx="14" fill="{tile}"/>')
        b.append(f'<g transform="translate({x + 38} {y + 38}) scale(1.167)" fill="none" stroke="#fff" '
                 f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">{lucide(icon)}</g>')
        b.append(t(x + 26, y + 120, title, 24))
        b.append(lines(x + 26, y + 152, wrap(desc, 40), 13.5, "#666", 21))
        b.append(f'<line x1="{x + 26}" y1="{y + 232}" x2="{x + 314}" y2="{y + 232}" stroke="#EEEEEE"/>')
        for j, p in enumerate(points):
            py = y + 262 + j * 25
            b.append(f'<g transform="translate({x + 28} {py - 10})">{check}</g>')
            b.append(t(x + 48, py, p, 13.5, "#333"))

    # 6-я ячейка — форматы работы
    x, y = 60 + 2 * 370, 210 + 390
    b.append(f'<rect x="{x}" y="{y}" width="340" height="360" rx="16" fill="#0A0A0A"/>')
    b.append(led("ANY", x + 26, y + 30, 4, ACC, 1.7))
    b.append(t(x + 26, y + 104, "Любую услугу", 24, "#F2F2F2"))
    b.append(t(x + 26, y + 134, "можно заказать", 24, "#F2F2F2"))
    for j, s in enumerate(WORK_FORMATS):
        py = y + 196 + j * 38
        b.append(f'<rect x="{x + 26}" y="{py - 20}" width="288" height="30" rx="15" fill="none" stroke="#333"/>')
        b.append(f'<circle cx="{x + 44}" cy="{py - 5}" r="3.5" fill="{ACC}"/>')
        b.append(t(x + 58, py, s, 13.5, "#E6E6E6"))
    svg("services.svg", W, H, "".join(b))


# ───────────────────────── 02 СТЕК ─────────────────────────
def stack():
    W, H = 1200, 720
    cx, cy = 600, 360
    style = """<style>
@keyframes fl { 0%,100% { transform: translateY(0) } 50% { transform: translateY(-9px) } }
.fl { animation: fl ease-in-out infinite; }
</style>"""
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="#FAFAFA"/>']
    for i, (name, slug, color, tile, (px, py)) in enumerate(LANGS):
        x, y = cx + px * W, cy + py * (H - 60)
        border = ' stroke="#E2E2E2"' if tile.upper() == "#FFFFFF" else ""
        tile_svg = (f'<rect x="-38" y="-38" width="76" height="76" rx="20" fill="{tile}"{border} filter="url(#shadow)"/>'
                    f'<g transform="translate(-21 -21) scale(1.75)" fill="#{color}">{brand_icon(slug)}</g>'
                    + t(0, 62, name, 11.5, GREY, 500, "middle", MONO))
        b.append(f'<g transform="translate({x:.0f} {y:.0f})"><g class="fl" '
                 f'style="animation-duration:{5 + (i % 5) * 0.9:.1f}s;animation-delay:{-i * 0.7:.1f}s">{tile_svg}</g></g>')
    b.append(t(cx, cy - 92, "02 — СТЕК", 13, ACC, 600, "middle", MONO, 'letter-spacing="1"'))
    b.append(t(cx, cy - 58, "Один разработчик на весь стек", 16, "#555", 400, "middle"))
    b.append(lines(cx, cy, ["От сырого кода", "до готового"], 46, INK, 54, weight=400, anchor="middle",
                   extra='letter-spacing="-1"'))
    b.append(t(cx, cy + 108, "интерфейса.", 46, ACC, 400, "middle", extra='letter-spacing="-1"'))
    svg("stack.svg", W, H, "".join(b), style)


# ───────────────────────── 03 ПОДХОД ─────────────────────────
def approach():
    W, H = 1200, 560
    defs = """
<linearGradient id="mon" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#F6F6F6"/><stop offset="1" stop-color="#C9C9C9"/>
</linearGradient>
<linearGradient id="desk" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#EDE7DC"/><stop offset="1" stop-color="#D9D0C1"/>
</linearGradient>
"""
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="#FAFAFA"/>',
         header(80, "03 — ПОДХОД", "Как я работаю", x=70, anchor="start"),
         lines(70, 178, ["Беру ответственность за результат, а не только", "за код: от первого созвона до стабильной",
                         "работы после релиза."], 16, "#333", 24)]
    ic = 'fill="none" stroke="#222" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    rows = [
        (f'<g {ic}><rect x="70" y="282" width="26" height="20" rx="3"/><path d="M76 289 l4 3 l-4 3 M83 296 h6"/></g>',
         "От идеи до релиза", ["Интерфейс, API, база данных и сервер —", "в одних руках, без лишних посредников."]),
        (f'<g {ic}><circle cx="76" cy="356" r="3.5"/><circle cx="76" cy="380" r="3.5"/><circle cx="92" cy="362" r="3.5"/>'
         f'<path d="M76 359.5 v17 M92 365.5 q0 9 -14 12"/></g>',
         "Прозрачный процесс", ["Показываю прогресс по ходу работы,", "а не только в конце."]),
        (f'<g {ic}><rect x="70" y="430" width="28" height="19" rx="2"/><path d="M80 449 v5 M76 455 h12"/></g>',
         "Поддержка после запуска", ["Исправляю, ускоряю, добавляю функции."]),
    ]
    for i, (icon, title, desc) in enumerate(rows):
        y = 292 + i * 74
        b.append(icon)
        b.append(t(116, y, title, 15, INK, 600))
        b.append(lines(116, y + 20, desc, 12.5, GREY, 17))

    b.append('<rect x="560" y="470" width="640" height="16" fill="url(#desk)"/>')
    b.append('<rect x="560" y="486" width="640" height="10" fill="#000" opacity="0.06"/>')
    b.append('<ellipse cx="900" cy="470" rx="110" ry="6" fill="#000" opacity="0.25" filter="url(#soft)"/>')
    b.append('<path d="M872 404 h56 l14 62 h-84 z" fill="#D4D4D4" stroke="#BDBDBD"/>')
    b.append('<rect x="842" y="462" width="116" height="8" rx="4" fill="#CFCFCF" stroke="#BDBDBD"/>')
    b.append('<rect x="700" y="160" width="400" height="252" rx="18" fill="url(#mon)" stroke="#BDBDBD" filter="url(#shadow)"/>')
    b.append('<circle cx="900" cy="270" r="22" fill="none" stroke="#BDBDBD" stroke-width="1.5"/>')
    b.append(led("Z", 890.5, 259.5, 3.2, "#B5B5B5", 1.3))
    b.append('<rect x="893" y="148" width="14" height="14" rx="2" fill="#2A2A2A"/>')
    b.append('<rect x="818" y="106" width="164" height="46" rx="8" fill="#161616" filter="url(#shadow)"/>')
    b.append('<rect x="824" y="112" width="152" height="34" rx="5" fill="#0A0A0A"/>')
    sign = led("CODING", 852, 119, 3, "#FF2A1A", 1.25)
    b.append(f'<g filter="url(#glow)" opacity="0.8">{sign}</g>{sign}')
    b.append('<circle cx="838" cy="129" r="4.5" fill="#FF2A1A"><animate attributeName="opacity" values="1;0.2;1" dur="1.4s" repeatCount="indefinite"/></circle>')
    b.append('<path d="M1090 438 h44 l-5 32 h-34 z" fill="#FBFBFB" stroke="#D0D0D0"/>')
    for dx, dy, rot in [(-12, -12, -40), (12, -12, 40), (0, -18, 0), (-20, -2, -70), (20, -2, 70)]:
        b.append(f'<ellipse cx="{1112 + dx}" cy="{434 + dy}" rx="6" ry="13" fill="#6E8F4E" '
                 f'transform="rotate({rot} {1112 + dx} {434 + dy})"/>')
    svg("approach.svg", W, H, "".join(b), defs)


# ───────────────────────── 04 ПРОЕКТЫ ─────────────────────────
def pixel_logo(x, y, p):
    """Квадрат с «маркерами» как у QR и пиксельной Z в центре."""
    out = [f'<rect x="{x - p}" y="{y - p}" width="{23 * p}" height="{23 * p}" fill="#fff"/>']
    for fx, fy in [(0, 0), (14, 0), (0, 14)]:
        out.append(f'<rect x="{x + fx * p}" y="{y + fy * p}" width="{7 * p}" height="{7 * p}" fill="#0D0D0D"/>'
                   f'<rect x="{x + (fx + 1) * p}" y="{y + (fy + 1) * p}" width="{5 * p}" height="{5 * p}" fill="#fff"/>'
                   f'<rect x="{x + (fx + 2) * p}" y="{y + (fy + 2) * p}" width="{3 * p}" height="{3 * p}" fill="#0D0D0D"/>')
    for ri, row in enumerate(FONT["Z"]):
        for ci, c in enumerate(row):
            if c == "1":
                out.append(f'<rect x="{x + (14 + ci) * p}" y="{y + (14 + ri) * p}" width="{p}" height="{p}" fill="#0D0D0D"/>')
    for i, j in [(8, 2), (9, 4), (10, 1), (11, 5), (8, 9), (10, 10), (12, 8), (2, 9), (4, 11), (5, 8), (1, 12), (9, 12), (11, 11)]:
        out.append(f'<rect x="{x + i * p}" y="{y + j * p}" width="{p}" height="{p}" fill="#0D0D0D"/>')
    return "".join(out)


def device_top():
    """Устройство «сверху» (координаты 420..1140 × 160..446)."""
    m = dict(font=MONO)
    d = ['<rect x="420" y="196" width="720" height="250" rx="44" fill="url(#body)" stroke="#C9C9C9" filter="url(#shadow)"/>',
         '<rect x="610" y="160" width="340" height="66" rx="10" fill="#FDFDFD" stroke="#D6D6D6"/>',
         t(780, 200, "download ⏎", 20, "#333", 500, "middle", MONO),
         '<circle cx="505" cy="214" r="46" fill="#FAFAFA" stroke="#D3D3D3"/>',
         f'<circle cx="505" cy="214" r="30" fill="none" stroke="{ACC}" stroke-width="3" stroke-dasharray="2 4"/>',
         f'<circle cx="505" cy="214" r="18" fill="{ACC}"/>',
         t(505, 218, "ok", 11, "#fff", 600, "middle", MONO),
         f'<rect x="1020" y="200" width="80" height="24" rx="12" fill="{ACC}"/>',
         t(1060, 192, "RELEASE", 9, "#666", 600, "middle", MONO),
         '<rect x="440" y="262" width="680" height="166" rx="26" fill="#0B0B0B"/>',
         t(466, 294, "Built with ⚡ RUST", 12, "#E6E6E6", **m),
         lines(466, 316, ["› Tauri 2 / React 19", "› Axum / Tokio", "› FastAPI / Telethon"], 11, "#9C9C9C", 17, **m),
         t(466, 404, "codix hub", 10, "#666", **m),
         '<rect x="690" y="278" width="176" height="114" rx="8" fill="#141414" stroke="#2E2E2E"/>',
         t(778, 300, "▶▶▶ ACTIVE ◀◀◀", 11, "#EDEDED", 600, "middle", MONO),
         t(744, 344, "▶25", 34, "#fff", 700, "middle", MONO),
         f'<text x="788" y="342" font-family="{MONO}" font-size="30" font-weight="700" fill="#fff" text-anchor="middle">:'
         '<animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></text>',
         t(822, 344, "59", 34, "#fff", 700, "middle", MONO),
         '<rect x="736" y="356" width="84" height="22" rx="2" fill="#F2F2F2"/>',
         t(778, 372, "v1.0.0", 14, "#000", 800, "middle", MONO),
         t(892, 294, "Download", 12, "#E6E6E6", **m),
         lines(892, 316, ["› Windows", "› macOS"], 11, "#9C9C9C", 17, **m),
         pixel_logo(1062, 350, 2.4)]
    return "".join(d)


def projects():
    W, H = 1200, 600
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
         header(64, "04 — ПРОЕКТЫ", "Что уже запущено и работает",
                "Открытые релизы — скачать и попробовать можно прямо сейчас.")]
    x, y = 60, 210
    b.append(f'<rect x="{x}" y="{y}" width="440" height="340" rx="16" fill="#fff" filter="url(#shadow)"/>')
    b.append(t(x + 28, y + 44, "#00", 13, ACC, 700, font=MONO))
    b.append(t(x + 28, y + 84, "CODIX HUB", 30, INK, 500))
    b.append(t(x + 28, y + 112, "Desktop · Backend · Telegram", 12.5, GREY, 500, font=MONO))
    desc = ("Личный центр автоматизации: деплой на VPS в один клик, облачное хранилище, "
            "заказы и отзывы из Telegram, отложенные рассылки и удаление фона нейросетью "
            "прямо на устройстве. Клиент на Tauri и React, бэкенд на Axum и FastAPI.")
    b.append(lines(x + 28, y + 150, wrap(desc, 52), 13.5, "#555", 21))
    b.append(pills(x + 28, y + 252, ["Tauri 2", "Rust", "React", "FastAPI"]))
    b.append(f'<rect x="{x + 28}" y="{y + 290}" width="150" height="34" rx="4" fill="{ACC}"/>')
    b.append(t(x + 103, y + 312, "СКАЧАТЬ ↗", 12.5, "#fff", 600, "middle", extra='letter-spacing="1"'))
    b.append(t(x + 196, y + 312, "Windows · macOS", 12.5, GREY))
    b.append(f'<g transform="translate(212 108) scale(0.85)">{device_top()}</g>')
    svg("projects.svg", W, H, "".join(b))


# ───────────────────────── 05 КОНТАКТЫ ─────────────────────────
def contacts():
    W, H = 1200, 400
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="#FAFAFA"/>',
         header(72, "05 — КОНТАКТЫ", "Есть задача? Напишите.",
                "Расскажите, что нужно сделать, сроки и бюджет — предложу решение и оценку.")]
    cw, gap = 300, 24
    x0 = 600 - (len(CONTACTS) * cw + (len(CONTACTS) - 1) * gap) / 2
    for i, (label, value) in enumerate(CONTACTS):
        x = x0 + i * (cw + gap)
        b.append(f'<rect x="{x}" y="232" width="{cw}" height="110" rx="16" fill="#fff" filter="url(#shadow)"/>')
        b.append(t(x + 26, 270, label.upper(), 12, GREY, 600, font=MONO, extra='letter-spacing="1"'))
        b.append(t(x + 26, 314, value, 20, INK, 500))
        b.append(f'<circle cx="{x + cw - 34}" cy="266" r="14" fill="{ACC if i == 0 else INK}"/>'
                 + t(x + cw - 34, 271, "↗", 15, "#fff", 700, "middle"))
    svg("contacts.svg", W, H, "".join(b))


# ───────────────────────── FOOTER ─────────────────────────
def footer():
    W, H = 1200, 250
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="#0A0A0A"/>',
         led(NICK, 60, 66, 4, "#F2F2F2", 1.7),
         t(60, 132, "Fullstack-разработчик", 13, "#8C8C8C"),
         lines(60, 190, [f"Designed &amp; coded by {NICK}", "© 2026 All rights reserved"], 12, "#5E5E5E", 18)]
    for x, items in [(460, ["Услуги", "Стек"]), (600, ["Проекты", "Контакты"]), (740, ["GitHub", "CODIX HUB"])]:
        b.append(lines(x, 82, items, 15, "#F2F2F2", 28))
    b.append(t(1140, 82, "github.com/KUZURAKI ↗", 14, "#F2F2F2", anchor="end"))
    b.append(lines(1140, 190, ["Desktop · Web · Bots", "Rust · TypeScript · Python"], 12, "#5E5E5E", 18, anchor="end"))
    b.append(f'<rect x="1120" y="100" width="20" height="4" fill="{ACC}"/>')
    svg("footer.svg", W, H, "".join(b))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for f in ("multitool.svg", "live.svg", "modes.svg", "stats.svg"):
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            os.remove(p)
    hero(); services(); stack(); approach(); projects(); contacts(); footer()
