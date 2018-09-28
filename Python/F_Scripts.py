import nuke

from menu import pipe_path


#-----------------------------------------------------------------------------------------------------------------
# W_HOTBOX
#-----------------------------------------------------------------------------------------------------------------
try:      # > Nuke 7
	import W_hotbox, W_hotboxManager   # '<'
	nuke.tprint(' ')
except:   # < Nuke 6
	W = '- W_hotbox ...................... NONE'
	nuke.tprint(W)
	pass

#-----------------------------------------------------------------------------------------------------------------
# CRYPTOMATTE
#-----------------------------------------------------------------------------------------------------------------
try:      # 3DE Exist
	import cryptomatte_utilities
	cryptomatte_utilities.setup_cryptomatte_ui()
	C1 = '- Cryptomatte ................... OK'
	nuke.tprint(C1)
except:   # 3DE Don't exist
	C2 = '- Cryptomatte ................... NONE'
	nuke.tprint(C2)
	pass

#-----------------------------------------------------------------------------------------------------------------
# SHORTCUT EDITOR
#-----------------------------------------------------------------------------------------------------------------
try:
    import shortcuteditor
    shortcuteditor.nuke_setup()
except Exception:
    import traceback
    traceback.print_exc()


#-----------------------------------------------------------------------------------------------------------------
# OTHER SCRIPTS FOR NUKE > 7
#-----------------------------------------------------------------------------------------------------------------
try:      # ALL Exist
	import knob_scripter                   # 'Alt + z'

	import channel_hotbox                  # 'racine carre'           (link to F_Tools)
	nuke.menu('Nuke').findItem('Edit').addCommand('C_HotboxotBox', 'channel_hotbox.start()', '²')

	import reduceKeyframes
	m = nuke.menu( 'Animation' )
	m.addCommand( 'Reduce Keyframes', "reduceKeyframes.doReduceKeyframes()" )
	
		  # PRINT
	ALL1 = '- Knob Scripter ................. OK\n- C_Hotbox ...................... OK'
	nuke.tprint(ALL1)

except:   # ALL Don't exist
		  # PRINT
	ALL2 = '- Knob Scripter ................. NONE\n- C_Hotbox ...................... NONE'
	nuke.tprint(ALL2)
	pass

#-----------------------------------------------------------------------------------------------------------------
# OTHER SCRIPTS FOR NUKE < 7
#-----------------------------------------------------------------------------------------------------------------
try:      # ALL Exist
	import pixelfudger
	import Dots
	import mirrorNodes

	import autoBackdrop as autoBackdrop    # 'Alt + b'
	nukescripts.autoBackdrop = autoBackdrop.autoBackdrop
	nuke.menu('Nodes').addCommand( 'Other/Backdrop', 'autoBackdrop.autoBackdrop()', 'alt+b', 'Backdrop.png')

	import viewerInputNodes
	v = nuke.menu("Viewer")
	v.addCommand("-", '', '')
	fv = v.addMenu("IP")
	fv.addCommand('IP List','nuke.load("viewerInputNodes"), viewerInput()', "Ctrl+Alt+i",  icon="F_ip.png") 
	fv.addCommand('IP Remove','nuke.load("viewerInputNodes"), viewerInput(ipNode="Remove")', "Ctrl+Alt+Shift+i",  icon="F_ipr.png")

		  # PRINT
	ALL3 = '- Auto Backdrop ................. OK\n- Pixelfudger ................... OK'
	nuke.tprint(ALL3)

except:   # ALL Don't exist
		  # PRINT
	ALL4 = '- Auto Backdrop ................. NONE\n- Pixelfudger ................... NONE'
	nuke.tprint(ALL4)
	pass


FS = '- Franklin Scripts .............. OK'
nuke.tprint(FS)
      ##############################    #