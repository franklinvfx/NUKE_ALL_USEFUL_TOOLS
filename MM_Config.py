import nuke
from menu import pipe_path


#-----------------------------------------------------------------------------------------------------------------
# ADD STARTING PRINT
#-----------------------------------------------------------------------------------------------------------------
L1 = '\n          _________________________ '
L2 = '\n         |      Machine Molle      |'
L3 = '\n         |        Franklin         |'
L4 = '\n         |________  2018  _________|'

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
import MM_Tools 
import MM_Hub
import MM_Preset


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


#-----------------------------------------------------------------------------------------------------------------
# SET NUKE PREFERENCES - W_HOTBOX
#-----------------------------------------------------------------------------------------------------------------
pipe_path = pipe_path.replace('\\', "/")
pref = nuke.toNode('preferences')

pref.knob('hotboxLocation').setValue(pipe_path + 'W_hotbox/')
pref.knob('hotboxIconLocation').setValue(pipe_path + 'W_hotbox/icons/')
pref.knob('hotboxShortcut').setValue('<')

pref.knob('platformPathRemaps').setValue(['W_hotbox/'], [2], [3])


print '- Pipe Directory:  ' + pipe_path
print '- Pipe Version: ................. 1.01\n'
##############################           #