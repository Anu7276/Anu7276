# Demo video

`make video` -> `media/3d-demo.mp4` (about 55 s, 1214x1028, H.264).

How it works (`scripts/make_video.py`): renders `README.md` to HTML with markdown-it, wraps it in a GitHub-dark page,
opens it in headless Chromium with video recording on, eases a scroll from top to bottom over `DUR` seconds
(default 50), then converts the recording with ffmpeg.

* External widgets (shields badges, typing text, stats cards) cannot load offline, so they are replaced by local
  look-alikes for the video only. The real README is untouched.
* Requirements: `pip install playwright markdown-it-py`, `playwright install chromium`, and `ffmpeg` on PATH.
* The scroll is slower if the page grows; raise `DUR` when you add sections.
* `media/classic-demo.mp4` is the video of the original flat version, kept for comparison.
