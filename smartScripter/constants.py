"""Constant values for this package."""

# Import built-in modules
from collections import OrderedDict
import os

# Abbreviation for Python command. This wil be displayed in the drop down
# menu for new commands and will be used internally.
PY = "py"

# Abbreviation for TCL command. This wil be displayed in the drop down menu for
# new commands and will be used internally.
TCL = "tcl"

# Nuke snippet to add in RegisterCommand drop down menu. This wil be displayed
# in the drop down menu for new commands and will be used internally.
NODES = "nodes"

# Label for a new stack in the stacks combo.
NEW_STACK = "--- new ---"

# Nuke paste snippet contains this sub string. Handle a command differently
# when it contains this sub string because this is a Nuke nodes clipboard.
NK_SNIPPET = "cut_paste_input"

# Default settings to apply when there is no smartScripter settings file.
DEFAULT_SETTINGS = {
    "tooltips": True,
    "command_tooltips": True,
    "auto_clear_command": True,
    "auto_close_script": False,
    "auto_close_command": False,
    "language": "py",
    "default_language_new_commands": "py",
    "show_command_widgets": True,
    "current_stack": "",
    "stack_root": os.path.join(os.path.expanduser("~"), "cragl",
                               "smartScripter"),
    "history": [],
    "command_size": "medium"
}

# Crucial keys that are needed when parsing a command settings file. If any
# of these keys are not contained in the settings file then we will skip
# this command.
COMMANDS_CRUCIAL_KEYS = ["lang", "icon", "color"]

# Size of the commands. The size can be set in the settings panel.
COMMAND_SIZE = OrderedDict([
    ("small", {
        "column": 50,
        "widget": 30,
        "icon": 10
    }),
    ("medium", {
        "column": 60,
        "widget": 40,
        "icon": 20
    }),
    ("large", {
        "column": 80,
        "widget": 50,
        "icon": 30
    })
])
