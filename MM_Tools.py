import nuke

menubar = nuke.menu("Nuke")
 

toolbar = nuke.toolbar("Nodes")

m = toolbar.addMenu("GIZMO", icon="icon.png")
m.addCommand("Dugrain2", "nuke.createNode(\"Dugrain2.gizmo\")", icon="icon.png")
m.addCommand("DespillMadness", "nuke.createNode(\"DespillMadness.gizmo\")", icon="key.png")
m.addCommand("PushPixel", "nuke.createNode(\"PushPixel.gizmo\")", icon="key.png")
m.addCommand("PushPixel2", "nuke.createNode(\"PushPixel2.gizmo\")", icon="key.png")
m.addCommand("bm_Despill", "nuke.createNode(\"bm_Despill.gizmo\")", icon="key.png")
m.addCommand("AdditiveKeyer2", "nuke.createNode(\"AdditiveKeyer2.gizmo\")", icon="key.png")
m.addCommand("KillOutline", "nuke.createNode(\"KillOutline.gizmo\")", icon="key.png")
m.addCommand("LUE4NUKE", "nuke.createNode(\"LUE4NUKE.gizmo\")", icon="icon.png")
m.addCommand("Aberration", "nuke.createNode(\"Aberration_jb.gizmo\")", icon="icon.png")
m.addCommand("bm_Lightwrap", "nuke.createNode(\"bm_Lightwrap.gizmo\")", icon="icon.png")
m.addCommand("bm_OpticalGlow", "nuke.createNode(\"bm_OpticalGlow.gizmo\")", icon="icon.png")
m.addCommand("expoglow", "nuke.createNode(\"expoglow.gizmo\")", icon="icon.png")
m.addCommand("ColorMatch", "nuke.createNode(\"ColorMatch.gizmo\")", icon="icon.png")
m.addCommand("SprutEmitter", "nuke.createNode(\"SprutEmitter.gizmo\")", icon="icon.png")
m.addCommand("SprutInspect", "nuke.createNode(\"SprutInspect.gizmo\")", icon="icon.png")
m.addCommand("SprutSolver", "nuke.createNode(\"SprutSolver.gizmo\")", icon="icon.png")
m.addCommand("BokehBlur", "nuke.createNode(\"BokehBlur.gizmo\")", icon="icon.png")
m.addCommand("L_AlphaClean_v03", "nuke.createNode(\"L_AlphaClean_v03.gizmo\")", icon="icon.png")
m.addCommand("L_BlurHue_v01", "nuke.createNode(\"L_BlurHue_v01.gizmo\")", icon="icon.png")
m.addCommand("L_Despill_v05", "nuke.createNode(\"L_Despill_v05.gizmo\")", icon="icon.png")
m.addCommand("L_Fuse_v06", "nuke.createNode(\"L_Fuse_v06.gizmo\")", icon="icon.png")
m.addCommand("LumaKeyer", "nuke.createNode(\"LumaKeyer.gizmo\")", icon="icon.png")
m.addCommand("CardToTrack", "nuke.createNode(\"CardToTrack.gizmo\")", icon="my.png")



#-------------------------------------------------------------------------------------------------------------------
# GONZO TOOLS
#------------------------------------------------------------------------------------------------------
gonzoToolBar = nuke.menu("Nodes").addMenu("Gonzo_Tools", icon = "gonzoicon24.png")
gonzoToolBar.addCommand("Filters/G_FineEdgeDetect", 'nuke.createNode("G_FineEdgeDetect")')
gonzoToolBar.addCommand("Filters/G_AngleEdgeDetect", 'nuke.createNode("G_AngleEdgeDetect")')
gonzoToolBar.addCommand("Filters/G_ChannelReBuild", 'nuke.createNode("G_ChannelReBuild")')
gonzoToolBar.addCommand("Keyers/G_ScreenXchange", 'nuke.createNode("G_ScreenXchange")')
gonzoToolBar.addCommand("CC/G_EdgeHammer", 'nuke.createNode("G_EdgeHammer")')
gonzoToolBar.addCommand("CC/G_Matchtone", 'nuke.createNode("G_Matchtone")')
gonzoToolBar.addCommand("Showreel/G_Breakdowner", 'nuke.createNode("G_Breakdowner")')
gonzoToolBar.addCommand("CC/G_WrappersDelight", 'nuke.createNode("G_WrappersDelight")')
gonzoToolBar.addCommand("Filters/G_Sharpen", 'nuke.createNode("G_Sharpen")')



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
	DE1 = '- 3DE ........................... OK'
	nuke.tprint(DE1)
except:   # 3DE Don't exist
	DE2 = '- 3DE ........................... FALSE'
	nuke.tprint(DE2)
	##############################           #
	pass



#-----------------------------------------------------------------------------------------------------------------
# Machine Molle Tools LOAD
#-----------------------------------------------------------------------------------------------------------------
print '- Machine Molle Tools ........... OK'
##############################    \n       #
