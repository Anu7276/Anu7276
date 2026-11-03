#!/usr/bin/env python3
"""src/fire.png -> src/cut2/{boy,tricera,head}.png
1) removes the solid background, 2) separates the two characters using connected components (no stray pieces),
3) bakes pseudo-3D volume: light/shadow shading from an alpha height-map + a thick extruded edge."""
import os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "src", "fire.png")
OUT = os.path.join(HERE, "src", "cut2")
TARGET_H = {"boy": 600, "tricera": 330}
LEFT_PAD = {"boy": 10, "tricera": 0}   # keeps the same coordinate system the rig clip-paths were authored in
PAD = 10          # extra canvas at right/bottom for the extrusion
DEPTH = 8         # extrusion thickness in px (at target height)
LIGHT = np.array([-0.55, -0.65, 0.52])


def remove_bg(im):
    a = np.array(im.convert("RGB")).astype(int)
    d = np.abs(a - np.array([6, 7, 13])).sum(axis=2)
    lab, _ = ndi.label(d <= 24)
    border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
    bg = np.isin(lab, list(border)); fg = ~bg
    alpha = np.where(fg, 255., 0.)
    edge = ndi.binary_dilation(bg, iterations=1) & fg
    alpha[edge] = np.clip(d[edge] * 6, 60, 255)
    return a.astype(np.uint8), alpha, fg


def shade(rgb, alpha):
    """Pseudo-3D lighting from the silhouette: inflate the alpha into a height map, light it, add AO and a soft highlight."""
    a = alpha / 255.0
    h = ndi.gaussian_filter(a, sigma=max(rgb.shape[:2]) / 55.0)
    gy, gx = np.gradient(h)
    k = 38.0
    n = np.dstack([-gx * k, -gy * k, np.ones_like(h)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    L = LIGHT / np.linalg.norm(LIGHT)
    lam = np.clip((n * L).sum(axis=2), 0, 1)
    f = 0.78 + 0.62 * lam
    f /= f[a > .5].mean()
    yy = np.linspace(0, 1, rgb.shape[0])[:, None]
    f *= 1 - 0.16 * yy ** 3                                   # ambient occlusion toward the feet
    out = rgb.astype(float) * f[..., None]
    lum = (rgb.astype(float).mean(axis=2) / 255.0)[..., None]
    out += 255 * 0.16 * (lam ** 9)[..., None] * (a[..., None] > .5) * (0.1 + lum)   # soft specular (dark parts stay dark)
    # rim light on the top-left silhouette edge
    rim = np.clip(a - ndi.gaussian_filter(a, 3.0), 0, 1) ** 1.2
    out += np.array([255, 190, 120]) * (0.5 * rim)[..., None]
    return np.clip(out, 0, 255).astype(np.uint8)


def extrude(rgb, alpha, depth=DEPTH, pad=PAD):
    H, W = alpha.shape
    canvas = np.zeros((H + pad, W + pad, 4), np.uint8)
    for i in range(depth, 0, -1):          # far -> near
        dx, dy = int(round(i * .65)), int(round(i * .85))
        t = i / depth
        col = np.array([58, 18, 8]) * (1 - .55 * t) + np.array([120, 44, 16]) * (.55 * t)  # near = lighter, far = darker
        sh = np.zeros((H + pad, W + pad), np.float32); sh[dy:dy + H, dx:dx + W] = (alpha > 128) * 255
        m = sh > 0
        canvas[m, :3] = col.astype(np.uint8); canvas[m, 3] = 255
    top = Image.fromarray(np.dstack([rgb, alpha.astype(np.uint8)]), "RGBA")
    base = Image.fromarray(canvas, "RGBA"); base.alpha_composite(top, (0, 0))
    return base


def main():
    im = Image.open(SRC)
    rgb, alpha, fg = remove_bg(im)
    lab, n = ndi.label(ndi.binary_dilation(fg, iterations=5))
    sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
    comps = sorted(range(1, n + 1), key=lambda i: -sizes[i - 1])[:2]
    objs = {i: ndi.find_objects((lab == i).astype(int))[0] for i in comps}
    # the taller component is the boy
    boy_id = max(comps, key=lambda i: objs[i][0].stop - objs[i][0].start)
    tri_id = [i for i in comps if i != boy_id][0]
    os.makedirs(OUT, exist_ok=True)
    for name, cid in (("boy", boy_id), ("tricera", tri_id)):
        mask = ndi.binary_dilation(lab == cid, iterations=2)        # only THIS character (drops pieces of the other one)
        a = np.where(mask, alpha, 0.)
        ys, xs = np.where(a > 0); y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
        c_rgb, c_a = rgb[y0:y1, x0:x1], a[y0:y1, x0:x1]
        r = TARGET_H[name] / c_rgb.shape[0]
        size = (round(c_rgb.shape[1] * r), TARGET_H[name])
        im_rgba = Image.fromarray(np.dstack([c_rgb, c_a.astype(np.uint8)]), "RGBA").resize(size, Image.LANCZOS)
        arr = np.array(im_rgba)
        shaded = shade(arr[..., :3], arr[..., 3].astype(float))
        res = extrude(shaded, arr[..., 3].astype(float))
        lp = LEFT_PAD[name]
        if lp:
            wide = Image.new('RGBA', (res.size[0] + lp, res.size[1]), (0, 0, 0, 0)); wide.alpha_composite(res, (lp, 0)); res = wide
        res.save(os.path.join(OUT, name + ".png"), optimize=True)
        print(name, res.size)
        if name == "boy":
            res.crop((0, 0, res.size[0], int(TARGET_H["boy"] * 0.36))).save(os.path.join(OUT, "head.png"))


if __name__ == "__main__":
    main()
