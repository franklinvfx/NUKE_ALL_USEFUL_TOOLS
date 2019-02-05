"""This module provides the about window to show tool about information."""

# Import built-in modules
import datetime

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
from smartScripter import controller
from smartScripter import helper
from smartScripter.info import (__version__, __author__, __web__, __mail__,
                                __product__)

# Constants
ABOUT_WINDOW = None
ICONS = helper.load_icons()


class About(QtWidgets.QWidget):
    """About window that shows the about information for this tool."""

    def __init__(self):
        """Initialize About instance."""
        super(About, self).__init__()
        self.setWindowTitle("about {}".format(__product__))
        self.setObjectName("about")
        self.setWindowIcon(QtGui.QIcon(ICONS["logo"]))

        self.build_ui()

    def build_ui(self):
        """Build user interface."""
        self.create_widgets()
        self.create_layouts()

    def create_widgets(self):
        """Create widgets."""
        self.help_img = QtWidgets.QLabel()
        about = QtGui.QImage(ICONS["about"])
        self.help_img.setPixmap(QtGui.QPixmap.fromImage(about))

        # Load authorme info.
        authorme = "Simon Jokuschie<br />"

        info = "{product} v{version}<br />" \
               "(c) {year} {author}<br />{authorme}<br />" \
               "{web}<br />" \
               "email: {mail}<br /><br />" \
               "For more tools please visit {web}"

        info = info.format(product=__product__, version=__version__,
                           year=datetime.date.today().year, author=__author__,
                           authorme=authorme, web=__web__, mail=__mail__)

        self.help_info = QtWidgets.QTextEdit(info)

        self.help_info.setReadOnly(True)
        self.help_info.setMaximumHeight(120)
        self.help_push_web = QtWidgets.QPushButton("Watch In Depth Tutorial")
        self.help_push_web.setProperty("style", "blue")
        self.push_uninstall = QtWidgets.QPushButton("uninstall {}".format(
            __product__))
        self.push_uninstall.setProperty("color", "red")
        self.help_push_close = QtWidgets.QPushButton("close")

        # License info
        self.help_lic = QtWidgets.QTextEdit()
        self.help_lic.setReadOnly(True)
        self.help_lic.setMaximumHeight(60)
        self.help_lic.setObjectName("text_info")

        self.help_lic.setText("No license required")

    def create_layouts(self):
        """Create layouts."""
        self.help_layout_top = QtWidgets.QHBoxLayout()
        self.help_layout_info = QtWidgets.QVBoxLayout()
        self.help_layout_widgets = QtWidgets.QVBoxLayout()
        self.help_layout_push = QtWidgets.QHBoxLayout()
        self.help_layout_top.addWidget(self.help_img)
        self.help_layout_info.addWidget(self.help_info)
        self.help_layout_info.addWidget(self.help_lic)
        self.help_layout_info.addWidget(self.push_uninstall)
        self.help_layout_top.addLayout(self.help_layout_info)
        self.help_layout_widgets.addLayout(self.help_layout_top)
        self.help_layout_widgets.addWidget(self.help_push_web)
        self.help_layout_widgets.addLayout(self.help_layout_push)
        self.help_layout_widgets.addStretch()
        self.help_group = QtWidgets.QGroupBox()
        self.help_group.setLayout(self.help_layout_widgets)
        self.help_layout_main = QtWidgets.QVBoxLayout()

        self.help_layout_main.addWidget(self.help_group)
        self.help_layout_main.addWidget(self.help_push_close)

        self.setLayout(self.help_layout_main)
        self.help_push_close.setFocus()
        helper.set_style_sheet(self)
        self.help_info.setFocus()

    def keyPressEvent(self, event):
        """Overwrite keyPressEvent to close the window when hitting escape."""
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


def show_about():
    """Shot about window."""
    # We need to make this global in here otherwise Nuke won't show the window.
    global ABOUT_WINDOW  # pylint: disable=global-statement

    # Make sure there exists only one about panel present at a time. Close the
    # panel if it already exists.
    try:
        ABOUT_WINDOW.close()
        del ABOUT_WINDOW
    # Catch all exceptions to ensure that we always pass, no matter what.
    except Exception:  # pylint: disable=broad-except
        pass

    ABOUT_WINDOW = About()
    ABOUT_WINDOW.show()
    ABOUT_WINDOW.raise_()

    controller.AboutController(ABOUT_WINDOW)
