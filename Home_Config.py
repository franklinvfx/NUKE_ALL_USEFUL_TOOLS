import nuke
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
nuke.pluginAddPath(pipe_path + './Gizmos/pixelfudger');


#-----------------------------------------------------------------------------------------------------------------
# IMPORT MACHINE MOLLE PIPE
#-----------------------------------------------------------------------------------------------------------------
# import MM_Tools 
# import MM_Hub
# import MM_Preset



#-----------------------------------------------------------------------------------------------------------------
# IMPORT FRANKLIN PIPE
#-----------------------------------------------------------------------------------------------------------------
nuke.load("F_Hub")
nuke.load("F_Tools")
nuke.load("F_Panels")
nuke.load("F_Scripts")


#-----------------------------------------------------------------------------------------------------------------
# IMPORT CGEV TOOLS
#-----------------------------------------------------------------------------------------------------------------
import C_Tools                         # C gizmos



PP = '- Pipe Directory:  ' + pipe_path
nuke.tprint(PP)
PV = '- Pipe Version: ................. 1.01\n'
##############################           #
nuke.tprint(PV)