"""Main controller for the ScripterPanel."""

# Import built-in modules
import json
import os

# Import local modules
from smartScripter import dialogs
from smartScripter import helper
from smartScripter import view
from smartScripter import widgets
from smartScripter import model
from smartScripter import scanner
from smartScripter.constants import (COMMAND_SIZE, NEW_STACK, NODES,
                                     NK_SNIPPET, PY, TCL)
from smartScripter.info import __product__

# Constants
COLORPICKER = None
ICONPICKER = None
NEW_STACK_VIEW = None
REGISTER_VIEWER = None


class MainController(object):
    """Main controller that drives the ScriptPanel view."""

    def __init__(self, view_window):
        """Initialize the Controller instance.

        Args:
            view_window (scripter.view.ScripterView): View to drive.

        """
        self.view = view_window

        self.icons = helper.get_session_icons()
        self.create_signals()
        self.settings = model.load()
        self.scanner = scanner.Scanner(self.settings["stack_root"], self)
        self.history_current_item = 0

        # Save the stack that was previously opened before closing the scripter
        # window because the current stack will be changed once we populate
        # the combo_stack with elements.
        startup_stack = self.settings["current_stack"]

        self.setup_view_widgets()
        self.populate_scripts_table()

        # We need set the current stack in here so that we resume with the
        # last stack that we had open when we closed the scripter window.
        self.view.combo_stack.setCurrentIndex(
            self.view.combo_stack.findText(startup_stack))

        self.setup_settings_widgets()

        if self.settings["tooltips"]:
            self.create_tooltips()
            helper.load_tooltips(self.view, "smartScripter")
            helper.load_tooltips(self.view, "settings")

    def create_tooltips(self):
        """Create tooltips for all widgets."""
        # Main panel.
        self.view.combo_stack.setProperty("tt", "combo_stacks")
        self.view.button_toggle_command.setProperty("tt", "toggle_command")
        self.view.button_refresh.setProperty("tt", "refresh")
        self.view.button_settings.setProperty("tt", "settings")
        self.view.button_language.setProperty("tt", "command_language_switch")
        self.view.input_command.setProperty("tt", "command_prompt")

        # Settings panel.
        settings = self.view.settings_panel

        settings.check_tooltips.setProperty(
            "tt", "tooltips")
        settings.check_command_tooltips.setProperty(
            "tt", "command_tooltips")
        settings.check_auto_clear_command.setProperty(
            "tt", "auto_clear_command")
        settings.check_auto_close_script.setProperty(
            "tt", "auto_close_script")
        settings.check_auto_close_command.setProperty(
            "tt", "auto_close_command")
        settings.label_command_size.setProperty(
            "tt", "commands_size")
        settings.combo_command_size.setProperty(
            "tt", "commands_size")
        settings.label_lang_new_commands.setProperty(
            "tt", "default_lang_new_command")
        settings.combo_lang_new_commands.setProperty(
            "tt", "default_lang_new_command")
        settings.label_stack_root.setProperty(
            "tt", "stack_root")
        settings.input_stack_root.setProperty(
            "tt", "stack_root")
        settings.button_stack_root.setProperty(
            "tt", "stack_root")
        settings.button_clear_history.setProperty(
            "tt", "clear_history")
        settings.button_close.setProperty(
            "tt", "save_and_close")

    def create_signals(self):
        """Create signals."""
        settings = self.view.settings_panel
        self.view.button_language.clicked.connect(
            lambda: self.change_language())
        self.view.input_command.returnPressed.connect(
            lambda: self.execute_command())
        self.view.input_command.history.connect(self.cycle_history)
        self.view.button_toggle_command.clicked.connect(
            lambda: self.toggle_command_widgets())
        self.view.scripts_table.cellClicked.connect(self.execute_cell)
        self.view.scripts_table.command_dragged.connect(self.register_command)
        self.view.registered_new_command.connect(self.refresh)
        self.view.combo_stack.currentIndexChanged.connect(
            lambda: self.load_stack())
        self.view.button_settings.clicked.connect(self.toggle_settings)
        self.view.button_refresh.clicked.connect(lambda: self.refresh())
        settings.button_close.clicked.connect(
            lambda: self.save_and_close_settings())
        settings.button_clear_history.clicked.connect(
            lambda: self.clear_history())
        settings.button_stack_root.clicked.connect(
            self.show_browser_stack_root)
        settings.combo_command_size.currentIndexChanged.connect(
            lambda: self.update_command_size())
        settings.button_reveal_stack_root.clicked.connect(
            lambda: self.reveal_stack_root())

    def reveal_stack_root(self):
        """Reveal the stack root directory in the explorer."""
        helper.reveal_in_explorer(self.settings["stack_root"])

    def update_command_size(self):
        """Update the command size when changed in command size drop down."""
        self.settings["command_size"] = \
            self.view.settings_panel.combo_command_size.currentText()

        self.populate_scripts_table()

    def show_browser_stack_root(self):
        """Show browser for stack root."""
        title = "Choose Stack Root"
        stack_root = dialogs.show_path_browser(title)
        if stack_root:
            self.view.settings_panel.input_stack_root.setText(stack_root)
            self.refresh()

    def clear_history(self):
        """Clear command history."""
        self.settings = helper.clear_history()

    def save_and_close_settings(self):
        """Update settings and close setting section."""
        panel = self.view.settings_panel

        self.settings["tooltips"] = \
            panel.check_tooltips.isChecked()

        self.settings["command_tooltips"] = \
            panel.check_command_tooltips.isChecked()

        self.settings["auto_clear_command"] = \
            panel.check_auto_clear_command.isChecked()

        self.settings["auto_close_script"] = \
            panel.check_auto_close_script.isChecked()

        self.settings["auto_close_command"] = \
            panel.check_auto_close_command.isChecked()

        self.settings["default_language_new_commands"] = \
            panel.combo_lang_new_commands.currentText()

        self.settings["command_size"] = \
            panel.combo_command_size.currentText()

        stack_root_temp = self.settings["stack_root"]
        self.settings["stack_root"] = panel.input_stack_root.text()

        self.settings = model.save(self.settings)

        self.toggle_settings()

        # Refresh the scripts table only when the stack root directory has
        # changed. Always refreshing is kind of an overkill.
        if stack_root_temp != self.settings["stack_root"]:
            self.scanner = scanner.Scanner(self.settings["stack_root"], self)
            self.setup_view_widgets(add_new_command=False)
            self.refresh()
            self.view.combo_stack.setCurrentIndex(0)

    def toggle_settings(self):
        """Toggle show / hide the settings section and the main section."""
        self.view.settings_panel.setVisible(
            not self.view.settings_panel.isVisible())

        self.view.adjustSize()

    def load_stack(self):
        """Load stack or show window to create a new stack."""
        new_stack_index = self.view.combo_stack.findText(NEW_STACK)
        if self.view.combo_stack.currentIndex() == new_stack_index:

            # We need to make this global in here otherwise Nuke won't show the
            # window.
            global NEW_STACK_VIEW  # pylint: disable=global-statement

            NEW_STACK_VIEW = view.NewStack(self.view)
            NEW_STACK_VIEW.raise_()
            NEW_STACK_VIEW.show()

            NewStackController(NEW_STACK_VIEW)
        else:
            new_stack = self.view.combo_stack.currentText()
            self.settings["current_stack"] = new_stack
            model.save(self.settings)

            self.populate_scripts_table()

    def refresh(self):
        """Reload scripts table."""
        self.settings = model.load()
        self.scanner = scanner.Scanner(self.settings["stack_root"], self)
        self.populate_scripts_table()

    def register_command(self, command):
        """Show window to register command from clipboard as a new command.

        Args:
            command (str): Command that is stored as mimedata in the clipboard.

        """
        # We need to make this global in here otherwise Nuke won't show the
        # window.
        global REGISTER_VIEWER  # pylint: disable=global-statement

        REGISTER_VIEWER = view.RegisterCommandView(self.view)
        REGISTER_VIEWER.raise_()
        REGISTER_VIEWER.show()

        RegisterCommandController(REGISTER_VIEWER, command)

    def execute_cell(self):
        """Execute the command for the clicked cell."""
        row = self.view.scripts_table.currentRow()
        column = self.view.scripts_table.currentColumn()
        widget = self.view.scripts_table.cellWidget(row, column)
        widget.execute()

    def change_language(self):
        """Toggle the language and save to settings."""
        current = self.view.button_language.text()
        new = TCL if current == PY else PY
        self.view.button_language.setText(new)
        self.settings["language"] = new
        model.save(self.settings)

    def execute_command(self):
        """Execute the input command and clear the command input when set.

        When the command has been executed successfully, it will be added to
        the history. If the command has some errors, then the input command
        turns red.

        """
        command = self.view.input_command.text()
        language = self.view.button_language.text()

        if not command:
            return

        try:
            helper.execute(language, command)
        except ValueError:
            self.view.input_command.setProperty("style", "red")
            helper.set_style_sheet(self.view)
            return

        self.settings = helper.add_to_history(command)

        self.view.input_command.setProperty("style", "")
        helper.set_style_sheet(self.view)

        if self.settings["auto_clear_command"]:
            self.view.input_command.setText("")

        auto_close_command = self.settings["auto_close_command"]
        floating = self.view.floating
        if all([auto_close_command, floating]):
            self.view.close()

    def cycle_history(self, direction):
        """Cycle the command history using the given direction.

        Args:
            direction (str): If 'up', go history up showing previous commands,
                else if 'down' go down showing the latest commands.

        """
        if not self.settings["history"]:
            return

        if direction == "up":
            self.history_current_item -= 1

        elif direction == "down":
            self.history_current_item += 1

        try:
            command = self.settings["history"][self.history_current_item]
        except IndexError:
            self.history_current_item = 0
            command = self.settings["history"][0]

        self.view.input_command.setText(command)

    def toggle_command_widgets(self, show=None):
        """Show/ hide the command inputs and update settings.

        Args:
            show (bool, default is None): If True force the command widgets to
                show, otherwise hide them.

        """
        command_widgets = (
            self.view.button_language,
            self.view.input_command
        )

        # We need indeed to check for 'is not None' explicitly in here because
        # this value might explicitly be set to False which would otherwise
        # evaluate to the second term instead.
        visibility = (show if show is not None
                      else not command_widgets[0].isVisible())

        for widget in command_widgets:
            widget.setVisible(visibility)

        self.view.adjustSize()

        self.settings["show_command_widgets"] = visibility
        model.save(self.settings)

    def setup_view_widgets(self, add_new_command=True):
        """Set up the viewer ui based on current settings.

        Args:
            add_new_command (bool): If True add a '---new---' command,
                otherwise don't create it. We need this to switch from one
                stack root to another and avoid creating twice a 'new' command
                because we cannot simply remove it from the menu because this
                would trigger the 'New Stack' command which would show the
                according window to create a new stack.

        """
        self.view.button_language.setText(self.settings["language"])
        self.toggle_command_widgets(show=self.settings["show_command_widgets"])

        stacks = self.scanner.stacks.keys()

        if add_new_command:
            stacks.append(NEW_STACK)

        helper.clear_combo(self.view.combo_stack)

        self.view.combo_stack.addItems(stacks)

    def populate_scripts_table(self):
        """Populate the viewer main panel with commands of current stack."""
        self.view.scripts_table.clear()
        # Creating a new scanner by scanning from scratch seems like a
        # performance hit, however this runs without any noticeable delay. Keep
        # an eye for this and change the way the CommandWidget items get
        # created and registered.
        # We need to re-scan here because when we change the stack, the Widgets
        # will be deleted because they will loose their parent and thus we get
        # an "Internal c++ object already deleted" error.
        self.scanner = scanner.Scanner(self.settings["stack_root"], self)

        current_stack = self.settings["current_stack"]
        if current_stack not in self.scanner.stacks:
            return

        current_stack_widgets = self.scanner.stacks[current_stack]
        self.view.scripts_table.setColumnCount(len(current_stack_widgets)+1)

        size = COMMAND_SIZE[self.settings["command_size"]]
        column_size = size["column"]

        index = 0
        for index, widget in enumerate(current_stack_widgets):
            self.view.scripts_table.setCellWidget(0, index, widget)
            self.view.scripts_table.setColumnWidth(index, column_size)

        plus = widgets.CommandPlus(self, self.view)

        plus_widget_index = index + 1
        if not current_stack_widgets:
            plus_widget_index = 0

        self.view.scripts_table.setCellWidget(0, plus_widget_index, plus)
        self.view.scripts_table.setColumnWidth(plus_widget_index, column_size)

        self.view.scripts_table.resizeRowsToContents()

    def setup_settings_widgets(self):
        """Set up settings widgets based on current settings."""
        settings = self.view.settings_panel

        settings.check_tooltips.setChecked(
            self.settings["tooltips"])

        settings.check_command_tooltips.setChecked(
            self.settings["command_tooltips"])

        settings.check_auto_clear_command.setChecked(
            self.settings["auto_clear_command"])

        settings.check_auto_close_script.setChecked(
            self.settings["auto_close_script"])

        settings.check_auto_close_command.setChecked(
            self.settings["auto_close_command"])

        settings.input_stack_root.setText(
            self.settings["stack_root"])

        settings.combo_lang_new_commands.setCurrentIndex(
            settings.combo_lang_new_commands.findText(
                self.settings["default_language_new_commands"]))

        settings.combo_command_size.setCurrentIndex(
            settings.combo_command_size.findText(
                self.settings["command_size"]))


class RegisterCommandController(object):
    """Controller for the RegisterCommand window instance."""

    def __init__(self, view_window, command):
        """Initialize the RegisterCommandController instance.

        Args:
            view_window (scripter.widgets.RegisterCommandPanel):
                RegisterCommand instance to drive.
            command (str): Command to store. Can be edited in the text area
                of this widget.

        """
        self.view = view_window
        self.command = command

        self.settings = model.load()

        self.create_signals()
        self.setup_view()
        self.setup_from_command_widget()

        self.detect_nk_snippet()

    def create_signals(self):
        """Create signals."""
        self.view.button_save.clicked.connect(lambda: self.register())
        self.view.button_color.clicked.connect(lambda: self.show_colorpicker())
        self.view.button_icon.clicked.connect(lambda: self.show_iconpicker())
        self.view.combo_language.currentIndexChanged.connect(
            lambda: self.check_for_icon_update())
        self.view.text_command.textChanged.connect(lambda: self.set_up_icon())
        self.view.input_name.returnPressed.connect(lambda: self.register())

    def set_up_icon(self):
        """Convenience function to set up Nuke icon due to text recognition.

        This will check the first time that text is inserted/ pasted into the
        text command, if it is a nuke node snippet. If it is, then we will
        automatically set the icon to a Nuke icon and set the language drop
        down menu to "nodes". A Nuke node snippet can be detected by the
        key word "cut_paste_input".

        The set up icon function should only be executed once immediately after
        the user has pasted some code into the command text field in order to
        set up the icon automatically but giving them the chance to update the
        icon manually if needed.

        """
        if self.view.text_command.toPlainText():
            if self.view.text_inserted:
                return
            self.view.text_inserted = True
            self.detect_nk_snippet()

    def check_for_icon_update(self):
        """Automatically set the icon to nuke when 'nodes' lang is set."""
        if self.view.combo_language.currentText() == NODES:
            icon = "nuke_command"
        else:
            icon = "command"
        self.view.update_icon(helper.get_icon(icon), icon)

    def show_iconpicker(self):
        """Show icon picker window to use as icon for new command."""
        # We need to make this global in here otherwise Nuke won't show the
        # window.
        global ICONPICKER  # pylint: disable=global-statement

        ICONPICKER = view.ChooseIconView(self.view)
        ICONPICKER.raise_()
        ICONPICKER.show()

        ChooseIconController(ICONPICKER)

    def show_colorpicker(self):
        """Show color picker dialog to use as color for new command."""
        # We need to make this global in here otherwise Nuke won't show the
        # window.
        global COLORPICKER  # pylint: disable=global-statement

        COLORPICKER = dialogs.ColorPicker(self.view)
        COLORPICKER.raise_()
        COLORPICKER.show()

        if COLORPICKER.exec_():
            self.view.button_color.setProperty("color", COLORPICKER.color)
            self.view.update_color(str(COLORPICKER.color))

    def register(self):
        """Register new command and write to disk."""
        name = self.view.input_name.text()
        command = self.view.text_command.toPlainText()
        language = self.view.combo_language.currentText()
        icon = self.view.button_icon.property("icon_name") or ""
        color = self.view.button_color.property("color") or ""

        path = os.path.join(self.settings["stack_root"],
                            self.settings["current_stack"],
                            name)

        if os.path.exists(path) and name:
            if self.view.command_widget:
                message = "Do you want to update the command?"
                process_label = "Update"
                color_process = "48, 138, 167"
            else:
                message = ("The name '{}' already exists. Do you want to "
                           "overwrite it?".format(name))
                process_label = "Overwrite"
                color_process = "90, 30, 30"

            overwrite = dialogs.ask_dialog(
                message, process_label=process_label,
                color_process=color_process, cancel_label="Cancel")
            if not overwrite:
                return

        try:
            self._register(path, name, command, language, icon, color)
        except ValueError as error:
            dialogs.show_message_box(self.view, error.message)
            return

        self.view.scripter_panel.registered_new_command.emit()
        self.view.close()

    # This method simply needs a few more arguments as a command contains
    # multiple crucial members.
    @staticmethod
    def _register(path, name, command, language, icon="", color=""):  # pylint: disable=too-many-arguments, line-too-long
        """Write new command and command settings file to disk.

        Args:
            path (str): Absolute path of the commands file to write. This
                commands file does not contain any file extension.
            name (str): Name of the command to write.
            command (str) The command to write.
            language (str): the language to use ("py", "tcl").
            icon (str): The name of the icon to use without extension.
            color (str): The hex color code to use for the command.

        Raises:
            ValueError: When the name is not set.
            scripter.helper.ExistError: When a command with that name already
                exists in the current stack.

        """
        if not name:
            raise ValueError("Please enter a name for the command.")

        # Write commands file.
        with open(path, "w") as file_:
            file_.write(command)

        # Write commands settings file.
        data = {
            "lang": language,
            "icon": icon,
            "color": color
        }
        with open("{}.json".format(path), "w") as file_:
            json.dump(data, file_, indent=4, sort_keys=True)

    def setup_view(self):
        """Set up view widgets."""
        self.view.text_command.setText(self.command)
        self.view.combo_language.addItems([PY, TCL, NODES])

        default_lang = self.settings["default_language_new_commands"]
        index_default_lang = self.view.combo_language.findText(default_lang)
        self.view.combo_language.setCurrentIndex(index_default_lang)

    def setup_from_command_widget(self):
        """Set up information from command_widget if it exists."""
        # When there is a command_widget then we are in edit mode.
        if self.view.command_widget:
            title = "Edit Command"
            widget = self.view.command_widget
            self.view.input_name.setText(widget.name)
            self.view.combo_language.setCurrentIndex(
                self.view.combo_language.findText(widget.language))

            icon_name = os.path.splitext(os.path.basename(widget.icon))[0]
            self.view.button_icon.setProperty("icon_name", icon_name)
            self.view.update_icon(widget.icon, icon_name)
            self.view.update_color(widget.color)

        # There is no command_widget so we are in the store new command mode.
        else:
            title = "Store New Command"

        self.view.setWindowTitle(title)

    def detect_nk_snippet(self):
        """Detect if the command is a nk file snippet and set up icon."""

        detected_nk_snippet = any(
            [
                NK_SNIPPET in self.command,
                NK_SNIPPET in self.view.text_command.toPlainText()
            ]
        )
        if detected_nk_snippet:
            nk_cmd = "nuke_command"
            self.view.update_icon(helper.get_icon(nk_cmd), nk_cmd)
            combo = self.view.combo_language
            combo.setCurrentIndex(combo.findText(NODES))


class ChooseIconController(object):
    """Controller for the ChooseIcon window."""

    def __init__(self, view_window):
        """Initialize the ChooseIconController instance.

        Args:
            view_window (scripter.view.ChooseIconView): ChooseIconView instance
            to drive.

        """
        self.view = view_window

        self.create_signals()

    def create_signals(self):
        """Create signals."""
        self.view.icon_set.connect(lambda path: self.set_icon(path))

    def set_icon(self, path):
        """Set icon and close view."""
        icon_name = os.path.splitext(os.path.basename(path))[0]
        self.view.register_command_view.button_icon.setProperty("icon_name",
                                                                icon_name)
        self.view.register_command_view.update_icon(path, icon_name)
        self.view.close()


class NewStackController(object):
    """Controller to drive the NewStack window."""

    def __init__(self, view_window):
        """Initialize the NewStackController instance.

        Args:
            view_window (scripter.view.NewStack): NewStack instance to drive.

        """
        self.view = view_window

        self.create_signals()

        self.view.input_stack_name.setFocus()

    def create_signals(self):
        """Create signals."""
        self.view.button_create.clicked.connect(
            lambda: self.create_new_stack())
        self.view.input_stack_name.returnPressed.connect(
            lambda: self.create_new_stack())

    def create_new_stack(self):
        """Create new stack."""
        self.settings = model.load()

        stack_name = self.view.input_stack_name.text()
        if not stack_name:
            return

        stack_path = os.path.join(self.settings["stack_root"], stack_name)
        if os.path.isdir(stack_path):
            message = ("The stack name '{}' already exists. Please choose "
                       "a different name.".format(stack_name))
            dialogs.show_message_box(self.view, message)
            return

        os.makedirs(stack_path)

        self.view.scripter_view.combo_stack.addItem(stack_name)
        self.view.scripter_view.combo_stack.setCurrentIndex(
            self.view.scripter_view.combo_stack.findText(stack_name))
        self.view.close()


# No need to use multiple public methods in here as this is just a small
# controller anyways.
# pylint: disable=too-few-public-methods
class AboutController(object):
    """Controller to drive the About window."""

    def __init__(self, view_window):
        """Inittialize the AboutController instance.

        Args:
            view_window (smartScripter.about.About): About window to drive.

        """
        self.view = view_window
        self.create_signals()

    def create_signals(self):
        """Create signals."""
        from smartScripter import osl
        self.view.help_push_web.clicked.connect(lambda: helper.open_website(
            "http://www.cragl.com/tool.php?tool={}&a=tut".format(
                __product__)))
        self.view.help_push_close.clicked.connect(lambda: self.view.close())
        self.view.push_uninstall.clicked.connect(
            lambda: osl.uninstall_manually())
