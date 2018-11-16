"""This module contains dialog windows classes for multiple occasions."""

# PySide import switch
try:
    from PySide import QtGui as QtWidgets
    from PySide import QtCore
except ImportError:
    from PySide2 import QtWidgets
    from PySide2 import QtCore


# Import local modules
from smartScripter import helper


def show_message_box(window, message):
    """Show message box with message as content.

    Args:
        window (QtWidgets.QWidget): Parent window in order to keep the message
            box on top of the parent window.
        message (str): Message to display in the window.

    """
    msg = QtWidgets.QMessageBox()
    msg.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    msg.information(window, 'information', message)


def ask_dialog(message, process_label="ok", color_process="actionButton",
               cancel_label="cancel"):
    """Create and show ask dialog.

    Args:
        message (str): Message to display.
        process_label (str): Label of process button.
        color_process (str): Color of process button in the format:
            "r,g,b,a"; if set to "actionButton" then this button will become a
            blue button like all actionButton QPushWidgets.
        cancel_label (str): Label of reject button.

    Returns:
        Bool: True if clicked process button, otherwise False.

    """
    msg_box = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Warning,
                                    "QMessageBox.warning()", message,
                                    QtWidgets.QMessageBox.NoButton, None)
    msg_box.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    msg_box.setObjectName("ask_dialog")
    helper.set_style_sheet(msg_box)
    msg_box.raise_()
    process_button = msg_box.addButton(process_label,
                                       QtWidgets.QMessageBox.AcceptRole)
    if color_process != "":
        if color_process == "actionButton":
            color_process = "51, 204, 255, 100"

        style = "QPushButton {background-color: rgba(%s)}" % color_process
        process_button.setStyleSheet(style)
    process_button.clearFocus()
    msg_box.setFocus()
    msg_box.addButton(cancel_label, QtWidgets.QMessageBox.RejectRole)
    return msg_box.exec_() == QtWidgets.QMessageBox.AcceptRole


def show_path_browser(title):
    """Show browser to browse to path and return browsed path.

    Args:
        title (str): Title to display for browser.

    Returns:
        str: Absolute path that was browsed to.

    """
    dialog = QtWidgets.QFileDialog()
    dialog.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
    dialog.setWindowTitle(title)
    dialog.setFileMode(QtWidgets.QFileDialog.Directory)
    dialog.setOption(QtWidgets.QFileDialog.ShowDirsOnly)

    if dialog.exec_() == QtWidgets.QDialog.Accepted:
        return dialog.selectedFiles()[0]
    return ""


class ColorPicker(QtWidgets.QColorDialog):
    """Custom color picker dialog that stores and returns color values."""

    color_changed = QtCore.Signal(tuple)

    def __init__(self, parent=None):
        super(ColorPicker, self).__init__()
        self.setWindowFlags(QtCore.Qt.Widget | QtCore.Qt.WindowStaysOnTopHint)
        self.setOptions(QtWidgets.QColorDialog.DontUseNativeDialog)
        self.setVisible(False)
        self.color = None

    def accept(self):
        """Clicked on OK.

        Save current color as hex decimal value and fire signal.

        """
        super(ColorPicker, self).accept()
        self.color = self.currentColor().name().replace("#", "")
        self.color_changed.emit(self.color)
