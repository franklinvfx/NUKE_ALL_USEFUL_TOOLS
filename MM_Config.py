import nuke, nukescripts, sys, os, platform

from menu import path

# Add Directory 
nuke.pluginAddPath(path + './icons');
nuke.pluginAddPath(path + './icons/nodes');
nuke.pluginAddPath(path + './Python');
nuke.pluginAddPath(path + './Python/More');
nuke.pluginAddPath(path + './Gizmos');
nuke.pluginAddPath(path + './Gizmos/Franklin');
nuke.pluginAddPath(path + './Gizmos/C');


#-----------------------------------------------------------------------------------------------------------------
# IMPORT MACHINE MOLLE PIPE
#-----------------------------------------------------------------------------------------------------------------
import MM_Tools 
import MM_Hub
import MM_Preset



#-----------------------------------------------------------------------------------------------------------------
# IMPORT FRANKLIN PIPE
#-----------------------------------------------------------------------------------------------------------------
import F_Tools
import F_Panels
# import F_Hub


#-----------------------------------------------------------------------------------------------------------------
# IMPORT CGEV TOOLS
#-----------------------------------------------------------------------------------------------------------------
import C_Tools                         # C gizmos



#-----------------------------------------------------------------------------------------------------------------
# IMPORT SCRIPTS
#-----------------------------------------------------------------------------------------------------------------
import Dots, mirrorNodes               # import now               (link to F_Hub)

try:      # > Nuke 7
	import W_hotbox, W_hotboxManager   # '<'
except:   # < Nuke 6
	nuke.error(' W_hotbox has not been load!\n                   - Maybe the Nuke version is to old\n')
	pass

import knob_scripter                   # 'Alt + z'
import channel_hotbox                  # 'racine carre'           (link to F_Tools)
import autoBackdrop as autoBackdrop    # 'Alt + b'                (link to F_Tools)




#-----------------------------------------------------------------------------------------------------------------
#DEBUG OPTIONS
#-----------------------------------------------------------------------------------------------------------------
# import callbacksTrace                 # show all callbacks




print 'LOADING TOOLS FROM PATH: ' + path