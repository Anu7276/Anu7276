#!/usr/bin/env python3
"""Renders assets/hero.svg to a 1280x640 social-preview PNG."""
import os
from PIL import Image
from playwright.sync_api import sync_playwright
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tmp = os.path.join(ROOT, "assets", "_hero.png")
with sync_playwright() as p:
    b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1000, "height": 700}, device_scale_factor=1.28)
    pg.goto("file://" + os.path.join(ROOT, "assets", "hero.svg")); pg.wait_for_timeout(400)
    pg.screenshot(path=tmp, animations="disabled", clip={"x": 0, "y": 0, "width": 1000, "height": 560}); b.close()
im = Image.open(tmp).convert("RGB"); os.remove(tmp)
c = Image.new("RGB", (1280, 640), (18, 10, 8)); c.paste(im.resize((1280, 717))
    .crop((0, 38, 1280, 678)), (0, 0)); c.save(os.path.join(ROOT, "assets", "social-preview.png"))
print("wrote assets/social-preview.png")
