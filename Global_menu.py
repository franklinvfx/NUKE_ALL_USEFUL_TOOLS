import nuke, nukescripts, sys

from MMP import path

#---------------------------------------------------------

#import callbacksTrace                 # show all callbacks

import C_Tools                         # C gizmos
import F_Tools, F_Panels, F_Hub        # gizmos / panels / menu

import Dots, mirrorNodes               # import now               (link to F_Hub)

try:
	import W_hotbox, W_hotboxManager   # '<'
except:
	nuke.error(' W_hotbox has not been load!\n                   - Maybe the Nuke version is to old\n')

import knob_scripter                   # 'Alt + z'
import channel_hotbox                  # 'racine carre'           (link to F_Tools)
import autoBackdrop as autoBackdrop    # 'Alt + b'                (link to F_Tools)