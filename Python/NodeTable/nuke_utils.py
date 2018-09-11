"""Functions to interact with Nuke.

"""


# Import built-in modules.
import os
import logging

# Import third party modules.
NUKE_LOADED = True
try:
    import nuke
except ImportError:
    # We need some Qt to mimic nukes interface functions.
    from Qt import QtWidgets
    NUKE_LOADED = False

# Import internal modules.
# pylint: disable=wrong-import-position
from NodeTable.constants import PACKAGE_NICE_NAME
from NodeTable.constants import SHADE_DAG_NODES_NON_COMMERCIAL


LOG = logging.getLogger(__name__)


def node_exists(node):
    """Check if python object node is still attached to a Node.

    Nuke throws a ValueError if node is not attached. This happens when the
    user deleted a node that is still in use by a python script.

    Args:
        node (nuke.Node): node python object

    Returns:
        bool: True if node exists
    """
    try:
        node.name()
    except ValueError:
        return False

    return True


def get_selected_nodes(recurse_groups=False):
    """get current selection

    Returns:
        list: of nuke.Node
    """
    selection = nuke.selectedNodes()

    if recurse_groups:
        for node in selection:
            if node.Class() == 'Group':
                with node:
                    selection += get_selected_nodes(recurse_groups)

    return selection


def to_hex(color_rgb):
    """convert rgb color values to hex

    Args:
        color_rgb (tuple): color values 0-1

    Returns:
        str: color in hex notation
    """
    return  int('%02x%02x%02x%02x' % (int(color_rgb[0] * 255),
                                      int(color_rgb[1] * 255),
                                      int(color_rgb[2] * 255),
                                      int(color_rgb[3] * 255)), 16)


def to_rgb(color_hex):
    """hex to rgb
    Author: Ivan Busquets

    Args:
        color_hex: color in hex format

    Returns (tuple): color in 0-1 range

    """

    red = (0xFF & color_hex >> 24) / 255.0
    green = (0xFF & color_hex >> 16) / 255.0
    blue = (0xFF & color_hex >> 8) / 255.0
    alpha = (0xFF & color_hex >> 0) / 255.0

    return red, green, blue, alpha


def get_unique(seq):
    """returns all unique items in of a list of strings

    Args:
        seq (list): list of strings

    Returns:
        list: unique items
    """
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def get_node_tile_color(node):
    """return the nodes tile color or default node color if not set

    Args:
        node (nuke.Node): node

    Returns:
        tuple: colors in rgb
    """
    color = None
    tile_color_knob = node.knob('tile_color')
    if tile_color_knob:
        color = tile_color_knob.value()
    if not color:
        color = nuke.defaultNodeColor(node.Class())

    if color:
        return to_rgb(color)[:3]


def get_node_font_color(node):
    """Get the label color of a node.

    Args:
        node (nuke.Node): node

    Returns:
        tuple: color in rgb
    """
    color_knob = node.knob('note_font_color')
    if color_knob:
        return to_rgb(color_knob.value())[:3]


def get_node_classes(no_ext=True):
    """returns list of all available node classes (plugins)

    Args:
        no_ext: strip extension to return only class name

    Returns:
        list: available node classes
    """
    if NUKE_LOADED:
        plugins = nuke.plugins(nuke.ALL | nuke.NODIR, "*." + nuke.PLUGIN_EXT)
    else:
        plugins = ['Merge2', 'Mirror', 'Transform']
    plugins = get_unique(plugins)
    if no_ext:
        plugins = [os.path.splitext(plugin)[0] for plugin in plugins]

    return plugins


def select_node(node, zoom=1):
    """selects and (optionally) zooms DAG to given node.

    Warnings:
        If name of node inside a group is given,
        the surrounding group will be selected instead of the node

    Args:
        node (nuke.Node, str): node or name of node. If name of node inside a group is given,
            the surrounding group will be selected instead of the node.
        zoom (int): optionally zoom to given node. If zoom = 0, no DAG will not zoom to given node.

    Returns:
        None
    """
    # deselecting all nodes:  looks stupid but works in non-commercial mode
    nuke.selectAll()
    nuke.invertSelection()

    # Get the top-most parent nodes name.
    if isinstance(node, nuke.Node):
        full_name = node.fullName()
        if '.' in full_name:
            node = full_name.split('.')[0]

    # Starting from the node name get the top-most parent node.
    if isinstance(node, basestring):
        # if node is part of a group: select the group
        if "." in node:
            node_name = node.split(".")[0]
            node = nuke.toNode(node_name)

    # Select and zoom to Node.
    if isinstance(node, nuke.Node):
        node['selected'].setValue(True)
        if zoom:
            nuke.zoom(zoom, [node.xpos(), node.ypos()])


def shade_dag_nodes_enabled():
    """Check if nodes are shaded in DAG

    Note:
        Skipping check of the preferences node since that counts towards the
        10 nodes limit in non-commercial edition.

    Returns:
        bool: True if nodes are shaded

    """

    # nuke.GlobalsEnvironment.get() returns None for non-existing key.
    # Not setting default return value because it can only be a string.
    if not nuke.env.get('nc'):
        pref_node = nuke.toNode("preferences")
        shaded = pref_node['ShadeDAGNodes'].value()
    else:
        shaded = SHADE_DAG_NODES_NON_COMMERCIAL

    return shaded


def ask(prompt=""):
    """Ask user a yes/no question.

    Args:
        prompt: Question to display.

    Returns:
        bool: users answer.
    """
    reply = True
    if NUKE_LOADED:
        reply = nuke.ask(prompt)
    else:
        reply = QtWidgets.QMessageBox.question(None,
                                               PACKAGE_NICE_NAME,
                                               prompt,
                                               (QtWidgets.QMessageBox.Yes |
                                                QtWidgets.QMessageBox.No))
        reply = reply == QtWidgets.QMessageBox.Yes

    return reply
