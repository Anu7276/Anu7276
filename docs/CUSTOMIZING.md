# Customizing

After any change: `make all` (rebuild + validate), then commit.

## 1. Text and numbers in the art — `config/profile.json`

| Key | Controls | Notes |
|---|---|---|
| `identity.terminal` | green-ish terminal line at the top of the hero | blinking cursor is placed automatically |
| `identity.first_name` / `last_name` | the two big extruded lines | keep each <= 7 letters at the default size, or lower the size in `hero()` |
| `identity.role`, `tagline` | subtitle lines under the name | |
| `hero_chips[]` | pill badges under the tagline | `label` + `color` |
| `stats.pillars[]` | the four 3D pillars | `value` (on the top face), `label` (below), `height` px (60-150 looks right), `color` |
| `skills.cubes[]` | cube labels, 6 per row | 18 fit the default canvas; more needs a taller `H` in `skills()` |
| `skills.colors[]` | colour cycle for the cubes | |
| `about.*` | the About card: `kicker`, two title lines, `sub`, three `cards[]` (title, text, color, icon = `arrow`/`nodes`/`rocket`), `quote` | |
| `squad.title` | caption over the four pedestals | |
| `contact.buttons[]` | 3D buttons | `label` (on top), `text` (below), `color` |
| `footer.title`, `subline` | footer banner | |
| `chapters[]` | all section headers | `key` becomes the filename `h3d_<key>.svg` |

**Colours** accept a palette name — `orange, red, amber, yellow, lava, coral, blue` — or any `#rrggbb`.

## 2. Add a new chapter
1. Add `{ "key": "talks", "label": "CHAPTER 09", "title": "Talks" }` to `chapters`.
2. `make 3d` creates `assets/3d/h3d_talks.svg`.
3. In `README.md` add `<img src="assets/3d/h3d_talks.svg" alt="Talks" width="100%"/>` where you want it.
4. `make check` confirms the file exists.

## 3. Add a project (README)
Copy an existing `<tr>…</tr>` block inside the Quest Log `<table>` and edit: title with its tag
(`BOSS QUEST` is the big one), event line, description, `**Stack:**`, `**Links:**`.
Keep descriptions factual; only claim results you can show.

## 4. Change the whole colour theme
Edit the palette constants at the top of `scripts/build_3d.py` (`BG1, BG2, ORANGE, RED, AMBER, LAVA, YELLOW`).
Everything derives from them (side faces use `shade()` to darken, top faces to lighten). Also update the
colour codes in the README's typing-text and badge URLs to match.

## 5. Swap or add characters
* Put a transparent PNG in `characters/cut2/` (cut out the background first).
* In `build_3d.py` load it with `uri("cut2/yourfile.png", scale)` — it returns the base64 URI and pixel size.
* Place it with `<image>` on a `pedestal(cx, cy, r)`; the `herd()` function is the simplest example.
* Check the character has no stray pixels at its edges. `uri()` already masks a leftover sliver in `boy.png`.

## 6. Tune the animation
All keyframes are in the `CSS` string at the top of `build_3d.py`: `.bob` (float), `.ring` (pedestal ring),
`.rise` (embers), `.grow` (pillars), `.press` (buttons), `.sweep` (header bar). Change durations there.
Reduce `embers(..., n)` counts for lighter files.

## 7. Dynamic widgets in the README
Typing text, badges, profile views and stats cards come from third-party URLs inside `README.md`.
Their colours are in the query strings (`color=FF6A3D` etc.); change them to stay on theme.
