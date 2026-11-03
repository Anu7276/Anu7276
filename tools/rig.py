"""Lightweight SVG 'puppet rig' for the two cut-out characters.
Each character image is embedded once (<image id=...>) and re-used via <use> with clip-paths so that
individual body parts (head, hair, arm, tail, feet, eyelids) can be animated with CSS."""
import os, io, base64
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
CUT = os.path.join(HERE, "src", "cut2")


def _uri(name):
    buf = io.BytesIO(); Image.open(os.path.join(CUT, name + ".png")).save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


BOY_W, BOY_H = 298, 600   # nominal sprite size (used for scaling/placement)
TRI_W, TRI_H = 363, 330


def _size(name):
    return Image.open(os.path.join(CUT, name + ".png")).size   # real canvas incl. extrusion padding


def defs():
    return (
        f'<image id="IMG_boy" href="{_uri("boy")}" width="{_size("boy")[0]}" height="{_size("boy")[1]}"/>'
        f'<image id="IMG_tri" href="{_uri("tricera")}" width="{_size("tricera")[0]}" height="{_size("tricera")[1]}"/>'
        # --- boy clips
        '<clipPath id="cb_lower"><polygon points="0,212 90,232 160,228 215,210 232,188 298,158 298,600 0,600"/></clipPath>'
        '<clipPath id="cb_head"><polygon points="0,0 298,0 298,170 232,200 215,222 160,240 90,244 0,224"/></clipPath>'
        '<clipPath id="cb_hair"><rect x="80" y="0" width="218" height="46"/></clipPath>'
        '<clipPath id="cb_fore"><polygon points="5,125 128,125 128,222 5,222"/></clipPath>'
        '<clipPath id="cb_arm"><polygon points="215,236 298,236 298,392 222,392"/></clipPath>'
        # --- tricera clips
        '<clipPath id="ct_base"><polygon points="0,203 48,203 60,240 215,238 225,226 300,203 363,203 363,330 0,330"/>'
        '<polygon points="292,90 363,90 363,203 292,203"/></clipPath>'
        '<clipPath id="ct_head"><polygon points="0,0 300,0 300,215 225,238 215,252 60,252 48,215 0,215"/></clipPath>'
        '<clipPath id="ct_tail"><rect x="290" y="92" width="60" height="76"/></clipPath>'
        '<clipPath id="ct_f1"><rect x="40" y="255" width="80" height="75"/></clipPath>'
        '<clipPath id="ct_f2"><rect x="125" y="262" width="95" height="68"/></clipPath>'
        '<clipPath id="ct_f3"><rect x="222" y="262" width="80" height="68"/></clipPath>'
        '<clipPath id="ct_f4"><rect x="285" y="250" width="78" height="80"/></clipPath>')


CSS = """
.rb-hop{animation:rbHop 1.8s ease-in-out infinite;transform-origin:150px 600px}
@keyframes rbHop{0%,100%{transform:translateY(0) scale(1,1)}50%{transform:translateY(-7px) scale(.995,1.012)}}
.rb-sway{animation:rbSway 3.6s ease-in-out infinite;transform-origin:150px 600px}
@keyframes rbSway{0%,100%{transform:rotate(-.9deg)}50%{transform:rotate(.9deg)}}
.rb-head{animation:rbHead 3.2s ease-in-out infinite;transform-origin:175px 238px}
@keyframes rbHead{0%,100%{transform:rotate(-2.2deg) translateY(1px)}50%{transform:rotate(2.6deg) translateY(-2px)}}
.rb-hair{animation:rbHair 1.3s ease-in-out infinite alternate;transform-origin:170px 70px}
@keyframes rbHair{from{transform:rotate(-4deg)}to{transform:rotate(5deg)}}
.rb-fore{animation:rbFore 3s ease-in-out infinite;transform-origin:40px 208px}
@keyframes rbFore{0%,60%,100%{transform:rotate(0)}68%{transform:rotate(-7deg)}76%{transform:rotate(1deg)}84%{transform:rotate(-6deg)}92%{transform:rotate(0)}}
.rb-arm{animation:rbArm 3.2s ease-in-out infinite;transform-origin:240px 240px}
@keyframes rbArm{0%,100%{transform:rotate(1.5deg)}50%{transform:rotate(-3.5deg)}}

.rt-body{animation:rtBody 1.1s ease-in-out infinite;transform-origin:180px 330px}
@keyframes rtBody{0%,100%{transform:translateY(0) rotate(0)}50%{transform:translateY(-6px) rotate(.8deg)}}
.rt-head{animation:rtHead 2.6s ease-in-out infinite;transform-origin:205px 228px}
@keyframes rtHead{0%,100%{transform:rotate(-2.8deg) translateY(1px)}50%{transform:rotate(3deg) translateY(-3px)}}
.rt-tail{animation:rtTail .8s ease-in-out infinite alternate;transform-origin:296px 150px}
@keyframes rtTail{from{transform:rotate(-10deg)}to{transform:rotate(12deg)}}
.rt-stepA{animation:rtA 1s ease-in-out infinite}
.rt-stepB{animation:rtB 1s ease-in-out infinite}
@keyframes rtA{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
@keyframes rtB{0%,100%{transform:translateY(-6px)}50%{transform:translateY(0)}}
.rt-lid{transform-box:fill-box;transform-origin:50% 0;animation:rtLid 4.2s infinite}
@keyframes rtLid{0%,93%,100%{transform:scaleY(0)}96%{transform:scaleY(1)}}
.puff{animation:puff 3s ease-out infinite}
@keyframes puff{0%{transform:translate(0,0) scale(.4);opacity:0}15%{opacity:.8}100%{transform:translate(-26px,-30px) scale(1.6);opacity:0}}
.walkA{transform-box:fill-box;transform-origin:center;animation:walkA 15s linear infinite}
@keyframes walkA{0%{transform:translateX(0) scaleX(1)}46%{transform:translateX(var(--d)) scaleX(1)}50%{transform:translateX(var(--d)) scaleX(-1)}96%{transform:translateX(0) scaleX(-1)}100%{transform:translateX(0) scaleX(1)}}
"""


def _tf(x, gy, w, h, s, flip):
    return (f"translate({x + w},{gy - h}) scale({-s},{s})" if flip else f"translate({x},{gy - h}) scale({s})")


def boy(x, gy, h, delay=0, flip=False):
    s = h / BOY_H; w = round(BOY_W * s)
    d = f'style="animation-delay:{-delay}s"'
    g = (f'<g transform="{_tf(x, gy, w, h, s, flip)}"><g class="rb-sway" {d}><g class="rb-hop" {d}>'
         f'<g clip-path="url(#cb_lower)"><use href="#IMG_boy"/></g>'
         f'<g clip-path="url(#cb_arm)"><g class="rb-arm" {d}><use href="#IMG_boy"/></g></g>'
         f'<g class="rb-head" {d}><g clip-path="url(#cb_head)"><use href="#IMG_boy"/></g>'
         f'<g clip-path="url(#cb_hair)"><g class="rb-hair" {d}><use href="#IMG_boy"/></g></g>'
         f'<g clip-path="url(#cb_fore)"><g class="rb-fore" {d}><use href="#IMG_boy"/></g></g></g>'
         f'</g></g></g>')
    return g, w


def tri(x, gy, h, delay=0, flip=False, step=1.0):
    s = h / TRI_H; w = round(TRI_W * s)
    d = f'style="animation-delay:{-delay}s;animation-duration:{step}s"'
    dd = f'style="animation-delay:{-delay}s"'
    use = '<use href="#IMG_tri"/>'
    lid = ('<g class="rt-lid" ' + dd + '><ellipse cx="87" cy="160" rx="13" ry="16" fill="#ffb628"/><path d="M74,168 Q87,176 100,168" stroke="#2a1708" stroke-width="3" fill="none" stroke-linecap="round"/>'
           '<ellipse cx="174" cy="160" rx="13" ry="16" fill="#ffb628"/><path d="M161,168 Q174,176 187,168" stroke="#2a1708" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
    g = (f'<g transform="{_tf(x, gy, w, h, s, flip)}"><g class="rt-body" {d}>'
         f'<g clip-path="url(#ct_base)">{use}</g>'
         f'<g clip-path="url(#ct_tail)"><g class="rt-tail" {dd}>{use}</g></g>'
         f'<g clip-path="url(#ct_f1)"><g class="rt-stepA" {d}>{use}</g></g>'
         f'<g clip-path="url(#ct_f2)"><g class="rt-stepB" {d}>{use}</g></g>'
         f'<g clip-path="url(#ct_f3)"><g class="rt-stepA" {d}>{use}</g></g>'
         f'<g clip-path="url(#ct_f4)"><g class="rt-stepB" {d}>{use}</g></g>'
         f'<g class="rt-head" {dd}><g clip-path="url(#ct_head)">{use}</g>{lid}</g>'
         f'</g></g>')
    return g, w
