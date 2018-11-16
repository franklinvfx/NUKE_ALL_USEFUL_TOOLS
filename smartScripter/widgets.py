"""Helper widgets for the package."""

# Import built-in modules
import os

# Import third-party modules
import nuke  # pylint: disable=import-error

# PySide import switch
try:
    from PySide import QtGui as QtWidgets
    from PySide import QtGui
    from PySide import QtCore
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtGui
    from PySide2 import QtCore


# Import local modules
from smartScripter import dialogs
from smartScripter import helper
from smartScripter.constants import NODES, NK_SNIPPET, PY, TCL, COMMAND_SIZE

# constants
SESSION_ICONS = helper.get_session_icons()
ICONS = helper.load_icons()

REGISTER_VIEW = None


class ScriptsTable(QtWidgets.QTableWidget):
    """Main panel with drag and drop functionality that holds the scripts."""

    command_dragged = QtCore.Signal(str)

    def __init__(self):
        super(ScriptsTable, self).__init__()

        self.setDragEnabled(True)
        self.setAcceptDrops(True)

        self.setMouseTracking(True)
        self.cellEntered.connect(self.set_current_cell)

        self.setRowCount(1)
        self.verticalHeader().hide()
        self.horizontalHeader().hide()
        self.setShowGrid(False)
        self.setSelectionMode(QtWidgets.QTableWidget.NoSelection)

    def set_current_cell(self, row, column):
        """Set the current cell to the given row and column.

        Args:
            row (int): Index of row to set.
            column (int): Index of column to set.

        """
        self.setCurrentCell(row, column)

    def dragEnterEvent(self, event):
        """Overwrite dragEnterEvent to set mimeData."""
        event.accept()

    def dragMoveEvent(self, event):
        """Overwrite dragMoveEvent to accept drags."""
        event.setDropAction(QtCore.Qt.CopyAction)
        event.accept()

    def dropEvent(self, event):
        """Overwrite dragMoveEvent to accept drops and fire file_dropped
        signal.
        """
        event.setDropAction(QtCore.Qt.CopyAction)
        event.accept()

        self.command_dragged.emit(event.mimeData().text())


class CommandInput(QtWidgets.QLineEdit):
    """QLineEdit using custom arrow up and down functionality.

    In here we can use the up and down arrow keys to cycle through the command
    history.

    """

    history = QtCore.Signal(str)

    def __init__(self):

        super(CommandInput, self).__init__()

    def keyPressEvent(self, event):
        """Catch keyPressEvent to execute custom events.

        Pressing escape will close the widget if we are running in floating
        mode.

        """
        super(CommandInput, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Up:
            self.history.emit("up")

        if event.key() == QtCore.Qt.Key_Down:
            self.history.emit("down")


class RightClickMenuButton(QtWidgets.QToolButton):
    """Button with context menu."""

    def __init__(self, icon, parent):
        """Initialize the RightClickMenuButton instance.

        Args:
            icon (str): Absolute path of icon to apply to the button.
            parent (smartScripter.widgets.CommandWidget): CommandWidget item
                that the command is parented to.

        """
        super(RightClickMenuButton, self).__init__()

        self.parent = parent
        self.icon = icon
        self.setIcon(QtGui.QIcon(icon))

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self):
        """Show right click menu."""
        self.menu = QtWidgets.QMenu()

        # Create items.
        self.action_execute = QtWidgets.QAction(QtGui.QIcon(ICONS["execute"]),
                                                "execute", self)

        self.action_edit = QtWidgets.QAction(QtGui.QIcon(ICONS["edit"]),
                                             "edit", self)
        self.menu_move = QtWidgets.QMenu("move")
        self.menu_move.setIcon(QtGui.QIcon(ICONS["move"]))

        all_stacks = helper.get_all_stacks()
        for stack in all_stacks:
            action_stack = QtWidgets.QAction(stack, self.menu_move)
            self.menu_move.addAction(action_stack)
            action_stack.triggered.connect(
                lambda to_stack=stack: self.move_stack(to_stack))

        self.action_remove = QtWidgets.QAction(
            QtGui.QIcon(ICONS["x"]), "delete", self)

        # Add items.
        self.menu.addAction(self.action_execute)
        self.menu.addAction(self.action_edit)
        self.menu.addMenu(self.menu_move)
        self.menu.addAction(self.action_remove)

        # Signals.
        self.action_remove.triggered.connect(self.remove_command)
        self.action_edit.triggered.connect(self.edit_command)
        self.action_execute.triggered.connect(lambda: self.parent.execute())

        # Show right click menu.
        current_loc = QtCore.QPoint((QtGui.QCursor.pos()))
        self.menu.popup(current_loc)

    def edit_command(self):
        """Edit the current command."""
        from smartScripter import view
        from smartScripter.controller import RegisterCommandController
        # We need to make this global in here otherwise Nuke won't show the
        # window.
        global REGISTER_VIEW  # pylint: disable=global-statement

        REGISTER_VIEW = view.RegisterCommandView(self.parent.controller.view,
                                                 command_widget=self.parent)
        REGISTER_VIEW.raise_()
        REGISTER_VIEW.show()

        RegisterCommandController(REGISTER_VIEW, self.parent.command)

    def move_stack(self, to_stack_name):
        """Move command to new stack and refresh ui."""
        stack_root = self.parent.controller.settings["stack_root"]
        new_stack_path = os.path.join(stack_root, to_stack_name)

        command_path_old = self.command_path
        settings_path_old = "{}.json".format(self.command_path)

        command_path_new = os.path.join(new_stack_path, self.command_name)
        settings_path_new = "{}.json".format(command_path_new)

        os.rename(command_path_old, command_path_new)
        os.rename(settings_path_old, settings_path_new)

        self.parent.controller.refresh()

    @property
    def command_path(self):
        """Assemble the absolute command file path.

        This is the absolute path of the command to execute.

        Returns:
            str: Absolute path of the command file.

        """
        return helper.assemble_command_path(self.parent.name)

    @property
    def command_name(self):
        """Return the name of the underlying parent.

        Returns:
            str: The name of the parent.

        """
        return self.parent.name

    def remove_command(self):
        """Remove command from hard drive.

        This will remove the command file and the settings json file for this
        command.

        """
        path = self.command_path

        message = "Do you want to delete the command '{}'?".format(
            self.parent.name)
        ask = dialogs.ask_dialog(message, process_label="delete",
                                 color_process="200, 30, 30, 100")

        if not ask:
            return

        os.remove(path)
        os.remove("{}.json".format(path))
        self.parent.controller.refresh()


# We want to explicitly bundle all of these member into the class.
# pylint: disable=too-many-instance-attributes
class CommandWidget(QtWidgets.QWidget):
    """Button that holds the commands to execute."""

    # pylint: disable=too-many-arguments
    def __init__(self, controller, name, language, command, icon="",
                 color=(0, 0, 0)):
        """Initialize the CommandWidget instance.

        Args:
            controller (smartScripter.controller.MainController): Controller to
                access the underlying view instance so that we can close it
                on successful script execution.
            name (str): Name of the command.
            language (str): Language to use for command execution.
            command (str): Command to execute.
            icon (str, default empty str): Name of the icon. The icon must be
                in Nuke's plugin path to be able to show up.
            color (int, int, int): RGB color code for the button.

        """
        super(CommandWidget, self).__init__()

        self.controller = controller
        self.name = name
        self.language = language
        self.command = command
        self.icon = self.get_icon_path(icon)
        self.color = color

        self.build_ui()

    def __repr__(self):
        """Get information about the instance.

        Returns:
            str: String representation of the current instance.

        """
        return "{}('{}', '{}', '{}', icon='{}', color={})".format(
            self.__class__.__name__, self.name, self.language, self.command,
            self.icon, self.color)

    @staticmethod
    def get_icon_path(icon):
        """Get absolute path of icon from session icons.

        Args:
            icon (str): File name of icon to look up in SESSION_ICONS.

        Returns:
            str: Absolute path of found icon if it exists in SESSION_ICONS,
                otherwise absolute path of default command.

        """
        return helper.get_icon(icon)

    def build_ui(self):
        """Build ui."""
        self.create_widgets()
        self.create_layouts()
        self.create_signals()

    def create_widgets(self):
        """Create widgets."""
        self.button = RightClickMenuButton(self.name, self)

        if self.controller.settings["command_tooltips"]:
            self.button.setToolTip(self.command)

        if self.color:
            style = "QToolButton {background-color: #%s; }" % self.color
            self.button.setStyleSheet(style)

        size = COMMAND_SIZE[self.controller.settings["command_size"]]
        widget_size = size["widget"]
        icon_size = size["icon"]

        self.button.setFixedSize(QtCore.QSize(widget_size, widget_size))
        self.button.setIcon(QtGui.QIcon(self.icon))
        self.button.setIconSize(QtCore.QSize(icon_size, icon_size))
        self.label = QtWidgets.QLabel(self.name)
        self.label.setWordWrap(True)

    def create_layouts(self):
        """Create layouts."""
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_button = QtWidgets.QHBoxLayout()
        self.layout_label = QtWidgets.QHBoxLayout()

        self.layout_button.addStretch()
        self.layout_button.addWidget(self.button)
        self.layout_button.addStretch()

        self.layout_label.addStretch()
        self.layout_label.addWidget(self.label)
        self.layout_label.addStretch()

        self.layout_main.addLayout(self.layout_button)
        self.layout_main.addLayout(self.layout_label)

        self.setLayout(self.layout_main)

    def create_signals(self):
        """Create signals."""
        self.button.clicked.connect(self.execute)

    def execute(self):
        """Execute underlying command."""
        # Command contains substring "cut_paste_input" and thus is a NK
        # snippet. Paste the command into the node graph.
        if NK_SNIPPET in self.command:
            clipboard = QtWidgets.QApplication.clipboard()
            clipboard.setText(self.command)
            nuke.nodePaste("%clipboard%")
            return
        # General python or tcl command.
        else:
            helper.execute(self.language, self.command)

            auto_close = self.controller.settings["auto_close_script"]
            floating = self.controller.view.floating
            if all([auto_close, floating]):
                self.controller.view.close()

    def mouseMoveEvent(self, *args):
        """Overwrite mouseMove event to move parent smartLinker window."""
        drag = QtGui.QDrag(self)
        drag_mime_data = QtCore.QMimeData()
        drag_mime_data.setText(self.command)

        drag.setMimeData(drag_mime_data)
        drag.exec_(QtCore.Qt.MoveAction)


class CommandPlus(QtWidgets.QWidget):
    """Button to create a new command when clicking it.

    This button is always located as last item at the very right of the
    scripts table. Clicking it opens the RegisterCommand view.

    """

    def __init__(self, controller, parent):
        """Initialize the CommandPlus instance.

        Args:
            parent (smartScripter.view.scripterView): Parent scripter view
                instance.

        """
        super(CommandPlus, self).__init__()

        self.controller = controller
        self.parent = parent

        self.build_ui()

    def build_ui(self):
        """Build ui."""
        self.create_widgets()
        self.create_layouts()
        self.create_signals()

    def create_widgets(self):
        """Create widgets."""
        self.button = QtWidgets.QToolButton()
        self.button.setIcon(QtGui.QIcon(ICONS["plus"]))

        size = COMMAND_SIZE[self.controller.settings["command_size"]]
        widget_size = size["widget"]
        icon_size = size["icon"]

        self.button.setFixedSize(QtCore.QSize(widget_size, widget_size))
        self.button.setIconSize(QtCore.QSize(widget_size, icon_size))

    def create_layouts(self):
        """Create layouts."""
        self.layout_main = QtWidgets.QHBoxLayout()

        self.layout_main.addStretch()
        self.layout_main.addWidget(self.button)
        self.layout_main.addStretch()

        self.setLayout(self.layout_main)

    def create_signals(self):
        """Create signals."""
        self.button.clicked.connect(self.execute)

    def execute(self):
        """Show RegisterCommand window and paste Clipboard."""
        from smartScripter.controller import RegisterCommandController
        from smartScripter import view
        # We need to make this global in here otherwise Nuke won't show the
        # window.
        global REGISTER_VIEW  # pylint: disable=global-statement

        REGISTER_VIEW = view.RegisterCommandView(self.parent)
        REGISTER_VIEW.raise_()
        REGISTER_VIEW.show()

        RegisterCommandController(REGISTER_VIEW, "")


class QHLine(QtWidgets.QFrame):
    """Horizontal line."""

    def __init__(self):
        """Initialize the QHLine instance."""
        super(QHLine, self).__init__()
        self.setFrameShape(QtWidgets.QFrame.HLine)
        self.setFrameShadow(QtWidgets.QFrame.Sunken)


class Settings(QtWidgets.QWidget):
    """Settings widget to customize the scripter panel."""

    def __init__(self):
        """Initialize the Settings instance."""
        super(Settings, self).__init__()
        self.build_ui()

    def build_ui(self):
        """Build ui."""
        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        """Create widgets."""
        self.check_tooltips = QtWidgets.QCheckBox("Tooltips")
        self.check_command_tooltips = QtWidgets.QCheckBox("Command tooltips")
        self.check_auto_clear_command = QtWidgets.QCheckBox(
            "Clear input after successful command execution")
        self.check_auto_close_script = QtWidgets.QCheckBox(
            "Close scripter after successful script execution")
        self.check_auto_close_command = QtWidgets.QCheckBox(
            "Close scripter after successful quick command execution")
        self.label_lang_new_commands = QtWidgets.QLabel(
            "Default language for new commands")
        self.label_command_size = QtWidgets.QLabel("Commands size")
        self.combo_command_size = QtWidgets.QComboBox()
        self.combo_command_size.addItems(COMMAND_SIZE.keys())
        self.combo_lang_new_commands = QtWidgets.QComboBox()
        self.combo_lang_new_commands.addItems([PY, TCL, NODES])
        self.label_stack_root = QtWidgets.QLabel("Stack root")
        self.input_stack_root = QtWidgets.QLineEdit()
        self.button_stack_root = QtWidgets.QToolButton()
        self.button_reveal_stack_root = QtWidgets.QToolButton()
        self.button_reveal_stack_root.setIcon(QtGui.QIcon(ICONS["reveal"]))
        self.button_stack_root.setIcon(QtGui.QIcon(ICONS["folder"]))
        self.button_clear_history = QtWidgets.QPushButton("clear history")
        self.button_close = QtWidgets.QPushButton("save and close")
        self.button_close.setProperty("style", "blue")

    def create_layouts(self):
        """Create signals."""
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_command_size = QtWidgets.QHBoxLayout()
        self.layout_lang_new_commands = QtWidgets.QHBoxLayout()
        self.layout_stack_root = QtWidgets.QHBoxLayout()

        self.layout_lang_new_commands.addWidget(self.label_lang_new_commands)
        self.layout_lang_new_commands.addWidget(self.combo_lang_new_commands)

        self.layout_stack_root.addWidget(self.label_stack_root)
        self.layout_stack_root.addWidget(self.input_stack_root)
        self.layout_stack_root.addWidget(self.button_stack_root)
        self.layout_stack_root.addWidget(self.button_reveal_stack_root)

        self.layout_command_size.addWidget(self.label_command_size)
        self.layout_command_size.addWidget(self.combo_command_size)

        self.layout_main.addWidget(QHLine())
        self.layout_main.addWidget(self.check_tooltips)
        self.layout_main.addWidget(self.check_command_tooltips)
        self.layout_main.addWidget(self.check_auto_clear_command)
        self.layout_main.addWidget(self.check_auto_close_script)
        self.layout_main.addWidget(self.check_auto_close_command)
        self.layout_main.addLayout(self.layout_command_size)
        self.layout_main.addLayout(self.layout_lang_new_commands)
        self.layout_main.addLayout(self.layout_stack_root)
        self.layout_main.addWidget(self.button_clear_history)
        self.layout_main.addStretch()
        self.layout_main.addWidget(self.button_close)

        helper.set_style_sheet(self)
        self.setLayout(self.layout_main)
