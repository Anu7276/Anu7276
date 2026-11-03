#!/usr/bin/env python3
"""Generates the Trainer SVG assets for the GitHub profile README.
Run:  python3 build_assets.py   (writes into ./assets)"""
import os, random, math

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
os.makedirs(OUT, exist_ok=True)

DISPLAY = "'Trebuchet MS','Comic Sans MS','Segoe UI',Verdana,sans-serif"
MONO = "'Courier New',Consolas,Menlo,monospace"

# palette
BG1, BG2 = "#120a08", "#3a1a10"
LIME, LIME2 = "#ff6a3d", "#e63b2e"
AMBER, LAVA = "#ffb347", "#ff3b30"
BONE, MUTED = "#fff1e0", "#c9aa9c"
PANEL, EDGE = "#251410", "#7a3320"
TEAL, CORAL = "#ffd54a", "#ff8f7a"

CSS = """
.bob{animation:bob 2.4s ease-in-out infinite}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}
.tail{animation:wag 1.8s ease-in-out infinite alternate}
@keyframes wag{from{transform:rotate(-5deg)}to{transform:rotate(7deg)}}
.wave{animation:wave .9s ease-in-out infinite alternate}
@keyframes wave{from{transform:rotate(-18deg)}to{transform:rotate(22deg)}}
.blink{transform-box:fill-box;transform-origin:center;animation:blink 4.5s infinite}
@keyframes blink{0%,94%,100%{transform:scaleY(1)}97%{transform:scaleY(.08)}}
.twinkle{animation:tw 3s ease-in-out infinite}
@keyframes tw{0%,100%{opacity:.25}50%{opacity:1}}
.rise{animation:rise 4s ease-in infinite}
@keyframes rise{0%{transform:translateY(0);opacity:0}15%{opacity:.9}100%{transform:translateY(-120px);opacity:0}}
.smoke{animation:smoke 6s ease-out infinite}
@keyframes smoke{0%{transform:translate(0,0) scale(.6);opacity:0}20%{opacity:.5}100%{transform:translate(20px,-90px) scale(1.8);opacity:0}}
.pulse{animation:pulse 1.6s ease-in-out infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.drift{animation:drift 30s linear infinite}
@keyframes drift{from{transform:translateX(-120px)}to{transform:translateX(1120px)}}
.dash{stroke-dasharray:8 8;animation:dash 1.2s linear infinite}
@keyframes dash{to{stroke-dashoffset:-16}}
.glow{animation:glow 2.5s ease-in-out infinite}
@keyframes glow{0%,100%{opacity:.55}50%{opacity:.95}}
.hop{animation:hop 1.4s ease-in-out infinite}
@keyframes hop{0%,100%{transform:translateY(0)}50%{transform:translateY(-9px)}}
.bar{transform-box:fill-box;transform-origin:left center;animation:grow 2s ease-out both}
@keyframes grow{from{transform:scaleX(0)}to{transform:scaleX(1)}}
"""


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def svg(w, h, body, defs="", extra_css=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">'
            f'<defs>{defs}<style>{CSS}{extra_css}</style></defs>{body}</svg>')


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", name, len(content) // 1024, "KB")


def text(x, y, s, size=16, fill=BONE, weight="normal", font=DISPLAY, anchor="start", extra=""):
    return (f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" fill="{fill}" '
            f'font-weight="{weight}" text-anchor="{anchor}" {extra}>{esc(s)}</text>')


def grad(id_, c1, c2, vertical=False, stops=None):
    d = 'x1="0" y1="0" x2="0" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    if stops:
        s = "".join(f'<stop offset="{o}" stop-color="{c}"/>' for o, c in stops)
    else:
        s = f'<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>'
    return f'<linearGradient id="{id_}" {d}>{s}</linearGradient>'


def footprint(x, y, s=1, fill=LIME, op=0.5, rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" opacity="{op}" fill="{fill}">'
            '<ellipse cx="0" cy="6" rx="7" ry="8"/><ellipse cx="-9" cy="-6" rx="3" ry="5" transform="rotate(-20 -9 -6)"/>'
            '<ellipse cx="0" cy="-9" rx="3" ry="5.5"/><ellipse cx="9" cy="-6" rx="3" ry="5" transform="rotate(20 9 -6)"/></g>')


# ------------------------------------------------------------------ characters
def trex(x, y, s=1.0, flip=False, c1=LIME2, c2="#3a8a3a", belly="#d3ee9a", spike=LAVA, delay=0):
    tf = f"translate({x + 250 * s},{y}) scale({-s},{s})" if flip else f"translate({x},{y}) scale({s})"
    d = f'style="animation-delay:{delay}s"'
    return f'''<g transform="{tf}"><g class="bob" {d}>
<g class="tail" style="transform-origin:150px 110px;animation-delay:{delay}s"><path d="M148,92 C190,88 228,104 252,152 C216,130 186,130 148,130 Z" fill="{c1}"/></g>
<rect x="126" y="118" width="28" height="52" rx="13" fill="{c2}"/><ellipse cx="136" cy="172" rx="23" ry="8" fill="{c2}"/>
<polygon points="98,62 108,38 120,58 132,34 144,58 158,40 164,70" fill="{spike}"/>
<ellipse cx="120" cy="100" rx="58" ry="46" fill="{c1}"/>
<path d="M68,108 Q108,152 168,120 Q152,142 116,148 Q80,144 68,108Z" fill="{belly}"/>
<circle cx="140" cy="86" r="6" fill="{c2}" opacity=".6"/><circle cx="156" cy="104" r="4" fill="{c2}" opacity=".6"/><circle cx="128" cy="72" r="4" fill="{c2}" opacity=".6"/>
<rect x="90" y="118" width="30" height="53" rx="14" fill="{c1}"/><ellipse cx="96" cy="173" rx="25" ry="9" fill="{c1}"/>
<ellipse cx="78" cy="175" rx="4" ry="5" fill="#fff"/><ellipse cx="90" cy="178" rx="4" ry="5" fill="#fff"/><ellipse cx="102" cy="178" rx="4" ry="5" fill="#fff"/>
<path d="M74,94 q-16,6 -10,20" stroke="{c2}" stroke-width="8" stroke-linecap="round" fill="none"/>
<rect x="8" y="28" width="98" height="46" rx="23" fill="{c1}"/>
<rect x="16" y="60" width="82" height="26" rx="13" fill="{c2}"/>
<path d="M24,66 Q56,76 94,66" stroke="#0f0907" stroke-width="2.5" fill="none" stroke-linecap="round"/>
<polygon points="28,64 33,74 38,64" fill="#fff"/><polygon points="44,66 49,76 54,66" fill="#fff"/><polygon points="62,67 67,76 72,67" fill="#fff"/><polygon points="80,66 85,75 90,65" fill="#fff"/>
<ellipse cx="20" cy="38" rx="3.5" ry="2.5" fill="#0f0907"/>
<circle cx="70" cy="40" r="9" fill="#fff"/><circle class="blink" cx="68" cy="41" r="4.6" fill="#0f0907"/><circle cx="66.5" cy="39" r="1.5" fill="#fff"/>
<path d="M58,28 L82,33" stroke="{c2}" stroke-width="5" stroke-linecap="round"/>
<circle cx="52" cy="54" r="5" fill="{LAVA}" opacity=".35"/>
</g></g>'''


def tricera(x, y, s=1.0, flip=False, c1="#ff9f5a", c2="#c75b2a", belly="#ffe0b5", delay=0):
    tf = f"translate({x + 230 * s},{y}) scale({-s},{s})" if flip else f"translate({x},{y}) scale({s})"
    dots = "".join(
        f'<circle cx="{62 + 41 * math.cos(math.radians(a)):.1f}" cy="{78 + 41 * math.sin(math.radians(a)):.1f}" r="4" fill="{BONE}"/>'
        for a in range(150, 391, 30))
    return f'''<g transform="{tf}"><g class="bob" style="animation-delay:{delay}s">
<path d="M196,98 C216,104 226,116 228,132 C214,120 204,118 190,120Z" fill="{c1}"/>
<rect x="148" y="108" width="24" height="46" rx="11" fill="{c2}"/><rect x="174" y="108" width="24" height="46" rx="11" fill="{c2}"/>
<ellipse cx="135" cy="100" rx="72" ry="46" fill="{c1}"/>
<path d="M80,112 Q130,160 196,112 Q170,140 135,144 Q100,142 80,112Z" fill="{belly}"/>
<rect x="68" y="108" width="26" height="48" rx="12" fill="{c1}"/><rect x="98" y="108" width="26" height="48" rx="12" fill="{c1}"/>
<ellipse cx="80" cy="156" rx="17" ry="6" fill="{c2}"/><ellipse cx="111" cy="156" rx="17" ry="6" fill="{c2}"/>
<circle cx="62" cy="78" r="49" fill="{c2}"/><circle cx="62" cy="78" r="38" fill="#e0763d"/>{dots}
<ellipse cx="45" cy="100" rx="36" ry="30" fill="{c1}"/>
<path d="M12,102 Q8,114 22,122 L40,116Z" fill="{BONE}"/>
<polygon points="26,88 12,66 38,82" fill="{BONE}"/>
<polygon points="50,80 40,36 64,74" fill="{BONE}"/><polygon points="70,80 74,36 86,78" fill="{BONE}"/>
<circle cx="54" cy="94" r="7" fill="#fff"/><circle class="blink" cx="52.5" cy="95" r="3.6" fill="#0f0907"/><circle cx="51" cy="93.5" r="1.2" fill="#fff"/>
<path d="M30,114 Q44,122 60,114" stroke="#0f0907" stroke-width="2.5" fill="none" stroke-linecap="round"/>
</g></g>'''


def raptor(x, y, s=1.0, flip=False, c1="#4fb8c9", c2="#2a7f93", belly="#d6f3f7", stripe=AMBER, delay=0):
    tf = f"translate({x + 210 * s},{y}) scale({-s},{s})" if flip else f"translate({x},{y}) scale({s})"
    return f'''<g transform="{tf}"><g class="bob" style="animation-delay:{delay}s">
<g class="tail" style="transform-origin:120px 80px;animation-delay:{delay}s"><path d="M112,60 C152,58 188,70 208,102 C178,86 150,90 114,94 Z" fill="{c1}"/><path d="M150,66 l6,18 M170,72 l6,16" stroke="{stripe}" stroke-width="4" stroke-linecap="round"/></g>
<path d="M118,100 L130,126 L140,138" stroke="{c2}" stroke-width="10" stroke-linecap="round" fill="none"/><ellipse cx="136" cy="144" rx="15" ry="5" fill="{c2}"/>
<ellipse cx="102" cy="76" rx="44" ry="27" fill="{c1}"/>
<ellipse cx="96" cy="90" rx="31" ry="13" fill="{belly}"/>
<path d="M88,64 l8,18 M104,60 l8,18 M120,62 l7,17" stroke="{stripe}" stroke-width="4.5" stroke-linecap="round"/>
<ellipse cx="64" cy="50" rx="14" ry="28" transform="rotate(-22 64 50)" fill="{c1}"/>
<path d="M96,104 L86,126 L78,142" stroke="{c1}" stroke-width="11" stroke-linecap="round" fill="none"/><ellipse cx="102" cy="92" rx="17" ry="22" fill="{c1}"/>
<ellipse cx="74" cy="146" rx="16" ry="5.5" fill="{c1}"/><path d="M60,144 q-10,2 -12,10" stroke="#fff" stroke-width="3.5" stroke-linecap="round" fill="none"/>
<path d="M70,80 q-14,4 -12,16" stroke="{c2}" stroke-width="5" stroke-linecap="round" fill="none"/>
<ellipse cx="42" cy="28" rx="27" ry="14" fill="{c1}"/><ellipse cx="38" cy="38" rx="22" ry="7" fill="{c2}"/>
<polygon points="22,35 26,42 30,35" fill="#fff"/><polygon points="34,36 38,43 42,36" fill="#fff"/><polygon points="46,36 50,42 54,35" fill="#fff"/>
<path d="M52,16 l6,-9 l4,12 l8,-8 l-2,13" fill="{stripe}"/>
<circle cx="50" cy="24" r="6" fill="#ffe14d"/><ellipse class="blink" cx="49" cy="24" rx="1.8" ry="4.2" fill="#0f0907"/>
<circle cx="19" cy="26" r="1.8" fill="#0f0907"/>
</g></g>'''


def boy(x, y, s=1.0, wave=True, delay=0, hair="#2b1b12", shirt=AMBER, cap="#e63946", pack=LIME2):
    """Cartoon boy explorer. Local box ~ 90x165, ground at y=162."""
    arm = (f'<g class="wave" style="transform-origin:64px 82px;animation-delay:{delay}s">'
           f'<rect x="60" y="40" width="11" height="44" rx="5.5" fill="#f2c28f" transform="rotate(8 64 82)"/>'
           f'<circle cx="68" cy="40" r="7" fill="#f2c28f"/></g>') if wave else (
        '<rect x="62" y="80" width="11" height="40" rx="5.5" fill="#f2c28f" transform="rotate(-8 64 82)"/>')
    return f'''<g transform="translate({x},{y}) scale({s})"><g class="bob" style="animation-delay:{delay}s">
<rect x="6" y="70" width="26" height="46" rx="10" fill="{pack}"/>
<rect x="28" y="140" width="13" height="18" rx="5" fill="#f2c28f"/><rect x="47" y="140" width="13" height="18" rx="5" fill="#f2c28f"/>
<ellipse cx="33" cy="160" rx="12" ry="5.5" fill="#5a3a22"/><ellipse cx="54" cy="160" rx="12" ry="5.5" fill="#5a3a22"/>
<rect x="24" y="118" width="40" height="28" rx="8" fill="#c9a26b"/>
<rect x="22" y="70" width="44" height="56" rx="14" fill="{shirt}"/>
<rect x="22" y="104" width="44" height="6" fill="#d98a1e"/>
<rect x="20" y="82" width="11" height="40" rx="5.5" fill="#f2c28f" transform="rotate(10 25 84)"/>
{arm}
<circle cx="44" cy="46" r="25" fill="#f2c28f"/>
<path d="M20,46 Q22,24 44,22 Q66,24 68,46 Q60,34 44,34 Q28,34 20,46Z" fill="{hair}"/>
<path d="M22,32 Q24,2 44,2 Q64,2 66,32Z" fill="{cap}" stroke="#1b1209" stroke-width="2.5" stroke-linejoin="round"/>
<path d="M18,34 Q44,26 72,34 Q66,42 44,38 Q24,42 18,34Z" fill="{cap}" stroke="#1b1209" stroke-width="2.5" stroke-linejoin="round"/>
<polygon points="44,10 49,18 44,26 39,18" fill="#ffd54a" stroke="#1b1209" stroke-width="1.5"/>
<circle cx="35" cy="48" r="3.4" fill="#2b1b12"/><circle cx="53" cy="48" r="3.4" fill="#2b1b12"/>
<circle cx="36" cy="47" r="1.1" fill="#fff"/><circle cx="54" cy="47" r="1.1" fill="#fff"/>
<circle cx="29" cy="55" r="4" fill="#ff9a8a" opacity=".55"/><circle cx="59" cy="55" r="4" fill="#ff9a8a" opacity=".55"/>
<path d="M36,58 Q44,66 52,58" stroke="#7a3b22" stroke-width="2.6" fill="none" stroke-linecap="round"/>
</g></g>'''


def egg_baby(x, y, s=1.0, delay=0):
    return f'''<g transform="translate({x},{y}) scale({s})"><g class="hop" style="animation-delay:{delay}s">
<circle cx="40" cy="48" r="21" fill="{LIME2}"/><circle class="blink" cx="33" cy="46" r="3.4" fill="#0f0907"/><circle class="blink" cx="47" cy="46" r="3.4" fill="#0f0907"/>
<path d="M33,56 Q40,62 47,56" stroke="#0f0907" stroke-width="2.2" fill="none" stroke-linecap="round"/>
<polygon points="32,28 36,18 40,28 44,18 48,28" fill="{LAVA}"/>
<path d="M8,64 L18,52 L26,64 L36,50 L46,64 L56,52 L64,64 L72,56 L72,70 C72,96 58,108 40,108 C22,108 8,96 8,70Z" fill="{BONE}"/>
<circle cx="26" cy="84" r="4" fill="#d8c9a3"/><circle cx="52" cy="92" r="5" fill="#d8c9a3"/><circle cx="44" cy="76" r="3" fill="#d8c9a3"/></g></g>'''


# ------------------------------------------------------------------ scenery
def stars(w, h, n=26, seed=3, maxy=None):
    r = random.Random(seed)
    out = ""
    for i in range(n):
        out += (f'<circle class="twinkle" cx="{r.randint(10, w - 10)}" cy="{r.randint(8, maxy or h // 2)}" '
                f'r="{r.choice([1, 1.4, 1.8])}" fill="{BONE}" style="animation-delay:{r.random() * 3:.1f}s"/>')
    return out


def fern(x, y, s=1.0, flip=False):
    sx = -s if flip else s
    leaves = ""
    for i in range(7):
        a = -80 + i * 26
        leaves += f'<path d="M0,0 Q{40},{-18} {92},{-4}" fill="none" stroke="#8a3b1c" stroke-width="9" stroke-linecap="round" transform="rotate({a})"/>'
    return f'<g transform="translate({x},{y}) scale({sx},{s})" opacity=".95">{leaves}</g>'


def volcano(x, y, s=1.0):
    smoke = "".join(
        f'<circle class="smoke" cx="{x + 100 * s}" cy="{y - 10 * s}" r="{14 * s}" fill="#5b6b62" style="animation-delay:{i * 2}s"/>'
        for i in range(3))
    embers = "".join(
        f'<circle class="rise" cx="{x + (96 + i * 6) * s}" cy="{y + 6 * s}" r="2.6" fill="{AMBER}" style="animation-delay:{i * .7:.1f}s"/>'
        for i in range(6))
    return f'''{smoke}
<polygon points="{x},{y + 190 * s} {x + 76 * s},{y} {x + 124 * s},{y} {x + 200 * s},{y + 190 * s}" fill="#2e1a13"/>
<polygon points="{x + 76 * s},{y} {x + 124 * s},{y} {x + 200 * s},{y + 190 * s} {x + 130 * s},{y + 190 * s}" fill="#231510"/>
<ellipse class="glow" cx="{x + 100 * s}" cy="{y + 2 * s}" rx="{30 * s}" ry="{8 * s}" fill="{LAVA}"/>
<path class="glow" d="M{x + 82 * s},{y + 4 * s} q-6,{40 * s} 4,{70 * s} q4,-30 10,-70Z M{x + 112 * s},{y + 4 * s} q8,{50 * s} 0,{90 * s} q10,-40 6,-90Z" fill="{LAVA}"/>
{embers}'''


def ground(w, h, top, id_="gr"):
    return (f'<path d="M0,{top} Q{w * .2},{top - 22} {w * .42},{top - 6} T{w * .8},{top - 12} T{w},{top - 4} L{w},{h} L0,{h}Z" fill="#1a0f0b"/>'
            f'<path d="M0,{top + 14} Q{w * .3},{top - 2} {w * .6},{top + 10} T{w},{top + 6} L{w},{h} L0,{h}Z" fill="#140b08"/>')


def frame(w, h, body, defs="", extra_css="", bg="url(#cardbg)", stroke="url(#edge)"):
    d = (grad("cardbg", "", "", True, [(0, "#160d0a"), (1, "#1f120d")]) +
         grad("edge", "", "", False, [(0, EDGE), (.5, AMBER), (1, EDGE)]) + defs)
    b = (f'<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="22" fill="{bg}" stroke="{stroke}" stroke-width="2"/>' + body)
    return svg(w, h, b, d, extra_css)


def chip(x, y, w, h, label, dot, size=13):
    return (f'<g transform="translate({x},{y})"><rect width="{w}" height="{h}" rx="12" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>'
            f'<circle cx="16" cy="{h / 2}" r="5" fill="{dot}"/>'
            f'{text(30, h / 2 + 4.5, label, size, BONE, "bold")}</g>')



# ------------------------------------------------------------------ chibi pack (original designs)
OL = 'stroke="#1b1209" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"'


def _eyes(cx1, cx2, cy, r=11):
    out = ""
    for cx in (cx1, cx2):
        out += (f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 1.2:.1f}" fill="#fff" {OL}/>'
                f'<ellipse class="blink" cx="{cx}" cy="{cy + 1}" rx="{r * .6:.1f}" ry="{r * .8:.1f}" fill="#12202a"/>'
                f'<circle cx="{cx - 2}" cy="{cy - 3}" r="2.6" fill="#fff"/>')
    return out


def chibi_tricera(x, y, s=1.0, flip=False, body="#4aa3df", frill="#8b5cf6", frill2="#c9a8ff", delay=0):
    tf = f"translate({x + 250 * s},{y}) scale({-s},{s})" if flip else f"translate({x},{y}) scale({s})"
    dots = "".join(f'<circle cx="{88 + 46 * math.cos(math.radians(a)):.1f}" cy="{80 + 46 * math.sin(math.radians(a)):.1f}" r="4.5" fill="#fff6c9"/>'
                   for a in range(160, 381, 36))
    return f'''<g transform="{tf}"><g class="bob" style="animation-delay:{delay}s">
<path d="M214,112 C238,112 248,128 246,146 C232,136 222,134 206,138Z" fill="{body}" {OL}/>
<rect x="176" y="118" width="30" height="44" rx="14" fill="#3586bd" {OL}/>
<rect x="150" y="122" width="30" height="42" rx="14" fill="#3586bd" {OL}/>
<ellipse cx="150" cy="108" rx="82" ry="50" fill="{body}" {OL}/>
<ellipse cx="136" cy="140" rx="46" ry="14" fill="#e8f6ff"/>
<rect x="96" y="122" width="32" height="44" rx="15" fill="{body}" {OL}/>
<rect x="64" y="124" width="32" height="42" rx="15" fill="{body}" {OL}/>
<path d="M68,160 l0,6 M80,160 l0,6 M100,160 l0,6 M112,160 l0,6" stroke="#fff6c9" stroke-width="5" stroke-linecap="round"/>
<circle cx="88" cy="80" r="64" fill="{frill}" {OL}/><circle cx="88" cy="80" r="52" fill="{frill2}"/>{dots}
<ellipse cx="70" cy="112" rx="50" ry="42" fill="{body}" {OL}/>
<path d="M50,78 Q40,46 60,34 Q64,56 72,78Z" fill="#ffd54a" {OL}/>
<path d="M92,78 Q96,46 118,40 Q108,62 104,80Z" fill="#ffd54a" {OL}/>
<path d="M30,108 Q18,112 22,124 Q34,126 42,118Z" fill="#fff6c9" {OL}/>
{_eyes(56, 88, 104)}
<circle cx="38" cy="124" r="6" fill="#ff8fa3" opacity=".6"/><circle cx="104" cy="124" r="6" fill="#ff8fa3" opacity=".6"/>
<path d="M56,128 Q72,138 90,128" stroke="#1b1209" stroke-width="3" fill="none" stroke-linecap="round"/>
</g></g>'''


def chibi_parasaur(x, y, s=1.0, flip=False, body="#ff8fa3", crest="#ffd54a", delay=0):
    tf = f"translate({x + 190 * s},{y}) scale({-s},{s})" if flip else f"translate({x},{y}) scale({s})"
    return f'''<g transform="{tf}"><g class="bob" style="animation-delay:{delay}s">
<g class="tail" style="transform-origin:120px 190px;animation-delay:{delay}s"><path d="M118,176 C150,176 182,196 190,214 C160,208 140,208 112,206Z" fill="{body}" {OL}/></g>
<rect x="64" y="190" width="30" height="40" rx="14" fill="#e8708a" {OL}/><rect x="100" y="190" width="30" height="40" rx="14" fill="#e8708a" {OL}/>
<ellipse cx="78" cy="232" rx="20" ry="8" fill="#e8708a" {OL}/><ellipse cx="116" cy="232" rx="20" ry="8" fill="#e8708a" {OL}/>
<ellipse cx="96" cy="160" rx="52" ry="58" fill="{body}" {OL}/>
<ellipse cx="88" cy="176" rx="32" ry="40" fill="#fff0e6"/>
<path d="M54,150 q-14,6 -10,20" stroke="#1b1209" stroke-width="10" stroke-linecap="round" fill="none"/><path d="M54,150 q-14,6 -10,20" stroke="{body}" stroke-width="5" stroke-linecap="round" fill="none"/>
<path d="M70,112 C62,86 66,66 74,52" stroke="#1b1209" stroke-width="30" stroke-linecap="round" fill="none"/><path d="M70,112 C62,86 66,66 74,52" stroke="{body}" stroke-width="24" stroke-linecap="round" fill="none"/>
<path d="M70,24 C92,-8 128,0 150,30" stroke="#1b1209" stroke-width="22" stroke-linecap="round" fill="none"/><path d="M70,24 C92,-8 128,0 150,30" stroke="{crest}" stroke-width="15" stroke-linecap="round" fill="none"/>
<ellipse cx="66" cy="50" rx="36" ry="28" fill="{body}" {OL}/>
<path d="M36,54 Q18,52 20,62 Q24,72 42,70Z" fill="#ffb3c0" {OL}/>
{_eyes(58, 80, 44, 9)}
<path d="M44,66 Q56,72 68,66" stroke="#1b1209" stroke-width="2.6" fill="none" stroke-linecap="round"/>
</g></g>'''


def chibi_carno(x, y, s=1.0, flip=False, body="#ff6b5a", belly="#ffe9c9", delay=0):
    tf = f"translate({x + 210 * s},{y}) scale({-s},{s})" if flip else f"translate({x},{y}) scale({s})"
    return f'''<g transform="{tf}"><g class="bob" style="animation-delay:{delay}s">
<g class="tail" style="transform-origin:130px 170px;animation-delay:{delay}s"><path d="M128,156 C160,156 196,170 208,196 C176,190 150,192 120,190Z" fill="{body}" {OL}/><path d="M160,166 l6,16 M180,174 l5,14" stroke="#1b1209" stroke-width="4" stroke-linecap="round"/></g>
<rect x="60" y="184" width="30" height="42" rx="14" fill="#d9503f" {OL}/><rect x="98" y="184" width="30" height="42" rx="14" fill="#d9503f" {OL}/>
<path d="M54,228 l-8,4 M64,230 l-4,6 M104,230 l-4,6 M116,230 l8,4" stroke="#1b1209" stroke-width="4" stroke-linecap="round"/>
<ellipse cx="92" cy="156" rx="50" ry="56" fill="{body}" {OL}/>
<ellipse cx="82" cy="172" rx="30" ry="38" fill="{belly}"/>
<path d="M104,128 l12,10 M110,150 l12,8 M106,172 l12,6" stroke="#1b1209" stroke-width="4" stroke-linecap="round"/>
<path d="M52,150 q-14,4 -10,18" stroke="#1b1209" stroke-width="10" stroke-linecap="round" fill="none"/><path d="M52,150 q-14,4 -10,18" stroke="{body}" stroke-width="5" stroke-linecap="round" fill="none"/>
<rect x="18" y="66" width="100" height="70" rx="34" fill="{body}" {OL}/>
<rect x="18" y="106" width="64" height="30" rx="15" fill="#d9503f" {OL}/>
<path d="M28,112 Q50,124 78,112" stroke="#1b1209" stroke-width="2.6" fill="none" stroke-linecap="round"/>
<polygon points="32,112 36,120 40,112" fill="#fff"/><polygon points="52,116 56,124 60,116" fill="#fff"/>
<path d="M44,70 Q36,44 54,38 Q56,56 60,72Z" fill="#ffd54a" {OL}/>
<path d="M84,68 Q88,42 106,40 Q100,58 98,74Z" fill="#ffd54a" {OL}/>
{_eyes(56, 86, 92, 9.5)}
<ellipse cx="22" cy="94" rx="3.5" ry="2.5" fill="#1b1209"/>
</g></g>'''


# ------------------------------------------------------------------ 1. HERO
def hero():
    W, H = 1000, 420
    defs = (grad("sky", "", "", True, [(0, "#07130f"), (.6, "#143524"), (1, "#2a4a2b")]) +
            grad("name", "", "", False, [(0, "#c7f56b"), (.55, LIME), (1, AMBER)]) +
            '<radialGradient id="sun" cx="0.5" cy="0.5" r="0.5"><stop offset="0" stop-color="#ff8a3d" stop-opacity=".55"/><stop offset="1" stop-color="#ff8a3d" stop-opacity="0"/></radialGradient>')
    b = f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="26" fill="url(#sky)" stroke="url(#sk2)" stroke-width="2"/>'
    defs += grad("sk2", "", "", False, [(0, EDGE), (.5, AMBER), (1, EDGE)])
    b += stars(W, H, 34, 7, 200)
    b += '<circle cx="790" cy="190" r="230" fill="url(#sun)"/>'
    b += '<circle cx="880" cy="70" r="26" fill="#ffe9b0" opacity=".9"/><circle cx="890" cy="64" r="22" fill="#143524" opacity=".35"/>'
    b += volcano(690, 120, 1.1)
    b += ground(W, H, 360)
    b += fern(20, 395, 1.1) + fern(960, 400, 1.0, True) + fern(140, 410, .8)
    b += chibi_tricera(548, 262, .5, delay=.2) + chibi_carno(850, 240, .5, delay=.6) + boy(700, 150, 1.5, delay=0)
    b += footprint(520, 395, 1.2, LIME, .35, 80) + footprint(470, 385, 1.2, LIME, .25, 80) + footprint(420, 396, 1.2, LIME, .18, 80)
    # text
    b += text(50, 62, "anurag@trainer-hq:~$ adventure --start", 14, LIME, "bold", MONO)
    b += '<rect x="372" y="50" width="9" height="15" fill="%s" class="pulse"/>' % LIME
    b += text(50, 122, "Hi, I'm", 30, BONE, "bold")
    b += (f'<text x="50" y="200" font-family="{DISPLAY}" font-size="78" font-weight="900" fill="url(#name)" stroke="#0a0504" '
          f'stroke-width="7" paint-order="stroke" stroke-linejoin="round" textLength="500" lengthAdjust="spacingAndGlyphs">ANURAG VERMA</text>')
    b += text(50, 240, "Software Developer  |  AI / ML Enthusiast", 20, AMBER, "bold")
    b += text(50, 268, "Still thinking. Always building. Trainer of the agent squad.", 14.5, MUTED)
    chips = [("#119", "HACKERRANK / 1,773", LIME), ("GOLD", "CODECHEF BADGE", AMBER), ("100%", "CLAIM PIPELINE", TEAL)]
    for i, (v, l, c) in enumerate(chips):
        cx = 50 + i * 128
        b += (f'<g transform="translate({cx},296)"><rect width="118" height="58" rx="13" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>'
              f'{text(59, 28, v, 22, c, "900", anchor="middle")}{text(59, 46, l, 8.5, MUTED, "bold", MONO, "middle")}</g>')
    b += (f'<g transform="translate(434,296)"><rect width="116" height="58" rx="13" fill="#3a1a10" stroke="{LIME}" stroke-width="1.5"/>'
          f'<circle class="pulse" cx="22" cy="29" r="6" fill="{LIME}"/>{text(36, 27, "OPEN TO", 12, LIME, "900")}{text(36, 43, "WORK", 12, LIME, "900")}</g>')
    b += text(50, 388, "THINK  >  BUILD  >  SHIP", 11.5, AMBER, "bold", MONO, extra='letter-spacing="3"')
    save("hero.svg", svg(W, H, b, defs))


# ------------------------------------------------------------------ 2. HERD
def herd():
    W, H = 1000, 190
    b = f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="#140b08" stroke="{EDGE}" stroke-width="2"/>'
    b += stars(W, H, 18, 11, 70)
    b += '<g class="drift"><ellipse cx="0" cy="40" rx="46" ry="12" fill="#3a1c14"/><ellipse cx="22" cy="32" rx="26" ry="12" fill="#3a1c14"/></g>'
    b += f'<line x1="20" y1="168" x2="{W - 20}" y2="168" stroke="{EDGE}" stroke-width="3" class="dash"/>'
    b += boy(90, 18, .86, hair="#2b1b12", shirt=AMBER, cap="#e63946", delay=0) + chibi_parasaur(200, 36, .5, delay=.3)
    b += boy(400, 18, .86, hair="#6b3f1d", shirt="#4aa3df", cap="#2f6fd6", pack=AMBER, delay=.4) + chibi_tricera(505, 76, .4, delay=.6)
    b += boy(700, 18, .86, hair="#1c1c1c", shirt=LIME2, cap="#7a3fd1", pack=CORAL, delay=.8) + chibi_carno(805, 40, .5, delay=1)
    for i in range(8):
        b += footprint(40 + i * 120, 180, .5, LIME, .18, 90)
    save("herd.svg", svg(W, H, b))


# ------------------------------------------------------------------ 3. ABOUT / MISSION
def about():
    W, H = 1000, 460
    defs = ('<clipPath id="art"><rect x="1" y="1" width="370" height="458" rx="22"/></clipPath>' +
            grad("art", "", "", True, [(0, "#10301f"), (1, "#1d4a2c")]))
    b = '<g clip-path="url(#art)"><rect width="372" height="460" fill="url(#art)"/>'
    b += stars(372, 440, 14, 5, 160) + '<circle cx="310" cy="70" r="30" fill="#ffe9b0" opacity=".85"/>'
    b += volcano(150, 160, .75)
    b += ground(372, 460, 400) + fern(14, 460, 1.0) + fern(358, 460, .9, True)
    b += boy(60, 225, 1.45) + chibi_tricera(190, 318, .56, delay=.4)
    b += '</g>'
    b += text(404, 62, "// MY TRAINER HQ", 12, AMBER, "bold", MONO, extra='letter-spacing="3"')
    b += text(404, 112, "Think it — then ship it", 38, BONE, "900")
    b += text(404, 140, "AI agent builder  ·  B.Tech CSE (AI) @ Parul University", 14, MUTED)
    feats = [("AGENTS THAT ACT", "Read pitch decks, verify claims, run voice interviews.", LIME),
             ("MULTI-AGENT TEAM", "Groq + Gemini orchestration, RAG that doesn't hallucinate.", AMBER),
             ("IDEA TO DEPLOYED", "From a messy 2 AM sketch to a demo-able product.", TEAL)]
    for i, (t, d, c) in enumerate(feats):
        y = 168 + i * 66
        b += (f'<g transform="translate(404,{y})"><rect width="556" height="56" rx="14" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>'
              f'<rect x="10" y="10" width="36" height="36" rx="10" fill="{c}" opacity=".18"/>'
              f'<g transform="translate(28,28)"><path d="M-9,-3 L0,-12 L9,-3 M0,-12 L0,10" stroke="{c}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
              f'{text(60, 24, t, 12, c, "900", MONO, extra="letter-spacing=\"1.5\"")}{text(60, 43, d, 13, BONE)}</g>')
    b += (f'<g transform="translate(404,372)"><rect width="556" height="46" rx="14" fill="#2a1d0e" stroke="{AMBER}" stroke-width="1.5"/>'
          f'{text(18, 29, chr(8220) + "If it can" + chr(8217) + "t be demoed, it isn" + chr(8217) + "t done." + chr(8221), 17, AMBER, "bold", extra="font-style=\"italic\"")}</g>')
    b += text(404, 442, "TOP 7% GLOBAL  ·  CODECHEF GOLD  ·  SIH 2026", 10.5, MUTED, "bold", MONO, extra='letter-spacing="1.5"')
    save("about.svg", frame(W, H, b, defs))


# ------------------------------------------------------------------ 4. TOOLS
def tools():
    W, H = 1000, 400
    defs = ('<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd27a" stop-opacity=".55"/>'
            '<stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>')
    b = text(372, 56, "// CREATURE DEX", 12, AMBER, "bold", MONO, extra='letter-spacing="3"')
    b += text(372, 98, "Tools in my backpack", 36, BONE, "900")
    b += stars(W, H, 10, 2, 60)
    b += '<polygon class="glow" points="150,236 360,120 360,360" fill="url(#beam)"/>'
    b += ground(W, H, 372)
    b += chibi_tricera(30, 196, 1.0, delay=.3) + fern(20, 400, .9)
    groups = [("AI", AMBER, ["Groq", "Gemini", "RAG · FAISS", "ChromaDB", "Multi-Agent"]),
              ("FULL STACK", LIME, ["React", "Next.js", "Node.js", "Socket.io", "TypeScript"]),
              ("DATA", TEAL, ["MongoDB", "PostgreSQL", "SQLite", "Prisma", "SQL"]),
              ("CORE", CORAL, ["Java", "C++", "Python", "Git", "FastAPI"])]
    for r, (g, c, items) in enumerate(groups):
        y = 128 + r * 58
        for i, it in enumerate(items):
            b += chip(372 + i * 120, y, 112, 46, it, c, 13)
    b += text(372, 372, "AI · FULL STACK · DATA · CORE", 10.5, MUTED, "bold", MONO, extra='letter-spacing="2"')
    for i, (g, c, _) in enumerate(groups):
        pass
    save("tools.svg", frame(W, H, b, defs))


# ------------------------------------------------------------------ 5. ID + STATS
def stats():
    W, H = 1000, 480
    defs = ('<clipPath id="av"><circle cx="190" cy="172" r="62"/></clipPath>' +
            grad("av", "", "", True, [(0, "#1c4a30"), (1, "#0f2a1c")]) + grad("lan", "", "", True, [(0, LAVA), (1, AMBER)]))
    b = f'<rect x="178" y="0" width="24" height="52" fill="url(#lan)"/><rect x="170" y="44" width="40" height="14" rx="5" fill="#cfd6d2"/>'
    b += f'<rect x="52" y="56" width="276" height="400" rx="20" fill="#1c0f0b" stroke="{AMBER}" stroke-width="2.5"/>'
    b += f'<rect x="52" y="56" width="276" height="40" rx="20" fill="{AMBER}"/><rect x="52" y="76" width="276" height="20" fill="{AMBER}"/>'
    b += text(190, 82, "TRAINER LICENSE", 12, "#2a1a05", "900", MONO, "middle", 'letter-spacing="1.5"')
    b += '<circle cx="190" cy="172" r="66" fill="#0f0907" stroke="%s" stroke-width="3"/><circle cx="190" cy="172" r="62" fill="url(#av)"/>' % LIME
    b += '<g clip-path="url(#av)">' + boy(110, 100, 1.9, wave=False).replace('class="bob"', '') + '</g>'
    b += text(190, 272, "ANURAG VERMA", 23, BONE, "900", anchor="middle")
    b += text(190, 294, "AI AGENT BUILDER", 12, LIME, "bold", MONO, "middle", 'letter-spacing="2"')
    rows = [("RANK", "Gym Challenger"), ("ID", "AV-7276"), ("BASE", "Parul University"), ("STATUS", "Open to work")]
    for i, (k, v) in enumerate(rows):
        y = 328 + i * 26
        b += text(78, y, k, 11, MUTED, "bold", MONO) + text(150, y, v, 13.5, BONE, "bold")
    bars = "".join(f'<rect x="{82 + i * 6}" y="428" width="{[2, 4, 2, 5, 3, 2][i % 6]}" height="18" fill="{BONE}" opacity=".7"/>' for i in range(36))
    b += bars
    # right side
    b += text(372, 70, "// TRAINER DASHBOARD", 12, AMBER, "bold", MONO, extra='letter-spacing="3"')
    b += text(372, 108, "Stats from the field", 34, BONE, "900")
    b += f'<g transform="translate(836,52)"><rect width="124" height="26" rx="13" fill="#3a1a10" stroke="{LIME}"/><circle class="pulse" cx="16" cy="13" r="4.5" fill="{LIME}"/>{text(28, 17.5, "LIVE · NOV 2026", 9.5, LIME, "bold", MONO)}</g>'
    tiles = [("#119", "GLOBAL RANK / 1,773", LIME), ("TOP 7%", "HACKERRANK JUN 2026", AMBER),
             ("100%", "CLAIM ACCURACY", TEAL), ("GOLD", "CODECHEF BADGE", CORAL)]
    for i, (v, l, c) in enumerate(tiles):
        x = 372 + i * 148
        b += (f'<g transform="translate({x},132)"><rect width="140" height="88" rx="16" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>'
              f'<rect x="14" y="14" width="26" height="5" rx="2.5" fill="{c}"/>'
              f'{text(70, 56, v, 30, c, "900", anchor="middle")}{text(70, 76, l, 8.5, MUTED, "bold", MONO, "middle")}</g>')
    # expedition log
    b += f'<g transform="translate(372,238)"><rect width="300" height="216" rx="16" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>'
    b += text(18, 28, "BATTLE LOG · BEATS % OF FIELD", 10.5, AMBER, "bold", MONO)
    logs = [("Orchestrate · Jun 2026", "#119 / 1,773", 93.3, LIME), ("Orchestrate · May 2026", "#306 / 1,349", 77.3, AMBER)]
    for i, (t, r, pct, c) in enumerate(logs):
        y = 56 + i * 56
        b += text(18, y, t, 13, BONE, "bold") + text(282, y, r, 12, MUTED, "bold", MONO, "end")
        b += f'<rect x="18" y="{y + 10}" width="264" height="12" rx="6" fill="#0c0706"/><rect class="bar" x="18" y="{y + 10}" width="{264 * pct / 100:.0f}" height="12" rx="6" fill="{c}"/>'
        b += text(282, y + 40, f"{pct:.0f}%", 11, c, "bold", MONO, "end")
    b += text(18, 178, "SIH 2026 Internal · Team MindMesh", 12.5, BONE, "bold")
    b += text(18, 198, "Startup-AYUSH Portal · SIH1345", 11.5, MUTED)
    b += '</g>'
    # hatching
    b += f'<g transform="translate(684,238)"><rect width="276" height="216" rx="16" fill="{PANEL}" stroke="{EDGE}" stroke-width="1.5"/>'
    b += text(18, 28, "NEXT QUESTS", 10.5, AMBER, "bold", MONO)
    nxt = [("CAMPAIGNIX", "to production"), ("VIVORA", "to production"), ("SDE Internship", "top-tier"), ("Open source", "contribute")]
    for i, (t, d) in enumerate(nxt):
        y = 46 + i * 41
        b += (f'<g transform="translate(14,{y})"><rect width="248" height="34" rx="10" fill="#0f0907"/>'
              f'<ellipse cx="20" cy="17" rx="8" ry="10" fill="{BONE}"/><path d="M13,15 l4,-3 l3,3 l3,-3 l4,3" stroke="#9a8a63" stroke-width="1.5" fill="none"/>'
              f'{text(38, 15, t, 12.5, BONE, "bold")}{text(38, 28, d, 9.5, MUTED, "normal", MONO)}'
              f'<rect x="176" y="9" width="62" height="16" rx="8" fill="{LAVA}" opacity=".2"/>{text(207, 20.5, "IN PROGRESS", 8.5, LAVA, "900", MONO, "middle")}</g>')
    b += '</g>'
    save("stats.svg", frame(W, H, b, defs))


# ------------------------------------------------------------------ 6. CONTACT
def contact():
    W, H = 1000, 290
    b = stars(W, H, 12, 9, 70) + ground(W, H, 262) + fern(980, 290, .9, True)
    b += raptor(30, 112, 1.0, delay=.2) + egg_baby(260, 168, .55, .3)
    b += text(360, 62, "// JOIN MY TEAM", 12, AMBER, "bold", MONO, extra='letter-spacing="3"')
    b += text(360, 108, "Let's build something legendary", 34, BONE, "900")
    items = [("PORTFOLIO", "anurag-six.vercel.app", LIME), ("LINKEDIN", "in/anurag-verma4", "#5aa9ff"), ("GITHUB", "@Anu7276", AMBER)]
    for i, (k, v, c) in enumerate(items):
        x = 360 + i * 205
        b += (f'<g transform="translate({x},134)"><rect width="195" height="74" rx="14" fill="{PANEL}" stroke="{c}" stroke-width="1.5"/>'
              f'<rect x="16" y="16" width="22" height="5" rx="2.5" fill="{c}"/>{text(16, 44, k, 11, c, "900", MONO, extra="letter-spacing=\"2\"")}{text(16, 62, v, 13.5, BONE, "bold")}</g>')
    b += f'<circle class="pulse" cx="366" cy="236" r="5" fill="{LIME}"/>' + text(380, 241, "Open to the right opportunity · freelance, collabs & hackathon teams", 12.5, MUTED)
    save("contact.svg", frame(W, H, b))


# ------------------------------------------------------------------ 7. FOOTER
def footer():
    W, H = 1000, 220
    defs = grad("fg", "", "", True, [(0, "#0f0907"), (1, "#3a1a10")])
    b = f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="url(#fg)" stroke="{EDGE}" stroke-width="2"/>'
    b += stars(W, H, 22, 13, 90) + volcano(790, 70, .55) + ground(W, H, 180)
    b += egg_baby(40, 98, .85) + trex(140, 70, .56, delay=.4) + raptor(700, 82, .62, flip=True, delay=.9) + boy(905, 60, .62)
    b += text(500, 92, "Code · Build · Learn · Evolve", 26, BONE, "900", anchor="middle", extra='stroke="#0a0504" stroke-width="5" paint-order="stroke"')
    b += text(500, 122, "Adventure awaits. Keep coding, keep growing.", 14, AMBER, "bold", anchor="middle")
    for i in range(7):
        b += footprint(120 + i * 110, 205, .6, LIME, .22, 90)
    save("footer.svg", svg(W, H, b, defs))


# ------------------------------------------------------------------ section headers
def header(name, title, label):
    W, H = 1000, 74
    defs = grad("hl", "", "", False, [(0, LIME), (.6, AMBER), (1, "rgba(0,0,0,0)")])
    b = footprint(36, 38, 1.5, LIME, 1, 90) + footprint(68, 30, 1.1, AMBER, .6, 90)
    b += text(100, 30, label, 11, AMBER, "bold", MONO, extra='letter-spacing="3"')
    b += (f'<text x="100" y="62" font-family="{DISPLAY}" font-size="30" font-weight="900" fill="{BONE}" stroke="#0a0504" stroke-width="5" '
          f'paint-order="stroke" stroke-linejoin="round">{esc(title)}</text>')
    b += f'<line x1="100" y1="70" x2="960" y2="70" stroke="url(#hl)" stroke-width="3" stroke-linecap="round" class="dash"/>'
    b += (f'<path class="bob" d="M900,24 q10,-14 24,-6 q-8,-6 -2,-14 q12,10 6,24 q-6,18 -28,14z" fill="{LIME2}" opacity=".0"/>')
    save(f"h_{name}.svg", svg(W, H, b, defs))


def main():
    hero(); herd(); about(); tools(); stats(); contact(); footer()
    for n, t, l in [("about", "About the Trainer", "CHAPTER 01"), ("receipts", "Receipts, Not Claims", "CHAPTER 02"),
                    ("projects", "Quest Log", "CHAPTER 03"), ("more", "Side Quests", "CHAPTER 04"),
                    ("hackathons", "Gym Battles: Hackathons & Code", "CHAPTER 05"), ("analytics", "Trainer Analytics", "CHAPTER 06"),
                    ("mission", "Current Mission", "CHAPTER 07"), ("connect", "Join My Team", "CHAPTER 08")]:
        header(n, t, l)


if __name__ == "__main__":
    main()
