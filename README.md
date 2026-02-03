# Cheater

A modern pentesting command launcher with improved features and clean interface.

**Based on [Arsenal](https://github.com/Orange-Cyberdefense/arsenal)** by Orange Cyberdefense.

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

## Installation

```bash
# Clone the repository
git clone https://github.com/lainonz/cheater.git
cd cheater

# Install dependencies
pip3 install -r requirements.txt

# Run cheater
./run
```

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
- `Password Cracking/`
- etc.

Supported formats: `.md`, `.rst`, `.yml`

## License

GPLv3 - See LICENSE file

## Credits

Based on [Arsenal](https://github.com/Orange-Cyberdefense/arsenal) by Orange Cyberdefense.
Improvements and rewrite by lainonz.
