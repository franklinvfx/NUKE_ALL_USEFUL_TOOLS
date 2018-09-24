import nuke

try:
    # < Nuke 11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets
except:
    # >= Nuke 11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets

from menu import pipe_path


#-----------------------------------------------------------------------------------------------------------------
# ADD STARTING PRINT
#-----------------------------------------------------------------------------------------------------------------
L1 = '\n          _________________________ '
L2 = '\n         |                         |'
L3 = '\n         |        Franklin         |'
L4 = '\n         |_________________________|'

info = L1 + L2 + L3 + L4 + '\n\n'
nuke.tprint(info)


#-----------------------------------------------------------------------------------------------------------------
# ADD PATH
#-----------------------------------------------------------------------------------------------------------------
nuke.pluginAddPath(pipe_path + './icons');
nuke.pluginAddPath(pipe_path + './icons/nodes');
nuke.pluginAddPath(pipe_path + './icons/nodes/color');
nuke.pluginAddPath(pipe_path + './Python');
nuke.pluginAddPath(pipe_path + './Python/More');
nuke.pluginAddPath(pipe_path + './Python/NodeTable');
nuke.pluginAddPath(pipe_path + './Gizmos');
nuke.pluginAddPath(pipe_path + './Gizmos/Franklin');
nuke.pluginAddPath(pipe_path + './Gizmos/C');
nuke.pluginAddPath(pipe_path + './Gizmos/C/icons');
nuke.pluginAddPath(pipe_path + './Gizmos/Other');
nuke.pluginAddPath(pipe_path + './Gizmos/Other/pixelfudger');


#-----------------------------------------------------------------------------------------------------------------
# IMPORT MACHINE MOLLE PIPE
#-----------------------------------------------------------------------------------------------------------------
# import MM_Tools 
# import MM_Hub
# import MM_Presets


#-----------------------------------------------------------------------------------------------------------------
# IMPORT FRANKLIN PIPE
#-----------------------------------------------------------------------------------------------------------------
nuke.load("F_Hub")
nuke.load("F_Panels")
nuke.load("F_Scripts")
nuke.load("F_Tools")
nuke.load("F_Presets")


#-----------------------------------------------------------------------------------------------------------------
# IMPORT CGEV TOOLS
#-----------------------------------------------------------------------------------------------------------------
import C_Tools                         # C gizmos


#-----------------------------------------------------------------------------------------------------------------
# SET NUKE PREFERENCES - W_HOTBOX
#-----------------------------------------------------------------------------------------------------------------
pipe_path = pipe_path.replace('\\', "/")
pref = nuke.toNode('preferences')

pref.knob('hotboxLocation').setValue(pipe_path + 'W_hotbox/')
pref.knob('hotboxIconLocation').setValue(pipe_path + 'W_hotbox/icons/')
pref.knob('hotboxShortcut').setValue('<')



PP = '- Pipe Directory:  ' + pipe_path
nuke.tprint(PP)
PV = '- Pipe Version: ................. 1.01\n'
##############################           #
nuke.tprint(PV)