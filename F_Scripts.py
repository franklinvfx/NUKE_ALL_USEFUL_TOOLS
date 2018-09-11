import nuke
from menu import path


#-----------------------------------------------------------------------------------------------------------------
# W_HOTBOX
#-----------------------------------------------------------------------------------------------------------------
try:      # > Nuke 7
	import W_hotbox, W_hotboxManager   # '<'
	print '\n- W_hotbox ...................... OK'
	##############################           #
except:   # < Nuke 6
	print '\n- W_hotbox ...................... FALSE'
	##############################           #
	pass



#-----------------------------------------------------------------------------------------------------------------
# CRYPTOMATTE
#-----------------------------------------------------------------------------------------------------------------
try:      # 3DE Exist
	import cryptomatte_utilities
	cryptomatte_utilities.setup_cryptomatte_ui()
	print '- Cryptomatte ................... OK'
except:   # 3DE Don't exist
	print '- Cryptomatte ................... FALSE'
	##############################           #
	pass



#-----------------------------------------------------------------------------------------------------------------
# Pixelfudger
#-----------------------------------------------------------------------------------------------------------------
try:      # 3DE Exist
	import pixelfudger
	print '- Pixelfudger ................... OK'
except:   # 3DE Don't exist
	print '- Pixelfudger ................... FALSE'
	##############################           #
	pass



import Dots, mirrorNodes               # import now               (link to F_Hub)
import knob_scripter                   # 'Alt + z'
import channel_hotbox                  # 'racine carre'           (link to F_Tools)
import autoBackdrop as autoBackdrop    # 'Alt + b'                (link to F_Tools)

print '- Franklin Scripts .............. OK\n'
##############################           #