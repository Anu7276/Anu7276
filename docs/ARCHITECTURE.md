# Architecture

## Folder map

```
trainer-profile/
├── README.md                    the profile page visitors see (hand-written text, 3D images)
├── config/profile.json          single source of truth for all text/numbers drawn inside the 3D art
├── assets/
│   ├── 3d/                      GENERATED 3D banners (15 SVGs)           <- scripts/build_3d.py
│   └── classic/                 original flat banners (kept; about.svg is still used)
├── profile-3d-contrib/          3D contribution city (written by the GitHub Action; fixed folder name)
├── characters/                  character art used by the builders
│   ├── cut/                     v1 cut-outs: boy poses, parasaur, carno, tricera, head
│   ├── cut2/                    v2 cut-outs used by the 3D art: boy, tricera, head
│   └── fire/                    "fire" colourway source + cut
├── source/                      raw inputs: sprite sheets and hero.mp4 (only the archived script needs these)
├── scripts/
│   ├── build_3d.py              MAIN builder (config -> assets/3d + placeholder city)
│   ├── check.py                 validates README links, SVG XML, config keys
│   ├── make_video.py            records the scroll-through demo
│   ├── classic/                 builders for the original flat set (build_assets, build_fire, rig)
│   └── archive/                 old experiments (hero.webp pipeline) - not needed day to day
├── media/                       classic-demo.mp4, 3d-demo.mp4
├── docs/                        you are here
├── .github/workflows/           profile-3d.yml (daily refresh + manual button)
├── Makefile                     make 3d | check | video | classic | all | clean
└── requirements.txt             pillow, markdown-it-py, playwright
```

## Data flow

```
config/profile.json ─┐
characters/*.png ────┼─► scripts/build_3d.py ─► assets/3d/*.svg ─┐
                     │                                           ├─► README.md  (<img src="assets/3d/...">)
GitHub API ──► Action ─► profile-3d-contrib/*.svg ───────────────┘
                                                                  └─► scripts/make_video.py ─► media/3d-demo.mp4
```

## Design decisions

* **Pure SVG + CSS.** GitHub renders README images through `<img>`, which blocks JavaScript. SVG with CSS
  `@keyframes` is the richest thing that animates there, so every "3D" effect is drawn geometry (see 3D-TECHNIQUES.md).
* **Characters are embedded as base64 PNG inside each SVG.** An SVG loaded through `<img>` cannot fetch other files,
  so each banner is fully self-contained (this is why `hero3d.svg` and `herd3d.svg` are 150-250 KB).
* **Text is config, layout is code.** Strings, numbers, colours and chapter titles live in JSON. Positions and
  geometry live in `build_3d.py`, so you can restyle without touching coordinates.
* **The README prose stays hand-written.** Projects, hackathon results and the mission table are normal Markdown so
  they are easy to edit and render natively on GitHub.
* **Generated files are committed.** GitHub serves the repo directly, so the SVGs must exist in git. The workflow
  rebuilds and commits them; `make 3d` does the same locally.
* **`profile-3d-contrib/` sits at the root** because the contribution-city Action always writes to that folder name.

## Where things are used

| README section | Image(s) | Built by |
|---|---|---|
| Hero | `assets/3d/hero3d.svg`, `stats3d.svg`, `herd3d.svg` | `hero()`, `stats()`, `herd()` |
| Every chapter title | `assets/3d/h3d_<key>.svg` | `header()` driven by `chapters[]` |
| About card | `assets/3d/about3d.svg` | `about()` |
| Tools | `assets/3d/skills3d.svg` | `skills()` |
| Contribution city | `profile-3d-contrib/profile-night-rainbow.svg` | Action (placeholder from `contrib_placeholder()`) |
| Contact | `assets/3d/contact3d.svg` | `contact()` |
| Footer | `assets/3d/footer3d.svg` | `footer()` |
