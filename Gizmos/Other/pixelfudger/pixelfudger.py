import nuke

t=nuke.menu("Nodes")
u=t.addMenu("Pixelfudger", icon="PxF_Menu.png")
 
t.addCommand( "Pixelfudger/PxF_Bandpass", "nuke.createNode('PxF_Bandpass')", icon="PxF_Bandpass.png" ) 
t.addCommand( "Pixelfudger/PxF_ChromaBlur", "nuke.createNode('PxF_ChromaBlur')", icon="PxF_ChromaBlur.png") 
t.addCommand( "Pixelfudger/PxF_Distort", "nuke.createNode('PxF_Distort')", icon="PxF_Distort.png") 
t.addCommand( "Pixelfudger/PxF_Erode", "nuke.createNode('PxF_Erode')", icon="PxF_Erode.png")
t.addCommand( "Pixelfudger/PxF_Filler", "nuke.createNode('PxF_Filler')", icon="PxF_Filler.png") 
t.addCommand( "Pixelfudger/PxF_Grain", "nuke.createNode('PxF_Grain')", icon="PxF_Grain.png") 
t.addCommand( "Pixelfudger/PxF_HueSat", "nuke.createNode('PxF_HueSat')", icon="PxF_HueSat.png")  
t.addCommand( "Pixelfudger/PxF_IDefocus", "nuke.createNode('PxF_IDefocus')", icon="PxF_IDefocus.png")
t.addCommand( "Pixelfudger/PxF_KillSpill", "nuke.createNode('PxF_KillSpill')", icon="PxF_KillSpill.png") 
t.addCommand( "Pixelfudger/PxF_Line", "nuke.createNode('PxF_Line')", icon="PxF_Line.png" ) 
t.addCommand( "Pixelfudger/PxF_MergeWrap", "nuke.createNode('PxF_MergeWrap')", icon="PxF_MergeWrap.png" ) 
t.addCommand( "Pixelfudger/PxF_ScreenClean", "nuke.createNode('PxF_ScreenClean')", icon="PxF_ScreenClean.png")