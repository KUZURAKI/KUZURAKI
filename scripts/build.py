"""Генератор SVG-секций для профиля GitHub.

Запуск:  python scripts/build.py   → файлы появятся в assets/
"""
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets")

SANS = "Inter, 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "'JetBrains Mono', 'SFMono-Regular', Consolas, 'Courier New', monospace"
ACC = "#EB4B1F"
INK = "#151515"
GREY = "#8A8A8A"
BG = "#EDEDED"

# 5x7 пиксельный шрифт для LED-матрицы
FONT = {
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
    "C": ["01110", "10001", "10000", "10000", "10000", "10001", "01110"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01111"],
    "I": ["01110", "00100", "00100", "00100", "00100", "00100", "01110"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "X": ["10001", "10001", "01010", "00100", "01010", "10001", "10001"],
    "Z": ["11111", "00001", "00010", "00100", "01000", "10000", "11111"],
    "2": ["01110", "10001", "00001", "00010", "00100", "01000", "11111"],
    "4": ["00010", "00110", "01010", "10010", "11111", "00010", "00010"],
    "7": ["11111", "00001", "00010", "00100", "01000", "01000", "01000"],
    "/": ["00001", "00001", "00010", "00100", "01000", "10000", "10000"],
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


def svg(name, w, h, body, defs=""):
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
           f'<defs>{defs}</defs>{body}</svg>')
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(doc)
    print(name, len(doc) // 1024, "KB")


COMMON_DEFS = f"""
<filter id="shadow" x="-20%" y="-20%" width="140%" height="160%">
  <feDropShadow dx="0" dy="6" stdDeviation="10" flood-color="#000" flood-opacity="0.10"/>
</filter>
<filter id="glow" x="-10%" y="-30%" width="120%" height="160%">
  <feGaussianBlur stdDeviation="3.5"/>
</filter>
<linearGradient id="body" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#FAFAFA"/><stop offset="1" stop-color="#D2D2D2"/>
</linearGradient>
"""


# ───────────────────────── HERO ─────────────────────────
def hero():
    W, H = 1200, 780
    defs = COMMON_DEFS + f"""
<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#F7F7F7"/><stop offset="1" stop-color="#E4E4E4"/>
</linearGradient>
<radialGradient id="spot" cx="0.5" cy="0.35" r="0.5">
  <stop offset="0" stop-color="#FFFFFF" stop-opacity="0.9"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/>
</radialGradient>
<pattern id="dots" x="292" y="238" width="9" height="9" patternUnits="userSpaceOnUse">
  <circle cx="4.5" cy="4.5" r="1.9" fill="#1E1E1E"/>
</pattern>
<filter id="soft" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="12"/></filter>
"""
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="url(#bg)"/>',
         f'<rect width="{W}" height="620" rx="24" fill="url(#spot)"/>']

    # навигация
    b.append(t(48, 54, "Home", 15))
    for x, s in [(110, "Projects"), (196, "Stack"), (262, "Stats")]:
        b.append(t(x, 54, s, 15, extra='text-decoration="underline"'))
    # облако справа
    b.append('<path d="M872 64 h52 a14 14 0 0 0 0-28 a20 20 0 0 0-38-6 a15 15 0 0 0-14 34 z" '
             'fill="none" stroke="#9A9A9A" stroke-width="1.6"/>')
    b.append(f'<rect x="878" y="46" width="40" height="14" rx="3" fill="{INK}"/>')
    b.append(t(898, 57, "ZDX", 10, "#fff", 700, "middle", MONO))
    b.append(t(950, 48, "GitHub Profile ↗", 15, extra='text-decoration="underline"'))
    b.append(lines(950, 70, ["Desktop · Backend · Automation", "Rust, Tauri, React, Python"], 12.5, GREY, 18))

    # устройство
    b.append('<ellipse cx="600" cy="372" rx="370" ry="16" fill="#000" opacity="0.28" filter="url(#soft)"/>')
    b.append('<rect x="330" y="146" width="540" height="46" rx="12" fill="#FCFCFC" stroke="#D6D6D6"/>')
    b.append(t(600, 176, "git push", 17, "#3A3A3A", 500, "middle", MONO))
    b.append('<circle cx="372" cy="169" r="15" fill="#F4F4F4" stroke="#CFCFCF"/>'
             f'<circle cx="372" cy="169" r="9" fill="{ACC}"/>')
    b.append(f'<circle cx="826" cy="169" r="15" fill="{ACC}"/><circle cx="826" cy="169" r="9" fill="none" stroke="#fff" stroke-width="1.5" opacity="0.7"/>')
    b.append('<rect x="240" y="180" width="720" height="182" rx="42" fill="url(#body)" stroke="#C9C9C9"/>')
    b.append('<rect x="262" y="198" width="676" height="146" rx="24" fill="#0A0A0A"/>')
    b.append('<rect x="262" y="198" width="676" height="146" rx="24" fill="url(#dots)"/>')
    red = led("ZEDKODEX", 292, 238, 9, "#FF2A1A", 3.7)
    b.append(f'<g filter="url(#glow)" opacity="0.85">{red}</g>')
    b.append(f'<g>{red}<animate attributeName="opacity" values="1;0.82;1;1" dur="3s" repeatCount="indefinite"/></g>')
    white = led("24/7", 806, 226, 4.5, "#F4F4F4", 1.9) + led("CODE", 806, 270, 4.5, "#F4F4F4", 1.9)
    b.append(f'<g filter="url(#glow)" opacity="0.5">{white}</g>{white}')

    # текст
    b.append(f'<text x="372" y="428" font-family="{SANS}" font-size="17" fill="{INK}">'
             f'<tspan font-weight="700">ZEDKODEX</tspan> — разработчик desktop-приложений,</text>')
    b.append(lines(372, 454, ["бэкенда и автоматизации. Делаю быстрые инструменты",
                              "на Rust и Tauri, Telegram-ботов и self-hosted сервисы.",
                              "Open-source и hacker-friendly."], 17, INK, 26))
    b.append(f'<rect x="540" y="540" width="120" height="44" rx="4" fill="{ACC}"/>')
    b.append(t(600, 567, "ПРОЕКТЫ", 14, "#fff", 600, "middle", extra='letter-spacing="1"'))

    # полоса фич
    b.append('<line x1="0" y1="626" x2="1200" y2="626" stroke="#D3D3D3"/>')
    b.append('<line x1="400" y1="626" x2="400" y2="780" stroke="#D3D3D3"/><line x1="800" y1="626" x2="800" y2="780" stroke="#D3D3D3"/>')
    ic = 'fill="none" stroke="#5A5A5A" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"'
    icons = [
        f'<g {ic}><circle cx="62" cy="680" r="19"/><path d="M62 668 v12 l8 6"/><path d="M50 662 l-4-4 M74 662 l4-4"/></g>',
        f'<g {ic}><rect x="444" y="664" width="13" height="13"/><rect x="463" y="664" width="13" height="13"/>'
        f'<rect x="444" y="683" width="13" height="13"/><path d="M469.5 683 v13 M463 689.5 h13"/></g>',
        f'<g {ic}><path d="M858 664 l10 6 v12 l-10 6 l-10-6 v-12 z"/><circle cx="858" cy="676" r="3.5"/>'
        f'<path d="M872 682 l7 4 v8 l-7 4 l-7-4 v-8 z"/></g>',
    ]
    cols = [("Desktop-приложения", ["Tauri 2 + React 19: лёгкие и быстрые,", "Windows и macOS из одного кода"]),
            ("Бэкенд и API", ["Axum, Tokio, FastAPI, SQLite,", "Docker, nginx, деплой на VPS"]),
            ("Автоматизация", ["Telegram-боты, рассылки, скрипты —", "всё, что можно не делать руками"])]
    for i, (title, desc) in enumerate(cols):
        x = i * 400 + 104
        b.append(icons[i])
        b.append(t(x, 676, title, 16))
        b.append(lines(x, 700, desc, 13, GREY, 19))
    svg("hero.svg", W, H, "".join(b), defs)


# ───────────────────────── MULTI-TOOL ─────────────────────────
def card(x, y, w, h, icon, title, desc, bullets):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="#fff" filter="url(#shadow)"/>', icon(x + 32, y + 40),
           t(x + 54, y + 49, title, 24), lines(x + 24, y + 84, desc, 15, INK, 22)]
    by = y + 84 + len(desc) * 22 + 18
    for i, s in enumerate(bullets):
        out.append(t(x + 28, by + i * 27, "•", 13, GREY))
        out.append(t(x + 42, by + i * 27, s, 13, "#555"))
    return "".join(out)


def ic_status(cx, cy):
    return f'<circle cx="{cx}" cy="{cy}" r="12" fill="{ACC}"/><rect x="{cx - 6}" y="{cy - 1.7}" width="12" height="3.4" rx="1" fill="#fff"/>'


def ic_apps(cx, cy):
    s = 9
    return "".join(f'<rect x="{cx - 11 + dx}" y="{cy - 11 + dy}" width="{s}" height="{s}" rx="1.5" fill="{INK}"/>'
                   for dx in (0, 12) for dy in (0, 12))


def ic_bolt(cx, cy):
    return (f'<circle cx="{cx}" cy="{cy}" r="12" fill="{INK}"/>'
            f'<path d="M{cx + 2} {cy - 8} l-7 10 h5 l-2 7 l7-10 h-5 z" fill="#fff"/>')


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


def multitool():
    W, H = 1200, 780
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
         t(600, 108, "Мультитул разработчика", 46, INK, 400, "middle", extra='letter-spacing="-1"')]

    b.append(card(60, 160, 330, 290, ic_status, "CODIX HUB",
                  ["Личный центр автоматизации:", "деплой, хранилище и заказы."],
                  ["Деплой на VPS: nginx, Docker, SSL", "Заказы и отзывы из Telegram",
                   "Отложенные рассылки в каналы", "Удаление фона нейросетью офлайн", "Windows · macOS · v1.0.0"]))

    # устройство сверху
    d = ['<rect x="420" y="196" width="720" height="250" rx="44" fill="url(#body)" stroke="#C9C9C9" filter="url(#shadow)"/>',
         '<rect x="610" y="160" width="340" height="66" rx="10" fill="#FDFDFD" stroke="#D6D6D6"/>',
         t(780, 200, "git push ⏎", 20, "#333", 500, "middle", MONO),
         '<circle cx="505" cy="214" r="46" fill="#FAFAFA" stroke="#D3D3D3"/>',
         f'<circle cx="505" cy="214" r="30" fill="none" stroke="{ACC}" stroke-width="3" stroke-dasharray="2 4"/>',
         f'<circle cx="505" cy="214" r="18" fill="{ACC}"/>',
         t(505, 218, "ok", 11, "#fff", 600, "middle", MONO),
         f'<rect x="1020" y="200" width="80" height="24" rx="12" fill="{ACC}"/>',
         t(1060, 192, "BACKEND", 9, "#666", 600, "middle", MONO),
         '<rect x="440" y="262" width="680" height="166" rx="26" fill="#0B0B0B"/>']
    m = dict(font=MONO)
    d.append(t(466, 294, "Stack via ⚡ RUST", 12, "#E6E6E6", **m))
    d.append(lines(466, 316, ["› Tauri 2 / React 19", "› Axum / Tokio", "› FastAPI / Python"], 11, "#9C9C9C", 17, **m))
    d.append(t(466, 404, "open-source", 10, "#666", **m))
    d.append('<rect x="690" y="278" width="176" height="114" rx="8" fill="#141414" stroke="#2E2E2E"/>')
    d.append(t(778, 300, "▶▶▶ ACTIVE ◀◀◀", 11, "#EDEDED", 600, "middle", MONO))
    d.append(t(744, 344, "▶25", 34, "#fff", 700, "middle", MONO))
    d.append(f'<text x="788" y="342" font-family="{MONO}" font-size="30" font-weight="700" fill="#fff" text-anchor="middle">:'
             '<animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></text>')
    d.append(t(822, 344, "59", 34, "#fff", 700, "middle", MONO))
    d.append('<rect x="736" y="356" width="84" height="22" rx="2" fill="#F2F2F2"/>')
    d.append(t(778, 372, "CODING", 14, "#000", 800, "middle", MONO))
    d.append(t(892, 294, "Contact via GitHub", 12, "#E6E6E6", **m))
    d.append(lines(892, 316, ["› github.com/KUZURAKI", "› Windows / macOS"], 11, "#9C9C9C", 17, **m))
    d.append(pixel_logo(1062, 350, 2.4))
    b += d

    b.append(card(60, 480, 330, 260, ic_apps, "Стек",
                  ["Rust — для скорости, React —", "для UI, Python — для ботов."],
                  ["Rust · Tokio · Axum", "TypeScript · React · Vite", "Python · FastAPI", "SQLite · Docker · nginx"]))
    b.append(card(410, 480, 330, 260, ic_bolt, "Автоматизация",
                  ["Telegram-боты, рассылки и", "деплой без ручной рутины."],
                  ["Telegram API / Telethon", "SSH-терминал и VPS", "Нейросети на устройстве (ONNX)", "Скрипты на PowerShell"]))

    # терминал
    b.append(f'<rect x="760" y="480" width="380" height="260" rx="16" fill="#fff" stroke="{INK}" stroke-width="1.8"/>')
    b.append(t(784, 514, "&gt;_ Developer friendly", 16, INK, 600, font=MONO))
    b.append(t(1116, 512, "_ □ ×", 13, "#9A9A9A", 400, "end", MONO))
    b.append(f'<line x1="760" y1="530" x2="1140" y2="530" stroke="{INK}" stroke-width="1.2"/>')
    c1 = ["Rust / Tauri 2", "React 19 + TS", "Axum + Tokio", "FastAPI", "SQLite", "ONNX Runtime"]
    c2 = ["Docker / nginx", "SSH deploy", "Windows / macOS", "Open-source", "No vendor lock-in", "Self-hosted"]
    b.append(lines(784, 562, ["&gt; " + s for s in c1], 12, "#333", 26, font=MONO))
    b.append(lines(962, 562, ["&gt; " + s for s in c2], 12, "#333", 26, font=MONO))
    b.append(f'<rect x="1100" y="702" width="9" height="15" fill="{ACC}">'
             '<animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')
    svg("multitool.svg", W, H, "".join(b), COMMON_DEFS)


# ───────────────────────── LIVE STATUS ─────────────────────────
def live():
    W, H = 1200, 560
    defs = COMMON_DEFS + """
<linearGradient id="mon" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="#F6F6F6"/><stop offset="1" stop-color="#C9C9C9"/>
</linearGradient>
<linearGradient id="desk" x1="0" y1="0" x2="0" y2="1">
  <stop offset="0" stop-color="#EDE7DC"/><stop offset="1" stop-color="#D9D0C1"/>
</linearGradient>
<filter id="soft" x="-20%" y="-200%" width="140%" height="500%"><feGaussianBlur stdDeviation="10"/></filter>
"""
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="#FAFAFA"/>',
         t(70, 140, "Live-статус", 44, INK, 400, extra='letter-spacing="-1"'),
         lines(70, 182, ["Профиль живёт сам: коммиты, релизы", "и статистика подтягиваются автоматически,",
                         "пока я пишу код."], 16, "#333", 24)]
    ic = 'fill="none" stroke="#222" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"'
    rows = [
        (f'<g {ic}><rect x="70" y="282" width="26" height="20" rx="3"/><path d="M76 289 l4 3 l-4 3 M83 296 h6"/></g>',
         "Статус «Coding»", ["Открыт редактор — значит, что-то", "уже компилируется."]),
        (f'<g {ic}><circle cx="76" cy="356" r="3.5"/><circle cx="76" cy="380" r="3.5"/><circle cx="92" cy="362" r="3.5"/>'
         f'<path d="M76 359.5 v17 M92 365.5 q0 9 -14 12"/></g>',
         "Релизы", ["Новые версии CODIX HUB сразу", "в CODIX-HUB-RELEASES."]),
        (f'<g {ic}><rect x="70" y="430" width="28" height="19" rx="2"/><path d="M80 449 v5 M76 455 h12"/></g>',
         "Мультиплатформенность", ["Windows / macOS / Linux"]),
    ]
    for i, (icon, title, desc) in enumerate(rows):
        y = 292 + i * 74
        b.append(icon)
        b.append(t(116, y, title, 15, INK, 600))
        b.append(lines(116, y + 20, desc, 12.5, GREY, 17))

    # стол, монитор, табличка
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
    # растение
    b.append('<path d="M1090 438 h44 l-5 32 h-34 z" fill="#FBFBFB" stroke="#D0D0D0"/>')
    for dx, dy, rot in [(-12, -12, -40), (12, -12, 40), (0, -18, 0), (-20, -2, -70), (20, -2, 70)]:
        b.append(f'<ellipse cx="{1112 + dx}" cy="{434 + dy}" rx="6" ry="13" fill="#6E8F4E" '
                 f'transform="rotate({rot} {1112 + dx} {434 + dy})"/>')
    svg("live.svg", W, H, "".join(b), defs)


# ───────────────────────── STATS HEADER ─────────────────────────
def stats_header():
    W, H = 1200, 200
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
         t(600, 100, "Статистика", 44, INK, 400, "middle", extra='letter-spacing="-1"'),
         t(600, 140, "Цифры из GitHub — обновляются автоматически, даже когда я сплю.", 16, "#444", 400, "middle")]
    svg("stats.svg", W, H, "".join(b))


# ───────────────────────── MODES / CONTROLS ─────────────────────────
def modes():
    W, H = 1200, 640
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="{BG}"/>',
         t(600, 96, "Режимы работы", 44, INK, 400, "middle", extra='letter-spacing="-1"'),
         t(600, 136, "Физические переключатели в голове: один режим — одна задача.", 16, "#333", 400, "middle"),
         t(600, 160, "Большие кнопки — чтобы не промахнуться в три часа ночи.", 16, "#333", 400, "middle")]

    # панель
    b.append('<rect x="320" y="300" width="560" height="150" rx="44" fill="url(#body)" stroke="#C6C6C6" filter="url(#shadow)"/>')
    labels = ["DESKTOP", "BACKEND", "OFF", "BOTS", "DEPLOY"]
    for i, s in enumerate(labels):
        y = 330 + i * 24
        if s == "BACKEND":
            b.append(f'<rect x="364" y="{y - 13}" width="68" height="18" rx="9" fill="{ACC}"/>')
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
    # левые подписи
    left = [("Desktop", ["Tauri + React: окна,", "трей, автозапуск"]),
            ("Backend", ["Axum и FastAPI —", "API, базы, очереди"]),
            ("Боты", ["Telegram: заказы,", "отзывы, рассылки"]),
            ("Деплой", ["VPS, Docker, nginx,", "SSL за одну кнопку"])]
    targets = [330, 354, 402, 426]
    for i, ((title, desc), ty) in enumerate(zip(left, targets)):
        y = 240 + i * 82
        b.append(t(70, y, title, 15, INK, 600))
        b.append(lines(70, y + 20, desc, 12, GREY, 16))
        b.append(f'<polyline points="214,{y - 5} 290,{y - 5} 350,{ty - 4}" {line}/>' + dot(350, ty - 4))
    # верх
    b.append(t(520, 222, "Кнопка git push", 15, INK, 600))
    b.append(lines(520, 242, ["Коммит и пуш. Работает", "и как OK в меню."], 12, GREY, 16))
    b.append(f'<line x1="650" y1="270" x2="650" y2="340" {line}/>' + dot(650, 340))
    b.append(t(910, 222, "Кнопка Back", 15, INK, 600))
    b.append(lines(910, 242, ["git revert — если что-то", "пошло не так."], 12, GREY, 16))
    b.append(f'<polyline points="905,236 880,236 768,306" {line}/>' + dot(768, 306))
    # низ
    b.append(f'<line x1="491" y1="376" x2="491" y2="520" {line}/>' + dot(491, 376))
    b.append(t(510, 530, "5-позиционный селектор", 15, INK, 600))
    b.append(t(510, 550, "Переключение между режимами", 12, GREY))
    b.append(f'<polyline points="850,414 900,520 912,520" {line}/>' + dot(850, 414))
    b.append(t(920, 525, "Колесо прокрутки", 15, INK, 600))
    b.append(lines(920, 545, ["Листаю логи и документацию,", "OK — запуск сборки."], 12, GREY, 16))
    svg("modes.svg", W, H, "".join(b), COMMON_DEFS)


# ───────────────────────── FOOTER ─────────────────────────
def footer():
    W, H = 1200, 250
    b = [f'<rect width="{W}" height="{H}" rx="24" fill="#0A0A0A"/>',
         led("ZEDKODEX", 60, 66, 4, "#F2F2F2", 1.7),
         t(60, 132, "Desktop · Backend · Automation", 13, "#8C8C8C"),
         lines(60, 190, ["Designed &amp; coded by ZEDKODEX", "© 2026 All rights reserved"], 12, "#5E5E5E", 18)]
    for x, items in [(460, ["Projects", "Releases"]), (600, ["Stack", "Stats"]), (720, ["GitHub", "CODIX HUB"])]:
        b.append(lines(x, 82, items, 15, "#F2F2F2", 28))
    b.append(lines(1140, 82, ["github.com/KUZURAKI ↗"], 14, "#F2F2F2", anchor="end"))
    b.append(lines(1140, 190, ["Windows · macOS · Linux", "Rust · TypeScript · Python"], 12, "#5E5E5E", 18, anchor="end"))
    b.append(f'<rect x="1120" y="100" width="20" height="4" fill="{ACC}"/>')
    svg("footer.svg", W, H, "".join(b))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    hero(); multitool(); live(); stats_header(); modes(); footer()
