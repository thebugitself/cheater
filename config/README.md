# Cheater Configuration

This folder contains the configuration file for Cheater application.

## Quick Start

Edit [config.py](config.py) to customize your Cheater settings:

```python
# Example: Add your cheatsheet path
CHEATSHEET_PATHS = [
    "~/Documents/cheater/cheatsheet",  
    "~/my-personal-cheats",  # Your custom path
]

# Example: Change file formats
FORMATS = ["md", "yml"]  # Only scan markdown and YAML files

# Example: Add more exclusions
EXCLUDE_DIRECTORIES = [
    "env", "venv", ".git",
    "my-backup-folder",  # Custom exclusion
]
```

## Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `CHEATSHEET_PATHS` | Directories where cheatsheets are stored | `["~/Documents/cheater/cheatsheet"]` |
| `FORMATS` | File formats to scan (md, rst, yml) | `["md", "rst", "yml"]` |
| `EXCLUDE_FILES` | Filenames to skip | `["README.md", "README.rst", "index.rst"]` |
| `EXCLUDE_DIRECTORIES` | Directories to skip (important!) | `["env", "venv", ".git", ...]` |
| `FUZZING_WORDLIST_PATHS` | Wordlist paths for fuzzing | `["/usr/share/wordlists/**/*.txt"]` |
| `SAVE_VARIABLES_FILE` | Where to save persistent variables | `"~/.cheater.json"` |
| `USE_LOCAL_VARIABLES_FILE` | Use local directory for variables | `False` |
| `GLOBAL_VARIABLE_PREFIX` | Prefix for global variables | `"cheater_prefix_cmd"` |
| `ESCAPE_DELAY` | ESC key delay (milliseconds) | `25` |
| `TERM_TYPE` | Terminal type | `"xterm-256color"` |

## Important Notes

⚠️ **EXCLUDE_DIRECTORIES** is critical! Always exclude:
- Python virtual environments (`env`, `venv`, `.venv`)
- Package directories (`site-packages`, `node_modules`)
- Cache directories (`__pycache__`, `.git`)

This prevents the application from scanning thousands of unnecessary files.

## How It Works

1. When Cheater starts, it loads `config/config.py`
2. All settings are Python variables - just edit them directly
3. Changes take effect on next run
4. If config.py is missing, defaults are used

## Path Tips

- Use `~` for home directory: `"~/my-cheats"`
- Use absolute paths: `"/opt/shared/cheats"`
- Use relative paths: `"./local-cheats"`

## Need Help?

Just open [config.py](config.py) - it's heavily commented with explanations for each setting!
