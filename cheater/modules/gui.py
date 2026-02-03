import time
import curses
import math
import json
import os
from curses import wrapper
from os.path import commonprefix, exists, isdir
from os import sep
import glob

# local
from . import config
from . import command


def draw_custom_border(window, y, x, height, width):
    """
    Draw a custom ASCII border on a window using +, -, | characters.
    Used for consistent styling across all UI elements.
    """
    try:
        win_height, win_width = window.getmaxyx()
        for row in range(y, min(y + height, win_height)):
            for col in range(x, min(x + width, win_width)):
                if row == y or row == y + height - 1:
                    # Top and bottom border
                    if col == x or col == x + width - 1:
                        window.addstr(row, col, "+")
                    else:
                        window.addstr(row, col, "-")
                elif col == x or col == x + width - 1:
                    # Left and right border
                    window.addstr(row, col, "|")
    except (curses.error, ValueError):
        # Silently fail if coordinates are invalid (terminal too small, etc)
        pass


class CheatslistMenu:
    globalcheats = []  # all cheats
    cheats = []  # cheats after search
    max_visible_cheats = 0
    input_buffer = ''
    position = 0
    page_position = 0

    xcursor = None
    x_init = None
    y_init = None

    def draw_prompt(self):
        """
        Create a prompt box
        at x : 0 / y : 5
        size 5 chars
        :return: the windows created
        """
        y, x = 5, 0
        ncols, nlines = 5, 1
        promptwin = curses.newwin(nlines, ncols, y, x)
        try:
            promptwin.addstr("  >", curses.color_pair(Gui.BASIC_COLOR))
        except:
            promptwin.addstr(">>>", curses.color_pair(Gui.BASIC_COLOR))
        promptwin.refresh()
        return promptwin

    def draw_infobox(self):
        """
        Draw the top infobox (4 lines / width from param)
        :return: the window created
        """
        y, x = 0, 0
        ncols, nlines = self.width, 4
        infowin = curses.newwin(nlines, ncols, y, x)
        selected_cheat = self.selected_cheat()
        if selected_cheat is not None:
            infowin.addstr(y + 1, x + 2, Gui.draw_string(selected_cheat.name, self.width - 3),
                           curses.color_pair(Gui.INFO_NAME_COLOR))
            # infowin.addstr(y + 2, x + 2, Gui.draw_string(selected_cheat.description.split('\n')[0], self.width - 3),
            #                curses.color_pair(Gui.INFO_DESC_COLOR))
            infowin.addstr(y + 2, x + 2, Gui.draw_string(selected_cheat.printable_command, self.width - 3),
                           curses.color_pair(Gui.INFO_CMD_COLOR))
        # Show current working directory in top-right corner
        cwd_text = f"CWD: {config.ORIGINAL_CWD}"
        if len(cwd_text) < self.width - 4:
            infowin.addstr(y, self.width - len(cwd_text) - 2, cwd_text, curses.color_pair(Gui.INFO_DESC_COLOR))
        # Draw custom border
        draw_custom_border(infowin, 0, 0, nlines, ncols)
        infowin.refresh()
        return infowin

    def draw_shortcut_hints(self):
        """
        Draw shortcut hints above the search bar
        :return: the window created
        """
        y, x = 4, 0
        ncols, nlines = self.width, 1
        hintwin = curses.newwin(nlines, ncols, y, x)
        hint_text = "Shift+G: Global Options"
        try:
            hintwin.addstr(hint_text, curses.color_pair(Gui.INFO_DESC_COLOR))
        except:
            pass  # Silently fail if text doesn't fit
        hintwin.refresh()
        return hintwin

    def draw_editbox(self):
        """
        Draw the edition box (in the right of the prompt box
        """
        y, x = 5, 6
        ncols, nlines = self.width - 5, 1
        editwin = curses.newwin(nlines, ncols, y, x)
        editwin.addstr(self.input_buffer, curses.color_pair(Gui.BASIC_COLOR))
        editwin.refresh()
        return editwin

    @staticmethod
    def draw_cheat(win, cheat, selected):
        """
        Draw a cheat line in the cheats list menu
        :param win:
        :param cheat:
        :param selected:
        """
        win_height, win_width = win.getmaxyx()
        prompt = '> '
        max_width = win_width - len(prompt) - len("\n")

        title = cheat.tags if cheat.tags != '' else cheat.str_title

        tags = cheat.get_tags()

        columns_list = ["title", "name", "description"]
        if Gui.with_tags:
            columns_list = ["tags"] + columns_list

        def get_col_size(max_width, ratio):
            """
            Return the column size from the given ratio

            :param max_width: The width maximal of the screen
            :param ratio: The ratio of the column
            """
            return math.floor((max_width * ratio) / 100)

        ratios = Gui.get_ratios_for_column(columns_list)

        columns = {"tags": {"width": get_col_size(max_width, ratios.get("tags", 0)),
                            "val": tags,
                            "color": Gui.COL4_COLOR_SELECT if selected else Gui.COL4_COLOR},
                   "title": {"width": get_col_size(max_width, ratios.get("title", 0)),
                             "val": cheat.str_title,
                             "color": Gui.COL3_COLOR_SELECT if selected else Gui.COL1_COLOR},
                   "name": {"width": get_col_size(max_width, ratios.get("name", 0)),
                            "val": cheat.name,
                            "color": Gui.COL2_COLOR_SELECT if selected else Gui.COL2_COLOR},
                   "description": {"width": get_col_size(max_width, ratios.get("description", 0)),
                                   "val": cheat.printable_command,
                                   "color": Gui.COL3_COLOR_SELECT if selected else Gui.COL3_COLOR}}

        if selected:
            win.addstr(prompt, curses.color_pair(Gui.CURSOR_COLOR_SELECT))
        else:
            win.addstr(' ' * len(prompt), curses.color_pair(Gui.BASIC_COLOR))

        for column_name in columns_list:
            win.addstr("{:{}s}".format(Gui.draw_string(columns[column_name]["val"],
                                                       columns[column_name]["width"]),
                                       columns[column_name]["width"]),
                       curses.color_pair(columns[column_name]["color"]))
        win.addstr("\n")

    def draw_cheatslistbox(self):
        """
        Draw the box to show the cheats list
        """
        y, x = 6, 0
        ncols, nlines = self.width, self.height - 6
        listwin = curses.newwin(nlines, ncols, y, x)

        visible_cheats = self.cheats[self.page_position:self.max_visible_cheats + self.page_position]
        counter = self.page_position

        for cheat in visible_cheats:
            self.draw_cheat(listwin, cheat, counter == self.position)
            counter += 1

        listwin.refresh()

    def draw_footbox(self, info):
        """
        Draw the footer (number infos)
        :param info: str info to draw
        """
        y, x = self.height - 1, 0
        ncols, nlines = self.width, 1

        # print nb cmd info (bottom left)
        nbinfowin = curses.newwin(nlines, ncols, y, x)
        nbinfowin.addstr(info, curses.color_pair(Gui.BASIC_COLOR))
        nbinfowin.refresh()

        # print cheatsheet filename (bottom right)
        if self.selected_cheat() is not None:
            cheat_file = self.selected_cheat().filename

            # protection in case screen to small or name too long        
            if len(cheat_file) > self.width - 16:
                cheat_file = cheat_file[0:self.width - 17] + ".."

            fileinfowin = curses.newwin(nlines, ncols, y, self.width - (len(cheat_file) + 3))
            fileinfowin.addstr(cheat_file, curses.color_pair(Gui.BASIC_COLOR))
            fileinfowin.refresh()

    def match(self, cheat):
        """
        Function called by the iterator to verify if the cheatsheet match the entered values
        :param cheat: cheat to check
        :return: boolean
        """
        # if search begin with '>' print only internal CMD
        if self.input_buffer.startswith('>') and not cheat.command.startswith('>'):
            return False

        for value in self.input_buffer.lower().split(' '):
            is_value_excluded = False
            if value.startswith("!") and len(value) > 1:
                value = value[1:]
                is_value_excluded = True

            if (value in cheat.str_title.lower()
                    or value in cheat.name.lower()
                    or value in cheat.tags.lower()
                    or value in "".join(cheat.command_tags.values()).lower()
                    or value in cheat.command.lower()):
                if is_value_excluded:
                    return False

            elif not is_value_excluded:
                return False
        return True

    def search(self):
        """
        Return the list of cheatsheet who match the searched term
        :return: list of cheatsheet to show
        """
        if self.input_buffer != '':
            list_cheat = list(filter(self.match, self.globalcheats))
        else:
            list_cheat = self.globalcheats
        return list_cheat

    def selected_cheat(self):
        """
        Return the selected cheat in the list
        :return: selected cheat
        """
        if len(self.cheats) == 0:
            return None
        return self.cheats[self.position % len(self.cheats)]

    def draw(self, stdscr):
        """
        Draw the main menu to select a cheatsheet
        :param stdscr: screen
        """
        self.height, self.width = stdscr.getmaxyx()
        self.max_visible_cheats = self.height - 7
        # create prompt windows
        self.draw_prompt()
        # create info windows
        self.draw_infobox()
        # create shortcut hints
        self.draw_shortcut_hints()
        # create cheatslist box
        self.draw_cheatslistbox()
        # draw footer
        info = "> %d / %d " % (self.position + 1, len(self.cheats))
        self.draw_footbox(info)
        # create edit windows
        self.draw_editbox()
        # init cursor position (if first draw)
        if self.x_init is None or self.y_init is None or self.xcursor is None:
            self.y_init, self.x_init = curses.getsyx()
            self.xcursor = self.x_init
        # set cursor as normal block cursor
        curses.curs_set(2)
        # set cursor position
        curses.setsyx(self.y_init, self.xcursor)
        curses.doupdate()

    def move_position(self, step):
        """
        :param step:
        """
        # SCROLL ?
        #
        # 0                                ---------      
        # 1                                |       |
        # 2                       ->   -----------------    <-- self.page_position
        # 3                      |     |   |       |   |       
        # 4 max_visible_cheats = |     |   |       |   |
        # 5                      |     |  >|xxxxxxx|   |    <-- self.position      
        # 6                      |     |   |       |   |       
        # 7                       ->   -----------------    <-- self.page_position+max_visible_cheats
        # 8                                |       |
        # 9                                ---------        <-- len(self.cheats)
        self.position += step

        # clean position
        if self.position < 0: self.position = 0
        if self.position >= len(self.cheats) - 1: self.position = len(self.cheats) - 1

        # move page view UP
        if self.page_position > self.position:
            self.page_position -= (self.page_position - self.position)

            # move page view DOWN
        if self.position >= (self.page_position + self.max_visible_cheats):
            self.page_position += 1 + (self.position - (self.page_position + self.max_visible_cheats))

    def move_page(self, step):
        """
        :param step:
        """
        # only move if it is possible
        if len(self.cheats) > self.max_visible_cheats:
            new_pos = self.page_position + step * self.max_visible_cheats
            # clean position
            if new_pos >= (len(self.cheats) + 1 - self.max_visible_cheats):
                self.position = len(self.cheats) - 1
                self.page_position = len(self.cheats) - self.max_visible_cheats
            elif new_pos < 0:
                self.position = self.page_position = 0
            else:
                self.position = self.page_position = new_pos

    def check_move_cursor(self, n):
        return self.x_init <= (self.xcursor + n) < self.x_init + len(self.input_buffer) + 1

    def run(self, stdscr):
        """
        Cheats selection menu processing..
        :param stdscr: screen
        """
        # init
        Gui.init_colors()
        stdscr.clear()
        self.height, self.width = stdscr.getmaxyx()
        self.max_visible_cheats = self.height - 7
        self.cursorpos = 0

        while True:
            stdscr.refresh()
            self.cheats = self.search()
            self.draw(stdscr)
            c = stdscr.getch()
            
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                # Process selected command (if not empty)
                if self.selected_cheat() is not None:
                    Gui.cmd = command.Command(self.selected_cheat(), Gui.cheaterGlobalVars)
                    # check if arguments are needed
                    # if len(Gui.cmd.args) != 0:
                    # args needed -> ask
                    args_menu = ArgslistMenu(self)
                    args_menu.run(stdscr)
                    stdscr.refresh()
                    break
            elif c == curses.KEY_F10 or c == 27:
                Gui.cmd = None
                break  # Exit the while loop
            # In normal mode, handle navigation and search input
            elif c == curses.KEY_UP:
                # Move UP in cheats list
                self.move_position(-1)
            elif c == curses.KEY_DOWN:
                # Move DOWN in cheats list
                self.move_position(1)
            elif c == 339 or c == curses.KEY_PPAGE:
                # Page UP
                self.move_page(-1)
            elif c == 338 or c == curses.KEY_NPAGE:
                # Page DOWN
                self.move_page(1)
            elif c == ord('G'):
                # Shift+G - Open global options
                try:
                    global_menu = GlobalOptionsMenu(self)
                    global_menu.run(stdscr)
                    # Redraw main screen after menu closes
                    stdscr.clear()
                    stdscr.refresh()
                except Exception as e:
                    # Show error if menu fails
                    stdscr.clear()
                    stdscr.addstr(0, 0, f"Error opening Global Options: {str(e)}")
                    stdscr.addstr(1, 0, "Press any key to continue...")
                    stdscr.refresh()
                    stdscr.getch()
                    stdscr.clear()
            elif c == 9:
                # TAB cmd auto complete
                if self.input_buffer != "":
                    predictions = []
                    for cheat in self.cheats:
                        if cheat.command.startswith(self.input_buffer):
                            predictions.append(cheat.command)
                    if len(predictions) != 0:
                        self.input_buffer = commonprefix(predictions)
                        self.xcursor = self.x_init + len(self.input_buffer)
                        self.position = 0
                        self.page_position = 0
            elif c == curses.KEY_BACKSPACE or c == 127 or c == 8:
                # Delete character
                if self.check_move_cursor(-1):
                    i = self.xcursor - self.x_init - 1
                    self.input_buffer = self.input_buffer[:i] + self.input_buffer[i + 1:]
                    self.xcursor -= 1
                    # new search -> reset position
                    self.position = 0
                    self.page_position = 0
            elif c == curses.KEY_DC or c == 127:
                # Delete character at cursor
                if self.check_move_cursor(1):
                    i = self.xcursor - self.x_init - 1
                    self.input_buffer = self.input_buffer[:i + 1] + self.input_buffer[i + 2:]
                    # new search -> reset position
                    self.position = 0
                    self.page_position = 0
            elif c == curses.KEY_LEFT:
                # Move cursor LEFT in search box
                if self.check_move_cursor(-1): 
                    self.xcursor -= 1
            elif c == curses.KEY_RIGHT:
                # Move cursor RIGHT in search box
                if self.check_move_cursor(1): 
                    self.xcursor += 1
            elif c == curses.KEY_BEG or c == curses.KEY_HOME:
                # Move cursor to the BEGIN of search box
                self.xcursor = self.x_init
            elif c == curses.KEY_END:
                # Move cursor to the END of search box
                self.xcursor = self.x_init + len(self.input_buffer)
            elif 32 <= c < 127:
                # Type character in search box
                i = self.xcursor - self.x_init
                self.input_buffer = self.input_buffer[:i] + chr(c) + self.input_buffer[i:]
                self.xcursor += 1
                # new search -> reset position
                self.position = 0
                self.page_position = 0


class FilePicker:
    """File picker menu for selecting files to append to arguments"""
    
    def __init__(self, initial_path=None):
        self.current_dir = initial_path or config.ORIGINAL_CWD
        self.files = []
        self.dirs = []
        self.current_position = 0
        self.selected_file = None
        self.load_directory()
    
    def load_directory(self):
        """Load files and directories from current directory"""
        try:
            self.files = []
            self.dirs = []
            
            # Add parent directory option (..)
            if self.current_dir != '/':
                self.dirs.append('..')
            
            # List all items in directory
            for item in sorted(os.listdir(self.current_dir)):
                full_path = os.path.join(self.current_dir, item)
                if os.path.isdir(full_path):
                    self.dirs.append(item)
                else:
                    self.files.append(item)
            
            # Reset position when loading new directory
            self.current_position = 0
        except PermissionError:
            self.files = []
            self.dirs = []
    
    def get_items(self):
        """Get all items (dirs first, then files)"""
        return self.dirs + self.files
    
    def draw(self, stdscr):
        """Draw the file picker menu"""
        try:
            height, width = stdscr.getmaxyx()
            stdscr.clear()
            
            # Calculate dimensions
            box_width = min(80, width - 4)
            max_items_visible = min(20, height - 8)
            items = self.get_items()
            box_height = min(len(items) + 6, height - 4)
            
            start_y = max(0, (height - box_height) // 2)
            start_x = max(0, (width - box_width) // 2)
            
            # Draw border using custom function
            draw_custom_border(stdscr, start_y, start_x, box_height, box_width)
            
            # Title
            title = " File Picker (@) "
            title_x = start_x + max(1, (box_width - len(title)) // 2)
            stdscr.addstr(start_y, title_x, title, curses.A_BOLD)
            
            # Current directory
            dir_text = f" {self.current_dir} "
            if len(dir_text) < box_width - 4:
                stdscr.addstr(start_y + 1, start_x + 2, dir_text[:box_width - 4])
            
            # Instructions
            instructions = "j/k: Navigate | Enter: Select/Open | Esc: Cancel"
            if len(instructions) < box_width - 4:
                stdscr.addstr(start_y + box_height - 2, start_x + 2, instructions[:box_width - 4])
            
            # Draw file list
            items = self.get_items()
            start_item = max(0, self.current_position - max_items_visible // 2)
            
            for idx, item in enumerate(items[start_item:start_item + max_items_visible]):
                y = start_y + 3 + idx
                actual_idx = start_item + idx
                
                if y >= start_y + box_height - 2:
                    break
                
                # Check if this is a directory
                is_dir = actual_idx < len(self.dirs)
                item_display = f"  {item}/" if is_dir else f"  {item}"
                
                # Truncate if too long
                if len(item_display) > box_width - 6:
                    item_display = item_display[:box_width - 9] + "..."
                
                if actual_idx == self.current_position:
                    # Highlight current selection
                    stdscr.addstr(y, start_x + 2, item_display, curses.A_REVERSE)
                else:
                    # Different color for directories
                    if is_dir:
                        stdscr.addstr(y, start_x + 2, item_display, curses.color_pair(Gui.INFO_NAME_COLOR))
                    else:
                        stdscr.addstr(y, start_x + 2, item_display, curses.color_pair(Gui.BASIC_COLOR))
            
            # Show counter
            counter = f"{self.current_position + 1}/{len(items)}" if items else "0/0"
            counter_x = start_x + box_width - len(counter) - 3
            if counter_x > start_x + 2:
                stdscr.addstr(start_y + 2, counter_x, counter)
            
            stdscr.refresh()
            
        except Exception as e:
            stdscr.clear()
            stdscr.addstr(0, 0, f"Error in FilePicker: {str(e)}")
            stdscr.addstr(1, 0, "Press any key...")
            stdscr.refresh()
            stdscr.getch()
    
    def run(self, stdscr):
        """Run the file picker"""
        Gui.init_colors()
        
        while True:
            self.draw(stdscr)
            c = stdscr.getch()
            
            items = self.get_items()
            
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                # Select or open
                if self.current_position < len(items):
                    selected = items[self.current_position]
                    
                    if self.current_position < len(self.dirs):
                        # It's a directory
                        if selected == '..':
                            # Go to parent directory
                            self.current_dir = os.path.dirname(self.current_dir.rstrip('/'))
                        else:
                            # Go to subdirectory
                            self.current_dir = os.path.join(self.current_dir, selected)
                        self.load_directory()
                    else:
                        # It's a file - return relative path from ORIGINAL_CWD
                        self.selected_file = os.path.relpath(
                            os.path.join(self.current_dir, selected),
                            config.ORIGINAL_CWD
                        )
                        break
                else:
                    break
            
            elif c == 27:  # Esc
                break
            
            elif c == curses.KEY_UP or c == ord('k'):
                # Move up
                if self.current_position > 0:
                    self.current_position -= 1
            
            elif c == curses.KEY_DOWN or c == ord('j'):
                # Move down
                if self.current_position < len(items) - 1:
                    self.current_position += 1
            
            elif c == curses.KEY_HOME:
                # Jump to start
                self.current_position = 0
            
            elif c == curses.KEY_END:
                # Jump to end
                if items:
                    self.current_position = len(items) - 1


class GlobalOptionsMenu:
    """Global options menu for setting common variables like DC_IP, USERNAME, etc."""
    
    common_vars = [
        "IP",
        "Username", 
        "Password",
        "Domain",
        "LHOST",
        "LPORT",
        "RHOST",
        "RPORT",
    ]
    
    current_field = 0
    values = {}
    xcursor = None
    x_init = None
    y_init = None
    
    def __init__(self, prev):
        self.previous_menu = prev
        # Load existing values
        if exists(config.SAVEVARFILE):
            with open(config.SAVEVARFILE, 'r') as f:
                self.values = json.load(f)
        # Initialize missing fields
        for var in self.common_vars:
            if var not in self.values:
                self.values[var] = ""
    
    def draw(self, stdscr):
        """Draw the global options menu"""
        try:
            height, width = stdscr.getmaxyx()
            stdscr.clear()
            
            # Calculate dimensions
            box_width = min(70, width - 4)
            box_height = min(len(self.common_vars) + 8, height - 4)
            start_y = max(0, (height - box_height) // 2)
            start_x = max(0, (width - box_width) // 2)
            
            # Draw border using custom function
            draw_custom_border(stdscr, start_y, start_x, box_height, box_width)
            
            # Title
            title = " Global Options (Shift+G) "
            title_x = start_x + max(1, (box_width - len(title)) // 2)
            stdscr.addstr(start_y, title_x, title, curses.A_BOLD)
            
            # Instructions
            instructions = "Tab/Down: Navigate | Enter: Save | Esc: Cancel"
            if len(instructions) < box_width - 4:
                stdscr.addstr(start_y + box_height - 2, start_x + 2, instructions)
            
            # Draw fields
            for idx, var in enumerate(self.common_vars):
                y = start_y + 2 + idx
                if y >= start_y + box_height - 3:
                    break
                # Variable name
                var_label = f"{var}:"
                stdscr.addstr(y, start_x + 2, var_label.ljust(15))
                
                # Value field
                value = self.values.get(var, "")
                max_value_len = box_width - 20
                display_value = value[:max_value_len] if len(value) <= max_value_len else value[:max_value_len]
                
                if idx == self.current_field:
                    # Highlighted field - inverse video
                    field_text = display_value.ljust(max_value_len)
                    stdscr.addstr(y, start_x + 18, field_text, curses.A_REVERSE)
                else:
                    if display_value:
                        stdscr.addstr(y, start_x + 18, display_value)
            
            # Set cursor position for current field
            cursor_y = start_y + 2 + self.current_field
            cursor_x = start_x + 18
            
            if self.xcursor is None or self.x_init is None:
                current_var = self.common_vars[self.current_field]
                self.x_init = cursor_x
                self.y_init = cursor_y
                self.xcursor = cursor_x + len(self.values.get(current_var, ""))
            
            # Enable cursor and set position
            curses.curs_set(1)
            stdscr.move(cursor_y, self.xcursor)
            stdscr.refresh()
            
        except Exception as e:
            # Debug: show error
            stdscr.clear()
            stdscr.addstr(0, 0, f"Error in draw: {str(e)}")
            stdscr.addstr(1, 0, f"Terminal size: {height}x{width}")
            stdscr.addstr(2, 0, f"Box size: {box_height}x{box_width}")
            stdscr.addstr(3, 0, f"Position: ({start_y},{start_x})")
            stdscr.addstr(4, 0, "Press any key...")
            stdscr.refresh()
            stdscr.getch()
    
    def save_values(self):
        """Save values to config file"""
        # Remove empty values
        filtered_values = {k: v for k, v in self.values.items() if v}
        with open(config.SAVEVARFILE, 'w') as f:
            json.dump(filtered_values, f, indent=2)
        # Update Gui global vars
        Gui.cheaterGlobalVars = filtered_values
    
    def run(self, stdscr):
        """Run the global options menu"""
        Gui.init_colors()
        
        while True:
            self.draw(stdscr)
            c = stdscr.getch()
            
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                # Save and close
                self.save_values()
                break
            elif c == 27:  # Esc
                # Cancel without saving
                break
            elif c == 9 or c == curses.KEY_DOWN:  # Tab or Down
                # Next field
                self.current_field = (self.current_field + 1) % len(self.common_vars)
                self.xcursor = None
                self.x_init = None
                self.y_init = None
            elif c == curses.KEY_UP:
                # Previous field
                self.current_field = (self.current_field - 1) % len(self.common_vars)
                self.xcursor = None
                self.x_init = None
                self.y_init = None
            elif c == curses.KEY_BACKSPACE or c == 127 or c == 8:
                # Delete character
                var = self.common_vars[self.current_field]
                value = self.values.get(var, "")
                if value and self.xcursor and self.x_init and self.xcursor > self.x_init:
                    i = self.xcursor - self.x_init - 1
                    self.values[var] = value[:i] + value[i + 1:]
                    self.xcursor -= 1
            elif c == curses.KEY_DC:  # Delete key
                # Delete character at cursor
                var = self.common_vars[self.current_field]
                value = self.values.get(var, "")
                if self.xcursor and self.x_init:
                    i = self.xcursor - self.x_init
                    if i < len(value):
                        self.values[var] = value[:i] + value[i + 1:]
            elif c == curses.KEY_LEFT:
                # Move cursor left
                if self.xcursor and self.x_init and self.xcursor > self.x_init:
                    self.xcursor -= 1
            elif c == curses.KEY_RIGHT:
                # Move cursor right
                var = self.common_vars[self.current_field]
                value = self.values.get(var, "")
                if self.xcursor and self.x_init and self.xcursor < self.x_init + len(value):
                    self.xcursor += 1
            elif c == curses.KEY_HOME:
                # Move to start
                if self.x_init:
                    self.xcursor = self.x_init
            elif c == curses.KEY_END:
                # Move to end
                var = self.common_vars[self.current_field]
                value = self.values.get(var, "")
                if self.x_init:
                    self.xcursor = self.x_init + len(value)
            elif 32 <= c < 127:
                # Type character
                var = self.common_vars[self.current_field]
                value = self.values.get(var, "")
                if self.xcursor and self.x_init:
                    i = self.xcursor - self.x_init
                    self.values[var] = value[:i] + chr(c) + value[i:]
                    self.xcursor += 1
                else:
                    # First character being typed
                    self.values[var] = value + chr(c)


class ArgslistMenu:
    current_arg = 0
    max_preview_size = 0
    prev_lastline_len = 0

    # init arg box margins
    AB_TOP = 0
    AB_SIDE = 0

    xcursor = None
    x_init = None
    y_init = None

    def __init__(self, prev):
        self.previous_menu = prev

    def get_nb_preview_new_lines(self):
        """
        Returns the number of preview lines
        :return:
        """
        next_arg = 0
        nblines = 0
        multiline = '\n' in Gui.cmd.cmdline
        firstline = True
        parts = Gui.cmd.get_command_parts()
        nb_args_todo = len(parts) - 1
        # in case of multiline cmd process each line separately
        # for each line we have to count each char and deduce the
        # number of lines needed to print it
        for line in Gui.cmd.cmdline.split('\n'):
            nbchar = 0

            # for all lines except the first one we have ' >' in addition
            if multiline and (not firstline):
                nbchar = 2
            else:
                firstline = False

            # extract len of args in the current line
            i = 0
            for arg_name, arg_val in Gui.cmd.args:
                if i == next_arg and nb_args_todo > 0:
                    if arg_val != "":
                        # use value len if not empty
                        nbchar += len(arg_val)
                    else:
                        # else use name len + 2 for '<' and '>'
                        nbchar += (len(arg_name) + 2)
                    next_arg += 1
                    nb_args_todo -= 1
                i += 1

            # len of the cmd body
            for p in parts:
                nbchar += len(p)

            nblines += 1 + ((nbchar - 1) // self.max_preview_size)

        return nblines - 1

    def next_arg(self):
        """
        Select the next argument in the list, skip duplicates
        """
        # reset cursor position
        self.xcursor = None
        self.x_init = None
        self.y_init = None
        # change selected arg and skip duplicates
        start = self.current_arg
        while True:
            if self.current_arg < Gui.cmd.nb_args - 1:
                self.current_arg += 1
            else:
                self.current_arg = 0
            # Check if this arg name was already seen before this position
            arg_name = Gui.cmd.args[self.current_arg][0]
            is_duplicate = any(Gui.cmd.args[i][0] == arg_name for i in range(self.current_arg))
            if not is_duplicate or self.current_arg == start:
                break

    def previous_arg(self):
        """
        Select the previous argument in the list, skip duplicates
        """
        # reset cursor position
        self.xcursor = None
        self.x_init = None
        self.y_init = None
        # change selected arg and skip duplicates
        start = self.current_arg
        while True:
            if self.current_arg > 0:
                self.current_arg -= 1
            else:
                self.current_arg = Gui.cmd.nb_args - 1
            # Check if this arg name was already seen before this position
            arg_name = Gui.cmd.args[self.current_arg][0]
            is_duplicate = any(Gui.cmd.args[i][0] == arg_name for i in range(self.current_arg))
            if not is_duplicate or self.current_arg == start:
                break

    def draw_preview_part(self, win, text, color):
        """
        Print a part of the preview cmd line
        And start a new line if the last line of the preview is too long
        :param win: window
        :param text: part of the preview to draw
        :param color: color used to draw the text
        """
        for c in text:
            if c == "\n":
                # multi line cmd -> new line
                self.prev_lastline_len = 2
                win.addstr("\n    > ", color)
            elif self.prev_lastline_len < self.max_preview_size:
                # size ok -> print the char
                self.prev_lastline_len += 1
                win.addstr(c, color)
            else:
                # last line too long -> new line
                self.prev_lastline_len = 1
                win.addstr("\n    " + c, color)

    def draw_selected_arg(self, y_pos):
        """
        Draw the selected argument line in the argument menu
        """
        # Calculate display position based on unique args only
        unique_position = 0
        for i in range(self.current_arg):
            arg_name = Gui.cmd.args[i][0]
            # Check if this is the first occurrence of this arg name
            if not any(Gui.cmd.args[j][0] == arg_name for j in range(i)):
                unique_position += 1
        
        y, x = self.AB_TOP + y_pos + unique_position, self.AB_SIDE + 1
        ncols, nlines = self.width - 2 * (self.AB_SIDE + 1), 1
        arg = Gui.cmd.args[self.current_arg]
        max_size = self.max_preview_size - 4 - len(arg[0])
        selectedargline = curses.newwin(nlines, ncols, y, x)
        selectedargline.addstr("   > ", curses.color_pair(Gui.BASIC_COLOR))
        selectedargline.addstr(arg[0], curses.color_pair(Gui.ARG_NAME_COLOR))
        selectedargline.addstr(" = " + Gui.draw_string(arg[1], max_size), curses.color_pair(Gui.BASIC_COLOR))
        selectedargline.refresh()

    def draw_args_list(self, y_pos):
        """
        Draw the asked arguments list in the argument menu (only unique args)
        """
        # Get unique args (skip duplicates)
        unique_args = []
        seen_names = set()
        for arg in Gui.cmd.args:
            if arg[0] not in seen_names:
                unique_args.append(arg)
                seen_names.add(arg[0])
        
        y, x = self.AB_TOP + y_pos, self.AB_SIDE + 1
        ncols, nlines = self.width - 2 * (self.AB_SIDE + 1), len(unique_args) + 1
        argwin = curses.newwin(nlines, ncols, y, x)
        for arg in unique_args:
            max_size = self.max_preview_size + 4
            argline = Gui.draw_string("     {} = {}".format(*arg), max_size) + "\n"
            argwin.addstr(argline, curses.color_pair(Gui.BASIC_COLOR))
        argwin.refresh()

    def draw_desc_preview(self, argprev, p_x, p_y, description_lines):
        """
        Draw the descriptions_line preview in the preview windows (argprev)
        """
        # draw description
        if len(description_lines) > 0:
            argprev.addstr(p_y, p_x, "-----", curses.color_pair(Gui.BASIC_COLOR))
            p_y += 1
            for description_line in description_lines:
                argprev.addstr(p_y, p_x, description_line, curses.color_pair(Gui.BASIC_COLOR))
                p_y += 1
            p_y += 1
            argprev.refresh()
        return p_y

    def draw_cmd_preview(self, argprev, p_x, p_y=1):
        """
        Draw the cmd preview in the argument menu
        Also used to draw the borders of this menu
        """
        cmdparts = Gui.cmd.get_command_parts()

        # draw command
        argprev.addstr(p_y, p_x, "$ ", curses.color_pair(Gui.BASIC_COLOR))

        # draw preview cmdline
        for i in range(len(cmdparts) + Gui.cmd.nb_args):
            if i % 2 == 0:
                # draw cmd parts in white
                self.draw_preview_part(argprev, cmdparts[i // 2], curses.color_pair(Gui.BASIC_COLOR))
            else:
                # get argument value
                if Gui.cmd.args[(i - 1) // 2][1] == "":
                    # if arg empty use its name
                    arg = '<' + Gui.cmd.args[(i - 1) // 2][0] + '>'
                else:
                    # else its value
                    arg = Gui.cmd.args[(i - 1) // 2][1]

                # draw argument
                if (i - 1) // 2 == self.current_arg:
                    # if arg is selected print in blue
                    self.draw_preview_part(argprev, arg, curses.color_pair(Gui.ARG_NAME_COLOR))
                else:
                    # else in white
                    self.draw_preview_part(argprev, arg, curses.color_pair(Gui.BASIC_COLOR))
        
        # Draw custom border
        height, width = argprev.getmaxyx()
        draw_custom_border(argprev, 0, 0, height, width)
        argprev.refresh()

    def draw(self, stdscr):
        """
        Draw the arguments menu to ask them
        :param stdscr: screen
        """
        # init vars and set margins values
        self.height, self.width = stdscr.getmaxyx()
        self.AB_SIDE = 5
        padding_text_border = 3
        self.max_preview_size = self.width - (2 * self.AB_SIDE) - (2 * padding_text_border)

        # draw background cheatslist menu (clean resize)
        self.previous_menu.draw(stdscr)

        # draw argslist menu popup
        self.prev_lastline_len = 0
        nbpreviewnewlines = self.get_nb_preview_new_lines()
        # if Gui.cmd.nb_args != 0:
        #     nbpreviewnewlines = self.get_nb_preview_new_lines()
        # else:
        #     nbpreviewnewlines = 0

        # -------------- border
        # cmd
        # nbpreviewnewlines
        # .............. args margin top
        # args
        # ------
        # description
        # .............  description margin
        # ---------- border

        # width - preview
        ncols = self.width - 2 * self.AB_SIDE

        # prepare showed description
        description_lines = Gui.cmd.get_description_cut_by_size(ncols - (padding_text_border * 2))

        # Count unique args only for display
        unique_arg_count = len(set(arg[0] for arg in Gui.cmd.args))

        border_height = 1
        cmd_height = 2 + nbpreviewnewlines
        args_height = (2 + unique_arg_count) if (unique_arg_count > 0) else 0
        desc_height = (len(description_lines) + 1 + 1) if (len(description_lines) > 0) else 0

        cmd_pos = 2
        args_pos = border_height + cmd_height + 1
        desc_pos = args_pos + args_height - 1

        nlines = border_height * 2 + cmd_height + args_height + desc_height
        if nlines > self.height:
            nlines = self.height

        self.AB_TOP = (self.height - nlines) // 2
        y, x = self.AB_TOP, self.AB_SIDE

        try:
            argprev = curses.newwin(nlines, ncols, y, x)

            # draw command
            self.draw_cmd_preview(argprev, padding_text_border, cmd_pos)

            # draw description
            self.draw_desc_preview(argprev, padding_text_border, desc_pos, description_lines)
            
            # Show @ shortcut info and CWD on the top inside row (reserved)
            has_choices = bool(getattr(Gui.cmd, 'arg_choices', {}))
            file_picker_info = "@: File Picker"
            if has_choices:
                file_picker_info += " | Shift+O: Auth choice"
            cwd_info = f"CWD: {config.ORIGINAL_CWD}"
            info_row = 1
            info_x = padding_text_border
            try:
                if 1 <= info_row < nlines - 1:
                    argprev.addstr(info_row, info_x, file_picker_info, curses.color_pair(Gui.INFO_DESC_COLOR))
                    if len(cwd_info) < ncols - 4:
                        argprev.addstr(info_row, ncols - len(cwd_info) - 2, cwd_info,
                                       curses.color_pair(Gui.INFO_DESC_COLOR))
                argprev.refresh()
            except:
                pass  # Ignore if it doesn't fit

            if len(Gui.cmd.args) > 0:
                self.draw_args_list(args_pos)
                self.draw_selected_arg(args_pos)
                # init cursor position (if first draw)
                if self.x_init is None or self.y_init is None or self.xcursor is None:
                    self.y_init, self.x_init = curses.getsyx()
                    # prefill compatibility
                    self.x_init -= len(Gui.cmd.args[self.current_arg][1])
                    self.xcursor = self.x_init + len(Gui.cmd.args[self.current_arg][1])
                # set cursor position
                curses.setsyx(self.y_init, self.xcursor)
                curses.doupdate()
        except curses.error:
            # catch all curses error to not end with an exception in case of size error
            pass

    def check_move_cursor(self, n):
        if Gui.cmd.nb_args == 0:
            return False
        return self.x_init <= (self.xcursor + n) < self.x_init + len(Gui.cmd.args[self.current_arg][1]) + 1

    def autocomplete_arg(self):
        """
        Autocomplete the current argument
        """
        # current argument value
        argument = Gui.cmd.args[self.current_arg][1]
        
        # Save current directory and switch to original working directory
        current_dir = os.getcwd()
        matches = []
        autocompleted_argument = ""
        
        try:
            os.chdir(config.ORIGINAL_CWD)
            # look for all files that match the argument in the working directory
            matches = glob.glob('{}*'.format(argument))
            
            if not matches:
                return False

            # init the autocompleted argument
            # autocompleted argument is the longest start common string in all matches
            for i in range(len(min(matches))):
                if not all(min(matches)[:i + 1] == match[:i + 1] for match in matches):
                    break
                autocompleted_argument = min(matches)[:i + 1]

            # add a "/" at the end of the autocompleted argument if it is a directory
            # Check while still in ORIGINAL_CWD
            if isdir(autocompleted_argument) and autocompleted_argument[-1] != sep:
                autocompleted_argument = autocompleted_argument + sep
        finally:
            # Always restore the directory
            os.chdir(current_dir)

        # autocomplete the argument 
        Gui.cmd.args[self.current_arg][1] = autocompleted_argument
        # Sync to duplicates
        self._sync_duplicate_args(self.current_arg, autocompleted_argument)
        # update cursor position
        self.xcursor = self.x_init + len(autocompleted_argument)

    def _sync_duplicate_args(self, arg_index, new_value):
        """
        Sync value to all duplicate arguments with same name
        """
        arg_name = Gui.cmd.args[arg_index][0]
        for i, arg in enumerate(Gui.cmd.args):
            if arg[0] == arg_name:
                Gui.cmd.args[i][1] = new_value

    def _find_arg_index(self, arg_name):
        for i, arg in enumerate(Gui.cmd.args):
            if arg[0] == arg_name:
                return i
        return None

    def open_choice_popup(self, stdscr, arg_index=None):
        """
        Open a popup to select from predefined choices for a given argument
        """
        if arg_index is None:
            arg_index = self.current_arg
        choices = getattr(Gui.cmd, 'arg_choices', {}).get(arg_index)
        if not choices:
            return False

        labels = getattr(Gui.cmd, 'arg_choice_labels', {}).get(arg_index)
        display_items = labels if labels and len(labels) == len(choices) else choices

        height, width = stdscr.getmaxyx()
        max_item_len = max(len(item) for item in display_items)
        box_width = min(max_item_len + 10, width - 2)
        box_height = min(len(display_items) + 4, height - 2)
        start_y = (height - box_height) // 2
        start_x = (width - box_width) // 2

        win = curses.newwin(box_height, box_width, start_y, start_x)
        win.keypad(True)

        selected = 0
        current_val = Gui.cmd.args[arg_index][1]
        if current_val in choices:
            selected = choices.index(current_val)

        while True:
            win.clear()
            draw_custom_border(win, 0, 0, box_height, box_width)
            title = "Select Authentication"
            win.addstr(1, 2, Gui.draw_string(title, box_width - 4), curses.color_pair(Gui.INFO_NAME_COLOR))

            for i, item in enumerate(display_items[:box_height - 4]):
                prefix = "> " if i == selected else "  "
                color = Gui.COL4_COLOR_SELECT if i == selected else Gui.BASIC_COLOR
                win.addstr(2 + i, 2, Gui.draw_string(prefix + item, box_width - 4), curses.color_pair(color))

            win.refresh()
            c = win.getch()
            if c in (curses.KEY_ENTER, 10, 13):
                Gui.cmd.args[arg_index][1] = choices[selected]
                # Sync to all duplicate args
                self._sync_duplicate_args(arg_index, choices[selected])
                if self.x_init is not None:
                    self.xcursor = self.x_init + len(Gui.cmd.args[self.current_arg][1])
                return True
            elif c in (27, curses.KEY_F10):
                return False
            elif c == curses.KEY_UP:
                selected = (selected - 1) % len(display_items)
            elif c == curses.KEY_DOWN:
                selected = (selected + 1) % len(display_items)

    def run(self, stdscr):
        """
        Arguments selection menu processing..
        :param stdscr: screen
        """
        # init
        Gui.init_colors()
        stdscr.clear()
        while True:
            stdscr.refresh()
            self.draw(stdscr)
            c = stdscr.getch()
            if c == curses.KEY_ENTER or c == 10 or c == 13:
                # try to build the cmd
                # if cmd build is ok -> exit
                # else continue in args menu
                if Gui.cmd.build():
                    break
            elif c == curses.KEY_F10 or c == 27:
                # exit args_menu -> return to cheatslist_menu
                self.previous_menu.run(stdscr)
                stdscr.refresh()
                break
            elif c == curses.KEY_DOWN:
                self.next_arg()
            elif c == curses.KEY_UP:
                self.previous_arg()
            elif c == 9:
                if Gui.cmd.args:
                    # autocomplete the current argument
                    if Gui.cmd.args[self.current_arg][1]:
                        self.autocomplete_arg()
                    # go to the next argument
                    else:
                        self.next_arg()
            elif c == ord('@'):
                # @: Open file picker
                if Gui.cmd.args:
                    try:
                        file_picker = FilePicker(config.ORIGINAL_CWD)
                        file_picker.run(stdscr)
                        if file_picker.selected_file:
                            # Append selected file to current argument
                            current_value = Gui.cmd.args[self.current_arg][1]
                            if current_value and not current_value.endswith(' '):
                                new_val = current_value + ' ' + file_picker.selected_file
                            else:
                                new_val = current_value + file_picker.selected_file
                            self._sync_duplicate_args(self.current_arg, new_val)
                            # Update cursor position
                            self.xcursor = self.x_init + len(Gui.cmd.args[self.current_arg][1])
                        # Redraw args menu
                        stdscr.clear()
                    except Exception as e:
                        pass  # Silently fail if file picker has issues
            elif c == ord('O'):
                # Shift+O: Open choices popup if defined
                if Gui.cmd.args:
                    creds_index = self._find_arg_index("Creds_Options")
                    if creds_index is None:
                        self.open_choice_popup(stdscr)
                    else:
                        self.open_choice_popup(stdscr, creds_index)
            elif c == 20:
                try:
                    from pyfzf.pyfzf import FzfPrompt
                    files = []
                    for fuzz_dir in config.FUZZING_DIRS:
                        files += glob.glob(fuzz_dir, recursive=True)
                    fzf = FzfPrompt().prompt(files)
                    # autocomplete the argument and sync
                    self._sync_duplicate_args(self.current_arg, fzf[0])
                    # update cursor position
                    self.xcursor = self.x_init + len(fzf[0])
                except ImportError:
                    pass
            elif c == curses.KEY_BACKSPACE or c == 127 or c == 8:
                if self.check_move_cursor(-1):
                    i = self.xcursor - self.x_init - 1
                    new_val = Gui.cmd.args[self.current_arg][1][:i] + \
                              Gui.cmd.args[self.current_arg][1][i + 1:]
                    self._sync_duplicate_args(self.current_arg, new_val)
                    self.xcursor -= 1
            elif c == curses.KEY_DC or c == 127:
                # DELETE key
                if self.check_move_cursor(1):
                    i = self.xcursor - self.x_init - 1
                    new_val = Gui.cmd.args[self.current_arg][1][:i + 1] + \
                              Gui.cmd.args[self.current_arg][1][i + 2:]
                    self._sync_duplicate_args(self.current_arg, new_val)
            elif c == curses.KEY_LEFT:
                # Move cursor LEFT
                if self.check_move_cursor(-1): self.xcursor -= 1
            elif c == curses.KEY_RIGHT:
                # Move cursor RIGHT
                if self.check_move_cursor(1): self.xcursor += 1
            elif c == curses.KEY_BEG or c == curses.KEY_HOME:
                # Move cursor to the BEGIN
                self.xcursor = self.x_init
            elif c == curses.KEY_END:
                # Move cursor to the END
                self.xcursor = self.x_init + len(Gui.cmd.args[self.current_arg][1])
            elif 20 <= c < 127 and Gui.cmd.nb_args > 0:
                i = self.xcursor - self.x_init
                new_val = Gui.cmd.args[self.current_arg][1][:i] + chr(c) + \
                          Gui.cmd.args[self.current_arg][1][i:]
                self._sync_duplicate_args(self.current_arg, new_val)
                self.xcursor += 1


class Gui:
    # result CMD
    cmd = None
    cheaterGlobalVars = {}
    savefile = config.SAVEVARFILE
    # colors
    BASIC_COLOR = 0  # output std
    COL1_COLOR = 7
    COL2_COLOR = 4  # gold
    COL3_COLOR = 14  # purple light 
    COL4_COLOR = 5  # 26  # violet clair: 14  # 4 yellow  # 6 purple # 7 cyan # 9 dark grey
    COL5_COLOR = 5  # blue
    COL1_COLOR_SELECT = 256  # output std invert
    COL2_COLOR_SELECT = 256
    COL3_COLOR_SELECT = 256
    COL4_COLOR_SELECT = 256
    CURSOR_COLOR_SELECT = 266  # background red
    PROMPT_COLOR = 0
    INFO_NAME_COLOR = 4  # 5
    INFO_DESC_COLOR = 0
    INFO_CMD_COLOR = 0
    ARG_NAME_COLOR = 5
    loaded_menu = False
    with_tags = False

    DEFAULT_RATIOS = {"tags": 14, "title": 8, "name": 23, "description": 55}

    def __init__(self):
        self.cheats_menu = None

    @staticmethod
    def init_colors():
        """ Init curses colors """
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, 255):
            curses.init_pair(i + 1, i, -1)

    @classmethod
    def get_ratios_for_column(cls, columns_in_use):
        """
        Calculate the column size from the column to print

        :param columns_in_use: List of the column to print when drawing
        :return: The updated ratios size of each columns
        """
        missing_ratio = 0
        for col in cls.DEFAULT_RATIOS.keys():
            if col not in columns_in_use:
                missing_ratio += cls.DEFAULT_RATIOS.get(col)
        if not missing_ratio:
            return cls.DEFAULT_RATIOS

        new_ratio = {}
        for column in columns_in_use:
            new_ratio[column] = math.floor(cls.DEFAULT_RATIOS[column] + missing_ratio / len(columns_in_use))
        return new_ratio

    @staticmethod
    def draw_string(str_value, max_size):
        """
        Return a string of the max size, ended with ... if >= max_size
        :param str_value:
        :param max_size:
        :return:
        """
        result_string = str_value
        if len(str_value) >= max_size:
            result_string = str_value[:max_size - 4] + '...'
        return result_string

    @staticmethod
    def prefix_cmdline_with_prefix():
        if config.PREFIX_GLOBALVAR_NAME in Gui.cheaterGlobalVars:
            Gui.cmd.cmdline = f"{Gui.cheaterGlobalVars[config.PREFIX_GLOBALVAR_NAME]} {Gui.cmd.cmdline}"

    def run(self, cheatsheets, has_prefix):
        """
        Gui entry point
        :param cheatsheets: cheatsheets dictionary
        """
        if self.cheats_menu is None:
            # Load cheatList if not already done
            self.cheats_menu = CheatslistMenu()
            for value in cheatsheets.values():
                self.cheats_menu.globalcheats.append(value)

        # if global var save exists load it
        if exists(Gui.savefile):
            with open(Gui.savefile, 'r') as f:
                Gui.cheaterGlobalVars = json.load(f)

        wrapper(self.cheats_menu.run)
        if Gui.cmd != None and Gui.cmd.cmdline[0] != '>' and has_prefix:
            self.prefix_cmdline_with_prefix()
        return Gui.cmd
