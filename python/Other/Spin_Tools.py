import nuke
from menu_pipe import pipe_path

#-----------------------------------------------------------------------------------------------------------------
# ADD PATH
#-----------------------------------------------------------------------------------------------------------------
nuke.pluginAddPath(pipe_path + './Gizmos/SPIN');

menubar = nuke.menu("Nuke")
toolbar = nuke.toolbar("Nodes")

m = toolbar.addMenu("SPIN", icon="spin_tools.png")
m.addCommand("Chromatik", "nuke.createNode(\"Chromatik.gizmo\")", icon="")
m.addCommand("Erode_Fine", "nuke.createNode(\"Erode_Fine.gizmo\")", icon="")
m.addCommand("Morph_Dissolve", "nuke.createNode(\"Morph_Dissolve.gizmo\")", icon="")
m.addCommand("Noise_3D", "nuke.createNode(\"Noise_3D.gizmo\")", icon="")
m.addCommand("Relight_Simple", "nuke.createNode(\"Relight_Simple.gizmo\")", icon="")
m.addCommand("Spill_Correct", "nuke.createNode(\"Spill_Correct.gizmo\")", icon="")
m.addCommand("Suppress_RGBCMY", "nuke.createNode(\"Suppress_RGBCMY.gizmo\")", icon="")


#-----------------------------------------------------------------------------------------------------------------
# SPIN VFX Tools LOAD
#-----------------------------------------------------------------------------------------------------------------
ST = '- SpinVFX Tools ................. OK\n'
nuke.tprint(ST)
############################             #
