#!/usr/bin/env python3
"""
Central location for application settings.
"""

__author__ = "Darragh Connaughton"
__copyright__ = "Copyright (c) Darragh Connaughton, 2023"
__license__ = "MIT License"

import time

PROJECT_ROOT = ""
PROJECT_DIR = ""
REPO_NAME = "https://gitlab.computing.dcu.ie/connaud5/streamingdatarepository.git"
BRANCH = "livecapture1-"
PROFILE_F = "/Users/darraghconnaughton/Library/Application Support/Firefox/Profiles/m3e7vaoq.default-release-1"
PROXY_PY = "/Users/darraghconnaughton/Github/MCM/Practicum/2023-mcm-video-fingerprinting-encrypted-network-traces-ml-sca/proxy.py"
PYPATH = "venv/bin/python"

CSS_SELECTORS = [
	"ytd-button-renderer.ytd-consent-bump-v2-lightbox:nth-child(2) > yt-button-shape:nth-child(1) > button:nth-child(1)",
	".yt-spec-button-shape-next--mono-inverse",
	".ytp-large-play-button"
]
TRACES_TO_CAPTURE = 50

TIMESTAMP = str(time.time()).split(".")[0]
