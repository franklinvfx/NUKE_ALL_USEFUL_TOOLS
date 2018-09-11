"""Custom knob editors where knobs.

Some knobs need to be translated into custom editor widgets to be editable.
"""

# Import third-party modules.
# pylint: disable=no-name-in-module
from Qt import QtWidgets

# pylint: disable=import-error
import nuke

# Import local modules.
from NodeTable import nuke_utils
from NodeTable import constants


class ArrayEditor(QtWidgets.QGroupBox):
    """Knob editor to allow changing multiple 'channels' of an Array_Knob.

    """

    def __init__(self, parent, length, rows=1):
        super(ArrayEditor, self).__init__(parent)

        self.length = length
        self.rows = rows

        self.layout = QtWidgets.QGridLayout(self)
        self.setLayout(self.layout)

        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setContentsMargins(4, 4, 4, 4)

        self.setAutoFillBackground(True)

        self.double_spin_boxes = []
        for i in range(length):
            spin_box = QtWidgets.QDoubleSpinBox(self)
            spin_box.setMinimumHeight(22)
            spin_box.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
            spin_box.setDecimals(constants.EDITOR_DECIMALS)
            spin_box.setRange(-9999999, 99999999)
            col = i % rows
            row = int(float(i) / self.rows)
            self.layout.addWidget(spin_box, col, row)
            self.double_spin_boxes.append(spin_box)

        self.adjustSize()
        self.raise_()

    def set_editor_data(self, data):
        """set data to editor.

        Args:
            data (float): knob value

        Returns:
            None
        """
        for i, value in enumerate(data):
            self.double_spin_boxes[i].setValue(value)

    def get_editor_data(self):
        """Return the current editor data.

        Returns:
            list,tuple: list of double values
        """
        data = [v.value() for v in self.double_spin_boxes]
        return data


class ColorEditor(ArrayEditor):
    """Editor for the AColor_Knob.

    An extra button allows to pick a new value.
    """

    def __init__(self, parent):
        super(ColorEditor, self).__init__(parent=parent, length=4, rows=1)

        self.pick_button = QtWidgets.QPushButton('c')
        self.pick_button.clicked.connect(self.get_color)
        self.pick_button.setMaximumWidth(32)
        self.layout.addWidget(self.pick_button, 0, 4)

    def get_color(self):
        """Set the editor to a color from nukes floating color picker.

        Returns:
            None
        """
        initial_color_hex = nuke_utils.to_hex(self.get_editor_data())
        new_color = nuke_utils.to_rgb(nuke.getColor(initial_color_hex))
        self.set_editor_data(new_color)
