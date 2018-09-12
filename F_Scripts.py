import nuke
from menu import path


#-----------------------------------------------------------------------------------------------------------------
# W_HOTBOX
#-----------------------------------------------------------------------------------------------------------------
try:      # > Nuke 7
	import W_hotbox, W_hotboxManager   # '<'
	WH1 = '\n- W_hotbox ...................... OK'
	nuke.tprint(WH1)
except:   # < Nuke 6
	WH2 = '\n- W_hotbox ...................... FALSE'
	nuke.tprint(WH2)
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
	C2 = '- Cryptomatte ................... FALSE'
	nuke.tprint(C2)
	pass



#-----------------------------------------------------------------------------------------------------------------
# Pixelfudger
#-----------------------------------------------------------------------------------------------------------------
try:      # Pixelfudger Exist
	import pixelfudger
	PF1 = '- Pixelfudger ................... OK'
	nuke.tprint(PF1)
except:   # Pixelfudger Don't exist
	PF2 = '- Pixelfudger ................... FALSE'
	nuke.tprint(PF2)
	pass



import Dots, mirrorNodes               # import now               (link to F_Hub)
import knob_scripter                   # 'Alt + z'
import channel_hotbox                  # 'racine carre'           (link to F_Tools)
import autoBackdrop as autoBackdrop    # 'Alt + b'                (link to F_Tools)

FS = '- Franklin Scripts .............. OK\n'
nuke.tprint(FS)
##############################           #