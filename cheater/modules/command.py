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
        Only ask once for duplicate argument names
        """
        self.args = []
        seen_args = {}  # Track args we've already seen
        
        # Use a list of tuples here instead of dict in case
        # the cmd has multiple args with the same name..
        for raw_arg in re.findall(r'<([^<>]+)>', cheat.command):
            if "|" in raw_arg:  # Format <name|default_value|opt2|opt3>
                parts = [p.strip() for p in raw_arg.split("|")]
                name = parts[0]
                options = [p for p in parts[1:] if p != ""]
                default_val = options[0] if options else ""
                
                # Only add to args list if we haven't seen this arg before
                if name not in seen_args:
                    self.args.append([name, default_val])
                    seen_args[name] = len(self.args) - 1
                    if len(options) > 1:
                        self.arg_choices[len(self.args) - 1] = options
                        if name == "Creds_Options":
                            self.arg_choice_labels[len(self.args) - 1] = [
                                "Normal Authentication (-p)",
                                "Pass-The-Hash (-H)",
                                "Kerberos Authentication (-p -k)",
                            ]
                # Variable has been added to cheat variables before, remove it
                cheat.command = cheat.command.replace(raw_arg, name)
                self.cmdline = cheat.command
            elif raw_arg in gvars and raw_arg not in seen_args:
                self.args.append([raw_arg, gvars[raw_arg]])
                seen_args[raw_arg] = len(self.args) - 1
            elif raw_arg in cheat.variables and raw_arg not in seen_args:
                self.args.append([raw_arg, cheat.variables[raw_arg]])
                seen_args[raw_arg] = len(self.args) - 1
            elif raw_arg not in seen_args:
                self.args.append([raw_arg, ""])
                seen_args[raw_arg] = len(self.args) - 1

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
        -> if some args values are still empty do nothing
        -> else build the final command string by adding args values
        """
        if self.nb_args == 0 :
            return True
        argsval = []
        # Build arg values - DON'T quote Creds_Options (needs word-splitting)
        for i, arg in enumerate(self.args):
            val = arg[1]
            argsval.append(val)
        
        if "" not in [a[1] for a in self.args]:
            # split cmdline at each arg position
            regex = ''.join('<' + re.escape(arg[0]) + '>|' for arg in self.args)[:-1]
            cmdparts = re.split(regex, self.cmdline)
            # concat command parts and arguments values to build the command
            self.cmdline = ""
            for i in range(len(cmdparts) + len(self.args)):
                if i % 2 == 0:
                    self.cmdline += cmdparts[i // 2]
                else:
                    self.cmdline += argsval[(i - 1) // 2]
            # Only call curses.endwin() if curses was initialized
            try:
                if curses.isendwin() == False:
                    curses.endwin()
            except:
                pass

        # build ok ?
        return "" not in argsval
