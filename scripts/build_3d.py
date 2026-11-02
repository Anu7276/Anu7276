#!/usr/bin/env python3
"""Generates the 3D-style SVG assets for the Trainer profile README  ->  ./assets3d
Run:  python3 build_3d.py
Techniques (pure SVG + CSS, so it works inside GitHub's <img> sandbox, no JS):
  - isometric cubes / pillars (3 shaded faces)      - extruded titles (stacked offset copies)
  - floating pedestals with glow rings              - perspective lava floor grid
  - depth-layered parallax embers"""
import os, io, json, base64, random, math
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repo root (scripts/ lives one level down)
OUT = os.path.join(ROOT, "assets", "3d")
SRC = os.path.join(ROOT, "characters")
CFG = json.load(open(os.path.join(ROOT, "config", "profile.json"), encoding="utf-8"))
os.makedirs(OUT, exist_ok=True)

DISPLAY = "'Trebuchet MS','Segoe UI',Verdana,sans-serif"
MONO = "'Courier New',Consolas,Menlo,monospace"
BG1, BG2 = "#120a08", "#3a1a10"
ORANGE, RED, AMBER, LAVA = "#ff6a3d", "#e63b2e", "#ffb347", "#ff3b30"
BONE, MUTED, PANEL, EDGE, YELLOW = "#fff1e0", "#c9aa9c", "#251410", "#7a3320", "#ffd54a"
PALETTE = {"orange": ORANGE, "red": RED, "amber": AMBER, "yellow": YELLOW, "lava": LAVA, "coral": "#ff8f7a", "blue": "#4aa3df"}


def pick(c): return PALETTE.get(c, c)   # palette name or raw hex

CSS = """
.bob{animation:bob 3s ease-in-out infinite}@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.bob2{animation:bob 3.6s ease-in-out infinite .6s}.bob3{animation:bob 2.7s ease-in-out infinite 1.1s}
.rise{animation:rise 5s ease-in infinite}@keyframes rise{0%{transform:translateY(0);opacity:0}15%{opacity:.95}100%{transform:translateY(-190px);opacity:0}}
.ring{stroke-dasharray:14 10;animation:ring 3s linear infinite}@keyframes ring{to{stroke-dashoffset:-96}}
.glow{animation:glow 2.6s ease-in-out infinite}@keyframes glow{0%,100%{opacity:.45}50%{opacity:.95}}
.grow{transform-box:fill-box;transform-origin:50% 100%;animation:grow 1.6s cubic-bezier(.2,.8,.2,1) both}
@keyframes grow{from{transform:scaleY(0)}to{transform:scaleY(1)}}
.press{animation:press 2.4s ease-in-out infinite}@keyframes press{0%,100%{transform:translateY(0)}50%{transform:translateY(5px)}}
.float{animation:float 3.4s ease-in-out infinite}@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-5px)}}
.zap{animation:zap 1.7s steps(1) infinite}@keyframes zap{0%,100%{opacity:0}6%,12%{opacity:1}18%{opacity:0}55%{opacity:0}58%,63%{opacity:.9}66%{opacity:0}}
.shine{animation:shine 4.2s ease-in-out infinite}@keyframes shine{0%{transform:translateX(0)}60%,100%{transform:translateX(760px)}}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 14s linear infinite}@keyframes spin{to{transform:rotate(360deg)}}
.blink{animation:blink 1s steps(1) infinite}@keyframes blink{50%{opacity:0}}
.sweep{animation:sweep 5s ease-in-out infinite}@keyframes sweep{0%,100%{transform:translateX(-14px)}50%{transform:translateX(14px)}}
"""


def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def save(name, w, h, body, defs=""):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
           f'viewBox="0 0 {w} {h}"><defs>{defs}<style>{CSS}</style>'
           f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>'
           f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{EDGE}"/></linearGradient>'
           f'<radialGradient id="halo"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".75"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>'
           f'<filter id="shadow" x="-30%" y="-30%" width="160%" height="170%"><feGaussianBlur stdDeviation="7"/></filter>'
           f'</defs><rect width="{w}" height="{h}" rx="22" fill="url(#bg)" stroke="url(#edge)" stroke-width="2.5"/>{body}</svg>')
    open(os.path.join(OUT, name), "w", encoding="utf-8").write(svg)
    print("wrote", name, f"{len(svg)//1024} KB")


def uri(path, scale=1.0):
    im = Image.open(os.path.join(SRC, path)).convert("RGBA")
    if path.endswith("cut2/boy.png"):  # remove the stray triceratops sliver baked into the left edge
        im.paste((0, 0, 0, 0), (0, 330, 52, im.height))
    if scale != 1: im = im.resize((int(im.width * scale), int(im.height * scale)), Image.LANCZOS)
    b = io.BytesIO(); im.save(b, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode(), im.size


def shade(hexc, f):
    r, g, b = (int(hexc[i:i + 2], 16) for i in (1, 3, 5))
    c = lambda v: max(0, min(255, int(v * f if f <= 1 else v + (255 - v) * (f - 1))))
    return f"#{c(r):02x}{c(g):02x}{c(b):02x}"


def text(x, y, s, size=16, fill=BONE, weight="bold", font=DISPLAY, anchor="start", extra=""):
    return f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" {extra}>{esc(s)}</text>'


# ---------------------------------------------------------------- 3D primitives
def pillar(cx, cy, s, h, color, cls="", delay=0):
    """isometric box; (cx,cy) = centre of the base diamond, s = half width, h = height"""
    t, l, r = shade(color, 1.35), color, shade(color, 0.62)
    top = f"{cx},{cy-s/2-h} {cx+s},{cy-h} {cx},{cy+s/2-h} {cx-s},{cy-h}"
    left = f"{cx-s},{cy-h} {cx},{cy+s/2-h} {cx},{cy+s/2} {cx-s},{cy}"
    right = f"{cx},{cy+s/2-h} {cx+s},{cy-h} {cx+s},{cy} {cx},{cy+s/2}"
    st = f'style="animation-delay:{delay}s"' if delay else ""
    return (f'<g class="{cls}" {st}><polygon points="{left}" fill="{l}"/><polygon points="{right}" fill="{r}"/>'
            f'<polygon points="{top}" fill="{t}"/><polyline points="{cx-s},{cy-h} {cx},{cy+s/2-h} {cx+s},{cy-h}" fill="none" stroke="#fff" stroke-opacity=".35" stroke-width="1.2"/></g>')


def top_label(cx, cy, h, s, label, size=15, fill="#1a0d08"):
    return (f'<g transform="translate({cx},{cy-h}) matrix(0.866 0.5 -0.866 0.5 0 0)">'
            f'<text x="0" y="{size*0.35}" font-family="{DISPLAY}" font-size="{size}" font-weight="800" fill="{fill}" text-anchor="middle">{esc(label)}</text></g>')


def extruded(x, y, s, size, face=BONE, side=EDGE, depth=9, anchor="start", dx=1.0, dy=1.0):
    """stacked copies create a solid 3D extrusion going down-right"""
    out = []
    for i in range(depth, 0, -1):
        col = shade(side, 0.45 + 0.55 * (1 - i / depth))
        out.append(text(x + i * dx, y + i * dy, s, size, col, "900", anchor=anchor))
    out.append(text(x, y, s, size, face, "900", anchor=anchor, extra=f'stroke="#fff" stroke-opacity=".25" stroke-width="1"'))
    return "".join(out)


def pedestal(cx, cy, r=95, color=ORANGE, delay=0):
    ry = r * 0.32
    return (f'<ellipse cx="{cx}" cy="{cy+24}" rx="{r*1.15}" ry="{ry*1.2}" fill="#000" opacity=".55" filter="url(#shadow)"/>'
            f'<path d="M{cx-r},{cy} v22 a{r},{ry} 0 0 0 {2*r},0 v-22z" fill="{shade(color,.45)}"/>'
            f'<path d="M{cx-r},{cy} v22 a{r},{ry} 0 0 0 {r},{ry}" fill="none" stroke="#000" stroke-opacity=".15"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{ry}" fill="{shade(color,.8)}" stroke="{shade(color,1.4)}" stroke-width="2"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r*.78}" ry="{ry*.78}" fill="none" stroke="{AMBER}" stroke-width="2.5" class="ring" style="animation-delay:{delay}s"/>'
            f'<ellipse cx="{cx}" cy="{cy}" rx="{r*.55}" ry="{ry*.55}" fill="url(#halo)" class="glow"/>')


def floor(w, h, horizon, color=ORANGE, n=18):
    vx = w / 2; g = []
    for i in range(-n, n + 1):
        g.append(f'<line x1="{vx}" y1="{horizon}" x2="{vx+i*w/n*1.1}" y2="{h}" stroke="{color}" stroke-opacity=".28" stroke-width="1.2"/>')
    k = 1
    while True:
        y = horizon + (h - horizon) * (k / 9) ** 2.1
        if y > h: break
        g.append(f'<line x1="0" y1="{y:.1f}" x2="{w}" y2="{y:.1f}" stroke="{color}" stroke-opacity="{.12+.03*k:.2f}" stroke-width="1.2"/>'); k += 1
    return f'<g clip-path="url(#fl)">{"".join(g)}</g>', f'<clipPath id="fl"><rect x="2" y="{horizon}" width="{w-4}" height="{h-horizon-2}" rx="20"/></clipPath>'


def embers(w, h, n=26, seed=7):
    rnd = random.Random(seed); o = []
    for _ in range(n):
        x, y, r = rnd.uniform(20, w - 20), rnd.uniform(h * .45, h - 10), rnd.uniform(1.2, 3.6)
        o.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.1f}" fill="{rnd.choice([AMBER, ORANGE, YELLOW])}" class="rise" style="animation-delay:{rnd.uniform(0,5):.1f}s;animation-duration:{rnd.uniform(3.5,7):.1f}s"/>')
    return "".join(o)


def volcano(cx, base, s=1.0):
    p = (f'<g transform="translate({cx},{base}) scale({s})"><polygon points="-230,0 -48,-190 48,-190 230,0" fill="#2b130c"/>'
         f'<polygon points="-48,-190 48,-190 230,0 40,0" fill="#1c0d08"/>'
         f'<polygon points="-48,-190 48,-190 30,-176 -30,-176" fill="{LAVA}" class="glow"/>'
         f'<path d="M-6,-180 L-22,-110 L-8,-60 L-30,0 L-4,0 L8,-70 L-2,-120 L14,-178z" fill="{ORANGE}" class="glow" opacity=".8"/></g>')
    return p


def chips(x, y, items, size=13):
    o, cx = [], x
    for lab, col in items:
        w = len(lab) * size * .66 + 28
        o.append(f'<rect x="{cx+3}" y="{y+4}" width="{w}" height="30" rx="9" fill="{shade(col,.5)}"/>'
                 f'<rect x="{cx}" y="{y}" width="{w}" height="30" rx="9" fill="{col}"/>'
                 + text(cx + w / 2, y + 20, lab, size, "#1a0d08", "800", MONO, "middle"))
        cx += w + 14
    return "".join(o)


# ---------------------------------------------------------------- assets
def hero():
    W, H = 1000, 560
    boy, (bw, bh) = uri("cut2/boy.png", .74); tri, (tw, th) = uri("cut2/tricera.png", .5)
    fl, fd = floor(W, H, 360)
    b = [volcano(640, 372, 1.15), fl, embers(W, H, 34)]
    b.append(text(46, 62, CFG["identity"]["terminal"], 15, AMBER, "bold", MONO) + f'<rect x="{46 + len(CFG["identity"]["terminal"]) * 9}" y="49" width="9" height="16" fill="{AMBER}" class="blink"/>')
    b.append(text(48, 118, CFG["identity"]["greeting"], 34, BONE, "800"))
    b.append(extruded(46, 214, CFG["identity"]["first_name"], 100, YELLOW, RED, 12))
    b.append(extruded(46, 318, CFG["identity"]["last_name"], 100, ORANGE, "#7a1d10", 12))
    b.append(text(50, 372, CFG["identity"]["role"], 22, BONE, "700"))
    b.append(text(50, 402, CFG["identity"]["tagline"], 17, MUTED, "normal", MONO))
    b.append(chips(46, 440, [(c["label"], pick(c["color"])) for c in CFG["hero_chips"]]))
    b.append(pedestal(715, 478, 105, ORANGE, 0)); b.append(pedestal(893, 488, 72, RED, 1.2))
    b.append(f'<g class="bob"><image href="{boy}" x="{715-bw/2}" y="{478-bh+10}" width="{bw}" height="{bh}"/></g>')
    b.append(f'<g class="bob2"><image href="{tri}" x="{893-tw/2}" y="{488-th+8}" width="{tw}" height="{th}"/></g>')
    save("hero3d.svg", W, H, "".join(b), fd)


def stats():
    W, H = 1000, 340
    data = [(p["value"], p["label"], p["height"], pick(p["color"])) for p in CFG["stats"]["pillars"]]
    fl, fd = floor(W, H, 190)
    b = [fl, embers(W, H, 14, 3), text(W / 2, 46, CFG["stats"]["title"], 16, AMBER, "bold", MONO, "middle")]
    for i, (v, lab, h, col) in enumerate(data):
        cx = 140 + i * 240
        b.append(f'<ellipse cx="{cx}" cy="274" rx="95" ry="26" fill="#000" opacity=".55" filter="url(#shadow)"/>')
        b.append(pillar(cx, 262, 62, h, col, "grow", i * .25))
        b.append(top_label(cx, 262, h, 62, v, 19 if len(v) <= 5 else 15))
        b.append(text(cx, 312, lab, 13, BONE, "800", MONO, "middle"))
    save("stats3d.svg", W, H, "".join(b), fd)


def skills():
    W, H = 1000, 460
    techs = CFG["skills"]["cubes"]
    cols = [pick(c) for c in CFG["skills"]["colors"]]
    b = [embers(W, H, 18, 5), text(W / 2, 46, CFG["skills"]["title"], 16, AMBER, "bold", MONO, "middle")]
    s_ = 64
    for idx, t in enumerate(techs):
        i, j = idx % 6, idx // 6   # 6 columns; add a row per 6 cubes (raise H in skills() if you add many)
        cx, base = 100 + i * 160, 170 + j * 120
        h = 22 + ((i * 7 + j * 13) % 4) * 9
        b.append(f'<ellipse cx="{cx}" cy="{base+16}" rx="{s_*1.1}" ry="{s_*.42}" fill="#000" opacity=".5" filter="url(#shadow)"/>')
        b.append(f'<g class="bob{["","2","3"][idx%3]}">{pillar(cx, base, s_, h, cols[idx % len(cols)])}{top_label(cx, base, h, s_, t, 13)}</g>')
    save("skills3d.svg", W, H, "".join(b))


def herd():
    W, H = 1000, 360
    items = [("cut/parasaur.png", .62, 150), ("cut2/boy.png", .4, 400), ("cut2/tricera.png", .6, 640), ("cut/carno.png", .68, 850)]
    fl, fd = floor(W, H, 215)
    b = [fl, embers(W, H, 16, 11), text(W / 2, 44, CFG["squad"]["title"], 16, AMBER, "bold", MONO, "middle")]
    for n, (p, sc, cx) in enumerate(items):
        im, (w, h) = uri(p, sc)
        py = 300 - (n % 2) * 6
        b.append(pedestal(cx, py, 78, [ORANGE, RED, AMBER, LAVA][n], n * .7))
        b.append(f'<g class="bob{["","2","3"][n%3]}"><image href="{im}" x="{cx-w/2}" y="{py-h+14}" width="{w}" height="{h}"/></g>')
    save("herd3d.svg", W, H, "".join(b), fd)


def glyph(kind):
    """flat icon drawn in local units (+-11) so it can lie on an isometric top face"""
    if kind == "arrow": return '<path d="M0,-11 L10,0 H4 V10 H-4 V0 H-10Z" fill="#1a0d08"/>'
    if kind == "nodes": return ('<g stroke="#1a0d08" stroke-width="2.2"><line x1="0" y1="-8" x2="-9" y2="7"/><line x1="0" y1="-8" x2="9" y2="7"/><line x1="-9" y1="7" x2="9" y2="7"/></g>'
                                '<g fill="#1a0d08"><circle cx="0" cy="-8" r="4"/><circle cx="-9" cy="7" r="4"/><circle cx="9" cy="7" r="4"/></g>')
    return '<path d="M0,-12 C8,-6 8,4 5,9 L0,6 L-5,9 C-8,4 -8,-6 0,-12Z" fill="#1a0d08"/><circle cx="0" cy="-3" r="2.6" fill="#ffd54a"/><path d="M-5,9 L0,14 L5,9" fill="#ff3b30"/>'


def about():
    A = CFG["about"]; W, H = 1000, 600
    boy, (bw, bh) = uri("cut2/boy.png", .62); tri, (tw, th) = uri("cut2/tricera.png", .5)
    fl, fd = floor(W, H, 470)
    defs = (fd + f'<linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
            f'<mask id="tm">{text(500, 150, A["title_1"], 66, "#fff", "900")}{text(500, 222, A["title_2"], 66, "#fff", "900")}</mask>'
            f'<linearGradient id="card" x1="0" x2="1"><stop offset="0" stop-color="#3a1a10"/><stop offset="1" stop-color="#1c0e0a"/></linearGradient>'
            f'<radialGradient id="aura"><stop offset="0" stop-color="{YELLOW}" stop-opacity=".55"/><stop offset=".5" stop-color="{ORANGE}" stop-opacity=".25"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>')
    b = []
    rnd = random.Random(4)   # starfield
    for _ in range(46):
        b.append(f'<circle cx="{rnd.uniform(14,986):.0f}" cy="{rnd.uniform(14,330):.0f}" r="{rnd.uniform(.6,1.8):.1f}" fill="{BONE}" class="glow" style="animation-delay:{rnd.uniform(0,3):.1f}s"/>')
    # volcano + eruption glow + lava rivers
    b.append(f'<circle cx="330" cy="260" r="250" fill="url(#aura)" class="glow"/>')
    b.append(volcano(330, 470, 1.5))
    rp = random.Random(9)   # eruption plume: sparks fountaining out of the crater
    for _ in range(26):
        b.append(f'<circle cx="{330+rp.uniform(-34,34):.0f}" cy="{190+rp.uniform(-8,8):.0f}" r="{rp.uniform(1.5,4.2):.1f}" fill="{rp.choice([YELLOW, ORANGE, LAVA])}" class="rise" style="animation-delay:{rp.uniform(0,4):.1f}s;animation-duration:{rp.uniform(2.2,4.5):.1f}s"/>')
    b.append(f'<ellipse cx="330" cy="188" rx="60" ry="16" fill="{YELLOW}" opacity=".6" class="glow"/>')
    for k, dx in enumerate((-70, -18, 40, 95)):
        b.append(f'<path d="M{330+dx*0.55},{300+abs(dx)*.2} q{dx*.18},70 {dx*.45},{170-abs(dx)*.4}" stroke="{ORANGE if k%2 else LAVA}" stroke-width="5" fill="none" stroke-linecap="round" class="glow" style="animation-delay:{k*.4}s"/>')
    b.append(fl); b.append(embers(W, H, 40, 12))
    # pedestals, aura, orbit ring, lightning
    b.append(pedestal(190, 505, 135, ORANGE, 0)); b.append(pedestal(372, 522, 78, RED, 1))
    b.append(f'<ellipse cx="190" cy="330" rx="150" ry="190" fill="url(#aura)" class="glow"/>')
    orbit = "M60,400 a130,38 0 1,0 260,0 a130,38 0 1,0 -260,0"
    b.append(f'<path d="{orbit}" fill="none" stroke="{AMBER}" stroke-opacity=".5" stroke-width="1.5" class="ring"/>')
    for k in range(3):
        b.append(f'<circle r="{6-k}" fill="{[YELLOW, ORANGE, BONE][k]}"><animateMotion dur="5.5s" begin="-{k*1.8}s" repeatCount="indefinite" path="{orbit}"/></circle>')
    for k, (x, y) in enumerate(((95, 250), (300, 230), (60, 380), (335, 360))):
        b.append(f'<g class="bob{["","2","3"][k%3]}">{pillar(x, y, 15, 15, [ORANGE, AMBER, RED, YELLOW][k])}</g>')
    b.append(f'<g class="bob"><image href="{boy}" x="{190-bw/2}" y="{505-bh+18}" width="{bw}" height="{bh}"/></g>')
    b.append(f'<g class="bob2"><image href="{tri}" x="{372-tw/2}" y="{522-th+12}" width="{tw}" height="{th}"/></g>')
    for k, pts in enumerate(("118,300 134,326 122,330 140,362", "262,290 246,318 258,322 242,352")):
        b.append(f'<polyline points="{pts}" fill="none" stroke="{YELLOW}" stroke-width="3" stroke-linejoin="round" class="zap" style="animation-delay:{k*.8}s"/>')
    # right column: kicker + title with extrusion + light sweep
    b.append(text(500, 76, A["kicker"], 15, AMBER, "bold", MONO))
    b.append(extruded(500, 150, A["title_1"], 66, BONE, "#c4381f", 8) + extruded(500, 222, A["title_2"], 66, YELLOW, RED, 8))
    b.append('<g mask="url(#tm)"><g class="shine"><rect x="-200" y="80" width="120" height="170" fill="url(#shine)" transform="skewX(-20)"/></g></g>')
    b.append(text(502, 256, A["sub"], 14, MUTED, "normal", MONO))
    # 3D cards
    for i, c in enumerate(A["cards"]):
        y = 284 + i * 80; colr = pick(c["color"])
        b.append(f'<g class="float" style="animation-delay:{i*.5}s">'
                 f'<rect x="506" y="{y+7}" width="470" height="62" rx="14" fill="{shade(colr,.45)}"/>'
                 f'<rect x="500" y="{y}" width="470" height="62" rx="14" fill="url(#card)" stroke="{colr}" stroke-width="2"/>'
                 f'<rect x="500" y="{y}" width="8" height="62" rx="4" fill="{colr}"/>'
                 f'{pillar(548, y+44, 22, 20, colr)}<g transform="translate(548,{y+24}) matrix(0.866 0.5 -0.866 0.5 0 0) scale(.85)">{glyph(c["icon"])}</g>'
                 + text(590, y + 26, c["title"], 14, colr, "900", MONO) + text(590, y + 48, c["text"], 13, BONE, "normal") + '</g>')
    # quote banner + chips
    b.append(f'<rect x="506" y="531" width="470" height="44" rx="12" fill="{shade(AMBER,.4)}"/><rect x="500" y="524" width="470" height="44" rx="12" fill="#1c0e0a" stroke="{AMBER}" stroke-width="2"/>')
    b.append(text(735, 553, f'"{A["quote"]}"', 19, AMBER, "bold", DISPLAY, "middle", 'font-style="italic"'))
    save("about3d.svg", W, H, "".join(b), defs)


def header(name, title, label):
    W, H = 1000, 110
    cube = pillar(70, 62, 26, 26, ORANGE) + f'<g class="glow"><polygon points="70,23 96,36 70,49 44,36" fill="{YELLOW}" opacity=".35"/></g>'
    body = (f'<rect x="2" y="2" width="996" height="106" rx="22" fill="url(#bg)"/>' + cube + text(122, 38, label, 13, AMBER, "bold", MONO)
            + extruded(120, 86, title, 44, BONE, "#c4381f", 6) + f'<rect x="760" y="60" width="200" height="6" rx="3" fill="{ORANGE}" opacity=".6" class="sweep"/>')
    save(f"h3d_{name}.svg", W, H, body)


def contact():
    W, H = 1000, 360
    boy, (bw, bh) = uri("cut2/boy.png", .47)
    fl, fd = floor(W, H, 230)
    b = [fl, embers(W, H, 14, 9), text(500, 54, CFG["contact"]["headline"], 34, BONE, "900", anchor="middle"),
         text(500, 84, CFG["contact"]["subline"], 15, AMBER, "bold", MONO, "middle")]
    links = [(c["label"], c["text"], pick(c["color"])) for c in CFG["contact"]["buttons"]]
    for i, (a, c, col) in enumerate(links):
        cx = 330 + i * 250
        b.append(f'<ellipse cx="{cx}" cy="306" rx="100" ry="26" fill="#000" opacity=".5" filter="url(#shadow)"/>')
        b.append(f'<g class="press" style="animation-delay:{i*.5}s">{pillar(cx, 290, 100, 34, col)}{top_label(cx, 290, 34, 100, a, 17)}</g>')
        b.append(text(cx, 350, c, 13, BONE, "bold", MONO, "middle"))
    b.append(f'<g class="bob"><image href="{boy}" x="30" y="{300-bh+10}" width="{bw}" height="{bh}"/></g>')
    save("contact3d.svg", W, H, "".join(b), fd)


def footer():
    W, H = 1000, 250
    tri, (tw, th) = uri("cut2/tricera.png", .3); boy, (bw, bh) = uri("cut2/boy.png", .3)
    fl, fd = floor(W, H, 120)
    b = [fl, embers(W, H, 20, 21),
         extruded(500, 112, CFG["footer"]["title"], 34, YELLOW, RED, 8, "middle"),
         text(500, 160, CFG["footer"]["subline"], 16, BONE, "normal", MONO, "middle"),
         pedestal(150, 205, 62, ORANGE), pedestal(850, 205, 62, RED),
         f'<g class="bob"><image href="{boy}" x="{150-bw/2}" y="{205-bh+8}" width="{bw}" height="{bh}"/></g>',
         f'<g class="bob2"><image href="{tri}" x="{850-tw/2}" y="{205-th+8}" width="{tw}" height="{th}"/></g>']
    save("footer3d.svg", W, H, "".join(b), fd)


def contrib_placeholder():
    """Neutral placeholder (flat tiles, no fake data). The workflow replaces it with the real 3D contribution city."""
    W, H = 1000, 380; b = [embers(W, H, 12, 4)]
    cells = sorted([(i, j) for j in range(7) for i in range(14)], key=lambda c: c[0] + c[1])
    for i, j in cells:
        b.append(pillar(500 + (i - j) * 34 - 0, 120 + (i + j) * 17, 17, 6, ORANGE if (i + j) % 2 else shade(ORANGE, .75)))
    b.append(text(500, 345, "Run the 'Generate 3D profile' workflow once: your real contribution city replaces this tile map", 14, AMBER, "bold", MONO, "middle"))
    os.makedirs(os.path.join(ROOT, "profile-3d-contrib"), exist_ok=True)
    full = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><defs><style>{CSS}</style>'
            f'<linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/></linearGradient>'
            f'<radialGradient id="halo"><stop offset="0" stop-color="{ORANGE}"/><stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>'
            f'</defs><rect width="{W}" height="{H}" rx="22" fill="url(#bg)"/>{"".join(b)}</svg>')
    open(os.path.join(ROOT, "profile-3d-contrib", "profile-night-rainbow.svg"), "w", encoding="utf-8").write(full)


if __name__ == "__main__":
    contrib_placeholder()
    hero(); stats(); skills(); herd(); about(); contact(); footer()
    for c in CFG["chapters"]:
        header(c["key"], c["title"], c["label"])

