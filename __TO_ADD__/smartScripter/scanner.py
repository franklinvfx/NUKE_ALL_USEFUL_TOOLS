"""Self contained scanner that will search for stacks and commands.

This will automatically scan the given root for so called "stacks". A stack is
nothing more than a directory that contains command.json files. The scanner
will create a hierarchical structure of all stacks containing all commands.
These commands are represented directly as CommandWidgets so that they can be
used by the ScripterPanel view and Controller instance directly.

Usage:
    >>> from scripter.scanner import Scanner
    # Create a new scanner instance; The controller is not necessary in this
    # example so we can leave it as None.
    >>> scanner = Scanner("path/to/stack_root", None)

    # By creating the scanner instance, it will automatically scan for stacks.
    # We can now call the 'stacks' member.
    >>> scanner.stacks
    OrderedDict([
        ('stack_a', [
            CommandWidget('CommandA', 'py', '#command to execute',
                          'path/to/icon.png', color=''),
            ...
            ],
        ),
        ...
    ])

"""

# Import built-in modules
from collections import OrderedDict
import json
import os

# Import local modules
from smartScripter import widgets
from smartScripter import helper


# We want to create a self-contained class explicitly. The user does not need
# to call any methods on this class as the calculation works automatically.
# pylint: disable=too-few-public-methods
class Scanner(object):
    """Scanner to search for stacks and commands."""

    def __init__(self, root, controller):
        """Initialize the scanner instance.

        Args:
            root (str): The root to scan.

        """
        self.controller = controller
        self.logger = helper.get_logger()
        self.stacks = self._load_stacks(root)

    def _load_stacks(self, root):
        """Load the stacks in the given root.

        Returns:
            OrderedDict: All scanned stacks containing their CommandWidgets in
                the format:

                OrderedDict([
                    ("stack1": [
                        CommandWidget_a,
                        CommandWidget_b,
                        CommandWidget_c,
                    ]),
                    ("stack2": [
                        CommandWidget_a,
                        CommandWidget_b,
                        CommandWidget_c,
                    ]),
                    ...
                ])

        """
        self.logger.debug("Scanning for stacks: %s", root)

        if not os.path.isdir(root):
            try:
                os.makedirs(root)
            except IOError as error:
                raise IOError("Cannot create stack root in directory: "
                              "{}\n".format(root, error.message))

        dirs = [os.path.join(root, dir_) for dir_ in os.listdir(root)
                if os.path.isdir(os.path.join(root, dir_))
                and not dir_.startswith("_")]

        self.logger.debug("Found stacks: %s", ", ".join(dirs))

        stacks = OrderedDict()
        for dir_ in dirs:
            stacks[os.path.basename(dir_)] = self._load_stack(dir_)

        return stacks

    def _load_stack(self, directory_path):
        """Load all commands json files from the given path.

        Args:
            directory_path (str): Absolute path of directory to scan for json
                files.

        Returns:
            list: All CommandWidgets that got created from the scan of the
                given path.

        """
        self.logger.debug("Scanning stack %s", directory_path)

        files = (file_ for file_ in os.listdir(directory_path)
                 if file_.endswith(".json"))

        commands = []

        for file_ in files:
            path = os.path.join(directory_path, file_)

            try:
                data = self._parse_json(path)
            except (IOError, KeyError, ValueError) as error:
                self.logger.warning(error.message)

            with open(os.path.splitext(path)[0], "r") as command_file:
                command = command_file.read()

            command_widget = widgets.CommandWidget(
                self.controller,
                os.path.splitext(file_)[0], data["lang"], command,
                data["icon"], data["color"]
            )

            commands.append(command_widget)
            self.logger.debug("Add %s.%s", os.path.basename(path), file_)

        return commands

    @staticmethod
    def _parse_json(path):
        """Parse given json file and check for command file existence.

        Args:
            path (str): Absolute path of file to parse.

        Returns:
            dict: The parsed json file.

        Raises:
            IOError: When there is no corresponding command file.
            KeyError: When a crucial key as defined in constants is missing.
            ValueError: When the json file is non well formed.

        """
        command_file = os.path.splitext(path)[0]
        if not os.path.isfile(command_file):
            raise IOError("Skipping command due no to command file {}".format(
                path
            ))

        with open(path, "r") as json_file:
            try:
                return json.load(json_file)
            except ValueError:
                raise ValueError("Skipping corrupt command {}".format(path))
            except KeyError:
                raise KeyError("Skipping insufficient command {}".format(path))
