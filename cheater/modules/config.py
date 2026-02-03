"""
Configuration module for Cheater
Loads settings from config/config.py file
"""
import os
import sys
from os.path import dirname, abspath, expanduser, join
from pathlib import Path

# Save original working directory where user launched cheater
# CHEATER_LAUNCH_DIR is set by the 'run' script before cd to cheater directory
ORIGINAL_CWD = os.environ.get('CHEATER_LAUNCH_DIR', os.getcwd())

# Base paths
DATAPATH = join(dirname(dirname(abspath(__file__))), 'data')
BASEPATH = dirname(dirname(dirname(abspath(__file__))))
HOMEPATH = expanduser("~")
CHEATS_ROOT = dirname(dirname(abspath(__file__)))  # Parent of cheater/ folder

# Load user configuration from config/config.py
CONFIG_DIR = join(BASEPATH, 'config')
sys.path.insert(0, CONFIG_DIR)

try:
    import config as user_config
    
    # Cheatsheet paths (expand ~ and resolve to absolute paths)
    raw_paths = getattr(user_config, 'CHEATSHEET_PATHS', [join(CHEATS_ROOT, "cheatsheet")])
    CHEATS_PATHS = []
    for p in raw_paths:
        expanded = Path(p).expanduser()
        # Replace Documents/cheater with actual project directory if it's a relative reference
        p_str = str(expanded)
        if 'Documents/cheater' in p_str:
            p_str = p_str.replace('Documents/cheater', BASEPATH.replace('/home/user/.work/Code/', ''))
        # Resolve to absolute path
        CHEATS_PATHS.append(str(Path(p_str).resolve()))
    
    # File formats to scan
    FORMATS = getattr(user_config, 'FORMATS', ["md", "rst", "yml"])
    
    # Files to exclude
    EXCLUDE_LIST = getattr(user_config, 'EXCLUDE_FILES', ["README.md", "README.rst", "index.rst"])
    
    # Directories to exclude
    EXCLUDE_DIRS = set(getattr(user_config, 'EXCLUDE_DIRECTORIES', [
        'env', 'venv', '.env', '.venv', 'site-packages', '__pycache__', 
        '.git', 'node_modules', 'dist', 'build', '.eggs'
    ]))
    
    # Fuzzing wordlists
    FUZZING_DIRS = getattr(user_config, 'FUZZING_WORDLIST_PATHS', [
        "/usr/share/wordlists/**/*.txt"
    ])
    
    # Global variable prefix
    PREFIX_GLOBALVAR_NAME = getattr(user_config, 'GLOBAL_VARIABLE_PREFIX', "cheater_prefix_cmd")
    
    # Terminal settings
    os.environ.setdefault('ESCDELAY', str(getattr(user_config, 'ESCAPE_DELAY', 25)))
    os.environ['TERM'] = getattr(user_config, 'TERM_TYPE', 'xterm-256color')
    
    # Save file for variables
    use_local = getattr(user_config, 'USE_LOCAL_VARIABLES_FILE', False) or os.environ.get('CHEATER_LOCAL')
    save_var_file = getattr(user_config, 'SAVE_VARIABLES_FILE', "~/.cheater.json")
    
    if use_local:
        SAVEVARFILE = join(os.getcwd(), ".cheater.json")
    else:
        SAVEVARFILE = str(Path(save_var_file).expanduser())
    
    print(f"✓ Configuration loaded from config/config.py")
    
except ImportError:
    # Fallback to hardcoded defaults if config/config.py doesn't exist
    print("⚠ Warning: config/config.py not found, using defaults")
    
    CHEATS_PATHS = [join(CHEATS_ROOT, "cheatsheet")]
    FORMATS = ["md", "rst", "yml"]
    EXCLUDE_LIST = ["README.md", "README.rst", "index.rst"]
    EXCLUDE_DIRS = {'env', 'venv', '.env', '.venv', 'site-packages', '__pycache__', 
                    '.git', 'node_modules', 'dist', 'build', '.eggs'}
    FUZZING_DIRS = ["/usr/share/wordlists/**/*.txt"]
    PREFIX_GLOBALVAR_NAME = "cheater_prefix_cmd"
    os.environ.setdefault('ESCDELAY', '25')
    os.environ['TERM'] = 'xterm-256color'
    SAVEVARFILE = join(HOMEPATH, ".cheater.json")

# Export exclude dirs for use in cheat.py
__all__ = ['CHEATS_PATHS', 'FORMATS', 'EXCLUDE_LIST', 'EXCLUDE_DIRS', 'FUZZING_DIRS',
           'PREFIX_GLOBALVAR_NAME', 'SAVEVARFILE', 'DATAPATH', 'BASEPATH', 'HOMEPATH']

# Error messages
ERROR_MISSING_ARGUMENTS = 'Error: missing arguments'

