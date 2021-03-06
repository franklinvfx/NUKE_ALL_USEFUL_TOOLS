﻿import nuke, nukescripts

from menu_pipe import pipe_path


#-----------------------------------------------------------------------------------------------------------------
# W_HOTBOX
#-----------------------------------------------------------------------------------------------------------------
try:      # > Nuke 7
	import W_hotbox, W_hotboxManager   # '<'
	# SET NUKE PREFERENCES FOR W_HOTBOX
	pipe_path = pipe_path.replace('\\', "/")
	pref = nuke.toNode('preferences')
	pref.knob('hotboxLocation').setValue(pipe_path + 'Python/W_hotbox/')
	pref.knob('hotboxIconLocation').setValue(pipe_path + 'Python/W_hotbox/icons/')
	pref.knob('hotboxShortcut').setValue('<')
	WH = '- Various Script:\n        W_Hotbox ................ OK'
	nuke.tprint(WH)
except:   # < Nuke 6
	W = '- Various Script:\n         W_hotbox ................ NONE'
	nuke.tprint(W)
	pass

# -----------------------------------------------------------------------------------------------------------------
# CRYPTOMATTE
# -----------------------------------------------------------------------------------------------------------------
try:      # 3DE Exist
	import cryptomatte_utilities
	cryptomatte_utilities.setup_cryptomatte()
	cryptomatte_utilities.setup_cryptomatte_ui()
	C1 = '        Cryptomatte ............. OK'
	nuke.tprint(C1)
except:   # 3DE Don't exist
	C2 = '        Cryptomatte ............. NONE'
	nuke.tprint(C2)
	pass

#-----------------------------------------------------------------------------------------------------------------
# SHORTCUT EDITOR
#-----------------------------------------------------------------------------------------------------------------
# try:
#     import shortcuteditor
#     shortcuteditor.nuke_setup()
# except Exception:
#     import traceback
#     traceback.print_exc()


#-----------------------------------------------------------------------------------------------------------------
# SCRIPTS WITH PYSIDE FOR NUKE
#-----------------------------------------------------------------------------------------------------------------
try:      # ALL Exist
	import knob_scripter                   # 'Alt + z'

	import channel_hotbox
	nuke.menu('Nuke').findItem('Edit').addCommand('C_HotboxotBox', 'channel_hotbox.start()', '²')

	import reduceKeyframes
	m = nuke.menu( 'Animation' )
	m.addCommand( 'Reduce Keyframes', "reduceKeyframes.doReduceKeyframes()" )
	
		  # PRINT
	ALL1 = '        Knob Scripter ........... OK\n        C_Hotbox ................ OK'
	nuke.tprint(ALL1)

except:   # ALL Don't exist
		  # PRINT
	ALL2 = '        Knob Scripter ........... NONE\n        C_Hotbox ................ NONE'
	nuke.tprint(ALL2)
	pass

#-----------------------------------------------------------------------------------------------------------------
# OTHER SCRIPTS
#-----------------------------------------------------------------------------------------------------------------
try:      # ALL Exist
	import pixelfudger
	import Dots
	import mirrorNodes
	import cmdExecute

	import F_Backdrop
	nukescripts.autoBackdrop = F_Backdrop.autoBackdrop # Original backdrop function replacement
	nuke.menu('Nodes').addCommand( 'Other/Backdrop', 'F_Backdrop.autoBackdrop()', 'alt+b', 'Backdrop.png')

	import viewerInputNodes
	v = nuke.menu("Viewer")
	v.addCommand("-", '', '')
	fv = v.addMenu("IP")
	fv.addCommand('IP List','nuke.load("viewerInputNodes"), viewerInput()', "Ctrl+Alt+i",  icon="F_ip.png") 
	fv.addCommand('IP Remove','nuke.load("viewerInputNodes"), viewerInput(ipNode="Remove")', "Ctrl+Alt+Shift+i",  icon="F_ipr.png")

		  # PRINT
	ALL3 = '        Pixelfudger ............. OK'
	nuke.tprint(ALL3)

except:   # ALL Don't exist
		  # PRINT
	ALL4 = '        Pixelfudger ............. NONE'
	nuke.tprint(ALL4)
	pass



#-----------------------------------------------------------------------------------------------------------------
# KEEP EXISTING FRAMES
#-----------------------------------------------------------------------------------------------------------------
try:      # > Nuke 11
	import j3p_renderdialog_n11
	nukescripts.showRenderDialog = j3p_renderdialog_n11.showRenderDialog 
	SF1 = '        Render Options........... OK\n'
except:   # < Nuke 10
	import j3p_renderdialog_n10
	nukescripts.showRenderDialog = j3p_renderdialog_n10.showRenderDialog 
	SF1 = '        Render Options........... OK\n'
	pass
nuke.tprint(SF1)




# from animatedSnap3D import *
# try:
#     m = nuke.menu('Axis').findItem('Snap')
#     m.addSeparator()
#     m.addCommand('Match position - ANIMATED', 'animatedSnap3D.translateThisNodeToPointsAnimated()')
#     m.addCommand('Match position, orientation - ANIMATED', 'animatedSnap3D.translateRotateThisNodeToPointsAnimated()')
#     m.addCommand('Match position, orientation, scale - ANIMATED', 'animatedSnap3D.translateRotateScaleThisNodeToPointsAnimated()')
# except:
#     pass



FS = '- Franklin Scripts .............. OK'
nuke.tprint(FS)
      ##############################    #