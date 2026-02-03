import re
import curses
import textwrap


class Command:
    cmdline = ""
    description = ""
    args = []  # [(name, value)]
    nb_args = 0
    nb_lines_cmd = 1
    nb_lines_desc = 0
    arg_choices = None
    arg_choice_labels = None

    def __init__(self, cheat, gvars):
        self.cmdline = cheat.command
        self.arg_choices = {}
        self.arg_choice_labels = {}

        self.cmd_tags = cheat.command_tags
        self.description = ''
        for tag in self.cmd_tags:
            self.description += '[' + self.cmd_tags[tag] + '] '
        if self.description != '' and cheat.description != '':
            self.description += '\n-----\n'
        self.description += cheat.description

        self.get_args(cheat, gvars)
        self.nb_args = len(self.args)
        # careful this is not the lines number in GUI
        self.nb_lines_cmd = len(cheat.command.split('\n'))
        # careful this is not the lines number in GUI
        self.nb_lines_desc = 0 if cheat.description == '' else len(cheat.description.split('\n'))

    def get_description_cut_by_size(self, size):
        """
        The description cut by lines inside the gui size
        """
        desc_lines = self.description.split('\n')
        result = []
        for line in desc_lines:
            result.extend(textwrap.wrap(line, size))
        return result

    def get_args(self, cheat, gvars):
        """
        Process cmdline from the cheatsheet to get args names
        """
        self.args = []
        # Use a list of tuples here instead of dict in case
        # the cmd has multiple args with the same name..
        for raw_arg in re.findall(r'<([^<>]+)>', cheat.command):
            if "|" in raw_arg:  # Format <name|default_value|opt2|opt3>
                parts = [p.strip() for p in raw_arg.split("|")]
                name = parts[0]
                options = [p for p in parts[1:] if p != ""]
                default_val = options[0] if options else ""
                self.args.append([name, default_val])
                if len(options) > 1:
                    self.arg_choices[len(self.args) - 1] = options
                    if name == "Creds_Options":
                        self.arg_choice_labels[len(self.args) - 1] = [
                            "Normal Authentication (-p)",
                            "Pass-The-Hash (-H)",
                            "Kerberos Authentication (-k -p)",
                        ]
                # Variable has been added to cheat variables before, remove it
                cheat.command = cheat.command.replace(raw_arg, name)
                self.cmdline = cheat.command
            elif raw_arg in gvars:
                self.args.append([raw_arg, gvars[raw_arg]])
            elif raw_arg in cheat.variables:
                self.args.append([raw_arg, cheat.variables[raw_arg]])
            else:
                self.args.append([raw_arg, ""])

    def get_command_parts(self):
        if self.nb_args != 0:
            regex = ''.join('<' + re.escape(arg[0]) + '>|' for arg in self.args)[:-1]
            cmdparts = re.split(regex, self.cmdline)
        else:
            cmdparts = [self.cmdline]
        return cmdparts

    def build(self):
        """
        Called after argument completion
        Allow empty args - they will be skipped in final command
        """
        if self.nb_args == 0:
            return True
        
        # split cmdline at each arg position
        regex = ''.join('<' + re.escape(arg[0]) + '>|' for arg in self.args)[:-1]
        cmdparts = re.split(regex, self.cmdline)
        
        # Build command, skipping empty args
        self.cmdline = ""
        arg_index = 0
        for i in range(len(cmdparts)):
            self.cmdline += cmdparts[i]
            # Add arg value if not at the end and arg is not empty
            if arg_index < len(self.args):
                if self.args[arg_index][1] != "":
                    self.cmdline += self.args[arg_index][1]
                arg_index += 1
        
        # Only call curses.endwin() if curses was initialized
        try:
            if curses.isendwin() == False:
                curses.endwin()
        except:
            pass

        # Always return True - allow empty args
        return True
