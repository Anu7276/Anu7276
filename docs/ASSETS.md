# Asset catalogue

All 3D assets are generated; never hand-edit them (edits are lost on the next `make 3d`).
Canvas width is 1000 px everywhere and the README shows them at `width="100%"`.

| File | Canvas | Size | What you see | Built by |
|---|---|---|---|---|
| `hero3d.svg` | 1000x560 | ~150 KB | extruded name, role, chips, volcano, lava floor, boy + triceratops on pedestals | `hero()` |
| `about3d.svg` | 1000x600 | ~140 KB | erupting volcano, trainer + triceratops on pedestals with orbiting energy and lightning, extruded title with light sweep, three floating 3D cards, quote banner | `about()` |
| `stats3d.svg` | 1000x340 | ~16 KB | 4 isometric pillars that grow on load, labels on the top faces | `stats()` |
| `herd3d.svg` | 1000x360 | ~250 KB | parasaur, boy, triceratops, carnotaur on four pedestals | `herd()` |
| `skills3d.svg` | 1000x460 | ~20 KB | 18 floating isometric cubes, labelled on top | `skills()` |
| `contact3d.svg` | 1000x360 | ~64 KB | headline, three pulsing 3D buttons, boy | `contact()` |
| `footer3d.svg` | 1000x250 | ~60 KB | extruded motto, boy and triceratops | `footer()` |
| `h3d_<key>.svg` x9 | 1000x110 | ~4 KB | chapter header with cube icon and extruded title | `header()` |
| `profile-3d-contrib/profile-night-rainbow.svg` | 1000x380 | small | placeholder tile map until the Action runs | `contrib_placeholder()` |

## Animations per asset
* **hero**: characters bob, pedestal rings rotate, embers rise, lava glows, cursor blinks.
* **about**: sparks erupt from the crater, three orbs circle the trainer, lightning flickers, a light sweep crosses the title, cards float in turn.
* **stats**: pillars scale up from the floor with staggered delays (0.25 s apart).
* **skills**: cubes bob in three alternating phases.
* **contact**: buttons "press" down 5 px in turn.
* **headers**: an accent bar sweeps sideways, the cube icon glows.

## Character art (inputs)
| Folder | Contents | Used by |
|---|---|---|
| `characters/cut2/` | `boy.png` 298x600, `tricera.png` 363x330, `head.png` | 3D builder, classic rig |
| `characters/cut/` | boy poses (stand, wave, cross), `parasaur`, `carno`, `tricera`, `head` | `herd()`, classic builder |
| `characters/fire/` | `fire.png`, `fire_cut.png` (fire colourway) | `scripts/classic/build_fire.py` |
| `source/` | `sheet.png`, `sheet_cut.png`, `hero.mp4` | archived scripts only |

> **Rights note:** the character artwork was supplied with the project. Make sure you own it or are licensed to
> publish it on a public profile. The MIT license in this repo covers code only.

## File-size guidance
GitHub serves README images fine up to a few MB, but lighter loads faster. If a banner feels heavy, lower the
`scale` passed to `uri()` for that character (the PNG is re-encoded at the new size).
