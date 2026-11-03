#!/usr/bin/env python3
"""Builds the profile assets from the user's supplied character art (src/fire.png -> src/cut2/*.png).
Run:  python3 build_fire.py        (writes ./assets/*.svg with the art embedded as base64)"""
import os, io, base64, random
from PIL import Image
import build_assets as B

HERE = os.path.dirname(os.path.abspath(__file__))
CUT = os.path.join(HERE, "src", "cut2")
YEL = "#ffd54a"


def cut(n):
    return Image.open(os.path.join(CUT, n + ".png"))


def uri(im, maxh=None):
    if maxh and im.size[1] > maxh:
        im = im.resize((round(im.size[0] * maxh / im.size[1]), maxh), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


import rig

_orig_save = B.save


def _save(name, content):
    if 'href="#IMG_' in content:  # inject the rig (images, clip-paths, animation CSS)
        content = content.replace("</style></defs>", rig.CSS + "</style>" + rig.defs() + "</defs>", 1)
    _orig_save(name, content)


B.save = _save


def place(n, x, gy, h, delay=0, flip=False, bob=True):
    if n == "boy":
        return rig.boy(x, gy, h, delay, flip)
    return rig.tri(x, gy, h, delay, flip)


def embers(w, h, n=14, seed=1, y0=None):
    r = random.Random(seed); o = ""
    for i in range(n):
        o += (f'<circle class="rise" cx="{r.randint(20, w - 20)}" cy="{(y0 or h) - r.randint(0, 40)}" r="{r.choice([1.6, 2.2, 3])}" '
              f'fill="{r.choice([B.AMBER, B.LIME, YEL])}" style="animation-delay:{r.random() * 4:.1f}s"/>')
    return o


def sky(w, h, id_="sk", glow=(.78, .75)):
    return (f'<linearGradient id="{id_}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0d0605"/><stop offset=".55" stop-color="#3a120c"/>'
            f'<stop offset="1" stop-color="#8a2e12"/></linearGradient>'
            f'<radialGradient id="{id_}g" cx="{glow[0]}" cy="{glow[1]}" r=".55"><stop offset="0" stop-color="#ff7a3d" stop-opacity=".55"/>'
            f'<stop offset="1" stop-color="#ff7a3d" stop-opacity="0"/></radialGradient>')


def hero():
    W, H = 1000, 520
    defs = (sky(W, H, "sk") + B.grad("nm", "", "", False, [(0, YEL), (.55, B.AMBER), (1, B.LIME)]) +
            B.grad("ed", "", "", False, [(0, B.EDGE), (.5, B.AMBER), (1, B.EDGE)]) +
            f'<clipPath id="cl"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="26"/></clipPath>')
    b = '<g clip-path="url(#cl)">'
    b += f'<rect width="{W}" height="{H}" fill="url(#sk)"/><rect width="{W}" height="{H}" fill="url(#skg)"/>'
    b += B.stars(W, H, 30, 4, 230)
    b += f'<circle class="glow" cx="800" cy="330" r="170" fill="#ff7a3d" opacity=".25"/><circle cx="800" cy="330" r="120" fill="#ff9a4d" opacity=".35"/>'
    b += B.volcano(590, 170, 1.25)
    b += B.ground(W, H, 460) + B.fern(24, 520, 1.1) + B.fern(985, 520, 1.0, True)
    b += embers(W, H, 22, 3, 480)
    g1, _ = place("tricera", 548, 500, 168, delay=.3)
    g2, _ = place("boy", 706, 506, 440, delay=0)
    b += g1 + g2 + "</g>"
    b += f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="26" fill="none" stroke="url(#ed)" stroke-width="2"/>'
    b += B.text(46, 64, "anurag@trainer-hq:~$ adventure --start", 14, B.LIME, "bold", B.MONO)
    b += f'<rect x="388" y="52" width="9" height="15" fill="{B.LIME}" class="pulse"/>'
    b += B.text(46, 126, "Hi, I'm", 30, B.BONE, "bold")
    b += (f'<text x="46" y="206" font-family="{B.DISPLAY}" font-size="78" font-weight="900" fill="url(#nm)" stroke="#0a0504" stroke-width="7" '
          f'paint-order="stroke" stroke-linejoin="round" textLength="500" lengthAdjust="spacingAndGlyphs">ANURAG VERMA</text>')
    b += B.text(48, 248, "Software Developer  |  AI / ML Enthusiast", 20, B.AMBER, "bold")
    b += B.text(48, 278, "Still thinking. Always building.", 15, B.MUTED)
    ch = [("#119", "HACKERRANK / 1,773", YEL), ("GOLD", "CODECHEF BADGE", B.AMBER), ("100%", "CLAIM PIPELINE", B.LIME)]
    for i, (v, l, c) in enumerate(ch):
        x = 48 + i * 128
        b += (f'<g transform="translate({x},312)"><rect width="118" height="58" rx="13" fill="{B.PANEL}" stroke="{B.EDGE}" stroke-width="1.5"/>'
              f'{B.text(59, 28, v, 22, c, "900", anchor="middle")}{B.text(59, 46, l, 8.5, B.MUTED, "bold", B.MONO, "middle")}</g>')
    b += (f'<g transform="translate(432,312)"><rect width="116" height="58" rx="13" fill="#3a1a10" stroke="{B.AMBER}" stroke-width="1.5"/>'
          f'<circle class="pulse" cx="22" cy="29" r="6" fill="{B.AMBER}"/>{B.text(36, 27, "OPEN TO", 12, B.AMBER, "900")}{B.text(36, 43, "WORK", 12, B.AMBER, "900")}</g>')
    b += B.text(48, 410, "THINK  >  BUILD  >  SHIP", 11.5, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    B.save("hero.svg", B.svg(W, H, b, defs))


def strip_bg(W, H, id_, seed):
    d = sky(W, H, id_, (.5, 1.0))
    r = (f'<clipPath id="c{id_}"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22"/></clipPath>'
         f'<g clip-path="url(#c{id_})"><rect width="{W}" height="{H}" fill="url(#{id_})"/><rect width="{W}" height="{H}" fill="url(#{id_}g)"/>'
         + B.stars(W, H, 14, seed, H // 2) + embers(W, H, 12, seed, H))
    return d, r


def herd():
    W, H = 1000, 220
    d, b = strip_bg(W, H, "hk", 6)
    b += f'<line x1="20" y1="{H - 18}" x2="{W - 20}" y2="{H - 18}" stroke="{B.EDGE}" stroke-width="3" class="dash"/>'
    gA, _ = place("tricera", 90, H - 14, 124, delay=0, flip=True)
    b += f'<g class="walkA" style="--d:330px;animation-delay:-1s">{gA}</g>'
    gB, _ = place("tricera", 790, H - 14, 124, delay=.5, flip=False)
    b += f'<g class="walkA" style="--d:-330px;animation-delay:-8.5s">{gB}</g>'
    gM, _ = place("boy", 452, H - 12, 196, delay=0)
    b += gM
    for i in range(7):
        b += B.footprint(60 + i * 140, H - 6, .45, B.LIME, .22, 90)
    b += "</g>" + f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="{B.EDGE}" stroke-width="2"/>'
    B.save("herd.svg", B.svg(W, H, b, d))


def about():
    W, H = 1000, 460
    d = sky(372, H, "ab", (.5, .95)) + '<clipPath id="art"><rect x="1" y="1" width="370" height="458" rx="22"/></clipPath>'
    b = f'<g clip-path="url(#art)"><rect width="372" height="{H}" fill="url(#ab)"/><rect width="372" height="{H}" fill="url(#abg)"/>'
    b += B.stars(372, H, 14, 5, 170) + '<circle class="glow" cx="190" cy="250" r="140" fill="#ff7a3d" opacity=".25"/>'
    b += B.volcano(120, 150, .8) + B.ground(372, H, 410)
    b += embers(372, H, 10, 8, 440)
    g1, _ = place("boy", 44, 452, 340, delay=0)
    g2, _ = place("tricera", 186, 456, 138, delay=.4)
    b += g1 + g2 + "</g>"
    b += B.text(404, 62, "// MY TRAINER HQ", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += B.text(404, 112, "Think it — then ship it", 38, B.BONE, "900")
    b += B.text(404, 140, "AI agent builder  ·  B.Tech CSE (AI) @ Parul University", 14, B.MUTED)
    feats = [("AGENTS THAT ACT", "Read pitch decks, verify claims, run voice interviews.", B.LIME),
             ("MULTI-AGENT TEAM", "Groq + Gemini orchestration, RAG that doesn't hallucinate.", B.AMBER),
             ("IDEA TO DEPLOYED", "From a messy 2 AM sketch to a demo-able product.", YEL)]
    for i, (t, dd, c) in enumerate(feats):
        y = 168 + i * 66
        b += (f'<g transform="translate(404,{y})"><rect width="556" height="56" rx="14" fill="{B.PANEL}" stroke="{B.EDGE}" stroke-width="1.5"/>'
              f'<rect x="10" y="10" width="36" height="36" rx="10" fill="{c}" opacity=".2"/>'
              f'<g transform="translate(28,28)"><path d="M-9,-3 L0,-12 L9,-3 M0,-12 L0,10" stroke="{c}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
              f'{B.text(60, 24, t, 12, c, "900", B.MONO, extra="letter-spacing=\"1.5\"")}{B.text(60, 43, dd, 13, B.BONE)}</g>')
    b += (f'<g transform="translate(404,372)"><rect width="556" height="46" rx="14" fill="#2e150c" stroke="{B.AMBER}" stroke-width="1.5"/>'
          f'{B.text(18, 29, chr(8220) + "If it can" + chr(8217) + "t be demoed, it isn" + chr(8217) + "t done." + chr(8221), 17, B.AMBER, "bold", extra="font-style=\"italic\"")}</g>')
    b += B.text(404, 442, "TOP 7% GLOBAL  ·  CODECHEF GOLD  ·  SIH 2026", 10.5, B.MUTED, "bold", B.MONO, extra='letter-spacing="1.5"')
    B.save("about.svg", B.frame(W, H, b, d))


def tools():
    W, H = 1000, 400
    d = ('<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd27a" stop-opacity=".5"/>'
         '<stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>')
    b = B.text(372, 56, "// CREATURE DEX", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += B.text(372, 98, "Tools in my backpack", 36, B.BONE, "900")
    b += B.stars(W, H, 10, 2, 60) + embers(360, H, 8, 4, 390)
    b += '<polygon class="glow" points="230,262 360,130 360,360" fill="url(#beam)"/>'
    g, _ = place("tricera", 18, 384, 220, delay=.3)
    b += g
    groups = [(B.AMBER, ["Groq", "Gemini", "RAG · FAISS", "ChromaDB", "Multi-Agent"]),
              (B.LIME, ["React", "Next.js", "Node.js", "Socket.io", "TypeScript"]),
              (YEL, ["MongoDB", "PostgreSQL", "SQLite", "Prisma", "SQL"]),
              (B.CORAL, ["Java", "C++", "Python", "Git", "FastAPI"])]
    for r, (c, items) in enumerate(groups):
        for i, it in enumerate(items):
            b += B.chip(372 + i * 120, 128 + r * 58, 112, 46, it, c, 13)
    b += B.text(372, 372, "AI · FULL STACK · DATA · CORE", 10.5, B.MUTED, "bold", B.MONO, extra='letter-spacing="2"')
    B.save("tools.svg", B.frame(W, H, b, d))


def stats():
    src = open(os.path.join(HERE, "assets", "stats.svg"), encoding="utf-8").read()
    head = uri(cut("head"), maxh=260)
    a = src.index('<g clip-path="url(#av)">'); end = src.index('<text x="190" y="272"')
    new = (f'<g clip-path="url(#av)"><image href="{head}" x="102" y="112" width="176" height="128" preserveAspectRatio="xMidYMax slice"/></g>')
    open(os.path.join(HERE, "assets", "stats.svg"), "w", encoding="utf-8").write(src[:a] + new + src[end:])
    print("patched stats.svg")


def hero_stats():
    W, H = 1000, 112
    b = ""
    items = [("#119", "HACKERRANK / 1,773", YEL), ("GOLD", "CODECHEF BADGE", B.AMBER), ("100%", "CLAIM PIPELINE", B.LIME), ("TOP 7%", "GLOBAL, JUN 2026", B.CORAL)]
    for i, (v, l, c) in enumerate(items):
        x = 30 + i * 176
        b += (f'<g transform="translate({x},26)"><rect width="164" height="60" rx="14" fill="{B.PANEL}" stroke="{B.EDGE}" stroke-width="1.5"/>'
              f'{B.text(82, 30, v, 24, c, "900", anchor="middle")}{B.text(82, 48, l, 9, B.MUTED, "bold", B.MONO, "middle")}</g>')
    b += (f'<g transform="translate(740,26)"><rect width="230" height="60" rx="14" fill="#3a1a10" stroke="{B.AMBER}" stroke-width="1.5"/>'
          f'<circle class="pulse" cx="26" cy="30" r="7" fill="{B.AMBER}"/>{B.text(44, 28, "OPEN TO THE RIGHT", 12, B.AMBER, "900")}{B.text(44, 46, "OPPORTUNITY", 12, B.AMBER, "900")}</g>')
    B.save("hero_stats.svg", B.frame(W, H, b))


def contact():
    W, H = 1000, 290
    b = B.stars(W, H, 12, 9, 70) + embers(400, H, 8, 2, 280)
    g, _ = place("boy", 36, 276, 224, delay=0)
    g2, _ = place("tricera", 200, 278, 112, delay=.5)
    b += g + g2
    b += B.text(420, 62, "// JOIN MY TEAM", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += B.text(420, 108, "Let's build something legendary", 32, B.BONE, "900")
    items = [("PORTFOLIO", "anurag-six.vercel.app", B.LIME), ("LINKEDIN", "in/anurag-verma4", "#5aa9ff"), ("GITHUB", "@Anu7276", B.AMBER)]
    for i, (k, v, c) in enumerate(items):
        x = 420 + i * 190
        b += (f'<g transform="translate({x},134)"><rect width="180" height="74" rx="14" fill="{B.PANEL}" stroke="{c}" stroke-width="1.5"/>'
              f'<rect x="16" y="16" width="22" height="5" rx="2.5" fill="{c}"/>{B.text(16, 44, k, 11, c, "900", B.MONO, extra="letter-spacing=\"2\"")}{B.text(16, 62, v, 13, B.BONE, "bold")}</g>')
    b += f'<circle class="pulse" cx="426" cy="238" r="5" fill="{B.AMBER}"/>' + B.text(440, 243, "Open to the right opportunity · freelance, collabs & hackathon teams", 12.5, B.MUTED)
    B.save("contact.svg", B.frame(W, H, b))


def footer():
    W, H = 1000, 230
    d, b = strip_bg(W, H, "ft", 13)
    g1, _ = place("tricera", 50, H - 12, 118, delay=.2)
    g2, _ = place("boy", 830, H - 8, 196, delay=0)
    g3, _ = place("tricera", 690, H - 12, 100, delay=.6, flip=True)
    b += g1 + g2 + g3 + "</g>"
    b += B.text(500, 100, "Code · Build · Learn · Evolve", 28, B.BONE, "900", anchor="middle", extra='stroke="#0a0504" stroke-width="5" paint-order="stroke"')
    b += B.text(500, 134, "Adventure awaits. Keep coding, keep growing.", 14.5, B.AMBER, "bold", anchor="middle")
    b += f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="{B.EDGE}" stroke-width="2"/>'
    B.save("footer.svg", B.svg(W, H, b, d))


if __name__ == "__main__":
    B.main()
    for f in ("hero.webp", "hero_poster.jpg"):
        p = os.path.join(HERE, "assets", f)
        if os.path.exists(p): os.remove(p)
    hero(); hero_stats(); herd(); about(); tools(); stats(); contact(); footer()
