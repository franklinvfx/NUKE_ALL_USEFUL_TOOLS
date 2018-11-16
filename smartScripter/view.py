"""Viewer module containing the main UI and other ui elements."""

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
from smartScripter import helper
from smartScripter import widgets

# Constants
ICONS = helper.load_icons()


class ScripterView(QtWidgets.QWidget):
    """Scripter main panel."""

    registered_new_command = QtCore.Signal()

    def __init__(self, floating):
        """Initialize the ScripterPanel widget."""
        super(ScripterView, self).__init__()

        self.floating = floating
        self.language = "py"
        self.clipboard = QtGui.QClipboard()

        self.set_up()
        self.build_ui()

    def set_up(self):
        """Set up the viewer widget."""
        self.setWindowTitle("smartScripter")
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setMinimumWidth(700)

        if self.floating:
            self.setMaximumHeight(50)

    def build_ui(self):
        """Build ui for the viewer widget."""
        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        """Create all widgets."""
        self.combo_stack = QtWidgets.QComboBox()
        self.button_refresh = QtWidgets.QToolButton()
        self.button_refresh.setIcon(QtGui.QIcon(ICONS["refresh"]))
        self.button_toggle_command = QtWidgets.QToolButton()
        self.button_toggle_command.setIcon(QtGui.QIcon(ICONS["command"]))
        self.button_settings = QtWidgets.QToolButton()
        self.button_settings.setIcon(QtGui.QIcon(ICONS["settings"]))
        self.scripts_table = widgets.ScriptsTable()
        self.button_language = QtWidgets.QPushButton(self.language)
        self.button_language.setVisible(False)
        self.button_language.setProperty("style", "simple")
        self.input_command = widgets.CommandInput()
        self.input_command.setVisible(False)
        self.settings_panel = widgets.Settings()
        self.settings_panel.setVisible(False)

    def create_layouts(self):
        """Create layouts."""
        self.layout_top = QtWidgets.QHBoxLayout()
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_bottom = QtWidgets.QHBoxLayout()

        self.layout_main.addLayout(self.layout_top)
        self.layout_main.addWidget(self.scripts_table)
        self.layout_main.addLayout(self.layout_bottom)

        self.layout_main.addWidget(self.settings_panel)

        self.layout_top.addWidget(self.combo_stack)
        self.layout_top.addStretch()
        self.layout_top.addWidget(self.button_toggle_command)
        self.layout_top.addWidget(self.button_refresh)
        self.layout_top.addWidget(self.button_settings)

        self.layout_bottom.addWidget(self.button_language, 1)
        self.layout_bottom.addWidget(self.input_command, 9)

        helper.set_style_sheet(self)
        self.setLayout(self.layout_main)

    def keyPressEvent(self, event):
        """Catch keyPressEvent to execute custom events."""
        super(ScripterView, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Escape and self.floating:
            self.close()


class RegisterCommandView(QtWidgets.QWidget):
    """Panel to store the currently dropped command.

    In here the user can set a name, color, icon and shortcut for the command.

    """

    def __init__(self, scripter_panel, command_widget=None):
        """Initialize the StoreCommand instance.

        Args:
            scripter_panel (scripter.view.ScripterView): The ScripterPanel
                instance to update when successfully registered a new command.
            command_widget (smartScripter.widgets.CommandWidget): If set then
                we are giving the window the CommandWidget to edit. We can
                thus draw the needed information from this instance in order
                to set up our RegisterCommandView instance.

        """
        super(RegisterCommandView, self).__init__()

        self.scripter_panel = scripter_panel
        self.command_widget = command_widget

        self.text_inserted = False

        self.setup()
        self.build_ui()

    def setup(self):
        """Set up window."""
        self.setMinimumSize(QtCore.QSize(400, 300))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def build_ui(self):
        """Build ui."""
        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        """Create widgets."""
        self.input_name = QtWidgets.QLineEdit()
        self.input_name.setPlaceholderText("name")
        self.combo_language = QtWidgets.QComboBox()
        self.button_icon = QtWidgets.QToolButton()
        self.button_icon.setIcon(QtGui.QIcon(ICONS["command"]))
        self.button_color = QtWidgets.QToolButton()
        self.button_color.setIcon(QtGui.QIcon(ICONS["color"]))
        self.text_command = QtWidgets.QTextEdit()
        self.button_save = QtWidgets.QPushButton("save")
        self.button_save.setProperty("style", "blue")

    def create_layouts(self):
        """Create layouts."""
        self.layout_main = QtWidgets.QVBoxLayout()
        self.layout_top = QtWidgets.QHBoxLayout()

        self.layout_main.addLayout(self.layout_top)
        self.layout_main.addWidget(self.text_command)
        self.layout_main.addWidget(self.button_save)

        self.layout_top.addWidget(self.input_name, 7)
        self.layout_top.addWidget(self.combo_language, 1)
        self.layout_top.addWidget(self.button_icon, 1)
        self.layout_top.addWidget(self.button_color, 1)

        self.setLayout(self.layout_main)
        helper.set_style_sheet(self)
        self.text_command.setFocus()

    def keyPressEvent(self, event):
        """Catch keyPressEvent to execute custom events.

        Pressing escape will close the widget if we are running in floating
        mode.

        """
        super(RegisterCommandView, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

    def remove_color_icon(self):
        """Unset the color icon.

        This is needed when the user has set a color. Then we want to get rid
        of the color icon and instead just show the color.

        """
        self.button_color.setIcon(QtGui.QIcon())

    def update_icon(self, path, icon_name):
        """Update icon to the icon using the given path and set property

        Args:
            path (str): Absolute path of icon to use as new icon.

        """
        icon = QtGui.QIcon(path)
        self.button_icon.setIcon(icon)

        self.button_icon.setProperty("icon_name", icon_name)

    def update_color(self, color):
        """Update color to the given color.

        Args:
            color (str): Color to apply in the given format: "r, g, b".
                Example: "255, 0, 0"
        """
        # If the user has not set any color, then color is of NoneType. In this
        # case we want to show the default color icon instead.
        if not color:
            self.button_color.setIcon(QtGui.QIcon(ICONS["color"]))
            return

        self.button_color.setProperty("color", color)
        style = "QToolButton {background-color: #%s}" % color
        self.button_color.setStyleSheet(style)
        self.remove_color_icon()


class ChooseIconView(QtWidgets.QDialog):
    """Window to choose an icon for the new command.

    This window shows all .png icons that are currently in Nuke's plugin path.
    By pressing on of the icon buttons, the clicked icon will be chosen as the
    command's icon.

    """

    icon_set = QtCore.Signal(str)

    def __init__(self, register_command_view):
        """Initialize the ChooseIconView instance.

        Args:
            register_command_view (scripter.view.RegisterCommandView): Parent
                RegisterCommandView instance to operate on.

        """
        super(ChooseIconView, self).__init__()

        self.register_command_view = register_command_view

        self.icon_paths = helper.get_session_icons()
        self.column_count = 4
        self.icons = []

        self.setup()
        self.build_ui()

    def setup(self):
        """Setup ui."""
        self.setWindowTitle("Choose Icon")
        self.resize(QtCore.QSize(445, 700))
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def build_ui(self):
        """Build ui."""
        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        """Create widgets."""
        self.table = QtWidgets.QTableWidget()

        self.table.setColumnCount(self.column_count)
        self.table.setRowCount(len(self.icon_paths) / self.column_count)

        self.table.verticalHeader().hide()
        self.table.horizontalHeader().hide()
        self.table.setShowGrid(False)
        self.table.setSelectionMode(QtWidgets.QTableWidget.NoSelection)

        button = None
        for icon_path in self.icon_paths:
            button = QtWidgets.QToolButton()
            button.setProperty("path", icon_path)
            button.setIcon(QtGui.QIcon(icon_path))
            self.icons.append(button)
            button.clicked.connect(
                lambda path=button.property("path"): self.set_icon(path))

        self.button_cancel = QtWidgets.QPushButton("Cancel")

    def set_icon(self, path):
        """Emit the icon set signal so that the icon will be updated."""
        self.icon_set.emit(path)

    def create_layouts(self):
        """Create layouts."""
        self.layout_main = QtWidgets.QVBoxLayout()

        row = 0
        column = 0
        for icon in self.icons:
            self.table.setCellWidget(row, column, icon)

            column += 1
            if column > 3:
                column = 0
                row += 1

        self.layout_main.addWidget(self.table)
        self.layout_main.addWidget(self.button_cancel)

        self.setLayout(self.layout_main)
        helper.set_style_sheet(self)


class NewStack(QtWidgets.QWidget):
    """Window to create a new Stack."""

    def __init__(self, scripter_view):
        """Initialize the NewStack instance.

        ArgS:
            scripter_view (scripter.view.ScripterView): ScripterView instance
                to update when a new stack has been created.

        """
        super(NewStack, self).__init__()

        self.scripter_view = scripter_view

        self.setup()
        self.build_ui()

    def setup(self):
        """Set up the NewStack instance."""
        self.setWindowTitle("New Stack")
        self.setMinimumWidth(300)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

    def build_ui(self):
        """Build ui."""
        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        """Create widgets."""
        self.input_stack_name = QtWidgets.QLineEdit()
        self.input_stack_name.setProperty("style", "tall")
        self.button_create = QtWidgets.QPushButton("create")
        self.button_create.setProperty("style", "blue")

    def create_layouts(self):
        """Create layouts."""
        self.layout_main = QtWidgets.QHBoxLayout()

        self.layout_main.addWidget(self.input_stack_name)
        self.layout_main.addWidget(self.button_create)

        helper.set_style_sheet(self)
        self.setLayout(self.layout_main)
        self.button_create.setFocus()

    def keyPressEvent(self, event):
        """Catch keyPressEvent to execute custom events."""
        super(NewStack, self).keyPressEvent(event)

        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
