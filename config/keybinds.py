"""
Keybinding Configuration for Cheater Tool

This module loads keybindings from config/keybinds.yaml and converts them
to the appropriate key codes for use in the application.

The YAML format is much simpler and more user-friendly than editing this file directly.
Please edit config/keybinds.yaml instead.
"""

import curses
import yaml
import os


def parse_keybinding(key_string):
    """
    Parse a user-friendly key string into a key code.
    
    Supported formats:
    - "Ctrl, G" -> Ctrl+G (code 7)
    - "Alt, G" -> Alt+G (code varies by terminal)
    - "Shift, G" -> uppercase G (code 71)
    - "F2" -> Function key F2
    - "Tab" -> Tab key (code 9)
    - "';'" or ";" -> semicolon character
    - "'G'" or "G" -> uppercase G
    
    Args:
        key_string: String representation of the key
        
    Returns:
        Integer key code
    """
    key_string = key_string.strip()
    
    # Handle special case for Tab
    if key_string.lower() == "tab":
        return 9
    
    # Handle special case for Enter
    if key_string.lower() == "enter":
        return 10
    
    # Handle special case for Esc
    if key_string.lower() == "esc":
        return 27
    
    # Handle special case for Space
    if key_string.lower() == "space":
        return 32
    
    # Check if it's a modifier combo (Ctrl, Alt, Shift)
    if "," in key_string:
        parts = [p.strip() for p in key_string.split(",")]
        if len(parts) == 2:
            modifier, key = parts
            modifier = modifier.lower()
            key = key.upper() if len(key) == 1 else key
            
            if modifier == "ctrl":
                # Ctrl+A=1, Ctrl+B=2, ..., Ctrl+Z=26
                if len(key) == 1 and 'A' <= key <= 'Z':
                    return ord(key) - ord('A') + 1
            
            elif modifier == "alt":
                # Alt+key is typically ESC (27) followed by the key
                # But some terminals use key + 128
                # We'll use the +128 method as it's more compatible with single key check
                if len(key) == 1:
                    return ord(key.lower()) + 128
            
            elif modifier == "shift":
                # Shift+letter is just uppercase letter
                if len(key) == 1 and key.isalpha():
                    return ord(key.upper())
                # For other keys with shift, return the shifted character
                # This is terminal-dependent, so we just return the char if provided
                return ord(key)
    
    # Check if it's a function key (F1-F12)
    if key_string.upper().startswith("F") and len(key_string) <= 3:
        try:
            num = int(key_string[1:])
            if 1 <= num <= 12:
                return getattr(curses, f"KEY_F{num}")
        except (ValueError, AttributeError):
            pass
    
    # Check if it's a quoted character
    if key_string.startswith("'") and key_string.endswith("'") and len(key_string) >= 3:
        char = key_string[1:-1]
        if len(char) == 1:
            return ord(char)
        # Handle escape sequences
        if char == "\\n":
            return 10
        elif char == "\\t":
            return 9
        elif char == "\\\\":
            return ord("\\")
    
    # If it's a single character without quotes
    if len(key_string) == 1:
        return ord(key_string)
    
    # If nothing matches, raise error
    raise ValueError(f"Cannot parse keybinding: {key_string}")


def load_keybindings():
    """
    Load keybindings from config/keybinds.yaml
    
    Returns:
        Dictionary with parsed keybindings
    """
    # Get the directory where this file is located
    config_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.join(config_dir, "keybinds.yaml")
    
    # Load YAML file
    try:
        with open(yaml_path, 'r') as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        # If YAML file doesn't exist, use defaults
        print(f"Warning: {yaml_path} not found, using default keybindings")
        return get_default_keybindings()
    except Exception as e:
        print(f"Error loading keybindings: {e}")
        return get_default_keybindings()
    
    # Parse keybindings
    result = {
        'CheatsListKeys': {},
        'ArgsListKeys': {},
        'KeyLabels': {}
    }
    
    for section in ['CheatsListKeys', 'ArgsListKeys']:
        if section in config:
            for key, value in config[section].items():
                try:
                    result[section][key] = parse_keybinding(str(value))
                except Exception as e:
                    print(f"Warning: Error parsing {section}.{key} = {value}: {e}")
                    # Use a safe default
                    result[section][key] = 0
    
    # Copy labels directly
    if 'KeyLabels' in config:
        result['KeyLabels'] = config['KeyLabels']
    
    return result


def get_default_keybindings():
    """
    Get default keybindings if YAML file is not available
    """
    return {
        'CheatsListKeys': {
            'Global_Options': 7,  # Ctrl+G
            'Tab_Complete': 9,  # Tab
        },
        'ArgsListKeys': {
            'Tab': 9,  # Tab
            'File_Picker': 6,  # Ctrl+F
            'Auth_Choice': 15,  # Ctrl+O
            'Fuzzy_Finder': 20,  # Ctrl+T
        },
        'KeyLabels': {
            'Global_Options': "Ctrl+G: Global Options",
            'File_Picker': "Ctrl+F: File Picker",
            'Auth_Choice': "Ctrl+O: Auth choice",
        }
    }


# Load keybindings on module import
_keybindings = load_keybindings()


# Main CheatsList Menu Keybindings
class CheatsListKeys:
    """Keybindings for the main cheats list menu"""
    GLOBAL_OPTIONS = _keybindings['CheatsListKeys'].get('Global_Options', 7)
    TAB_COMPLETE = _keybindings['CheatsListKeys'].get('Tab_Complete', 9)


# ArgslistMenu Keybindings
class ArgsListKeys:
    """Keybindings for the arguments list menu"""
    TAB = _keybindings['ArgsListKeys'].get('Tab', 9)
    FILE_PICKER = _keybindings['ArgsListKeys'].get('File_Picker', 6)
    AUTH_CHOICE = _keybindings['ArgsListKeys'].get('Auth_Choice', 15)
    FUZZY_FINDER = _keybindings['ArgsListKeys'].get('Fuzzy_Finder', 20)


# Human-readable labels for UI display
class KeyLabels:
    """Human-readable labels for keybindings shown in the UI"""
    GLOBAL_OPTIONS = _keybindings['KeyLabels'].get('Global_Options', "Ctrl+G: Global Options")
    FILE_PICKER = _keybindings['KeyLabels'].get('File_Picker', "Ctrl+F: File Picker")
    AUTH_CHOICE = _keybindings['KeyLabels'].get('Auth_Choice', "Ctrl+O: Auth choice")


# Helper function to get key description
def get_key_name(key_code):
    """
    Get a human-readable name for a key code
    
    Args:
        key_code: The numeric key code
        
    Returns:
        String description of the key
    """
    # Control keys
    ctrl_keys = {
        1: "Ctrl+A", 2: "Ctrl+B", 3: "Ctrl+C", 4: "Ctrl+D", 5: "Ctrl+E",
        6: "Ctrl+F", 7: "Ctrl+G", 8: "Ctrl+H", 9: "Tab", 10: "Ctrl+J",
        11: "Ctrl+K", 12: "Ctrl+L", 13: "Enter", 14: "Ctrl+N", 15: "Ctrl+O",
        16: "Ctrl+P", 17: "Ctrl+Q", 18: "Ctrl+R", 19: "Ctrl+S", 20: "Ctrl+T",
        21: "Ctrl+U", 22: "Ctrl+V", 23: "Ctrl+W", 24: "Ctrl+X", 25: "Ctrl+Y", 26: "Ctrl+Z",
        27: "Esc", 32: "Space"
    }
    
    # Function keys
    function_keys = {
        curses.KEY_F1: "F1", curses.KEY_F2: "F2", curses.KEY_F3: "F3",
        curses.KEY_F4: "F4", curses.KEY_F5: "F5", curses.KEY_F6: "F6",
        curses.KEY_F7: "F7", curses.KEY_F8: "F8", curses.KEY_F9: "F9",
        curses.KEY_F10: "F10", curses.KEY_F11: "F11", curses.KEY_F12: "F12"
    }
    
    if key_code in ctrl_keys:
        return ctrl_keys[key_code]
    elif key_code in function_keys:
        return function_keys[key_code]
    elif 65 <= key_code <= 90:
        # Uppercase letters (Shift+Letter)
        return f"Shift+{chr(key_code)}"
    elif 97 <= key_code <= 122:
        # Lowercase letters
        return f"'{chr(key_code)}'"
    elif 33 <= key_code <= 126:
        # Other printable characters
        return f"'{chr(key_code)}'"
    elif key_code > 128:
        # Possibly Alt+key
        base_key = key_code - 128
        if 32 <= base_key <= 126:
            return f"Alt+{chr(base_key)}"
    
    return f"Key({key_code})"
