#!/usr/bin/env python3
"""Records a scroll-through video of the README (GitHub-dark look) -> dino-profile-demo.mp4
External widgets (badges, typing text, stats cards) can't load offline, so they are replaced
with local stand-ins just for the video. The real README is untouched."""
import os, re, sys, subprocess, shutil, urllib.parse
from markdown_it import MarkdownIt
from playwright.sync_api import sync_playwright

TOOLS = os.path.dirname(os.path.abspath(__file__))
HERE = os.path.dirname(TOOLS)  # repo root (README.md + assets/)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "profile-demo.mp4")
W, H = 1214, 1028
DUR = 42  # seconds of scrolling

md = open(os.path.join(HERE, "README.md"), encoding="utf-8").read()
html = MarkdownIt("commonmark", {"html": True}).enable("table").render(md)


def badge(m):
    url = m.group(0)
    src = re.search(r'src="([^"]+)"', url).group(1)
    if not src.startswith("http"):
        return url  # local asset: keep
    q = urllib.parse.urlparse(src)
    if "shields.io" in q.netloc:
        label = urllib.parse.unquote(q.path.split("/badge/")[1].split("?")[0]).split("-")[0].replace("_", " ")
        col = "#" + re.search(r"badge/[^-?]+-([0-9A-Fa-f]{6})", q.path + "?").group(1)
        dark = col.lower() in ("#ff6a3d", "#ffb347")
        return f'<span class="badge" style="background:{col};color:{"#111" if dark else "#fff"}">{label.upper()}</span>'
    if "komarev" in q.netloc:
        return '<span class="badge" style="background:#ffb347;color:#111">PROFILE VIEWS &nbsp; 1,024</span>'
    if "readme-typing-svg" in q.netloc:
        qs = urllib.parse.parse_qs(q.query)
        lines = qs.get("lines", [""])[0].split(";")
        size = qs.get("size", ["22"])[0]
        color = "#" + qs.get("color", ["8BD450"])[0]
        return f'<div class="typing" data-lines="{"|".join(lines)}" style="color:{color};font-size:{size}px"></div>'
    return ""  # skillicons / stats cards: dropped in the video version


html = re.sub(r"<img[^>]+>", badge, html)
def _drop_missing(m):
    src = re.search(r'src="([^"]+)"', m.group(0)).group(1)
    return m.group(0) if os.path.exists(os.path.join(HERE, src)) else ""  # generated later by GitHub Actions


html = re.sub(r"<img[^>]+>", _drop_missing, html)
# keep local assets, drop anything else remote that slipped through
html = re.sub(r'<img[^>]+src="https?://[^"]+"[^>]*>', "", html)

css = """
body{margin:0;background:#0d1117;color:#e6edf3;font:16px/1.5 -apple-system,'Segoe UI',Helvetica,Arial,sans-serif}
.top{position:fixed;top:0;left:0;right:0;height:46px;background:#161b22;border-bottom:1px solid #30363d;display:flex;align-items:center;padding:0 24px;gap:10px;z-index:9;font-size:14px;color:#8b949e}
.top b{color:#e6edf3}.dot{width:12px;height:12px;border-radius:50%;background:#ff6a3d}
.wrap{max-width:900px;margin:70px auto 60px;border:1px solid #30363d;border-radius:8px;padding:28px 36px;background:#0d1117}
.wrap img{max-width:100%}h2,h3,h4{border-bottom:1px solid #21262d;padding-bottom:.3em}
h4{border:none}
table{border-collapse:collapse;margin:12px auto}th,td{border:1px solid #30363d;padding:6px 13px}tr:nth-child(2n){background:#161b22}
code,pre{background:#161b22;border-radius:6px}pre{padding:16px;overflow:auto;font-size:13.5px}
a{color:#58a6ff;text-decoration:none}
.badge{display:inline-block;padding:7px 14px;margin:3px;border-radius:5px;font:700 12px/1 'Courier New',monospace;letter-spacing:.5px}
.typing{font-family:'Courier New',monospace;font-weight:700;text-align:center;height:44px;line-height:44px}
.typing:after{content:'\\2588';animation:b 1s steps(1) infinite}@keyframes b{50%{opacity:0}}
td{vertical-align:top}
"""
js = """
document.querySelectorAll('.typing').forEach((el,k)=>{
  const L=el.dataset.lines.split('|');let i=0,j=0,dir=1,hold=0;
  setInterval(()=>{const t=L[i];
    if(hold>0){hold--;return}
    j+=dir;el.firstChild&&0;el.setAttribute('data-t',t.slice(0,j));el.textContent=t.slice(0,j);
    if(j>=t.length){dir=-1;hold=22}else if(j<=0){dir=1;i=(i+1)%L.length}
  },55+k*4);
});
"""
page = (f"<!doctype html><meta charset=utf-8><style>{css}</style>"
        f'<div class="top"><span class="dot"></span><b>Anu7276</b> / <b>README.md</b> &nbsp;&middot;&nbsp; Trainer profile</div>'
        f'<div class="wrap">{html}</div><script>{js}</script>')
open(os.path.join(HERE, "preview.html"), "w", encoding="utf-8").write(page)

tmp = os.path.join(HERE, "_rec")
shutil.rmtree(tmp, ignore_errors=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": W, "height": H}, record_video_dir=tmp, record_video_size={"width": W, "height": H})
    pg = ctx.new_page()
    pg.goto("file://" + os.path.join(HERE, "preview.html"))
    pg.wait_for_timeout(1500)
    total = pg.evaluate("document.documentElement.scrollHeight - innerHeight")
    print("scroll distance", total)
    pg.evaluate("""([total,dur])=>new Promise(res=>{const t0=performance.now();
      const ease=x=>x<.5?2*x*x:1-Math.pow(-2*x+2,2)/2;
      (function f(){const k=Math.min(1,(performance.now()-t0)/(dur*1000));scrollTo(0,total*ease(k));
        if(k<1)requestAnimationFrame(f);else res()})()})""", [total, DUR])
    pg.wait_for_timeout(1500)
    ctx.close(); b.close()

webm = [f for f in os.listdir(tmp) if f.endswith(".webm")][0]
subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", os.path.join(tmp, webm), "-c:v", "libx264", "-preset", "veryfast",
                "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", OUT], check=True)
shutil.rmtree(tmp, ignore_errors=True)
print("wrote", OUT)
