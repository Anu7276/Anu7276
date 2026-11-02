# Changelog

## 3D edition
* New: `assets/3d/` — isometric stats pillars, 18-cube skills grid, extruded hero title, pedestals, perspective lava
  floor, 3D buttons, 3D chapter headers, 3D footer.
* New: `config/profile.json` drives all art text, numbers and colours.
* New: 3D contribution city section + GitHub Actions workflow with daily refresh.
* New: `scripts/check.py`, `Makefile`, `docs/`, `LICENSE`, `media/3d-demo.mp4`.
* Reorganised: `src/` -> `characters/` + `source/`, flat builders -> `scripts/classic/`, `old/` -> `scripts/archive/`,
  classic SVGs -> `assets/classic/`.
* Fixed: stray triceratops sliver on the left edge of `boy.png` is masked when embedding.
* New: `about3d.svg` replaces the flat About card (volcano eruption, orbiting energy, lightning, floating 3D cards).
* Fixed: removed the stray triceratops sliver from `characters/cut2/boy.png` itself (was visible bottom-left of the old About card).
* Kept: classic README (`docs/README.classic.md`), classic assets and builders, original demo video.
