"""
Path configuration for Soplos Welcome.
"""

import os

# Base directory is the directory containing this file's parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Common paths
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
ICONS_DIR = os.path.join(ASSETS_DIR, "icons")
LOCALE_DIR = os.path.join(BASE_DIR, "locale")
CONFIG_DIR = os.path.join(BASE_DIR, "config")
UI_DIR = os.path.join(BASE_DIR, "ui")
UTILS_DIR = os.path.join(BASE_DIR, "utils")
