# Cheater

[![asciicast](https://asciinema.org/a/778814.svg)](https://asciinema.org/a/778814)

A modern pentesting command launcher with improved features and clean interface.

**Derivative work of [Arsenal](https://github.com/Orange-Cyberdefense/arsenal)** by Orange Cyberdefense - licensed under GPLv3.

## Features

✨ **Modern Interface**
- Clean search and navigation
- File picker with @ shortcut
- Global variables with Shift+G
- Working directory preservation

🎯 **Improved Features**
- Simplified navigation (Arrow keys, Tab, Page Up/Down)
- File picker for easy file selection (@)
- Current working directory display
- Global options menu (Shift+G)
- Support for markdown, rst, and yml cheatsheets

⚙️ **Easy Configuration**
- Simple Python config file in `config/config.py`
- Just edit variables directly - no complex tools needed
- Configure cheatsheet paths, formats, exclusions, and more
- See [config/README.md](config/README.md) for guide

## Installation

```bash
# Clone the repository
git clone https://github.com/lainonz/cheater.git
cd cheater

# Create virtual environment
python3 -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate

# Install dependencies
pip3 install -r requirements.txt

# Edit configuration
nano config/config.py

# Run cheater
./run
```

## Configuration

Edit `config/config.py` to customize your settings:

```python
# Set your cheatsheet directories
CHEATSHEET_PATHS = [
    "~/cheatsheet",
    "~/my-cheats",
]

# Choose file formats
FORMATS = ["md", "rst", "yml"]

# Exclude directories (important!)
EXCLUDE_DIRECTORIES = [
    "env", "venv", ".git", "__pycache__",
]
```

See [config/README.md](config/README.md) for complete configuration guide.

## Usage

```bash
# Launch interactive menu
./run

# Print command instead of prefill
./run --print

# Copy to clipboard
./run --copy

# Execute directly
./run --exec
```

## Keybindings

### Main Menu
- **Arrow Up/Down** - Navigate cheatsheets
- **Page Up/Down** - Scroll faster
- **Tab** - Autocomplete search
- **Type** - Search cheatsheet
- **Enter** - Select cheatsheet
- **Shift+G** - Global options
- **Esc** - Exit

### Arguments Menu
- **Tab** - Autocomplete argument
- **@** - Open file picker
- **Arrow Up/Down** - Navigate arguments
- **Enter** - Execute
- **Esc** - Back

### File Picker
- **j/k or Arrow Up/Down** - Navigate
- **Enter** - Select/Open
- **Esc** - Cancel

## Cheatsheets

Place your cheatsheets in the root directory:
- `Active Directory/`
- `Network/`
This project is licensed under the **GNU General Public License v3.0** - see the [LICENSE](LICENSE) file for details.

### License Attribution

Cheater is a derivative work of [Arsenal](https://github.com/Orange-Cyberdefense/arsenal) by [Orange Cyberdefense](https://www.orange-cyberdefense.com/), which is also licensed under GPLv3.

## Credits

- **Original Project**: [Arsenal](https://github.com/Orange-Cyberdefense/arsenal) by Orange Cyberdefense
- **Derivative Work**: Cheater - Improved features and rewrite

GPLv3 - See LICENSE file

## Credits

Based on [Arsenal](https://github.com/Orange-Cyberdefense/arsenal) by Orange Cyberdefense.
Improvements and rewrite by lainonz.
