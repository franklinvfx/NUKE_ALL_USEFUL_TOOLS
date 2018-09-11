"""models to server and filter nodes data to the view

"""
# Import built-in modules
import logging

# Import third-party modules.
# Importing Qt in main to enable auto completion.

if __name__ == '__main__':
    # pylint: disable=import-error
    from PySide2 import QtCore, QtGui, QtWidgets
else:
    # pylint: disable=no-name-in-module, E0611
    from Qt import QtCore, QtGui, QtWidgets

# pylint: disable=import-error, wrong-import-position
import nuke

# Import local modules.
# pylint: disable=wrong-import-position
from NodeTable import nuke_utils
from NodeTable import constants


LOG = logging.getLogger(__name__)


def scalar(tpl, multiplier):
    """multiply each value in tuple by scalar

    Args:
        tpl (tuple):
        scalar (float):

    Returns (tuple):
        tpl * sc
    """

    return tuple([multiplier * t for t in tpl])


def get_palette(widget=None):
    """return the applications palette

    Args:
        widget: current widget (optional)

    Returns:

    """
    app = QtWidgets.QApplication.instance() #tpye: QtWidget.QApplication
    return app.palette(widget)


def bisect_case_insensitive(sorted_list, new_item):
    """Locate the insertion point for new_item to maintain sorted order.

    Taken from https://stackoverflow.com/a/41903429

    Args:
        sorted_list (list): sorted list
        new_item (str): new string to add to list

    Returns:
        int: index at which point new_item must be inserted.
    """
    key = new_item.lower()
    low, high = 0, len(sorted_list)
    while low < high:
        mid = (low + high) // 2
        if key < sorted_list[mid].lower():
            high = mid
        else:
            low = mid + 1
    return low


def find_substring_in_dict_keys(dictionary,
                                key_str,
                                lower=True,
                                first_only=False,
                                substring=True):
    """find keys that include key

    TODO:
        test performance against:
        return list(key for k in d.iterkeys() if key_str in k.lower())

    Args:
        dictionary (dict): search this dictionary
        key_str (str): find this string in keys of dictionary
        lower (bool): case insensitive matching
        first_only (bool): return only first found key
    Returns:
        list: found keys
    """
    result = []
    for key in dictionary.keys():
        if lower:
            key = key.lower()
            key_str = key_str.lower()

        if substring:
            if key_str in key:
                if first_only:
                    return [key]
                else:
                    result.append(key)
        else:
            if key_str == key:
                if first_only:
                    return [key]
                else:
                    result.append(key)
    return result

class KnobStatesFilterModel(QtCore.QSortFilterProxyModel):
    """Filters columns by the knobs flags

    """

    def __init__(self, parent):
        super(KnobStatesFilterModel, self).__init__(parent)

        self._hidden_knobs = False
        self._disabled_knobs = False

    # pylint: disable=invalid-name, unused-argument
    def filterAcceptsColumn(self, column, parent):
        """filter hidden and disabled knobs

        Warning: if this knob is filtered out, but another knob is visible,
        both are hidden.

        @ TODO: filter by row and column using the models flags

        Args:
            column (int): current column
            parent (QtCore.QModelIndex): parent index

        Returns:
            bool: true if shown or false if column is excluded
        """
        knob_name = self.sourceModel().headerData(column,
                                             QtCore.Qt.Horizontal,
                                             QtCore.Qt.UserRole)

        # Return early if this filter when we show knobs of all states.
        if self.hidden_knobs and self.disabled_knobs:
            return True

        for row in range(self.sourceModel().rowCount()):
            node = self.sourceModel().headerData(row, QtCore.Qt.Vertical,
                                                 QtCore.Qt.UserRole)

            # Using knobs() to also get linked knobs.
            knob = node.knobs().get(knob_name)
            if knob:
                accept = knob.visible() or self._hidden_knobs
                accept &= knob.enabled() or self._disabled_knobs

                # Return early if any knob in th column is both visible
                # and enable or filter allow to show the knob.
                if accept:
                    return True

        return False

    @property
    def hidden_knobs(self):
        """hidden knobs filter

        Returns:
            bool: true if hidden knobs are shown
        """
        return self._hidden_knobs

    @hidden_knobs.setter
    def hidden_knobs(self, hidden):
        self._hidden_knobs = hidden
        self.invalidateFilter()

    @property
    def disabled_knobs(self):
        """disabled knobs filter

        Returns:
            bool: true if disabled knobs are shown
        """
        return self._disabled_knobs

    @disabled_knobs.setter
    def disabled_knobs(self, disabled):
        self._disabled_knobs = disabled
        self.invalidateFilter()


class ListFilterModel(QtCore.QSortFilterProxyModel):
    """abstract class that defines how the filter is set

    The derived FilterProxyModel should do substring matching if
    length of filter is 1.
    """

    def __init__(self, parent, filter_delimiter=constants.FILTER_DELIMITER):
        super(ListFilterModel, self).__init__(parent)
        self.filter_list = None
        self.filter_delimiter = filter_delimiter

    def set_filter_str(self, filter_str):
        """set filter as string with delimiter

        Args:
            filter_str (str): filter

        Returns:
            None
        """
        filter_list = [filter_s.strip().lower() for filter_s
                       in filter_str.split(self.filter_delimiter)]
        self.filter_list = filter_list
        self.invalidateFilter()

    def match(self, string):
        """Check if string is in filter_list or if it is substring when
        filtering by one item only.

        Args:
            string (str): match this string against filter

        Returns:
            bool: true if string is in filter_list
        """
        matching = True

        if not self.filter_list:
            return matching

        # Case sensitive filtering is confusing and unnecessary.
        string = string.lower()

        # Check for full name in case filter list is more than one item.
        if len(self.filter_list) > 1:
            matching = string in self.filter_list
        # Check for substring.
        elif len(self.filter_list) == 1:
            matching = self.filter_list[0] in string

        return matching


class HeaderHorizontalFilterModel(ListFilterModel):
    """Filter by knob name

    """

    # pylint: disable=invalid-name, unused-argument
    def filterAcceptsColumn(self, column, parent):
        """filter header with set filter

        Args:
            column (int): current column
            parent (QtCore.QModelIndex():

        Returns:
            bool: true if header matches filter
        """
        if not self.filter_list:
            return True

        header_name = self.sourceModel().headerData(column,
                                                    QtCore.Qt.Horizontal,
                                                    QtCore.Qt.DisplayRole)
        return self.match(header_name)

class NodeNameFilterModel(ListFilterModel):
    """Filter the model by nodename.

    """

    # pylint: disable=invalid-name, unused-argument
    def filterAcceptsRow(self, row, parent):
        """filter header with set filter

        Args:
            row (int): current row
            parent (QtCore.QModelIndex():

        Returns:
            bool: true if header matches filter
        """
        if not self.filter_list:
            return True

        header_name = self.sourceModel().headerData(row,
                                                    QtCore.Qt.Vertical,
                                                    QtCore.Qt.DisplayRole)
        return self.match(header_name)


class NodeClassFilterModel(ListFilterModel):
    """Filter by node classes.

    """

    # pylint: disable=invalid-name, unused-argument
    def filterAcceptsRow(self, row, parent):
        """Filter by node classes.

        Args:
            row (int): current row
            parent (QtCore.QModelIndex): parent index.

        Returns:
            bool: True if node's class matches the filter.
        """
        if not self.filter_list:
            return True
        node = self.sourceModel().headerData(row,
                                             QtCore.Qt.Vertical,
                                             QtCore.Qt.UserRole)
        node_class = node.Class()
        return self.match(node_class)


# pylint: disable=too-few-public-methods
class EmptyColumnFilterModel(QtCore.QSortFilterProxyModel):
    """filter out every empty column

    Notes:
        this Filter is expensive: O=pow(n,2)
    """

    # pylint: disable=invalid-name, unused-argument
    def filterAcceptsColumn(self, column, parent):
        """for every node check if current columns name is in its knobs

        Args:
            column (int): current column
            parent (QtCore.QModelIndex):

        Returns:
            bool: true if at least one node has a knob for current column
        """
        header_name = self.sourceModel().headerData(column,
                                                    QtCore.Qt.Horizontal,
                                                    QtCore.Qt.DisplayRole)

        for row in range(self.sourceModel().rowCount()):
            node = self.sourceModel().headerData(row, QtCore.Qt.Vertical,
                                                 QtCore.Qt.UserRole)
            if header_name in node.knobs():
                return True
        return False


# pylint: disable=invalid-name
class NodeTableModel(QtCore.QAbstractTableModel):
    """Digest and store nodes and serve their data.
    """
    def __init__(self, nodes=None):
        super(NodeTableModel, self).__init__()

        self._node_list = nodes or []  # type: list
        self._knob_list = []  # type: list

        self.palette = get_palette()  # type: QtGui.QPalette

    @property
    def node_list(self):
        """list: Current list of displayed nodes."""
        return self._node_list

    @property
    def node_names(self):
        """list: All names of the current node list."""
        return [node.name() for node in self.node_list]

    @property
    def knob_list(self):
        """list: List of current knob names.

        This list defines the horizontal header.
        To add a knob use insertColumns().

        """
        return self._knob_list

    @property
    def knob_names(self):
        """list:Names of all knobs.

        Note: this property is obsolete at the moment but might be needed
            when implementing header text from knobs label.
        """
        return self.knob_list

    @node_list.setter
    def node_list(self, nodes):
        new_nodes = set(nodes) - set(self.node_list)
        remove_nodes = set(self.node_list) - set(nodes)

        for node in remove_nodes:
            remove_index = self.node_list.index(node)
            self.removeRows(parent=QtCore.QModelIndex(),
                            row=remove_index,
                            count=1)

        for node in new_nodes:
            insert_index = bisect_case_insensitive(self.node_names,
                                                   node.name())
            self.insertRows(parent=QtCore.QModelIndex(),
                            row=insert_index,
                            count=1,
                            items=[node])

    def rowCount(self, parent=QtCore.QModelIndex()):
        """number of nodes

        Args:
            parent (QtCore.QModelIndex): parent index

        Returns:
            int: number of nodes

        """
        if parent.isValid():
            return 0

        if not self.node_list:
            return 0

        return len(self.node_list)

    def columnCount(self, parent):
        """Number of columns.

        Note: When implementing a table based model,
        PySide.QtCore.QAbstractItemModel.columnCount()
        should return 0 when the parent is valid.

        Args:
            parent (QtCore.QModelIndex): parent index

        Returns:
            int: number of columns
        """
        if parent.isValid():
            return 0

        if not self.node_list:
            return 0

        return len(self.knob_list)

    def setup_model_data(self):
        """Read all knob names from set self.node_list to define header.

        First all knobs to display are collected. To match this list, all
        knobs to remove and to add are collected and removed and inserted as
        needed.

        """
        old_header_knobs_names = set(self.knob_names)
        new_header_knobs = {}

        # collect all knobs to display
        # Iterating over copy of the node list to not saw off the tree
        # we're sitting on.
        for node in list(self.node_list):
            # If node was deleted, remove node and return.
            if not nuke_utils.node_exists(node):
                self.removeRows(row=self.node_list.index(node),
                                count=1,
                                parent=QtCore.QModelIndex(),
                                setup_model_data=False)
                # Continue with the next node, since we removed this node.
                continue

            # noinspection PyUnresolvedReferences
            for knob_name, knob in node.knobs().items():
                if knob_name not in new_header_knobs.keys():
                    new_header_knobs[knob_name] = knob

        # collect all knobs to remove
        remove_knobs = []
        for knob_name in self.knob_names:
            if knob_name not in new_header_knobs.keys():
                remove_knobs.append(knob_name)

        # remove all knobs that do not belong to current node selection.
        for knob_name in remove_knobs:
            remove_index = self.knob_names.index(knob_name)
            self.removeColumns(parent=QtCore.QModelIndex(),
                               column=remove_index,
                               count=1)

        # Add all knobs at once, if model is empty
        if not self.knob_list and new_header_knobs:
            # Sort knobs since they are not sorted on addition like below
            new_header_knobs_list = sorted(new_header_knobs.values(),
                                           key=lambda k: k.name().lower())
            self.insertColumns(parent=QtCore.QModelIndex(),
                               column=0,
                               count=len(new_header_knobs_list),
                               items=[knob.name() for
                                      knob in new_header_knobs_list])

        # Insert each knob in sorted order.
        else:
            for knob in new_header_knobs.values():
                if knob.name() in old_header_knobs_names:
                    continue
                header_names = self.knob_names
                insert_index = bisect_case_insensitive(header_names,
                                                       knob.name())
                self.insertColumns(parent=QtCore.QModelIndex(),
                                   column=insert_index,
                                   count=1,
                                   items=[knob.name()])

    def insertColumns(self, column, count, parent, items):
        """Add items to header

        Args:
            parent (QtCore.QModelIndex): parent index
            column: index of new columns
            count (int): number of items to add (ignored)
            item (list): items to add

        Returns:
            bool: True if items added
        """

        count = len(items)
        self.beginInsertColumns(parent,
                                column,
                                column + count - 1)
        for i, item in enumerate(items):
            self._knob_list.insert(column + i, item)
        self.endInsertColumns()
        return True

    def removeColumns(self, column, count, parent):
        """Remove columns

        Args:
            parent (QtCore.QModelIndex): parent index
            first (int): first column to remove
            last (int): last column to remove

        Returns:
            bool: True if successfully removed
        """
        self.beginRemoveColumns(parent, column, column + count - 1)

        for col in reversed(range(column, column + count)):
            self._knob_list.pop(col)
        self.endRemoveColumns()
        return True

    def insertRows(self, row, count, parent, items):
        """Add consecutive rows

        Args:
            parent (QtCore.QModelIndex): parent index
            column: index of new columns
            count (int): number of items to add (ignored)
            item (list): items to add

        Returns:
            bool: True if items added
        """

        count = len(items)
        self.beginInsertRows(parent,
                             row,
                             row + count - 1)
        for i, item in enumerate(items):
            self._node_list.insert(row + i, item)
        self.endInsertRows()

        self.setup_model_data()

        return True

    def removeRows(self, row, count, parent, setup_model_data=True):
        """Remove consecutive rows.

        Args:
            row (int): first row to remove
            count (int): number of rows to remove
            parent (QtCore.QModelIndex): parent index
            setup_model_data (bool): setup model after removing row.
                Disable to avoid recursion.

        Returns:
            bool: True if successfully removed.
        """
        self.beginRemoveRows(parent, row, row + count - 1)
        LOG.debug('Removing rows: %s to %s.', row, row + count - 1)
        for i in reversed(range(row, row + count)):
            self._node_list.pop(i)
        self.endRemoveRows()

        # Update horizontal header.
        if setup_model_data:
            self.setup_model_data()
        return True

    def get_background_color(self, row, node, knob):
        """Return the cell color.

        If a knob is animated, return colors matching Nuke's property panel.
        Else blend the nodes color with the apps palette color at certain
        amounts, depending on weather the node has a knob or not.
        """
        if knob and knob.isAnimated():
            # noinspection PyArgumentList
            if knob.isKeyAt(nuke.frame()):
                return QtGui.QBrush(QtGui.QColor().fromRgbF(
                    *constants.KNOB_HAS_KEY_AT_COLOR))
            return QtGui.QBrush(QtGui.QColor().fromRgbF(
                *constants.KNOB_ANIMATED_COLOR))

        else:
            color = nuke_utils.get_node_tile_color(node)
            if not row % 2:
                base = self.palette.base().color()  # type: QtGui.QColor
            else:
                base = self.palette.alternateBase().color()

            if knob:
                mix = constants.CELL_MIX_NODE_COLOR_AMOUNT_HAS_KNOB
            else:
                mix = constants.CELL_MIX_NODE_COLOR_AMOUNT_NO_KNOB

            base_color = base.getRgbF()[:3]

            # Blend Nodes color with base color
            base_color_blend = scalar(base_color, 1.0 - mix)
            color_blend = scalar(color, mix)
            color = [sum(x) for x in zip(base_color_blend, color_blend)]
            return QtGui.QBrush(QtGui.QColor().fromRgbF(*color))

    def data(self, index, role):
        """Returns the header data.

        For UserRole this returns the node or knob, depending on given
        orientation.

        Args:
            index (QtCore.QModelIndex): return headerData for this index
            role (QtCore.int): the current role
                QtCore.Qt.BackgroundRole: background color if knob is animated
                QtCore.Qt.EditRole: value of knob at current index
                QtCore.Qt.DisplayRole: current value of knob as str
                QtCore.Qt.UserRole: the knob itself at current index

        Returns:
            object
        """

        row = index.row()
        col = index.column()

        if not self.node_list:
            self.setup_model_data()
            return

        node = self.node_list[row]

        # Return early if node was deleted to prevent access to detached
        # python node object.
        if not nuke_utils.node_exists(node):
            self.removeRows(parent=QtCore.QModelIndex(),
                            row=row,
                            count=1)
            return

        knob = node.knob(self.knob_list[col])

        if role == QtCore.Qt.BackgroundRole:
            return self.get_background_color(row, node, knob)

        # Return early if node has no knob at current index.
        # Further data roles require a knob.
        if not knob:
            return

        if isinstance(knob, nuke.Boolean_Knob):
            if role == QtCore.Qt.CheckStateRole:
                if knob.value():
                    return QtCore.Qt.Checked
                else:
                    return QtCore.Qt.Unchecked
            if role == QtCore.Qt.DisplayRole:
                return None

        elif isinstance(knob, nuke.IArray_Knob):
            if (role == QtCore.Qt.DisplayRole) or (role == QtCore.Qt.EditRole):
                # dim = knob.dimensions()
                width = knob.width()
                height = knob.height()
                value = [knob.value(i / width, i % width)
                         for i in range(width * height)]
                # return value
                if role == QtCore.Qt.DisplayRole:
                    return str(value)
                else:
                    return value

        elif isinstance(knob, nuke.Transform2d_Knob):
            if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
                matrix_list = []
                matrix = knob.value()
                # enumerating over the matrix results in a RuntimeError:
                # index out of range. Iterating manually instead.
                # pylint: disable=consider-using-enumerate
                for idx in range(len(matrix)):
                    matrix_list.append(matrix[idx])

                if role == QtCore.Qt.DisplayRole:
                    return str(matrix_list)
                else:
                    return matrix_list

        elif isinstance(knob, nuke.Format_Knob):
            if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
                format = knob.value()  # type: nuke.Format
                return format.name()

        # Return data for all other knob classes.
        if role == QtCore.Qt.DisplayRole:
            return str(knob.value())

        elif role == QtCore.Qt.EditRole:
            return knob.value()

        elif role == QtCore.Qt.UserRole:
            return knob

    @staticmethod
    def safe_string(string):
        """encodes unicode to string because nuke knobs don't accept unicode.

            Args:
                string: encode this string

            Returns:
                str: string encoded or string unchanged if not unicode
        """
        if isinstance(string, unicode):
            return string.encode('utf-8')
        else:
            return string

    def setData(self, index, value, role):
        """Sets edited data to node.

        Warnings:
            Currently this only works for a few knob types.

        Args:
            index (QtCore.QModelIndex): current index
            value (object): new value
            role (QtCore.Qt.int): current Role. Only EditRole supported

        Returns:
            bool: True if successfully set knob to new value, otherwise False.

        """
        if not index.isValid():
            return

        if role == QtCore.Qt.EditRole:
            row = index.row()
            col = index.column()
            node = self.node_list[row]
            knob_name = self.headerData(col,
                                        QtCore.Qt.Horizontal,
                                        QtCore.Qt.DisplayRole)
            knob = node.knob(knob_name)

            if knob:
                edited = False
                if isinstance(value, (list, tuple)):

                    for i, val in enumerate(value):
                        frame = nuke.root()['frame'].value()
                        if knob.valueAt(frame, i) == val:
                            edited = True
                        else:
                            edited = knob.setValueAt(val, frame, i)

                elif isinstance(value, basestring):
                    value = self.safe_string(value)
                    edited = knob.setValue(value)

                else:
                    edited = knob.setValue(value)

                # Contrary to the reference, nuke.Knob.setValue() does not
                # always return True but None or even False if value was set
                # successfully:
                # nuke.createNode('NoOp')['label'].setValue('lorem ipsum')
                # >>> None
                # Therefore we must emit dataChanged() even when
                # the returned value from setValue() is None or True.
                # Otherwise we cause lagging in the UI.

                # noinspection PyUnresolvedReferences
                self.dataChanged.emit(index, index)
                return True

        return False

    def flags(self, index):
        """cell selectable and editable if the corresponding knob is enabled

        This ensures that NukeX features can't be edited with nuke_i license.
        Args:
            index (QtCore.QModelIndex): current index

        Returns:
            QtCore.Qt.ItemFlag: flags for current cell
        """
        row = index.row()
        node = self.node_list[row]

        flags = QtCore.Qt.NoItemFlags

        if not nuke_utils.node_exists(node):
            # Only return NoTIemFlags and don't remove the row here.
            # beginRemoveRows() calls flags() causing infinite recursion.
            return flags

        knob = self.data(index, QtCore.Qt.UserRole)  # type: nuke.Knob

        if not knob:
            return flags

        if isinstance(knob, nuke.Boolean_Knob):
            flags |= QtCore.Qt.ItemIsUserCheckable

        if knob.enabled():
            flags |= QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

            if not isinstance(knob, tuple(constants.READ_ONLY_KNOBS)) \
                    and not knob.hasExpression():
                flags |= QtCore.Qt.ItemIsEnabled

            return flags

        return QtCore.Qt.NoItemFlags

    def headerData(self, section, orientation, role):
        """Returns the header data.

        For UserRole this returns the node or knob, depending on given
        orientation.

        Args:
            section (QtCore.int): return headerData for this section
            orientation (QtCore.Qt.Orientation): header orientation
            role (QtCore.int): the current role.
                QtCore.Qt.DisplayRole: name of node or knob
                QtCore.Qt.UserRole: the node or knob itself
        """

        if orientation == QtCore.Qt.Horizontal:
            if section >= len(self.knob_list):
                return None

            if role == QtCore.Qt.DisplayRole:
                return self.knob_list[section]
            elif role == QtCore.Qt.UserRole:
                return self.knob_list[section]
            return None

        elif orientation == QtCore.Qt.Vertical:
            if section >= len(self.node_list):
                return None

            node = self.node_list[section]  # type: nuke.Node
            if not nuke_utils.node_exists(node):
                self.removeRows(row=section,
                                count=1,
                                parent= QtCore.QModelIndex())
                return

            if role == QtCore.Qt.DisplayRole:
                return node.name()
            elif role == QtCore.Qt.UserRole:
                return node
            elif role == QtCore.Qt.BackgroundRole:
                return QtGui.QBrush(QtGui.QColor.fromRgbF(
                    *(nuke_utils.get_node_tile_color(node))))
            elif role == QtCore.Qt.ForegroundRole:
                return QtGui.QPen(QtGui.QColor.fromRgbF(
                    *(nuke_utils.get_node_font_color(node))))
