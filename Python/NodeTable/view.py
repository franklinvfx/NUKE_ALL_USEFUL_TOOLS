"""Build the widget and stack the models.
"""

# Import built-in modules.
import math

# Import third party modules.
# pylint: disable=import-error
import nuke

# Keeping this for development to enable auto-completion.
# pylint: disable=no-name-in-module
if __name__ == '__main__':
    from PySide2 import QtCore, QtGui, QtWidgets
    __binding__ = 'PySide2'
else:
    from Qt import QtCore, QtGui, QtWidgets, __binding__

# Import internal modules.
# pylint: disable=wrong-import-position
from NodeTable import knob_editors
from NodeTable import nuke_utils
from NodeTable import model as models
from NodeTable import constants


class KnobsItemDelegate(QtWidgets.QStyledItemDelegate):
    """Delegate that offer custom editors for various nuke.Knob classes."""

    def __init__(self, parent):
        super(KnobsItemDelegate, self).__init__()
        self.parent = parent

    # pylint: disable=invalid-name
    def createEditor(self, parent, option, index):
        """

        Args:
            parent (QtWidgets.QWidget): parent widget
            option (QtWidget.QStyleOptionViewItem):
            index (QtCore.QModelIndex): current index

        Returns:
            new editor
        """
        model = index.model() # type: models.NodeTableModel
        # row = index.row() # type: int
        # column = index.column() # type: int

        knob = model.data(index, QtCore.Qt.UserRole)

        if isinstance(knob, (nuke.Array_Knob, nuke.Transform2d_Knob)):
            rows = 1
            if isinstance(knob, nuke.AColor_Knob):
                return knob_editors.ColorEditor(parent)

            elif isinstance(knob, nuke.Boolean_Knob):
            #    return QtWidgets.QCheckBox()
                return super(KnobsItemDelegate, self).createEditor(parent,
                                                                   option,
                                                                   index)

            elif isinstance(knob, nuke.Enumeration_Knob):

                combobox = QtWidgets.QComboBox(parent)
                for value in knob.values():
                    combobox.addItem(value)
                return combobox

            elif isinstance(knob, nuke.IArray_Knob):
                rows = knob.height()  # type: int

            elif isinstance(knob, nuke.Transform2d_Knob):
                rows = math.sqrt(len(model.data(index, QtCore.Qt.EditRole)))

            if isinstance(model.data(index, QtCore.Qt.EditRole),
                          (list, tuple)):
                items = len(model.data(index, QtCore.Qt.EditRole))
                return knob_editors.ArrayEditor(parent,
                                                items,
                                                rows)
        if isinstance(knob, nuke.Format_Knob):

            combobox = QtWidgets.QComboBox(parent)
            for format in nuke.formats():
                combobox.addItem(format.name())
            return combobox

        return super(KnobsItemDelegate, self).createEditor(parent,
                                                           option,
                                                           index)

    # pylint: disable=invalid-name
    def setEditorData(self, editor, index):
        """sets editor to knobs value

        Args:
            editor (QtWidgets.QWidget):
            index (QtCore.QModelIndex): current index

        Returns: None
        """

        model = index.model() # type: model.NodeTableModel
        data = model.data(index, QtCore.Qt.EditRole)

        # Array knobs:
        if isinstance(data, (list, tuple)):
            editor.set_editor_data(data)
        else:
            super(KnobsItemDelegate, self).setEditorData(editor, index)

    # pylint: disable=invalid-name
    def setModelData(self, editor, model, index):
        """sets new value to model

        Args:
            editor (knob_editors.QWidget):
            model (QtCore.QAbstractTableModel):
            index (QtCore.QModelIndex): current index

        Returns:
            None

        """

        model = index.model() # type: model.NodeTableModel

        knob = model.data(index, QtCore.Qt.UserRole)
        data = None

        # Array knobs:
        if isinstance(knob, (nuke.Array_Knob, nuke.Transform2d_Knob)):

            if isinstance(knob, nuke.Boolean_Knob):
                super(KnobsItemDelegate, self).setModelData(editor,
                                                            model,
                                                            index)

            elif isinstance(knob, nuke.Enumeration_Knob):
                data = editor.currentText()

            elif isinstance(editor, knob_editors.ArrayEditor):
                data = editor.get_editor_data()

            if data:
                model.setData(index, data, QtCore.Qt.EditRole)
            else:
                super(KnobsItemDelegate, self).setModelData(editor,
                                                            model,
                                                            index)
        else:
            super(KnobsItemDelegate, self).setModelData(editor,
                                                        model,
                                                        index)

    # pylint: disable=invalid-name
    def updateEditorGeometry(self, editor, option, index):
        """

        Args:
            editor (QtWidget.QWidget):
            option (QtWidget.QStyleOptionViewItem):
            index (QtCore.QModelIndex): current index

        Returns:
            None
        """
        model = index.model() # type: model.NodeTableModel
        column = index.column() # type: int

        knob = model.data(index, QtCore.Qt.UserRole)
        value = model.data(index, QtCore.Qt.EditRole)

        # Array knobs:
        if isinstance(knob, (nuke.Array_Knob, nuke.Transform2d_Knob)):
            if isinstance(knob, nuke.Boolean_Knob):
                super(KnobsItemDelegate, self).updateEditorGeometry(editor,
                                                                    option,
                                                                    index)
            elif isinstance(knob, nuke.Enumeration_Knob):
                super(KnobsItemDelegate, self).updateEditorGeometry(editor,
                                                                    option,
                                                                    index)
            else:
                rect = option.rect
                if isinstance(value, (list, tuple)):

                    if isinstance(knob, nuke.IArray_Knob):
                        rect.setWidth(constants.EDITOR_CELL_WIDTH *
                                      knob.width())
                        rect.setHeight(constants.EDITOR_CELL_HEIGHT *
                                       knob.height())

                    elif isinstance(knob, nuke.Transform2d_Knob):
                        root = math.sqrt(len(value))
                        width = constants.EDITOR_CELL_WIDTH * root
                        rect.setWidth(width)
                        rect.setHeight(constants.EDITOR_CELL_HEIGHT * root)

                    else:
                        if column == 0:
                            rect.adjust(0, 0, 100, 0)
                        else:
                            rect.adjust(-50, 0, 50, 0)

                editor.setGeometry(rect)
        else:
            super(KnobsItemDelegate, self).updateEditorGeometry(editor,
                                                                option,
                                                                index)

# pylint: disable=invalid-name
class NodeHeaderView(QtWidgets.QHeaderView):
    """This header view selects and zooms to node of clicked header section
    shows properties of node if double clicked
    """

    def __init__(self, orientation=QtCore.Qt.Vertical, parent=None):
        super(NodeHeaderView, self).__init__(orientation, parent)
        if "PySide2" in __binding__:
            self.setSectionsClickable(True)
        elif "PySide" in __binding__:
            self.setClickable(True)
        # noinspection PyUnresolvedReferences

        self.shade_dag_nodes_enabled = nuke_utils.shade_dag_nodes_enabled()

        self.sectionClicked.connect(self.select_node)
        self.sectionDoubleClicked.connect(self.show_properties)

    def paintSection(self, painter, rect, index):
        """Mimic Nuke's way of drawing nodes in DAG.

        Args:
            painter (QtGui.QPainter):
            rect (QtCore.QRect):
            index:

        Returns: None
        """
        painter.save()
        QtWidgets.QHeaderView.paintSection(self, painter, rect, index)
        painter.restore()

        bg_brush = self.model().headerData(index,
                                           QtCore.Qt.Vertical,
                                           QtCore.Qt.BackgroundRole)  # type: QtGui.QBrush

        fg_pen = self.model().headerData(index,
                                         QtCore.Qt.Vertical,
                                         QtCore.Qt.ForegroundRole)  # type: QtGui.QPen

        if self.shade_dag_nodes_enabled:
            gradient = QtGui.QLinearGradient(rect.topLeft(),
                                             rect.bottomLeft())
            gradient.setColorAt(0, bg_brush.color())
            gradient_end_color = models.scalar(bg_brush.color().getRgbF()[:3],
                                               0.6)
            gradient.setColorAt(1, QtGui.QColor.fromRgbF(*gradient_end_color))
            painter.fillRect(rect, gradient)
        else:
            painter.fillRect(rect, bg_brush)

        rect_adj = rect
        rect_adj.adjust(-1, -1, -1, -1)
        painter.setPen(fg_pen)
        text = self.model().headerData(index,
                                       QtCore.Qt.Vertical,
                                       QtCore.Qt.DisplayRole)
        painter.drawText(rect, QtCore.Qt.AlignCenter, text)
        painter.setPen(QtGui.QPen(QtGui.QColor.fromRgbF(0.0, 0.0, 0.0)))
        painter.drawRect(rect_adj)

    def get_node(self, section):
        """returns node at section

        Args:
            section (int): current section

        Returns:
            node (nuke.Node)
        """
        return self.model().headerData(section,
                                       QtCore.Qt.Vertical,
                                       QtCore.Qt.UserRole)

    def select_node(self, section):
        """selects node and zooms node graph

        Args:
            section (int):

        Returns:
            None
        """
        node = self.get_node(section)
        nuke_utils.select_node(node, zoom=1)

    def show_properties(self, section):
        """opens properties bin for node at current section

        Args:
            section (int):

        Returns:
            None
        """
        node = self.get_node(section)
        nuke.show(node)


class NodeTableView(QtWidgets.QTableView):
    """Table with multi-cell editing
    """

    def __init__(self, parent=None):
        super(NodeTableView, self).__init__(parent)
        self.setAlternatingRowColors(True)
        self.setSortingEnabled(True)

        self.delegate = KnobsItemDelegate(self)
        self.setItemDelegate(self.delegate)

        self.setHorizontalScrollMode(QtWidgets.QTableView.ScrollPerPixel)
        self.setVerticalScrollMode(QtWidgets.QTableView.ScrollPerPixel)

        self.nodes_header = NodeHeaderView(QtCore.Qt.Vertical, parent)
        self.setVerticalHeader(self.nodes_header)

    def mouseReleaseEvent(self, event):
        """enter edit mode after single click

        Necessary for multi cell editing
        Args:
            event (QtCore.QEvent): mouse event

        Returns:
            None
        """
        if event.button() == QtCore.Qt.LeftButton:
            index = self.indexAt(event.pos())
            self.edit(index)
        if event.button() == QtCore.Qt.RightButton:
            # TODO: implement right click options
            pass

        super(NodeTableView, self).mouseReleaseEvent(event)

    def commitData(self, editor):
        """Set the current editor data to the model for the whole selection.

        Args:
            editor:

        Returns:
            None
        """
        # call parent commitData first
        super(NodeTableView, self).commitData(editor)

        # self.currentIndex() is the QModelIndex of the cell just edited
        _model = self.currentIndex().model()
        # get the value that the user just submitted
        value = _model.data(self.currentIndex(), QtCore.Qt.EditRole)

        _row, _column = self.currentIndex().row(), self.currentIndex().column()

        # selection is a list of QItemSelectionRange instances
        for isr in self.selectionModel().selection():
            rows = range(isr.top(), isr.bottom() + 1)
            for row in rows:
                if row != _row:
                    # row,curCol is also in the selection. make an index:
                    idx = _model.index(row, _column)
                    # so we can apply the same value change
                    _model.setData(idx, value, QtCore.Qt.EditRole)


class MultiCompleter(QtWidgets.QCompleter):
    """QCompleter that supports completing multiple words in a QLineEdit,
        separated by delimiter.

    Args:
        model_list (QtCore.QStringListModel or list): complete these words
        delimiter (str): separate words by this string (optional, default: ",")
    """
    def __init__(self, model_list=None, delimiter=","):
        super(MultiCompleter, self).__init__(model_list)
        self.setCompletionMode(QtWidgets.QCompleter.InlineCompletion)
        self.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.delimiter = delimiter

    def pathFromIndex(self, index):
        """Complete the input

        Args:
            index (QtCore.QModelIndex):

        Returns:
            str: completed input
        """
        path = super(MultiCompleter, self).pathFromIndex(index)
        lst = str(self.widget().text()).split(self.delimiter)
        if len(lst) > 1:
            path = '%s%s %s' % (self.delimiter.join(lst[:-1]),
                                self.delimiter, path)
        return path

    def splitPath(self, path):
        """Split and strip the input

        Args:
            path (str):

        Returns:
            str
        """
        path = str(path.split(self.delimiter)[-1]).lstrip(' ')
        return [path]


# pylint: disable=too-few-public-methods
class KeepOpenMenu(QtWidgets.QMenu):
    """Menu that stays open to allow multiple selections

    Warnings: broken atm, manu actually doesn't stay open
    """
    # TODO: keep menu open

    def eventFilter(self, obj, event):
        """Eat the mouse event but trigger the objects action.

        Args:
            obj:
            event:

        Returns:
            bool
        """
        if event.type() in [QtCore.QEvent.MouseButtonRelease]:
            if isinstance(obj, QtWidgets.QMenu):
                if obj.activeAction():
                    # if the selected action does not have a submenu
                    if not obj.activeAction().menu():

                        # eat the event, but trigger the function
                        obj.activeAction().trigger()
                        return True
        return super(KeepOpenMenu, self).eventFilter(obj, event)


# pylint: disable=too-few-public-methods
class CheckAction(QtWidgets.QAction):
    """Creates a checkable QAction

    Args:
        text (str): text to display on QAction
        parent (QtWidgets.QWidget): parent widget (optional)
    """
    def __init__(self, text, parent=None):
        super(CheckAction, self).__init__(text, parent)
        self.setCheckable(True)


# pylint: disable=line-too-long, too-many-instance-attributes
class NodeTableWidget(QtWidgets.QWidget):
    """Creates the GUI for the table view and filtering

    Filtering is achieved by stacking multiple custom QSortFilterProxyModels.
    The node list and filters are accessible through pythonic properties.

    Examples:
        from NodeTable import view
        table = view.NodeTableWidget()
        table.node_list = nuke.selectedNodes()
        table.node_class_filter = 'Merge2, Blur'

    Args:
        node_list (list): list of nuke.Node nodes (optional).
        parent (QtGui.QWidget): parent widget (optional)
    """

    def __init__(self, node_list=None, parent=None):
        super(NodeTableWidget, self).__init__(parent)

        # Widget
        self.setWindowTitle('Node spreadsheet')

        # Variables:
        self._node_classes = []
        self._node_list = []  # make sure it's iterable
        self._node_names = []
        self._knob_names = []
        self._hidden_knobs = False
        self._all_knob_states = False
        self._disabled_knobs = False
        self._grouped_nodes = False
        self._knob_name_filter = None
        self._node_name_filter = None
        self._node_class_filter = None
        self._node_class_filter = None

        # Content
        # TODO: untangle this bad mix of ui and controller functions.
        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.menu_bar = QtWidgets.QMenuBar(self)
        # show menubar in parents window for osx and some linux dists
        self.menu_bar.setNativeMenuBar(False)

        self.load_selected_action = QtWidgets.QAction('Load selected Nodes',
                                                      self.menu_bar)
        self.menu_bar.addAction(self.load_selected_action)
        self.load_selected_action.triggered.connect(self.load_selected)

        self.show_menu = KeepOpenMenu('Show')  # type: QtWidgets.QMenu
        self.menu_bar.addMenu(self.show_menu)
        self.knobs_menu = KeepOpenMenu('Knobs')  # type: QtWidgets.QMenu
        self.show_menu.addMenu(self.knobs_menu)

        self.all_knobs_action = CheckAction('all', self.knobs_menu)
        self.knobs_menu.addAction(self.all_knobs_action)
        self.all_knobs_action.triggered[bool].connect(self.all_knob_states_changed)

        self.knobs_menu.addSeparator()

        self.hidden_knobs_action = CheckAction('hidden', self.knobs_menu)
        self.knobs_menu.addAction(self.hidden_knobs_action)
        self.hidden_knobs_action.triggered[bool].connect(self.hidden_knobs_changed)

        self.disabled_knobs_action = CheckAction('disabled')
        self.knobs_menu.addAction(self.disabled_knobs_action)
        self.disabled_knobs_action.triggered[bool].connect(self.disabled_knobs_changed)

        self.nodes_menu = self.show_menu.addMenu('Nodes')
        self.grouped_nodes_action = CheckAction('grouped')
        self.nodes_menu.addAction(self.grouped_nodes_action)
        self.grouped_nodes_action.triggered[bool].connect(self.grouped_nodes_changed)

        # Filter Widget
        self.filter_widget = QtWidgets.QWidget(self)
        self.filter_layout = QtWidgets.QHBoxLayout(self.filter_widget)
        self.filter_layout.setContentsMargins(0, 0, 0, 0)
        self.filter_widget.setLayout(self.filter_layout)

        # Filter by node class:
        self.node_class_filter_label = QtWidgets.QLabel('node: class:')
        self.filter_layout.addWidget(self.node_class_filter_label)
        self.node_class_filter_line_edit = QtWidgets.QLineEdit(self.filter_widget)
        self.node_class_completer = MultiCompleter(self.node_classes)
        self.node_class_model = self.node_class_completer.model()
        self.node_class_filter_line_edit.setCompleter(self.node_class_completer)
        self.node_class_filter_line_edit.textChanged.connect(self.node_class_filter_changed)
        self.filter_layout.addWidget(self.node_class_filter_line_edit)

        # Filter by node name:
        self.node_name_filter_label = QtWidgets.QLabel('name:')
        self.filter_layout.addWidget(self.node_name_filter_label)
        self.node_name_filter_line_edit = QtWidgets.QLineEdit()
        self.node_name_filter_label.setAcceptDrops(True)
        self.node_name_completer = MultiCompleter(self.node_names)
        self.node_name_model = self.node_name_completer.model()
        self.node_name_filter_line_edit.setCompleter(self.node_name_completer)
        self.node_name_filter_line_edit.textChanged.connect(self.node_name_filter_changed)
        self.filter_layout.addWidget(self.node_name_filter_line_edit)

        self.filter_separator_knobs = QtWidgets.QFrame(self.filter_widget)
        self.filter_separator_knobs.setFrameShape(QtWidgets.QFrame.VLine)
        self.filter_layout.addWidget(self.filter_separator_knobs)

        # Filter by knob name:
        self.knob_filter_label = QtWidgets.QLabel('knob: name')
        self.filter_layout.addWidget(self.knob_filter_label)

        self.knob_name_filter_line_edit = QtWidgets.QLineEdit()
        self.knob_name_filter_line_edit.setAcceptDrops(True)
        self.knob_name_filter_completer = MultiCompleter(self.knob_names)
        self.knob_name_filter_model = self.knob_name_filter_completer.model()
        self.knob_name_filter_line_edit.setCompleter(self.knob_name_filter_completer)
        self.knob_name_filter_line_edit.textChanged.connect(self.knob_name_filter_changed)
        self.filter_layout.addWidget(self.knob_name_filter_line_edit)

        self.layout.addWidget(self.menu_bar)
        self.layout.addWidget(self.filter_widget)

        self.table_view = NodeTableView(self)

        self.table_model = models.NodeTableModel()
        self.layout.addWidget(self.table_view)

        # Filter disabled or enabled knobs:
        self.knob_states_filter_model = models.KnobStatesFilterModel(self)
        self.knob_states_filter_model.setSourceModel(self.table_model)
        self.disabled_knobs = True
        self.hidden_knobs = False

        # Filter by Node name
        self.node_name_filter_model = models.NodeNameFilterModel(self)
        self.node_name_filter_model.setSourceModel(self.knob_states_filter_model)
        # self.node_name_filter_model.setSourceModel(self.table_model)

        # Filter by Node Class:
        self.node_class_filter_model = models.NodeClassFilterModel(self)
        self.node_class_filter_model.setSourceModel(self.node_name_filter_model)

        # Filter by knob name:
        self.knob_name_filter_model = models.HeaderHorizontalFilterModel(self)
        self.knob_name_filter_model.setSourceModel(self.node_class_filter_model)

        # Filter empty columns
        self.empty_column_filter_model = models.EmptyColumnFilterModel(self)
        self.empty_column_filter_model.setSourceModel(self.knob_name_filter_model)

        # Set model to view
        self.table_view.setModel(self.empty_column_filter_model)

        # Load given node list
        self.node_list = node_list or []

    def load_selected(self):
        """Sets the node list to current selection.

        Returns:
            None
        """

        self.node_list = nuke_utils.get_selected_nodes(self.grouped_nodes)

    @property
    def node_names(self):
        """list[str]: sorted list of current nodes
        names.

        """
        node_names = [node.name() for node in self.node_list]
        return sorted(node_names, key=lambda n: n.lower())

    @property
    def node_classes(self):
        """list[str]: sorted list of node classes

        If node_list is set, classes are updated to include only
        classes of current nodes else all possible node classes are returned.
        """
        if self.node_list:
            node_classes = set()
            for node in self.node_list:
                node_classes.add(node.Class())
        else:
            node_classes = nuke_utils.get_node_classes(no_ext=True)
        return sorted(list(node_classes), key=lambda s: s.lower())

    @property
    def knob_names(self):
        """list[str]: all knob names of current nodes.
        """
        knob_names = set()
        for node in self.node_list:
            for knob in node.knobs():
                knob_names.add(knob)
        self._knob_names = sorted(list(knob_names), key=lambda s: s.lower())
        return self._knob_names

    @property
    def node_list(self):
        """list[nuke.Node]: List of loaded nodes before all filtering.

        Setting this attribute updates all models and warns when loading too
        many nodes.
        """
        self._node_list = [node for node in self._node_list
                           if nuke_utils.node_exists(node)]
        return self._node_list

    @node_list.setter
    def node_list(self, nodes):
        num_nodes = len(nodes)

        # Ask for confirmation before loading too many nodes.
        if num_nodes > constants.NUM_NODES_WARN_BEFORE_LOAD:
            proceed = nuke_utils.ask('Loading {num_nodes} Nodes may take a '
                                     'long time. \n'
                                     'Dou you wish to proceed?'.format(
                                         num_nodes=num_nodes))

            if not proceed:
                return

        self._node_list = nodes or []
        self.table_model.node_list = self.node_list

        self.node_name_completer.setModel(
            QtCore.QStringListModel(self.node_names))
        self.node_class_completer.setModel(
            QtCore.QStringListModel(self.node_classes))
        self.knob_name_filter_completer.setModel(
            QtCore.QStringListModel(self.knob_names))

        self.table_view.resizeColumnsToContents()

    @QtCore.Slot(bool)
    def grouped_nodes_changed(self, checked=None):
        """Update the hidden knobs state filter.

        Args:
            checked (bool): If True, knobs with hidden state are displayed.

        Returns:
            None
        """
        # PySide doesn't pass checked state
        if checked is None:
            checked = self.grouped_nodes_action.isChecked()
        self.grouped_nodes = checked
        self.table_view.resizeColumnsToContents()

    @property
    def grouped_nodes(self):
        """bool: Show selected nodes inside of group nodes."""
        return self._grouped_nodes

    @grouped_nodes.setter
    def grouped_nodes(self, checked):
        self._grouped_nodes = checked
        self.load_selected()
        self.grouped_nodes_action.setChecked(checked)

    @QtCore.Slot(bool)
    def hidden_knobs_changed(self, checked=None):
        """Update the hidden knobs state filter.

        Args:
            checked (bool): If True, knobs with hidden state are displayed.

        Returns:
            None
        """
        # PySide doesn't pass checked state
        if checked is None:
            checked = self.hidden_knobs_action.isChecked()
        self.hidden_knobs = checked
        self.table_view.resizeColumnsToContents()

    @property
    def hidden_knobs(self):
        """bool: Show hidden knobs."""
        return self._hidden_knobs

    @hidden_knobs.setter
    def hidden_knobs(self, checked):

        self._hidden_knobs = checked
        self.knob_states_filter_model.hidden_knobs = checked
        self.table_view.resizeColumnsToContents()
        self.hidden_knobs_action.setChecked(checked)

    @QtCore.Slot(bool)
    def disabled_knobs_changed(self, checked=None):
        """Update the disabled knobs state filter.

        Args:
            checked (bool): If True, knobs with disabled state are displayed.

        Returns:
            None
        """
        # PySide doesn't pass checked state
        if checked is None:
            checked = self.disabled_knobs_action.isChecked()
        self.disabled_knobs = checked
        self.table_view.resizeColumnsToContents()

    @property
    def disabled_knobs(self):
        """bool: Show disabled knobs."""
        return self._disabled_knobs

    @disabled_knobs.setter
    def disabled_knobs(self, checked=None):
        self._disabled_knobs = checked
        self.knob_states_filter_model.disabled_knobs = checked
        self.table_view.resizeColumnsToContents()
        self.disabled_knobs_action.setChecked(checked)
        self.update_all_knob_states_action()

    @QtCore.Slot(bool)
    def all_knob_states_changed(self, checked=True):
        """Update the knob states filter.

        Args:
            checked: If True, show knobs with hidden or disabled state.

        Returns:
            None
        """
        # PySide doesn't pass checked state
        if checked is None:
            checked = self.all_knobs_action.isChecked()
        self.all_knob_states = checked
        self.table_view.resizeColumnsToContents()

    @property
    def all_knob_states(self):
        """bool: Knobs with hidden or disabled knob states are displayed."""
        self._all_knob_states = self.hidden_knobs and self._disabled_knobs
        return self._all_knob_states

    @all_knob_states.setter
    def all_knob_states(self, checked=None):
        self._all_knob_states = checked
        self.hidden_knobs = checked
        self.disabled_knobs = checked

    def update_all_knob_states_action(self):
        """Update action (checkbox) 'All' knob states.

        Returns:
            None
        """
        self.all_knobs_action.setChecked(all([self.hidden_knobs,
                                              self.disabled_knobs]))

    @QtCore.Slot(str)
    def knob_name_filter_changed(self, value=None):
        """Update the knob name filter.

        Args:
            value (str): list of knob names to display.

        Returns:
            None
        """
        if not value:
            value = self.knob_name_filter_line_edit.text()
        self.knob_name_filter = value
        self.table_view.resizeColumnsToContents()

    @property
    def knob_name_filter(self):
        """str: list of knob names separated by delimiters."""
        return self._knob_name_filter

    @knob_name_filter.setter
    def knob_name_filter(self, filter_str=None):
        if filter_str is None:
            filter_str = self.knob_name_filter_line_edit.text()
        else:
            self.knob_name_filter_line_edit.setText(filter_str)
        self._knob_name_filter = filter_str
        self.knob_name_filter_model.set_filter_str(filter_str)

    @property
    def node_name_filter(self):
        """str: list of node names seperated by delimiters.
        """
        return self._node_name_filter

    @node_name_filter.setter
    def node_name_filter(self, node_names=None):
        self._node_name_filter = node_names
        self.node_name_filter_model.set_filter_str(node_names)
        self.empty_column_filter_model.invalidateFilter()

    @QtCore.Slot(str)
    def node_name_filter_changed(self, node_names):
        """Update the node names filter.

        Args:
            node_names (str): list of node names separated by delimiter.

        Returns:
            None
        """
        if not node_names:
            node_names = self.node_name_filter_line_edit.text()
        self.node_name_filter = node_names
        self.table_view.resizeColumnsToContents()

    @property
    def node_class_filter(self):
        """str: List of node classes to display.
        """
        return self._node_class_filter

    @node_class_filter.setter
    def node_class_filter(self, node_classes=None):
        self._node_class_filter = node_classes
        self.node_class_filter_model.set_filter_str(node_classes)
        self.empty_column_filter_model.invalidateFilter()

    @QtCore.Slot(str)
    def node_class_filter_changed(self, node_classes=None):
        """Update the node class filter.

        Args:
            node_classes (str): delimited str list of node Classes to display.

        Returns:
            None
        """
        if not node_classes:
            node_classes = self.node_class_filter_line_edit.text()
        self.node_class_filter = node_classes
        self.table_view.resizeColumnsToContents()
