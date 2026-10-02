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

SERVICES = [
    ("Desktop-приложения",
     "Кроссплатформенные приложения для Windows и macOS: лёгкие, быстрые, с доступом к системе.",
     ["Tauri 2", "Rust", "React", "TypeScript"]),
    ("Сайты и веб-приложения",
     "Лендинги, личные кабинеты и админ-панели: адаптивные интерфейсы с API и данными в реальном времени.",
     ["React", "TypeScript", "Vite", "Sass"]),
    ("Telegram-боты",
     "Боты для заказов, отзывов, рассылок и поддержки — с админкой, статистикой и уведомлениями.",
     ["Python", "Telethon", "FastAPI", "SQLite"]),
    ("Backend и API",
     "REST и WebSocket API, бизнес-логика, авторизация и интеграции со сторонними сервисами.",
     ["Rust", "Axum", "Tokio", "FastAPI"]),
    ("Автоматизация",
     "Скрипты и сервисы, которые снимают рутину: парсинг, отложенный постинг, связки сервисов.",
     ["Python", "Telethon", "PowerShell"]),
    ("Деплой и серверы",
     "VPS, Docker, nginx и HTTPS, автодеплой — чтобы проект спокойно работал после релиза.",
     ["Docker", "nginx", "Linux", "SSH"]),
]

# (заголовок, строки описания) — выноски на схеме «Стек»
STACK = [
    ("Frontend", ["React · TypeScript · Vite", "Sass · JavaScript"]),
    ("Backend", ["Rust · Axum · Tokio", "Python · FastAPI"]),
    ("Данные и AI", ["SQLite · ONNX Runtime", "нейросети на устройстве"]),
    ("DevOps", ["Docker · nginx · Linux", "Git · SSH · PowerShell"]),
]

# (подпись, значение) — добавьте сюда Telegram, почту и т.д.
CONTACTS = [
    ("GitHub", "@KUZURAKI"),
    ("Проекты", "CODIX-HUB-RELEASES"),
]

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
    W, H = 1200, 800
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
         f'<rect width="{W}" height="640" rx="24" fill="url(#spot)"/>']

    # навигация
    b.append(t(48, 54, NICK.lower(), 15, INK, 700, font=MONO))
    for x, s in [(150, "Услуги"), (226, "Стек"), (282, "Проекты"), (368, "Контакты")]:
        b.append(t(x, 54, s, 15, extra='text-decoration="underline"'))
    b.append('<path d="M872 64 h52 a14 14 0 0 0 0-28 a20 20 0 0 0-38-6 a15 15 0 0 0-14 34 z" '
             'fill="none" stroke="#9A9A9A" stroke-width="1.6"/>')
    b.append(f'<rect x="878" y="46" width="40" height="14" rx="3" fill="{INK}"/>')
    b.append(t(898, 57, "ZDX", 10, "#fff", 700, "middle", MONO))
    b.append(t(950, 48, "GitHub ↗", 15, extra='text-decoration="underline"'))
    b.append(lines(950, 70, ["github.com/KUZURAKI", "Открыт для новых проектов"], 12.5, GREY, 18))

    # устройство
    b.append('<ellipse cx="600" cy="372" rx="370" ry="16" fill="#000" opacity="0.28" filter="url(#soft)"/>')
    b.append('<rect x="330" y="146" width="540" height="46" rx="12" fill="#FCFCFC" stroke="#D6D6D6"/>')
    b.append(t(600, 176, "idea → release", 17, "#3A3A3A", 500, "middle", MONO))
    b.append('<circle cx="372" cy="169" r="15" fill="#F4F4F4" stroke="#CFCFCF"/>'
             f'<circle cx="372" cy="169" r="9" fill="{ACC}"/>')
    b.append(f'<circle cx="826" cy="169" r="15" fill="{ACC}"/><circle cx="826" cy="169" r="9" fill="none" stroke="#fff" stroke-width="1.5" opacity="0.7"/>')
    b.append('<rect x="240" y="180" width="720" height="182" rx="42" fill="url(#body)" stroke="#C9C9C9"/>')
    b.append('<rect x="262" y="198" width="676" height="146" rx="24" fill="#0A0A0A"/>')
    b.append('<rect x="262" y="198" width="676" height="146" rx="24" fill="url(#dots)"/>')
    red = led(NICK, 292, 238, 9, "#FF2A1A", 3.7)
    b.append(f'<g filter="url(#glow)" opacity="0.85">{red}</g>')
    b.append(f'<g>{red}<animate attributeName="opacity" values="1;0.82;1;1" dur="3s" repeatCount="indefinite"/></g>')
    white = led("FULL", 790, 226, 4.5, "#F4F4F4", 1.9) + led("STACK", 790, 270, 4.5, "#F4F4F4", 1.9)
    b.append(f'<g filter="url(#glow)" opacity="0.5">{white}</g>{white}')

    # текст
    b.append(t(600, 432, f'<tspan font-weight="700">{NICK.lower()}</tspan> — fullstack-разработчик', 30, INK, 400, "middle",
               extra='letter-spacing="-0.5"'))
    b.append(t(600, 468, "Desktop-приложения, веб-сервисы, Telegram-боты и автоматизация", 17, "#333", 500, "middle"))
    b.append(lines(600, 504, ["Беру проект на этапе идеи и довожу до стабильного запуска:",
                              "интерфейс, API, база данных и сервер — в одних руках."], 15.5, GREY, 24, anchor="middle"))
    b.append(f'<rect x="452" y="566" width="140" height="44" rx="4" fill="{ACC}"/>')
    b.append(t(522, 593, "СВЯЗАТЬСЯ", 14, "#fff", 600, "middle", extra='letter-spacing="1"'))
    b.append(f'<rect x="608" y="566" width="140" height="44" rx="4" fill="none" stroke="{INK}" stroke-width="1.4"/>')
    b.append(t(678, 593, "ПРОЕКТЫ", 14, INK, 600, "middle", extra='letter-spacing="1"'))

    # полоса фич
    y0 = 646
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
    W, H = 1200, 790
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
         header(70, "01 — УСЛУГИ", "Что я делаю",
                "Закрываю задачу целиком или беру отдельную часть — фронтенд, бэкенд, бота или деплой.")]
    for i, (title, desc, tags) in enumerate(SERVICES):
        x, y = 60 + (i % 3) * 370, 210 + (i // 3) * 280
        b.append(f'<rect x="{x}" y="{y}" width="340" height="256" rx="16" fill="#fff" filter="url(#shadow)"/>')
        b.append(t(x + 26, y + 42, f"{i + 1:02d}", 13, ACC, 700, font=MONO))
        b.append(f'<rect x="{x + 300}" y="{y + 30}" width="14" height="14" rx="7" fill="none" stroke="#CFCFCF"/>')
        b.append(t(x + 26, y + 82, title, 22))
        b.append(lines(x + 26, y + 116, wrap(desc, 40), 13.5, "#666", 21))
        b.append(f'<line x1="{x + 26}" y1="{y + 196}" x2="{x + 314}" y2="{y + 196}" stroke="#EEEEEE"/>')
        b.append(pills(x + 26, y + 210, tags))
    svg("services.svg", W, H, "".join(b))


# ───────────────────────── 02 СТЕК ─────────────────────────
def stack():
    W, H = 1200, 640
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
         header(64, "02 — СТЕК", "Технологии по категориям",
                "От интерфейса и API до баз данных, AI и инфраструктуры.")]

    b.append('<rect x="320" y="300" width="560" height="150" rx="44" fill="url(#body)" stroke="#C6C6C6" filter="url(#shadow)"/>')
    labels = ["FRONTEND", "BACKEND", "OFF", "DATA/AI", "DEVOPS"]
    for i, s in enumerate(labels):
        y = 330 + i * 24
        if s == "BACKEND":
            b.append(f'<rect x="362" y="{y - 13}" width="72" height="18" rx="9" fill="{ACC}"/>')
            b.append(t(398, y, s, 10.5, "#fff", 700, "middle", MONO))
        else:
            b.append(t(398, y, s, 10.5, "#555", 600, "middle", MONO))
    b.append('<path d="M436 342 q20 0 30 12" fill="none" stroke="#777" stroke-width="1.4"/>')
    b.append(f'<rect x="452" y="350" width="78" height="26" rx="13" fill="{ACC}"/>'
             '<rect x="460" y="358" width="30" height="10" rx="5" fill="#fff" opacity="0.6"/>')
    b.append('<rect x="560" y="316" width="180" height="118" rx="14" fill="#FCFCFC" stroke="#D3D3D3"/>')
    b.append(t(650, 382, "git push", 20, "#333", 500, "middle", MONO))
    b.append(f'<circle cx="760" cy="318" r="16" fill="{ACC}"/>' + t(760, 321, "back", 8, "#fff", 700, "middle", MONO))
    b.append('<circle cx="816" cy="376" r="48" fill="#FAFAFA" stroke="#D3D3D3"/>')
    b.append(f'<circle cx="816" cy="376" r="38" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="2 4"/>')
    b.append(t(816, 381, "ok", 13, "#333", 600, "middle", MONO))

    line = 'fill="none" stroke="#9A9A9A" stroke-width="1"'
    dot = lambda x, y: f'<circle cx="{x}" cy="{y}" r="3" fill="#9A9A9A"/>'
    targets = [330, 354, 402, 426]
    for i, ((title, desc), ty) in enumerate(zip(STACK, targets)):
        y = 240 + i * 82
        b.append(t(70, y, title, 15, INK, 600))
        b.append(lines(70, y + 20, desc, 12, GREY, 16))
        b.append(f'<polyline points="250,{y - 5} 300,{y - 5} 352,{ty - 4}" {line}/>' + dot(352, ty - 4))
    b.append(t(520, 222, "Git и GitHub", 15, INK, 600))
    b.append(lines(520, 242, ["Ветки, ревью, релизы —", "каждая задача в истории."], 12, GREY, 16))
    b.append(f'<line x1="650" y1="270" x2="650" y2="340" {line}/>' + dot(650, 340))
    b.append(t(910, 222, "Рефакторинг", 15, INK, 600))
    b.append(lines(910, 242, ["Разбираю чужой код, чиню", "и ускоряю готовые проекты."], 12, GREY, 16))
    b.append(f'<polyline points="905,236 880,236 768,306" {line}/>' + dot(768, 306))
    b.append(f'<line x1="491" y1="376" x2="491" y2="520" {line}/>' + dot(491, 376))
    b.append(t(510, 530, "Фронт ↔ бэк", 15, INK, 600))
    b.append(t(510, 550, "Переключаюсь без потери контекста", 12, GREY))
    b.append(f'<polyline points="850,414 900,520 912,520" {line}/>' + dot(850, 414))
    b.append(t(920, 525, "Кроссплатформа", 15, INK, 600))
    b.append(lines(920, 545, ["Windows, macOS и Linux", "из одного кода."], 12, GREY, 16))
    svg("stack.svg", W, H, "".join(b))


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


# ───────────────────────── 05 СТАТИСТИКА ─────────────────────────
def stats_header():
    W, H = 1200, 200
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
         header(56, "05 — АКТИВНОСТЬ", "Статистика", "Цифры из GitHub — обновляются автоматически.")]
    svg("stats.svg", W, H, "".join(b))


# ───────────────────────── 06 КОНТАКТЫ ─────────────────────────
def contacts():
    W, H = 1200, 400
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="#FAFAFA"/>',
         header(72, "06 — КОНТАКТЫ", "Есть задача? Напишите.",
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
    for f in ("multitool.svg", "live.svg", "modes.svg"):
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            os.remove(p)
    hero(); services(); stack(); approach(); projects(); stats_header(); contacts(); footer()
