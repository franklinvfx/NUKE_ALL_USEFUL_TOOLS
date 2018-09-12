import nuke
from menu import pipe_path


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
try:      # Cryptomatte Exist
	import cryptomatte_utilities
	cryptomatte_utilities.setup_cryptomatte_ui()
	C1 = '- Cryptomatte ................... OK'
	nuke.tprint(C1)
except:   # Cryptomatte Don't exist
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



#-----------------------------------------------------------------------------------------------------------------
# 3DEQUALIZER
#-----------------------------------------------------------------------------------------------------------------
try:      # 3DE Exist
	nuke.menu("Nodes").addMenu("3DE4", icon = "3de.png")
	nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Anamorphic_Standard_Degree_4", "nuke.createNode('LD_3DE4_Anamorphic_Standard_Degree_4')")
	nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Anamorphic_Rescaled_Degree_4", "nuke.createNode('LD_3DE4_Anamorphic_Rescaled_Degree_4')")
	nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Anamorphic_Degree_6", "nuke.createNode('LD_3DE4_Anamorphic_Degree_6')")
	nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Radial_Standard_Degree_4", "nuke.createNode('LD_3DE4_Radial_Standard_Degree_4')")
	nuke.menu("Nodes").addCommand("3DE4/LD_3DE4_Radial_Fisheye_Degree_8", "nuke.createNode('LD_3DE4_Radial_Fisheye_Degree_8')")
	nuke.menu("Nodes").addCommand("3DE4/LD_3DE_Classic_LD_Model", "nuke.createNode('LD_3DE_Classic_LD_Model')")
	3DE1 = '- 3DE ........................... OK'
	nuke.tprint(3DE1)
except:   # 3DE Don't exist
	3DE2 = '- 3DE ........................... FALSE'
	nuke.tprint(3DE2)
	##############################           #
	pass



#-----------------------------------------------------------------------------------------------------------------
# OTHE TOOLS
#-----------------------------------------------------------------------------------------------------------------
try:      # ALL Exist
	import Dots, mirrorNodes               # import now               (link to F_Hub)
	import knob_scripter                   # 'Alt + z'
	# import channel_hotbox                  # 'racine carre'           (link to F_Tools)
	# import autoBackdrop as autoBackdrop    # 'Alt + b'                (link to F_Tools)

	ALL1 = '- Knob Scripter ................. OK\n- C_Hotbox ...................... OK\n- Auto Backdrop ................. OK'
	nuke.tprint(ALL1)

except:   # ALL Don't exist
	ALL2 = '- Knob Scripter ................. NONE\n- C_Hotbox ...................... NONE\n- Auto Backdrop ................. NONE'
	nuke.tprint(ALL2)
	pass



FS = '- Franklin Scripts .............. OK\n'
nuke.tprint(FS)
      ##############################    #