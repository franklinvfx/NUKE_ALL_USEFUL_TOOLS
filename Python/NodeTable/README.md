# README #

Spreadsheat showing and editing knobs of selected Nodes

![demo](demo.gif)

### How do I get set up? ###

download Qt.py and add into your .nuke folder or PYTHON_PATH:
https://github.com/mottosso/Qt.py

add to your menu.py:
```
from nukescripts import panels

def get_node_table_widget():
    from NodeTable import view as node_table_view
    reload(node_table_view)
    return node_table_view.NodeTableWidget(nuke.selectedNodes())

#pane = nuke.getPaneFor('Properties.1')
panels.registerWidgetAsPanel('get_node_table_widget', 'Node Spreadsheet',
                             'de.filmkorn.NodeSpreadsheet', False)
```
# License: MIT