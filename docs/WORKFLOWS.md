# GitHub Actions

File: `.github/workflows/profile-3d.yml`

## What it does
1. Runs `yoshi389111/github-profile-3d-contrib@0.7.1` for user `Anu7276`, which writes several SVG themes of your
   contribution calendar as an isometric 3D city into `profile-3d-contrib/`.
2. Reinstalls Python deps and runs `scripts/build_3d.py` so the hand-built banners are regenerated from config.
3. Commits changes (if any) as `github-actions[bot]`.

## Triggers
* daily at 18:00 UTC
* manual: Actions tab -> "Generate 3D profile" -> Run workflow
* on every push to `main`

## One-time setup
1. This repository must be named exactly like your username (`Anu7276/Anu7276`) for the README to show on your profile.
2. Settings -> Actions -> General -> Workflow permissions -> **Read and write permissions**.
3. Run the workflow once. `profile-3d-contrib/profile-night-rainbow.svg` is then replaced by the real city.

## Using another theme
The Action also writes other files into `profile-3d-contrib/`. Change the README line
`profile-3d-contrib/profile-night-rainbow.svg` to the theme you prefer after the first run
(open the folder to see the available names).

## Caveats
* The action version and output names come from the Action's own documentation; if it changes, update the pinned tag.
* If a push triggers the workflow and the workflow pushes back, the second run finds nothing to commit and exits.
