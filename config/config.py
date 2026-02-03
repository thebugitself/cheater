"""
CHEATER CONFIGURATION FILE
==========================
Edit this file to customize your Cheater application settings.
All settings are simple Python variables - just modify the values directly.
"""

from pathlib import Path
from os.path import expanduser

# =============================================================================
# CHEATSHEET PATHS
# =============================================================================
# Directories where your cheatsheet files are located
# You can add multiple paths, use absolute paths or ~ for home directory

CHEATSHEET_PATHS = [
    "./cheatsheet",  # Project cheatsheet folder
    # Add more paths below:
    # "~/my-cheats",
    # "/usr/share/cheats",
]

# =============================================================================
# FILE FORMATS
# =============================================================================
# Supported cheatsheet file formats to scan
# Options: "md" (Markdown), "rst" (ReStructuredText), "yml" (YAML)

FORMATS = ["md", "rst", "yml"]

# =============================================================================
# EXCLUSIONS
# =============================================================================
# Files to skip when scanning for cheatsheets
EXCLUDE_FILES = [
    "README.md",
    "README.rst", 
    "index.rst",
]

# Directories to skip when scanning (important to avoid virtual environments)
EXCLUDE_DIRECTORIES = [
    "env",           # Python virtual environment
    "venv",          # Python virtual environment
    ".env",          # Hidden virtual environment
    ".venv",         # Hidden virtual environment
    "site-packages", # Python packages
    "__pycache__",   # Python cache
    ".git",          # Git repository
    "node_modules",  # Node.js packages
    "dist",          # Distribution files
    "build",         # Build files
    ".eggs",         # Python eggs
]

# =============================================================================
# WORDLISTS (for fuzzing/security testing)
# =============================================================================
# Paths to wordlist files for security testing features
FUZZING_WORDLIST_PATHS = [
    "/usr/share/wordlists/**/*.txt",
    "~/wordlists/**/*.txt",
]

# =============================================================================
# VARIABLES FILE
# =============================================================================
# Where to save persistent variables between sessions
SAVE_VARIABLES_FILE = "~/.cheater.json"

# Set to True to save variables in current directory instead
USE_LOCAL_VARIABLES_FILE = False

# =============================================================================
# GLOBAL VARIABLE PREFIX
# =============================================================================
# Prefix name for global variables in cheatsheets
GLOBAL_VARIABLE_PREFIX = "cheater_prefix_cmd"

# =============================================================================
# TERMINAL SETTINGS
# =============================================================================
# ESC key delay in milliseconds (lower = faster ESC response)
ESCAPE_DELAY = 25

# Terminal type (usually don't need to change this)
TERM_TYPE = "xterm-256color"

# =============================================================================
# ADVANCED SETTINGS
# =============================================================================
# Maximum number of cheatsheets to display at once
MAX_DISPLAY_ITEMS = 1000

# Enable debug mode (shows more detailed error messages)
DEBUG_MODE = False
