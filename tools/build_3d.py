#!/usr/bin/env python3
"""3D-look re-skin of the whole profile (fire theme): perspective floors, isometric podiums/towers,
extruded titles, 3D keycap chips, parallax layers, drop shadows. Characters are the user's own art (animated rig).
Run:  python3 build_3d.py"""
import os, random, math
import build_assets as B
import build_fire as F
import rig

OUT = B.OUT
YEL = F.YEL
EXTRA = """
.par1{animation:par1 70s linear infinite}@keyframes par1{to{transform:translateX(-1000px)}}
.par2{animation:par2 40s linear infinite}@keyframes par2{to{transform:translateX(-1000px)}}
.fl{animation:fl 3.4s ease-in-out infinite}@keyframes fl{0%,100%{transform:translateY(0)}50%{transform:translateY(-12px)}}
.shine{animation:shine 5s ease-in-out infinite}@keyframes shine{0%{transform:translateX(-260px)}55%,100%{transform:translateX(460px)}}
.rim{animation:rim 2.6s ease-in-out infinite}@keyframes rim{0%,100%{opacity:.35}50%{opacity:1}}
.rise3{animation:rise3 3.2s ease-out infinite;transform-box:fill-box;transform-origin:bottom}@keyframes rise3{0%{transform:scaleY(0)}60%{transform:scaleY(1)}100%{transform:scaleY(1)}}
"""


# ------------------------------------------------------------------ 3D toolkit
def shade(hexc, f):
    h = hexc.lstrip("#"); r, g, b = (int(h[i:i + 2], 16) for i in (0, 2, 4))
    return "#%02x%02x%02x" % tuple(max(0, min(255, int(c * f))) for c in (r, g, b))


def iso_box(cx, cy, w, d, h, top, left=None, right=None, stroke="#0a0504", sw=1.5, cls="", style=""):
    """Isometric cuboid. (cx,cy) = centre of the BASE rhombus; w = half width, d = half depth, h = height."""
    left = left or shade(top, .62); right = right or shade(top, .42)
    T = f"{cx},{cy - h - d} {cx + w},{cy - h} {cx},{cy - h + d} {cx - w},{cy - h}"
    L = f"{cx - w},{cy - h} {cx},{cy - h + d} {cx},{cy + d} {cx - w},{cy}"
    R = f"{cx},{cy - h + d} {cx + w},{cy - h} {cx + w},{cy} {cx},{cy + d}"
    a = f'stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="round"'
    c = f' class="{cls}"' if cls else ""
    s = f' style="{style}"' if style else ""
    return f'<g{c}{s}><polygon points="{L}" fill="{left}" {a}/><polygon points="{R}" fill="{right}" {a}/><polygon points="{T}" fill="{top}" {a}/></g>'


def ext_text(x, y, s, size, fill, depth=9, side="#b8401a", far="#2a0b05", anchor="start", extra="", sw=6):
    out = ""
    def lerp(i):
        t = i / max(depth, 1)
        c1 = [int(side.lstrip('#')[k:k + 2], 16) for k in (0, 2, 4)]; c2 = [int(far.lstrip('#')[k:k + 2], 16) for k in (0, 2, 4)]
        return "#%02x%02x%02x" % tuple(int(c1[k] + (c2[k] - c1[k]) * t) for k in range(3))
    for i in range(depth, 0, -1):
        out += (f'<text x="{x + i * .6:.1f}" y="{y + i:.1f}" font-family="{B.DISPLAY}" font-size="{size}" font-weight="900" '
                f'fill="{lerp(i)}" stroke="{lerp(i)}" stroke-width="1" text-anchor="{anchor}" {extra}>{B.esc(s)}</text>')
    out += (f'<text x="{x}" y="{y}" font-family="{B.DISPLAY}" font-size="{size}" font-weight="900" fill="{fill}" stroke="#0a0504" '
            f'stroke-width="{sw}" paint-order="stroke" stroke-linejoin="round" text-anchor="{anchor}" {extra}>{B.esc(s)}</text>')
    return out


def keycap(x, y, w, h, color=None, r=12, depth=7, top="#2c1710", label=None):
    edge = color or B.EDGE
    return (f'<rect x="{x}" y="{y + depth}" width="{w}" height="{h}" rx="{r}" fill="#0f0705" stroke="#0a0504" stroke-width="1.5"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{top}" stroke="{edge}" stroke-width="1.5"/>'
            f'<rect x="{x + 5}" y="{y + 3}" width="{w - 10}" height="2.5" rx="1.2" fill="#fff" opacity=".13"/>')


def chip3d(x, y, w, h, label, dot, size=13):
    return (keycap(x, y, w, h, dot, 11, 6) + f'<circle cx="{x + 16}" cy="{y + h / 2}" r="5" fill="{dot}"/>'
            f'<circle cx="{x + 16}" cy="{y + h / 2}" r="8" fill="{dot}" opacity=".2"/>'
            + B.text(x + 30, y + h / 2 + 4.6, label, size, B.BONE, "bold"))


def mountains(period, seed, color, base, amp, op=1.0, cls="par1"):
    r = random.Random(seed); n = 9
    pts = [(i * period / n, base - r.randint(int(amp * .25), amp)) for i in range(n)]
    path = []
    for rep in range(3):
        for i, (px, py) in enumerate(pts):
            path.append((px + rep * period, py))
    d = "M-%d,%d " % (period, base) + " ".join(f"L{px - period:.0f},{py}" for px, py in path) + f" L{2 * period},{base} L{2 * period},700 L-{period},700Z"
    return f'<g class="{cls}"><path d="{d}" fill="{color}" opacity="{op}"/></g>'


def volcano3d(cx, by, w, h):
    ax, ay = cx, by - h
    smoke = "".join(f'<circle class="smoke" cx="{ax}" cy="{ay - 6}" r="{w * .045:.0f}" fill="#6b4a40" style="animation-delay:{i * 2}s"/>' for i in range(3))
    emb = "".join(f'<circle class="rise" cx="{ax + (i - 3) * w * .018:.0f}" cy="{ay + 4}" r="2.6" fill="{B.AMBER}" style="animation-delay:{i * .6:.1f}s"/>' for i in range(7))
    return (smoke +
            f'<polygon points="{cx - w / 2},{by} {ax - w * .1},{ay} {ax + w * .1},{ay} {cx + w / 2},{by}" fill="#4a2418"/>'
            f'<polygon points="{cx + w * .04},{by} {ax + w * .1},{ay} {cx + w / 2},{by}" fill="#2a130d"/>'
            f'<polygon points="{cx - w / 2},{by} {ax - w * .1},{ay} {ax - w * .02},{ay} {cx - w * .26},{by}" fill="#6a3322" opacity=".8"/>'
            f'<ellipse class="glow" cx="{ax}" cy="{ay}" rx="{w * .105:.0f}" ry="11" fill="{B.LAVA}"/><ellipse cx="{ax}" cy="{ay}" rx="{w * .08:.0f}" ry="7" fill="{B.AMBER}"/>'
            f'<path class="glow" d="M{ax - 8},{ay + 6} C{ax - w * .06},{ay + h * .4} {ax - w * .2},{ay + h * .6} {ax - w * .3},{by}" stroke="{B.LAVA}" stroke-width="7" fill="none" stroke-linecap="round"/>'
            f'<path class="glow" d="M{ax + 6},{ay + 6} C{ax + w * .05},{ay + h * .5} {ax + w * .12},{ay + h * .7} {ax + w * .2},{by}" stroke="{B.AMBER}" stroke-width="5" fill="none" stroke-linecap="round"/>'
            + emb)


def floor(W, H, y0, vp=(500, 300), cols=14):
    d = (f'<linearGradient id="fl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a1209"/><stop offset="1" stop-color="#0a0403"/></linearGradient>'
         f'<linearGradient id="fog" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff7a3d" stop-opacity="0"/><stop offset=".5" stop-color="#ff7a3d" stop-opacity=".25"/><stop offset="1" stop-color="#ff7a3d" stop-opacity="0"/></linearGradient>'
         f'<clipPath id="flc"><rect x="0" y="{y0}" width="{W}" height="{H - y0}"/></clipPath>')
    b = f'<rect y="{y0}" width="{W}" height="{H - y0}" fill="url(#fl)"/><g clip-path="url(#flc)">'
    for i in range(-cols, cols + 1):
        xb = W / 2 + i * (W / cols) * 1.5
        b += f'<line x1="{vp[0]}" y1="{vp[1]}" x2="{xb:.0f}" y2="{H}" stroke="{B.LIME}" stroke-width="1.6" opacity=".28" class="dash"/>'
    for k in range(1, 8):
        y = y0 + (H - y0) * (k / 7) ** 2
        b += f'<line x1="0" y1="{y:.0f}" x2="{W}" y2="{y:.0f}" stroke="{B.AMBER}" stroke-width="1.2" opacity="{.1 + k * .04:.2f}"/>'
    b += "</g>" + f'<rect y="{y0 - 22}" width="{W}" height="44" fill="url(#fog)"/>'
    return d, b


def place(n, x, gy, h, delay=0, flip=False, shadow=True):
    g, w = F.place(n, x, gy, h, delay, flip)
    sh = f'<ellipse cx="{x + w / 2}" cy="{gy + 2}" rx="{w * .42:.0f}" ry="{max(5, h * .035):.0f}" fill="#000" opacity=".42"/>' if shadow else ""
    return sh + g, w


# ------------------------------------------------------------------ HERO
def hero():
    W, H = 1000, 560
    fd, fb = floor(W, H, 424, (500, 300))
    defs = (F.sky(W, H, "sk", (.8, .7)) + fd + B.grad("nm", "", "", False, [(0, YEL), (.55, B.AMBER), (1, B.LIME)]) +
            B.grad("ed", "", "", False, [(0, B.EDGE), (.5, B.AMBER), (1, B.EDGE)]) +
            f'<clipPath id="cl"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="26"/></clipPath>'
            f'<radialGradient id="pg" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#ff7a3d" stop-opacity=".6"/><stop offset="1" stop-color="#ff7a3d" stop-opacity="0"/></radialGradient>')
    b = '<g clip-path="url(#cl)">'
    b += f'<rect width="{W}" height="{H}" fill="url(#sk)"/><rect width="{W}" height="{H}" fill="url(#skg)"/>' + B.stars(W, H, 34, 4, 230)
    b += '<circle class="glow" cx="800" cy="300" r="190" fill="#ff7a3d" opacity=".22"/><circle cx="800" cy="300" r="120" fill="#ff9a4d" opacity=".3"/>'
    b += mountains(1000, 3, "#2a120d", 400, 120, .95, "par1") + mountains(1000, 9, "#1c0b08", 430, 90, 1, "par2")
    b += volcano3d(800, 440, 440, 250)
    b += fb
    # podium
    cx, cy, w, d, h = 775, 486, 235, 66, 30
    b += f'<ellipse cx="{cx}" cy="{cy + d + 6}" rx="{w + 30}" ry="22" fill="#000" opacity=".4"/>'
    b += iso_box(cx, cy, w, d, h, "#43200f", "#2b130a", "#1b0b06", sw=2)
    top = f"{cx},{cy - h - d} {cx + w},{cy - h} {cx},{cy - h + d} {cx - w},{cy - h}"
    b += f'<polygon points="{top}" fill="none" stroke="{B.LIME}" stroke-width="3" class="rim"/>'
    b += (f'<polygon points="{cx},{cy - h - d + 16} {cx + w - 50},{cy - h} {cx},{cy - h + d - 16} {cx - w + 50},{cy - h}" fill="url(#pg)" opacity=".7"/>'
          f'<polygon points="{cx},{cy - h - d + 16} {cx + w - 50},{cy - h} {cx},{cy - h + d - 16} {cx - w + 50},{cy - h}" fill="none" stroke="{B.AMBER}" stroke-width="1.5" stroke-dasharray="6 6" class="dash"/>')
    # floating gems
    for (gx, gy2, ww, hh, col, dl) in [(580, 150, 16, 22, B.AMBER, 0), (940, 130, 14, 18, YEL, .8), (610, 300, 12, 16, B.LIME, 1.6), (965, 300, 13, 16, B.CORAL, 2.2)]:
        b += iso_box(gx, gy2, ww, ww * .55, hh, col, cls="fl", style=f"animation-delay:{dl}s")
    gB, _ = place("boy", 690, cy - h + 12, 410, delay=0)
    gT, _ = place("tricera", 650, cy - h + 36, 152, delay=.4)
    rf = (f'<clipPath id="podtop"><polygon points="{top}"/></clipPath><g clip-path="url(#podtop)" opacity=".2">'
          f'<g transform="translate(0,{2 * (cy - h + 12)}) scale(1,-1)">{gB}</g><g transform="translate(0,{2 * (cy - h + 36)}) scale(1,-1)">{gT}</g></g>')
    b += rf + gB + gT + F.embers(W, H, 18, 3, 500) + "</g>"
    b += f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="26" fill="none" stroke="url(#ed)" stroke-width="2"/>'
    b += B.text(46, 64, "anurag@trainer-hq:~$ adventure --start", 14, B.LIME, "bold", B.MONO)
    b += f'<rect x="388" y="52" width="9" height="15" fill="{B.LIME}" class="pulse"/>'
    b += B.text(46, 126, "Hi, I'm", 30, B.BONE, "bold")
    b += ext_text(46, 206, "ANURAG VERMA", 78, "url(#nm)", 10, extra='textLength="500" lengthAdjust="spacingAndGlyphs"')
    b += B.text(48, 262, "Software Developer  |  AI / ML Enthusiast", 20, B.AMBER, "bold")
    b += B.text(48, 292, "Still thinking. Always building.", 15, B.MUTED)
    ch = [("#119", "HACKERRANK / 1,773", YEL), ("GOLD", "CODECHEF BADGE", B.AMBER), ("100%", "CLAIM PIPELINE", B.LIME)]
    for i, (v, l, c) in enumerate(ch):
        x = 48 + i * 128
        b += keycap(x, 326, 118, 58, c) + B.text(x + 59, 354, v, 22, c, "900", anchor="middle") + B.text(x + 59, 372, l, 8.5, B.MUTED, "bold", B.MONO, "middle")
    b += keycap(432, 326, 116, 58, B.AMBER, top="#3a1a10") + f'<circle class="pulse" cx="454" cy="355" r="6" fill="{B.AMBER}"/>' + B.text(468, 353, "OPEN TO", 12, B.AMBER, "900") + B.text(468, 369, "WORK", 12, B.AMBER, "900")
    b += B.text(48, 440, "THINK  >  BUILD  >  SHIP", 11.5, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    B.save("hero.svg", B.svg(W, H, b, defs, EXTRA))


# ------------------------------------------------------------------ section headers
def headers():
    items = [("about", "About the Trainer", "CHAPTER 01"), ("receipts", "Receipts, Not Claims", "CHAPTER 02"), ("projects", "Quest Log", "CHAPTER 03"),
             ("more", "Side Quests", "CHAPTER 04"), ("hackathons", "Gym Battles: Hackathons & Code", "CHAPTER 05"),
             ("analytics", "Trainer Analytics", "CHAPTER 06"), ("mission", "Current Mission", "CHAPTER 07"), ("connect", "Join My Team", "CHAPTER 08")]
    for n, t, l in items:
        W, H = 1000, 92
        d = B.grad("hl", "", "", False, [(0, B.LIME), (.55, B.AMBER), (1, "rgba(0,0,0,0)")])
        b = f'<ellipse cx="52" cy="76" rx="30" ry="7" fill="#000" opacity=".45"/>'
        b += iso_box(52, 66, 24, 13, 26, B.LIME, cls="fl") + iso_box(86, 70, 11, 6, 12, B.AMBER, cls="fl", style="animation-delay:.9s")
        b += B.text(116, 30, l, 11, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
        b += ext_text(116, 70, t, 34, B.BONE, 6, side="#c2481f", far="#3a1209", sw=5)
        b += f'<line x1="116" y1="84" x2="965" y2="84" stroke="url(#hl)" stroke-width="3" stroke-linecap="round" class="dash"/>'
        B.save(f"h_{n}.svg", B.svg(W, H, b, d, EXTRA))


# ------------------------------------------------------------------ about / tools / contact / footer / herd
def podium_small(cx, cy, w=130, d=36, h=18):
    return (f'<ellipse cx="{cx}" cy="{cy + d + 4}" rx="{w + 14}" ry="13" fill="#000" opacity=".4"/>' + iso_box(cx, cy, w, d, h, "#43200f", "#2b130a", "#1b0b06") +
            f'<polygon points="{cx},{cy - h - d} {cx + w},{cy - h} {cx},{cy - h + d} {cx - w},{cy - h}" fill="none" stroke="{B.LIME}" stroke-width="2" class="rim"/>')


def about():
    W, H = 1000, 460
    fd, fb = floor(372, H, 372, (186, 250), 8)
    d = F.sky(372, H, "ab", (.5, .95)) + fd + '<clipPath id="art"><rect x="1" y="1" width="370" height="458" rx="22"/></clipPath>'
    b = f'<g clip-path="url(#art)"><rect width="372" height="{H}" fill="url(#ab)"/><rect width="372" height="{H}" fill="url(#abg)"/>'
    b += B.stars(372, H, 14, 5, 170) + mountains(1000, 5, "#2a120d", 330, 90, 1, "par2") + volcano3d(190, 360, 260, 170) + fb
    b += podium_small(186, 420)
    g1, _ = place("boy", 50, 412, 330, delay=0); g2, _ = place("tricera", 176, 436, 128, delay=.4)
    b += F.embers(372, H, 10, 8, 440) + g1 + g2 + "</g>"
    b += B.text(404, 62, "// MY TRAINER HQ", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += ext_text(404, 112, "Think it — then ship it", 38, B.BONE, 6, side="#c2481f", far="#3a1209", sw=5)
    b += B.text(404, 142, "AI agent builder  ·  B.Tech CSE (AI) @ Parul University", 14, B.MUTED)
    feats = [("AGENTS THAT ACT", "Read pitch decks, verify claims, run voice interviews.", B.LIME),
             ("MULTI-AGENT TEAM", "Groq + Gemini orchestration, RAG that doesn't hallucinate.", B.AMBER),
             ("IDEA TO DEPLOYED", "From a messy 2 AM sketch to a demo-able product.", YEL)]
    for i, (t, dd, c) in enumerate(feats):
        y = 170 + i * 66
        b += keycap(404, y, 556, 54, c, 14, 6)
        b += iso_box(432, y + 38, 14, 8, 16, c) + B.text(466, y + 23, t, 12, c, "900", B.MONO, extra='letter-spacing="1.5"') + B.text(466, y + 41, dd, 13, B.BONE)
    b += keycap(404, 376, 556, 44, B.AMBER, 14, 6, top="#2e150c") + B.text(422, 405, chr(8220) + "If it can" + chr(8217) + "t be demoed, it isn" + chr(8217) + "t done." + chr(8221), 17, B.AMBER, "bold", extra='font-style="italic"')
    b += B.text(404, 448, "TOP 7% GLOBAL  ·  CODECHEF GOLD  ·  SIH 2026", 10.5, B.MUTED, "bold", B.MONO, extra='letter-spacing="1.5"')
    B.save("about.svg", B.frame(W, H, b, d, EXTRA))


def tools():
    W, H = 1000, 410
    fd, fb = floor(340, H, 330, (170, 240), 7)
    d = ('<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd27a" stop-opacity=".5"/><stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>'
         '<clipPath id="fc"><rect x="1" y="1" width="340" height="408" rx="22"/></clipPath>' + fd)
    b = '<g clip-path="url(#fc)">' + fb + "</g>"
    b += B.text(372, 56, "// CREATURE DEX", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += ext_text(372, 100, "Tools in my backpack", 36, B.BONE, 7, side="#c2481f", far="#3a1209", sw=5)
    b += B.stars(W, H, 8, 2, 60) + '<polygon class="glow" points="250,262 360,140 360,370" fill="url(#beam)"/>'
    b += podium_small(172, 360, 120, 32, 16)
    g, _ = place("tricera", 40, 348, 220, delay=.3)
    b += F.embers(340, H, 8, 4, 380) + g
    groups = [(B.AMBER, ["Groq", "Gemini", "RAG · FAISS", "ChromaDB", "Multi-Agent"]), (B.LIME, ["React", "Next.js", "Node.js", "Socket.io", "TypeScript"]),
              (YEL, ["MongoDB", "PostgreSQL", "SQLite", "Prisma", "SQL"]), (B.CORAL, ["Java", "C++", "Python", "Git", "FastAPI"])]
    for r, (c, items) in enumerate(groups):
        for i, it in enumerate(items):
            b += chip3d(372 + i * 120, 130 + r * 60, 112, 46, it, c, 13)
    b += B.text(372, 394, "AI · FULL STACK · DATA · CORE", 10.5, B.MUTED, "bold", B.MONO, extra='letter-spacing="2"')
    B.save("tools.svg", B.frame(W, H, b, d, EXTRA))


def herd():
    """Tech-stack conveyor: isometric cubes slide across a belt between the two characters."""
    W, H = 1000, 240
    fd, fb = floor(W, H, 128, (500, 70), 14)
    d, b0 = F.strip_bg(W, H, "hk", 6)
    b = b0 + fd + fb
    cubes = [("Groq", B.AMBER), ("Gemini", B.AMBER), ("React", B.LIME), ("Node.js", B.LIME), ("Python", B.CORAL), ("Next.js", B.LIME),
             ("FAISS", B.AMBER), ("MongoDB", YEL), ("Git", B.CORAL), ("FastAPI", B.CORAL)]
    gap, w_, d_, h_ = 112, 40, 22, 40
    period = gap * len(cubes)
    d += '<style>.belt{animation:belt 26s linear infinite}@keyframes belt{to{transform:translateX(-%dpx)}}</style>' % period
    belt_y = 190
    lane = f'<polygon points="262,{belt_y - 24} 738,{belt_y - 24} 770,{belt_y + 12} 230,{belt_y + 12}" fill="#1a0b07" stroke="{B.EDGE}" stroke-width="2"/>'
    lane += f'<line x1="246" y1="{belt_y - 6}" x2="754" y2="{belt_y - 6}" stroke="{B.AMBER}" stroke-width="2" stroke-dasharray="10 10" class="dash" opacity=".7"/>'
    row = ""
    for rep in range(3):
        for i, (name, col) in enumerate(cubes):
            cx = 240 + rep * period + i * gap
            row += f'<ellipse cx="{cx}" cy="{belt_y + 4}" rx="{w_ + 6}" ry="12" fill="#000" opacity=".4"/>'
            row += iso_box(cx, belt_y - 8, w_, d_, h_, col)
            ang = math.degrees(math.atan2(d_, w_))
            row += (f'<text transform="translate({cx - w_ + 4},{belt_y - 8 - h_ + 9}) skewY({ang:.1f})" x="0" y="{d_ * .55 + 4:.0f}" font-family="{B.DISPLAY}" '
                    f'font-size="9.5" font-weight="900" fill="#fff6e8" stroke="#1b0a05" stroke-width="2.2" paint-order="stroke">{B.esc(name)}</text>')
    mask = ('<linearGradient id="mk" x1="0" x2="1"><stop offset="0" stop-color="#000"/><stop offset=".12" stop-color="#fff"/><stop offset=".88" stop-color="#fff"/>'
            '<stop offset="1" stop-color="#000"/></linearGradient><mask id="mm"><rect x="230" y="0" width="540" height="240" fill="url(#mk)"/></mask>')
    b += mask + lane + '<g mask="url(#mm)"><g class="belt">' + row + '</g></g>'
    b += B.text(500, 40, "TECH STACK  \u00b7  ALWAYS IN MOTION", 11, B.AMBER, "bold", B.MONO, "middle", 'letter-spacing="3"')
    b += podium_small(120, 206, 105, 28, 14) + podium_small(880, 206, 105, 28, 14)
    gT, _ = place("tricera", 40, 196, 128, delay=0, flip=True)
    gB, _ = place("boy", 812, 192, 176, delay=0)
    b += gT + gB + "</g>" + f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="{B.EDGE}" stroke-width="2"/>'
    B.save("herd.svg", B.svg(W, H, b, d, EXTRA))


def contact():
    W, H = 1000, 300
    fd, fb = floor(380, H, 236, (190, 150), 7)
    d = fd + '<clipPath id="cc"><rect x="1" y="1" width="378" height="298" rx="22"/></clipPath>'
    b = '<g clip-path="url(#cc)">' + fb + "</g>" + B.stars(W, H, 12, 9, 70)
    b += podium_small(170, 262, 120, 32, 16)
    g, _ = place("boy", 56, 252, 224, delay=0); g2, _ = place("tricera", 190, 272, 100, delay=.5)
    b += F.embers(380, H, 8, 2, 290) + g + g2
    b += B.text(420, 62, "// JOIN MY TEAM", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += ext_text(420, 110, "Let's build something legendary", 32, B.BONE, 6, side="#c2481f", far="#3a1209", sw=5)
    items = [("PORTFOLIO", "anurag-six.vercel.app", B.LIME), ("LINKEDIN", "in/anurag-verma4", "#5aa9ff"), ("GITHUB", "@Anu7276", B.AMBER)]
    for i, (k, v, c) in enumerate(items):
        x = 420 + i * 190
        b += keycap(x, 136, 180, 70, c, 14, 7) + f'<rect x="{x + 16}" y="150" width="22" height="5" rx="2.5" fill="{c}"/>' + B.text(x + 16, 178, k, 11, c, "900", B.MONO, extra='letter-spacing="2"') + B.text(x + 16, 196, v, 13, B.BONE, "bold")
    b += f'<circle class="pulse" cx="426" cy="248" r="5" fill="{B.AMBER}"/>' + B.text(440, 253, "Open to the right opportunity · freelance, collabs & hackathon teams", 12.5, B.MUTED)
    B.save("contact.svg", B.frame(W, H, b, d, EXTRA))


def footer():
    W, H = 1000, 250
    fd, fb = floor(W, H, 150, (500, 90), 14)
    d, b = F.strip_bg(W, H, "ft", 13)
    b += fd + fb
    gT, _ = place("tricera", 50, H - 22, 120, delay=.2); gB, _ = place("boy", 830, H - 20, 200, delay=0); gT2, _ = place("tricera", 690, H - 22, 104, delay=.6, flip=True)
    b += gT + gB + gT2 + "</g>"
    b += ext_text(500, 96, "Code · Build · Learn · Evolve", 28, B.BONE, 6, "#c2481f", "#3a1209", "middle")
    b += B.text(500, 134, "Adventure awaits. Keep coding, keep growing.", 14.5, B.AMBER, "bold", anchor="middle")
    b += f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="{B.EDGE}" stroke-width="2"/>'
    B.save("footer.svg", B.svg(W, H, b, d, EXTRA))


def hero_stats():
    W, H = 1000, 124
    b = ""
    items = [("#119", "HACKERRANK / 1,773", YEL), ("GOLD", "CODECHEF BADGE", B.AMBER), ("100%", "CLAIM PIPELINE", B.LIME), ("TOP 7%", "GLOBAL, JUN 2026", B.CORAL)]
    for i, (v, l, c) in enumerate(items):
        x = 30 + i * 176
        b += keycap(x, 24, 164, 60, c, 14, 8) + B.text(x + 82, 54, v, 24, c, "900", anchor="middle") + B.text(x + 82, 72, l, 9, B.MUTED, "bold", B.MONO, "middle")
    b += keycap(740, 24, 230, 60, B.AMBER, 14, 8, top="#3a1a10") + f'<circle class="pulse" cx="766" cy="54" r="7" fill="{B.AMBER}"/>' + B.text(784, 52, "OPEN TO THE RIGHT", 12, B.AMBER, "900") + B.text(784, 70, "OPPORTUNITY", 12, B.AMBER, "900")
    B.save("hero_stats.svg", B.frame(W, H, b, extra_css=EXTRA))


# ------------------------------------------------------------------ ID card + stats
def stats():
    W, H = 1000, 500
    head = F.uri(F.cut("head"), maxh=260)
    d = ('<clipPath id="av"><circle cx="190" cy="176" r="62"/></clipPath><clipPath id="idc"><rect x="52" y="60" width="276" height="400" rx="20"/></clipPath>'
         + B.grad("lan", "", "", True, [(0, B.LAVA), (1, B.AMBER)]) + B.grad("av", "", "", True, [(0, "#5a1f10"), (1, "#1c0b07")]) +
         '<linearGradient id="shn" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".28"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    b = '<rect x="178" y="0" width="24" height="56" fill="url(#lan)"/><rect x="170" y="48" width="40" height="14" rx="5" fill="#cfd6d2"/>'
    b += f'<rect x="62" y="72" width="276" height="400" rx="20" fill="#0a0403"/><rect x="57" y="66" width="276" height="400" rx="20" fill="#3a1a10"/>'
    b += f'<rect x="52" y="60" width="276" height="400" rx="20" fill="#1c0f0b" stroke="{B.AMBER}" stroke-width="2.5"/>'
    b += f'<rect x="52" y="60" width="276" height="40" rx="20" fill="{B.AMBER}"/><rect x="52" y="80" width="276" height="20" fill="{B.AMBER}"/>'
    b += B.text(190, 86, "TRAINER LICENSE", 12, "#2a1a05", "900", B.MONO, "middle", 'letter-spacing="1.5"')
    b += f'<circle cx="190" cy="176" r="68" fill="#0a0403"/><circle cx="190" cy="176" r="64" fill="url(#av)" stroke="{B.LIME}" stroke-width="3"/>'
    b += f'<g clip-path="url(#av)"><image href="{head}" x="102" y="116" width="176" height="128" preserveAspectRatio="xMidYMax slice"/></g>'
    b += B.text(190, 276, "ANURAG VERMA", 23, B.BONE, "900", anchor="middle") + B.text(190, 298, "AI AGENT BUILDER", 12, B.LIME, "bold", B.MONO, "middle", 'letter-spacing="2"')
    for i, (k, v) in enumerate([("RANK", "Gym Challenger"), ("ID", "AV-7276"), ("BASE", "Parul University"), ("STATUS", "Open to work")]):
        y = 332 + i * 26
        b += B.text(78, y, k, 11, B.MUTED, "bold", B.MONO) + B.text(150, y, v, 13.5, B.BONE, "bold")
    b += "".join(f'<rect x="{82 + i * 6}" y="432" width="{[2, 4, 2, 5, 3, 2][i % 6]}" height="18" fill="{B.BONE}" opacity=".7"/>' for i in range(36))
    b += '<g clip-path="url(#idc)"><rect class="shine" x="0" y="60" width="90" height="400" fill="url(#shn)" transform="skewX(-18)"/></g>'
    # right side
    b += B.text(372, 74, "// TRAINER DASHBOARD", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += ext_text(372, 116, "Stats from the field", 34, B.BONE, 6, side="#c2481f", far="#3a1209", sw=5)
    b += keycap(836, 52, 124, 26, B.AMBER, 13, 4, top="#3a1a10") + f'<circle class="pulse" cx="852" cy="65" r="4.5" fill="{B.AMBER}"/>' + B.text(864, 69.5, "LIVE · NOV 2026", 9.5, B.AMBER, "bold", B.MONO)
    tiles = [("#119", "GLOBAL RANK / 1,773", YEL), ("TOP 7%", "HACKERRANK JUN 2026", B.AMBER), ("100%", "CLAIM ACCURACY", B.LIME), ("GOLD", "CODECHEF BADGE", B.CORAL)]
    for i, (v, l, c) in enumerate(tiles):
        x = 372 + i * 148
        b += keycap(x, 140, 140, 84, c, 16, 8) + f'<rect x="{x + 14}" y="152" width="26" height="5" rx="2.5" fill="{c}"/>' + B.text(x + 70, 192, v, 30, c, "900", anchor="middle") + B.text(x + 70, 212, l, 8.5, B.MUTED, "bold", B.MONO, "middle")
    # battle log
    b += keycap(372, 256, 300, 214, None, 16, 8, top="#251410") + B.text(390, 284, "BATTLE LOG · BEATS % OF FIELD", 10.5, B.AMBER, "bold", B.MONO)
    for i, (t, r, pct, c) in enumerate([("Orchestrate · Jun 2026", "#119 / 1,773", 93.3, B.LIME), ("Orchestrate · May 2026", "#306 / 1,349", 77.3, B.AMBER)]):
        y = 312 + i * 56
        b += B.text(390, y, t, 13, B.BONE, "bold") + B.text(654, y, r, 12, B.MUTED, "bold", B.MONO, "end")
        b += f'<rect x="390" y="{y + 10}" width="264" height="14" rx="7" fill="#0c0706"/><rect class="bar" x="390" y="{y + 10}" width="{264 * pct / 100:.0f}" height="14" rx="7" fill="{c}"/><rect x="392" y="{y + 12}" width="{264 * pct / 100 - 4:.0f}" height="3" rx="1.5" fill="#fff" opacity=".25"/>'
        b += B.text(654, y + 40, f"{pct:.0f}%", 11, c, "bold", B.MONO, "end")
    b += B.text(390, 436, "SIH 2026 Internal · Team MindMesh", 12.5, B.BONE, "bold") + B.text(390, 456, "Startup-AYUSH Portal · SIH1345", 11.5, B.MUTED)
    # quests
    b += keycap(684, 256, 276, 214, None, 16, 8, top="#251410") + B.text(702, 284, "NEXT QUESTS", 10.5, B.AMBER, "bold", B.MONO)
    for i, (t, dd) in enumerate([("CAMPAIGNIX", "to production"), ("VIVORA", "to production"), ("SDE Internship", "top-tier"), ("Open source", "contribute")]):
        y = 300 + i * 41
        b += f'<rect x="698" y="{y}" width="248" height="34" rx="10" fill="#0f0907"/>' + iso_box(718, y + 26, 9, 5, 11, B.AMBER) + B.text(738, y + 15, t, 12.5, B.BONE, "bold") + B.text(738, y + 28, dd, 9.5, B.MUTED, "normal", B.MONO)
        b += f'<rect x="874" y="{y + 9}" width="62" height="16" rx="8" fill="{B.LAVA}" opacity=".2"/>' + B.text(905, y + 20.5, "IN PROGRESS", 8, B.LAVA, "900", B.MONO, "middle")
    B.save("stats.svg", B.frame(W, H, b, d, EXTRA))


# ------------------------------------------------------------------ ARENA (isometric towers)
def arena():
    W, H = 1000, 440
    fd, fb = floor(W, H, 250, (500, 130), 14)
    d = F.sky(W, H, "ar", (.5, .6)) + fd
    b = f'<clipPath id="arc"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24"/></clipPath><g clip-path="url(#arc)"><rect width="{W}" height="{H}" fill="url(#ar)"/><rect width="{W}" height="{H}" fill="url(#arg)"/>'
    b += B.stars(W, H, 22, 12, 140) + mountains(1000, 14, "#2a120d", 260, 90, 1, "par2") + fb
    b += B.text(40, 56, "// GYM BATTLES", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += ext_text(40, 98, "The Arena", 36, B.BONE, 7, side="#c2481f", far="#3a1209", sw=5)
    towers = [(190, 93.3, B.LIME, "#119 / 1,773", "ORCHESTRATE · JUN 2026", "beats 93%"),
              (380, 77.3, B.AMBER, "#306 / 1,349", "ORCHESTRATE · MAY 2026", "beats 77%"),
              (570, 52, YEL, "GOLD", "CODECHEF", "badge"),
              (760, 40, B.CORAL, "SIH 2026", "TEAM MINDMESH", "internal round")]
    for cx, pct, c, big, lab, sub in towers:
        h = pct * 1.45
        b += f'<ellipse cx="{cx}" cy="{370 + 36}" rx="64" ry="20" fill="#000" opacity=".4"/>'
        b += iso_box(cx, 370, 56, 32, h, c, cls="rise3", style=f"animation-delay:{cx / 800:.2f}s")
        top_y = 370 - h - 32
        b += B.text(cx, top_y - 30, big, 22, c, "900", anchor="middle") + B.text(cx, top_y - 12, sub, 11, B.BONE, "bold", B.MONO, "middle")
        b += B.text(cx, 370 + 62, lab, 10, B.MUTED, "bold", B.MONO, "middle")
        b += f'<polygon points="{cx},{top_y} {cx + 56},{top_y + 32} {cx},{top_y + 64} {cx - 56},{top_y + 32}" fill="none" stroke="#fff" opacity=".25" stroke-width="1"/>'
    gB, _ = place("boy", 846, 392, 250, delay=0)
    b += F.embers(W, H, 16, 5, 420) + gB + "</g>"
    B.save("arena.svg", B.frame(W, H, b, d, EXTRA, bg="none"))


if __name__ == "__main__":
    B.main()
    hero(); headers(); hero_stats(); herd(); about(); tools(); stats(); contact(); footer(); arena()
    print("3D assets done")
