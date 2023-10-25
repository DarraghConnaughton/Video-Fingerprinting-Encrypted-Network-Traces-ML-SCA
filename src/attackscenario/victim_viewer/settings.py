#!/usr/bin/env python3
"""
Central location for application settings.
"""

__author__ = "Darragh Connaughton"
__copyright__ = "Copyright (c) Darragh Connaughton, 2023"
__license__ = "MIT License"

import os

PROFILE_F = "/Users/darraghconnaughton/Library/Application Support/Firefox/Profiles/m3e7vaoq.default-release-1"
PROXY_PY = f"{os.getcwd()}/proxy.py"

PYPATH = "venv/bin/python"

CSS_SELECTORS = [
	"ytd-button-renderer.ytd-consent-bump-v2-lightbox:nth-child(2) > yt-button-shape:nth-child(1) > button:nth-child(1)",
	".yt-spec-button-shape-next--mono-inverse",
	".ytp-large-play-button"
]
