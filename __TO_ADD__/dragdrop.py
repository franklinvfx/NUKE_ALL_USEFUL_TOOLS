# dragdrop.py
#
# Provides enhanced drag and drop functionality within Nuke
#   - folder recursion by default
#   - geo read using ReadGeo2 nodes
#   - luts read using Vectorfield node
#   - chan data read into Camera node
#
# Usage:
#
#   If loaded with the mynk tools loader:
#     import nukescripts
#     nukescripts.drop.addDropDataCallback(mynk.tools.python.utils.drag_drop.dropHandler)
#
# TODO: extend chan file import to give user options for node to create
#

import os
import nuke
import nukescripts

def fileHandler(dropped_data):
  file_path = dropped_data
  file_range= ''
  
  if not os.path.isfile(file_path):
    file_path, sep, file_range = file_path.rpartition(' ')

  file_name, file_ext = os.path.splitext(file_path)
  file_ext = file_ext.lower()
  
  if file_ext.lower() == '.obj':
    read_node = nuke.createNode("ReadGeo2", inpanel=False)
    read_node["file"].fromUserText(dropped_data)
    read_node["selected"].setValue(0)
    return True

  elif file_ext.lower() == '.fbx':
    read_node = nuke.createNode("ReadGeo2", inpanel=False)
    read_node["file"].fromUserText(dropped_data)
    read_node["selected"].setValue(0) 
    read_node = nuke.createNode("Camera2", 'read_from_file 1 file {0}'.format(dropped_data), inpanel=False)
    read_node["selected"].setValue(0)
    read_node = nuke.createNode("Light2", 'read_from_file 1 file {0}'.format(dropped_data), inpanel=False)
    read_node["selected"].setValue(0)    
    return True
  
  elif file_ext.lower() in ['.3dl', '.blur', '.csp', '.cub', '.cube', '.vf', '.vfz']:
    read_node = nuke.createNode("Vectorfield", inpanel=False)
    read_node["vfield_file"].setValue(dropped_data)
    read_node["selected"].setValue(0)
    return True

  elif file_ext.lower() == '.chan':
    read_node = nuke.createNode("Camera2", inpanel=False)
    nuke.tcl('in {0} {import_chan_file {1} }'.format(read_node.name(), dropped_data))
    read_node["selected"].setValue(0)
    return True

  else:
    read_node = nuke.createNode("Read", inpanel=False)
    read_node["file"].fromUserText(dropped_data)
    return True


def pathHandler(dropped_data, recursive=True):
  if os.path.isdir(dropped_data):
    for each in nuke.getFileNameList(dropped_data, False, False, bool(recursive), False):
      pathHandler(os.path.join(dropped_data,each))
    return True
  else:
    return fileHandler(dropped_data)


def dropHandler(droptype, dropped_data):
  if dropped_data.startswith("file://"):
    dropped_data = dropped_data[7:]
  if os.path.isfile(dropped_data) or os.path.isdir(dropped_data):
    return pathHandler(dropped_data)
  return False

