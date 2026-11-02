#!/usr/bin/env python3
"""Builds the final profile assets from the user's own AI-generated art:
  src/hero.mp4     -> assets/hero.webp  (animated, with name/role overlay baked in)
  src/cut/*.png    -> embedded (base64) into the SVG cards
Run after build_assets.py:   python3 build_assets.py && python3 build_art.py"""
import os, io, base64, subprocess, shutil, glob
from PIL import Image, ImageFilter, ImageEnhance
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..", "classic"))
import build_assets as B
from playwright.sync_api import sync_playwright

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # repo root
SRC, CUT, OUT = (os.path.join(HERE, p) for p in ("source", "characters/cut", "assets/classic"))
TMP = os.path.join(HERE, "_tmp")
shutil.rmtree(TMP, ignore_errors=True)
os.makedirs(TMP)

HW, HH = 1000, 562  # hero size


# ---------------------------------------------------------------- helpers
def uri_png(im, maxh=None):
    if maxh and im.size[1] > maxh:
        im = im.resize((round(im.size[0] * maxh / im.size[1]), maxh), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def uri_jpg(im, q=78):
    buf = io.BytesIO(); im.convert("RGB").save(buf, "JPEG", quality=q, optimize=True)
    return "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()


def cut(name):
    return Image.open(os.path.join(CUT, name + ".png"))


def place(name, x, ground_y, h, delay=0, flip=False, bob=True):
    """Place a cutout so its feet sit on ground_y, scaled to height h."""
    im = cut(name)
    w = round(im.size[0] * h / im.size[1])
    hi = uri_png(im, maxh=int(h * 2))
    cls = ' class="bob"' if bob else ""
    tf = f' transform="translate({x + w},0) scale(-1,1) translate({-x},0)"' if flip else ""
    return (f'<g{tf}><image{cls} style="animation-delay:{delay}s" href="{hi}" x="{x}" y="{ground_y - h}" '
            f'width="{w}" height="{h}"/></g>'), w


# background frame from the video (painted jungle) for panels
FRAME = os.path.join(TMP, "frame.jpg")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", "3.0", "-i", os.path.join(SRC, "hero.mp4"), "-frames:v", "1", FRAME], check=True)
frame = Image.open(FRAME).convert("RGB")  # 1280x720


def bg_crop(box, size, dark=.45, blur=0):
    c = frame.crop(box).resize(size, Image.LANCZOS)
    if blur:
        c = c.filter(ImageFilter.GaussianBlur(blur))
    return ImageEnhance.Brightness(c).enhance(dark)


# ---------------------------------------------------------------- 1. HERO (video + overlay)
def hero():
    ov = B.svg(HW, HH,
        '<defs><linearGradient id="s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050d09" stop-opacity=".88"/>'
        '<stop offset="1" stop-color="#050d09" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="n" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#c7f56b"/><stop offset=".55" stop-color="#8bd450"/><stop offset="1" stop-color="#ffb347"/></linearGradient></defs>'
        f'<rect width="{HW}" height="230" fill="url(#s)"/>'
        + B.text(44, 44, "anurag@trainer-hq:~$ adventure --start", 14, B.LIME, "bold", B.MONO)
        + B.text(44, 84, "Hi, I'm", 26, B.BONE, "bold")
        + f'<text x="44" y="150" font-family="{B.DISPLAY}" font-size="72" font-weight="900" fill="url(#n)" stroke="#06100b" stroke-width="7" '
          f'paint-order="stroke" stroke-linejoin="round" textLength="520" lengthAdjust="spacingAndGlyphs">ANURAG VERMA</text>'
        + B.text(46, 184, "Software Developer  |  AI / ML Enthusiast", 19, B.AMBER, "bold")
        + B.text(46, 208, "Still thinking. Always building.", 14.5, "#e9f0df"),
        extra_css=".x{}")
    # strip animations so playwright can screenshot; overlay is static anyway
    p = os.path.join(TMP, "ov.svg"); open(p, "w", encoding="utf-8").write(ov)
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(viewport={"width": HW, "height": HH})
        pg.goto("file://" + p); pg.wait_for_timeout(300)
        pg.screenshot(path=os.path.join(TMP, "ov.png"), omit_background=True, animations="disabled"); b.close()
    overlay = Image.open(os.path.join(TMP, "ov.png")).convert("RGBA")
    fdir = os.path.join(TMP, "fr"); os.makedirs(fdir)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(SRC, "hero.mp4"), "-an",
                    "-vf", f"fps=12,scale={HW}:{HH}", os.path.join(fdir, "f_%03d.png")], check=True)
    frames = []
    for f in sorted(glob.glob(os.path.join(fdir, "f_*.png"))):
        im = Image.open(f).convert("RGBA"); im.alpha_composite(overlay); frames.append(im.convert("RGB"))
    out = os.path.join(OUT, "hero.webp")
    for q in (62, 52, 42, 34):
        frames[0].save(out, "WEBP", save_all=True, append_images=frames[1:], duration=83, loop=0, quality=q, method=4)
        mb = os.path.getsize(out) / 1e6
        print(f"hero.webp q={q}: {mb:.1f} MB, {len(frames)} frames")
        if mb < 6.5:
            break
    frames[0].save(os.path.join(OUT, "hero_poster.jpg"), quality=88)


# ---------------------------------------------------------------- 2. hero stats strip
def hero_stats():
    W, H = 1000, 112
    b = ""
    items = [("#119", "HACKERRANK / 1,773", B.LIME), ("GOLD", "CODECHEF BADGE", B.AMBER), ("100%", "CLAIM PIPELINE", B.TEAL), ("TOP 7%", "GLOBAL, JUN 2026", B.CORAL)]
    for i, (v, l, c) in enumerate(items):
        x = 30 + i * 176
        b += (f'<g transform="translate({x},26)"><rect width="164" height="60" rx="14" fill="{B.PANEL}" stroke="{B.EDGE}" stroke-width="1.5"/>'
              f'{B.text(82, 30, v, 24, c, "900", anchor="middle")}{B.text(82, 48, l, 9, B.MUTED, "bold", B.MONO, "middle")}</g>')
    b += (f'<g transform="translate(740,26)"><rect width="230" height="60" rx="14" fill="#143a1f" stroke="{B.LIME}" stroke-width="1.5"/>'
          f'<circle class="pulse" cx="26" cy="30" r="7" fill="{B.LIME}"/>{B.text(44, 28, "OPEN TO THE RIGHT", 12, B.LIME, "900")}{B.text(44, 46, "OPPORTUNITY", 12, B.LIME, "900")}</g>')
    B.save("hero_stats.svg", B.frame(W, H, b))


# ---------------------------------------------------------------- 3. herd row
def herd():
    W, H = 1000, 220
    bgu = uri_jpg(bg_crop((0, 0, 860, 190), (W, H), .5, 1.0))
    body = (f'<clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22"/></clipPath>'
            f'<g clip-path="url(#c)"><image href="{bgu}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>'
            f'<rect width="{W}" height="{H}" fill="#06120c" opacity=".25"/>')
    seq = [("boy_stand", 178), ("tricera", 126), ("boy_wave", 178), ("parasaur", 142), ("boy_cross", 178), ("carno", 138)]
    widths = [round(cut(n).size[0] * h / cut(n).size[1]) for n, h in seq]
    gap = (W - 60 - sum(widths)) / (len(seq) - 1)
    x = 30
    for i, ((n, h), w) in enumerate(zip(seq, widths)):
        g, _ = place(n, round(x), H - 14, h, delay=i * .25)
        body += g; x += w + gap
    body += "</g>" + f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="{B.EDGE}" stroke-width="2"/>'
    B.save("herd.svg", B.svg(W, H, body))


# ---------------------------------------------------------------- 4. about card
def about():
    W, H = 1000, 460
    bgu = uri_jpg(bg_crop((880, 0, 1280, 330), (372, 460), .55, 1.2))
    defs = '<clipPath id="art"><rect x="1" y="1" width="370" height="458" rx="22"/></clipPath>'
    b = f'<g clip-path="url(#art)"><image href="{bgu}" x="0" y="0" width="372" height="460" preserveAspectRatio="xMidYMid slice"/>'
    g1, _ = place("boy_cross", 36, 450, 330, delay=0)
    g2, _ = place("tricera", 190, 452, 175, delay=.4)
    b += g1 + g2 + "</g>"
    b += B.text(404, 62, "// MY TRAINER HQ", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += B.text(404, 112, "Think it — then ship it", 38, B.BONE, "900")
    b += B.text(404, 140, "AI agent builder  ·  B.Tech CSE (AI) @ Parul University", 14, B.MUTED)
    feats = [("AGENTS THAT ACT", "Read pitch decks, verify claims, run voice interviews.", B.LIME),
             ("MULTI-AGENT TEAM", "Groq + Gemini orchestration, RAG that doesn't hallucinate.", B.AMBER),
             ("IDEA TO DEPLOYED", "From a messy 2 AM sketch to a demo-able product.", B.TEAL)]
    for i, (t, d, c) in enumerate(feats):
        y = 168 + i * 66
        b += (f'<g transform="translate(404,{y})"><rect width="556" height="56" rx="14" fill="{B.PANEL}" stroke="{B.EDGE}" stroke-width="1.5"/>'
              f'<rect x="10" y="10" width="36" height="36" rx="10" fill="{c}" opacity=".18"/>'
              f'<g transform="translate(28,28)"><path d="M-9,-3 L0,-12 L9,-3 M0,-12 L0,10" stroke="{c}" stroke-width="3" fill="none" stroke-linecap="round" stroke-linejoin="round"/></g>'
              f'{B.text(60, 24, t, 12, c, "900", B.MONO, extra="letter-spacing=\"1.5\"")}{B.text(60, 43, d, 13, B.BONE)}</g>')
    b += (f'<g transform="translate(404,372)"><rect width="556" height="46" rx="14" fill="#2a1d0e" stroke="{B.AMBER}" stroke-width="1.5"/>'
          f'{B.text(18, 29, chr(8220) + "If it can" + chr(8217) + "t be demoed, it isn" + chr(8217) + "t done." + chr(8221), 17, B.AMBER, "bold", extra="font-style=\"italic\"")}</g>')
    b += B.text(404, 442, "TOP 7% GLOBAL  ·  CODECHEF GOLD  ·  SIH 2026", 10.5, B.MUTED, "bold", B.MONO, extra='letter-spacing="1.5"')
    B.save("about.svg", B.frame(W, H, b, defs))


# ---------------------------------------------------------------- 5. tools card
def tools():
    W, H = 1000, 400
    defs = ('<linearGradient id="beam" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ffd27a" stop-opacity=".5"/>'
            '<stop offset="1" stop-color="#ffd27a" stop-opacity="0"/></linearGradient>')
    b = B.text(372, 56, "// CREATURE DEX", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += B.text(372, 98, "Tools in my backpack", 36, B.BONE, "900")
    b += B.stars(W, H, 10, 2, 60)
    b += '<polygon class="glow" points="190,250 360,130 360,360" fill="url(#beam)"/>'
    g, _ = place("tricera", 24, 380, 210, delay=.3)
    g2, _ = place("parasaur", 150, 386, 120, delay=.9, flip=False)
    b += g + g2
    groups = [(B.AMBER, ["Groq", "Gemini", "RAG · FAISS", "ChromaDB", "Multi-Agent"]),
              (B.LIME, ["React", "Next.js", "Node.js", "Socket.io", "TypeScript"]),
              (B.TEAL, ["MongoDB", "PostgreSQL", "SQLite", "Prisma", "SQL"]),
              (B.CORAL, ["Java", "C++", "Python", "Git", "FastAPI"])]
    for r, (c, items) in enumerate(groups):
        for i, it in enumerate(items):
            b += B.chip(372 + i * 120, 128 + r * 58, 112, 46, it, c, 13)
    b += B.text(372, 372, "AI · FULL STACK · DATA · CORE", 10.5, B.MUTED, "bold", B.MONO, extra='letter-spacing="2"')
    B.save("tools.svg", B.frame(W, H, b, defs))


# ---------------------------------------------------------------- 6. stats / ID card (avatar = real art)
def stats():
    src = open(os.path.join(OUT, "stats.svg"), encoding="utf-8").read()
    head = uri_png(cut("head"), maxh=240)
    # replace the vector boy inside the avatar clip with the artwork head
    a = src.index('<g clip-path="url(#av)">')
    new = (f'<g clip-path="url(#av)"><image href="{head}" x="128" y="118" width="124" height="140" preserveAspectRatio="xMidYMid slice"/></g>')
    # the vector boy block ends right before the name text
    end = src.index('<text x="190" y="272"')
    src = src[:a] + new + src[end:]
    open(os.path.join(OUT, "stats.svg"), "w", encoding="utf-8").write(src)
    print("patched stats.svg")


# ---------------------------------------------------------------- 7. contact + footer
def contact():
    W, H = 1000, 290
    b = B.stars(W, H, 12, 9, 70)
    g, _ = place("parasaur", 28, 272, 168, delay=.2)
    g2, _ = place("carno", 232, 274, 112, delay=.6)
    b += g + g2
    b += B.text(420, 62, "// JOIN MY TEAM", 12, B.AMBER, "bold", B.MONO, extra='letter-spacing="3"')
    b += B.text(420, 108, "Let's build something legendary", 32, B.BONE, "900")
    items = [("PORTFOLIO", "anurag-six.vercel.app", B.LIME), ("LINKEDIN", "in/anurag-verma4", "#5aa9ff"), ("GITHUB", "@Anu7276", B.AMBER)]
    for i, (k, v, c) in enumerate(items):
        x = 420 + i * 190
        b += (f'<g transform="translate({x},134)"><rect width="180" height="74" rx="14" fill="{B.PANEL}" stroke="{c}" stroke-width="1.5"/>'
              f'<rect x="16" y="16" width="22" height="5" rx="2.5" fill="{c}"/>{B.text(16, 44, k, 11, c, "900", B.MONO, extra="letter-spacing=\"2\"")}{B.text(16, 62, v, 13, B.BONE, "bold")}</g>')
    b += f'<circle class="pulse" cx="426" cy="238" r="5" fill="{B.LIME}"/>' + B.text(440, 243, "Open to the right opportunity · freelance, collabs & hackathon teams", 12.5, B.MUTED)
    B.save("contact.svg", B.frame(W, H, b))


def footer():
    W, H = 1000, 230
    bgu = uri_jpg(bg_crop((420, 0, 1280, 198), (W, H), .45, 1.0))
    b = (f'<clipPath id="c"><rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22"/></clipPath>'
         f'<g clip-path="url(#c)"><image href="{bgu}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>')
    for n, x, h, d in [("tricera", 30, 120, 0), ("carno", 190, 128, .4), ("parasaur", 700, 132, .7), ("boy_wave", 880, 178, .2)]:
        g, _ = place(n, x, H - 12, h, delay=d); b += g
    b += "</g>"
    b += B.text(500, 100, "Code · Build · Learn · Evolve", 28, B.BONE, "900", anchor="middle", extra='stroke="#06100b" stroke-width="5" paint-order="stroke"')
    b += B.text(500, 134, "Adventure awaits. Keep coding, keep growing.", 14.5, B.AMBER, "bold", anchor="middle")
    b += f'<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="22" fill="none" stroke="{B.EDGE}" stroke-width="2"/>'
    B.save("footer.svg", B.svg(W, H, b))


if __name__ == "__main__":
    B.main()  # regenerate vector fallback + section headers + stats base
    hero(); hero_stats(); herd(); about(); tools(); stats(); contact(); footer()
    shutil.rmtree(TMP, ignore_errors=True)
