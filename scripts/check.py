#!/usr/bin/env python3
"""Repo health check:  python3 scripts/check.py
  1. every local image referenced in README.md exists
  2. every SVG in assets/3d and assets/classic is well-formed XML
  3. config/profile.json has every key the 3D builder reads
Exit code 1 on any failure (CI-friendly)."""
import os, re, sys, json, glob
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bad = []

readme = open(os.path.join(ROOT, "README.md"), encoding="utf-8").read()
refs = sorted(set(re.findall(r'src="([^"]+)"', readme)))
local = [r for r in refs if not r.startswith("http")]
for r in local:
    if not os.path.exists(os.path.join(ROOT, r)): bad.append(f"README references missing file: {r}")
print(f"README: {len(local)} local images checked, {len(refs) - len(local)} remote widgets skipped")

svgs = glob.glob(os.path.join(ROOT, "assets", "*", "*.svg")) + glob.glob(os.path.join(ROOT, "profile-3d-contrib", "*.svg"))
for f in svgs:
    try: ET.parse(f)
    except ET.ParseError as e: bad.append(f"malformed SVG {os.path.relpath(f, ROOT)}: {e}")
print(f"SVG: {len(svgs)} files parsed")

cfg = json.load(open(os.path.join(ROOT, "config", "profile.json"), encoding="utf-8"))
need = {"identity": ["terminal", "greeting", "first_name", "last_name", "role", "tagline"], "hero_chips": None,
        "stats": ["title", "pillars"], "skills": ["title", "cubes", "colors"], "squad": ["title"],
        "contact": ["headline", "subline", "buttons"], "footer": ["title", "subline"], "about": ["kicker", "title_1", "title_2", "sub", "cards", "quote"], "chapters": None}
for k, sub in need.items():
    if k not in cfg: bad.append(f"config missing '{k}'"); continue
    for s in sub or []:
        if s not in cfg[k]: bad.append(f"config missing '{k}.{s}'")
if len(cfg.get("skills", {}).get("cubes", [])) > 18: bad.append("skills.cubes > 18: increase H in skills() of build_3d.py")
print("config: ok" if not [b for b in bad if b.startswith("config")] else "config: problems")

for b in bad: print("FAIL:", b)
print("ALL CHECKS PASSED" if not bad else f"{len(bad)} problem(s)")
sys.exit(1 if bad else 0)
