# Trainer profile - common tasks.  `make help` lists them.
PY ?= python3

.PHONY: help install 3d classic video check all clean

help:            ## show this help
	@grep -E '^[a-z0-9]+:.*##' Makefile | sed 's/:.*##/\t/'

install:         ## install Python deps (+ Chromium for the video)
	$(PY) -m pip install -r requirements.txt
	$(PY) -m playwright install chromium

3d:              ## rebuild all 3D banners from config/profile.json
	$(PY) scripts/build_3d.py

classic:         ## rebuild the original flat SVG set into assets/classic
	$(PY) scripts/classic/build_assets.py

video:           ## record media/3d-demo.mp4 (needs playwright + ffmpeg)
	$(PY) scripts/make_video.py

check:           ## validate README links, SVGs and config
	$(PY) scripts/check.py

all: 3d check    ## rebuild + validate

clean:           ## remove temp files
	rm -rf _rec preview.html __pycache__ scripts/__pycache__ scripts/*/__pycache__
