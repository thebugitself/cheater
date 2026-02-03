"""
Configuration module for Cheater
Clean and improved configuration management
"""
import os
from os.path import dirname, abspath, expanduser, join

# Save original working directory where user launched cheater
# CHEATER_LAUNCH_DIR is set by the 'run' script before cd to cheater directory
ORIGINAL_CWD = os.environ.get('CHEATER_LAUNCH_DIR', os.getcwd())

# Base paths
DATAPATH = join(dirname(dirname(abspath(__file__))), 'data')
BASEPATH = dirname(dirname(dirname(abspath(__file__))))
HOMEPATH = expanduser("~")
CHEATS_ROOT = dirname(dirname(abspath(__file__)))  # Parent of cheater/ folder

# Supported cheatsheet formats
FORMATS = ["md", "rst", "yml"]
EXCLUDE_LIST = ["README.md", "README.rst", "index.rst", "FIXES_AND_IMPROVEMENTS.md"]

# Fuzzing wordlists directories
FUZZING_DIRS = [
    "/usr/local/share/wordlists/**/*.txt",
    "/usr/share/wordlists/**/*.txt"
]

# Cheatsheet search paths - use cheatsheet folder specifically
CHEATS_PATHS = [
    join(CHEATS_ROOT, "cheatsheet"),  # /home/user/.work/Code/cheater/cheatsheet (where cheatsheets are)
    join(HOMEPATH, ".cheats"),  # User's home cheats folder
]

# Error messages
ERROR_MISSING_ARGUMENTS = 'Error: missing arguments'

# Set lower delay to use ESC key (in ms)
os.environ.setdefault('ESCDELAY', '25')
os.environ['TERM'] = 'xterm-256color'

# Save file for variables
if os.environ.get('CHEATER_LOCAL'):
    SAVEVARFILE = join(os.getcwd(), ".cheater.json")
else:
    SAVEVARFILE = join(HOMEPATH, ".cheater.json")

# Global variable prefix name
PREFIX_GLOBALVAR_NAME = "cheater_prefix_cmd"
