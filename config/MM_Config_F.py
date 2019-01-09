import nuke, platform, os

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

from menu_pipe import pipe_path


#-----------------------------------------------------------------------------------------------------------------
# ADD STARTING PRINT
#-----------------------------------------------------------------------------------------------------------------
L1 = '\n          _________________________ '
L2 = '\n         |      Machine Molle      |'
L3 = '\n         |     Franklin CUSTOM     |'
L4 = '\n         |________  2018  _________|'

info = L1 + L2 + L3 + L4 + '\n\n'
nuke.tprint(info)


#-----------------------------------------------------------------------------------------------------------------
# ADD PATH
#-----------------------------------------------------------------------------------------------------------------
nuke.pluginAddPath(pipe_path + './icons');
nuke.pluginAddPath(pipe_path + './icons/nodes');
nuke.pluginAddPath(pipe_path + './icons/nodes/color');

nuke.pluginAddPath(pipe_path + './python');
nuke.pluginAddPath(pipe_path + './python/Franklin');
nuke.pluginAddPath(pipe_path + './python/C');
nuke.pluginAddPath(pipe_path + './python/MM');
nuke.pluginAddPath(pipe_path + './python/Other');

nuke.pluginAddPath(pipe_path + './gizmos');
nuke.pluginAddPath(pipe_path + './gizmos/Franklin');
nuke.pluginAddPath(pipe_path + './gizmos/C');
nuke.pluginAddPath(pipe_path + './gizmos/C/icons');
nuke.pluginAddPath(pipe_path + './gizmos/MM');
nuke.pluginAddPath(pipe_path + './gizmos/Other');
nuke.pluginAddPath(pipe_path + './gizmos/Other/pixelfudger');
# nuke.pluginAddPath(pipe_path + './smartScripter');


#-----------------------------------------------------------------------------------------------------------------
# SET NUKE PREFERENCES - W_HOTBOX
#-----------------------------------------------------------------------------------------------------------------
pipe_path = pipe_path.replace('\\', "/")
pref = nuke.toNode('preferences')


pref.knob('hotboxLocation').setValue(pipe_path + 'Python/W_hotbox/')
pref.knob('hotboxIconLocation').setValue(pipe_path + 'Python/W_hotbox/icons/')
pref.knob('hotboxShortcut').setValue('<')


#-----------------------------------------------------------------------------------------------------------------
# DEV OPTIONS
#-----------------------------------------------------------------------------------------------------------------
# dev = "True"
# if dev == "True":
#     devPrint = '- Dev Options ................... OK'
# else:
#     devPrint = '- Dev Options ................... FALSE'
# nuke.tprint(devPrint)


#-----------------------------------------------------------------------------------------------------------------
# IMPORT MACHINE MOLLE PIPE
#-----------------------------------------------------------------------------------------------------------------
import MM_Tools 
# import MM_Hub
import MM_Presets
import MM_Toolsets


#-----------------------------------------------------------------------------------------------------------------
# IMPORT FRANKLIN PIPE
#-----------------------------------------------------------------------------------------------------------------
nuke.load("F_Hub")
nuke.load("F_Panels")
nuke.load("F_Scripts")
nuke.load("F_Tools")
nuke.load("F_Presets")


#-----------------------------------------------------------------------------------------------------------------
# IMPORT OTHER TOOLS
#-----------------------------------------------------------------------------------------------------------------
import C_Tools                         # CGEV gizmos
import Spin_Tools                      # SpinVFX gizmos

# #-----------------------------------------------------------------------------------------------------------------
# # IMPORT GLOBAL
# #-----------------------------------------------------------------------------------------------------------------
# import Reload

#-----------------------------------------------------------------------------------------------------------------
# SET NUKE_LOCAL DIRECTORY
#-----------------------------------------------------------------------------------------------------------------
# Need to check all conditions
if platform.system() == "Windows":
	local_path = 'D://NUKE_LOCAL/'
	os.environ['NUKE_TEMP_DIR'] = local_path
	print '- Nuke Local Directory:  ' + local_path
else:
	print 'WARNING: nuke local path is not set!'


# Need to check all conditions
pref.knob('autoLocalCachePath').setValue('')
# pref.knob('localCachePath').setValue('[getenv NUKE_TEMP_DIR]')
pref.knob('localCachePath').setValue(local_path)





print '- Pipe Directory:        ' + pipe_path
print '- Pipe Version: ................. 1.02\n'
##############################           #