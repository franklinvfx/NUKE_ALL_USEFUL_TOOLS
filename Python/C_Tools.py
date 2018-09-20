import nuke

# from menu import path

# nuke.pluginAddPath(path + './icons');
# nuke.pluginAddPath(path + './Gizmos');
# nuke.pluginAddPath(path + './Gizmos/C');
# nuke.pluginAddPath(path + './Gizmos/C/icons');

##########################################################################################################################################

tools = nuke.toolbar("Nodes")
C_menu = tools.addMenu("C",  icon="C.png")

##########################################################################################################################################
C_menu.addMenu( 'Draw',  icon='Draw.png' )
C_menu.addCommand( 'Draw/Ramp Corner', "nuke.createNode(\"Ramp_Corner\")" , icon="Ramp_Corner.png")
C_menu.addCommand( 'Draw/Noise C', "nuke.createNode(\"Noise_C\")" , icon="Noise_C.png")
C_menu.addCommand( 'Draw/DuGrain', "nuke.createNode(\"DuGrain\")" , icon="DuGrain.png")

##########################################################################################################################################
C_menu.addMenu( 'Time',  icon='Time.png' )
C_menu.addCommand( 'Time/Rebuild Frames', "nuke.createNode(\"Rebuild\")" , icon="Rebuild_Frames.png")
C_menu.addCommand( 'Time/Curve Creator', "nuke.createNode(\"Curve_Creator\")" , icon="Curve_Creator.png")
C_menu.addCommand( 'Time/Curve ReTime', "nuke.createNode(\"Curve_ReTime\")" , icon="Curve_ReTime.png")
C_menu.addCommand( 'Time/Curve Normalise', "nuke.createNode(\"Curve_Normalise\")" , "")

##########################################################################################################################################
C_menu.addMenu( 'Color',  icon='Color.png' )
C_menu.addCommand( 'Color/Despill Mad', "nuke.createNode(\"Despill_Mad\")" , icon="Despill_Mad.png")
nuke.toolbar("Nodes").addMenu("C/Color").addSeparator()
C_menu.addCommand( 'Color/Crank It', "nuke.createNode(\"CrankIt\")" , icon="F_crankit.png")
C_menu.addCommand( 'Color/LayerContact Channel', "nuke.createNode(\"LayerContact_Channel\")" , icon="LayerContact_Channel.png")
C_menu.addCommand( 'Color/Chroma_Ab', "nuke.createNode(\"Chroma_Ab\")" , icon="Chroma_Ab.png")
C_menu.addCommand( 'Color/Expression Value', "nuke.createNode(\"Expression_Value\")" , icon="Expression_Value.png")
C_menu.addCommand( 'Color/Match_Intensity', "nuke.createNode(\"Match_Intensity\")" , icon="Match_Intensity.png")

##########################################################################################################################################
C_menu.addMenu( 'Filter',  icon='Filter.png' )
C_menu.addMenu( 'Filter/Edge',  icon='Blur.png' ) #Sous Menu
C_menu.addCommand( 'Filter/Edge/Push Pixel', "nuke.createNode(\"Push_Pixel\")" , icon="Push_Pixel.png")
C_menu.addCommand( 'Filter/Edge/Push Blur', "nuke.createNode(\"Push_Blur\")" , icon="Push_Blur.png")
nuke.toolbar("Nodes").addMenu("C/Filter/Edge").addSeparator()
C_menu.addCommand( 'Filter/Edge/Edge Tool', "nuke.createNode(\"Edge_Tool\")" , icon="Edge_Tool.png")
C_menu.addCommand( 'Filter/Edge/Edge Detect Acc', "nuke.createNode(\"EdgeDetect_Acc\")" , icon="EdgeDetect_Acc.png")
C_menu.addCommand( 'Filter/Edge/Edge Detect Angle', "nuke.createNode(\"EdgeDetect_Angle\")" , "")
nuke.toolbar("Nodes").addMenu("C/Filter/Edge").addSeparator()
C_menu.addCommand( 'Filter/Edge/Edge Roughen', "nuke.createNode(\"EdgeRoughen\")" , icon="F_edgeroughen.png")
#-----------------------------
C_menu.addCommand( 'Filter/IDefocus', "nuke.createNode(\"IDefocus\")" , icon="IDefocus.png")

##########################################################################################################################################
C_menu.addMenu( 'Merge',  icon='Merge.png' )
#-----------------------------
C_menu.addCommand( 'Merge/PSD Merge', "nuke.createNode(\"Merge_PSD\")" , icon="Merge_PSD.png")
C_menu.addCommand( 'Merge/Washer Merge', "nuke.createNode(\"Merge_Washer\")" , icon="Merge_Washer.png")

##########################################################################################################################################
C_menu.addMenu( 'Transform',  icon='Transform.png' )
#-----------------------------
C_menu.addCommand( 'Transform/Tracker Reformat', "nuke.createNode(\"Tracker_Reformat\")" , icon="Tracker_Reformat.png")
nuke.toolbar("Nodes").addMenu("C/Transform").addSeparator()
C_menu.addCommand( 'Transform/CornerPin Mix', "nuke.createNode(\"CornerPin_Mix\")" , icon="CornerPin_Mix.png")
C_menu.addCommand( 'Transform/ICornerPin C', "nuke.createNode(\"CornerPin_C\")" , icon="ICornerPin_C.png")
nuke.toolbar("Nodes").addMenu("C/Transform").addSeparator()
C_menu.addCommand( 'Transform/ITransform C', "nuke.createNode(\"ITransform_C\")" , icon="ITransform_C.png")
C_menu.addCommand( 'Transform/Transform_RefFrame', "nuke.createNode(\"Transform_RefFrame\")" , icon="Transform_RefFrame.png")
nuke.toolbar("Nodes").addMenu("C/Transform").addSeparator()
C_menu.addCommand( 'Transform/Crop C', "nuke.createNode(\"Crop_C\")" , icon="Crop_C.png")
C_menu.addCommand( 'Transform/Tile C', "nuke.createNode(\"Tile_C\")",  icon="Tile_C.png")

##########################################################################################################################################
C_menu.addMenu( '3D',  icon='3D.png' )
#-----------------------------
C_menu.addMenu( '3D/Position',  icon='Position.png' ) #Sous Menu
C_menu.addCommand( '3D/Position/Position To Card', "nuke.createNode(\"Position_To_Card\")" , icon="Position_To_Card.png")
C_menu.addCommand( '3D/Position/Position To UV', "nuke.createNode(\"Position_To_UV\")" , "")
nuke.toolbar("Nodes").addMenu("C/3D/Position").addSeparator()
C_menu.addCommand( '3D/Position/Position World Transform', "nuke.createNode(\"Position_World_Transform\")" , icon="Position_World_Transform.png")
#-----------------------------
C_menu.addMenu( '3D/Normal',  icon='Normal.png' ) #Sous Menu
C_menu.addCommand( '3D/Normal/Normal Mask', "nuke.createNode(\"Normal_Mask\")" , icon="Normal_Mask.png")
#-----------------------------
C_menu.addMenu( '3D/Deep',  icon='Deep.png' ) #Sous Menu
C_menu.addCommand( '3D/Deep/DeepSlice', "nuke.createNode(\"DeepSlice\")" , icon="DeepSlice.png")
nuke.toolbar("Nodes").addMenu("C/3D/Deep").addSeparator()
C_menu.addCommand( '3D/Deep/DeepMask (Beta)', "nuke.createNode(\"Deep_Mask\")" , "")
C_menu.addCommand( '3D/Deep/DeepRamp (Beta)', "nuke.createNode(\"Deep_Ramp\")" , "")
C_menu.addCommand( '3D/Deep/DeepHoldoutSmoother', "nuke.createNode(\"Deep_Holdout_Smoother\")" , "")
#-----------------------------
C_menu.addMenu( '3D/Camera',  icon='CameraFolder.png' ) #Sous Menu
C_menu.addCommand( '3D/Camera/CameraDissolve', "nuke.createNode(\"Camera_Dissolve\")", icon="Camera_Dissolve.png")
C_menu.addCommand( '3D/Camera/CameraRetimer', "nuke.createNode(\"Camera_Retimer\")", icon="Camera_Retimer.png")
C_menu.addCommand( '3D/Camera/CameraSmoother', "nuke.createNode(\"Camera_Smoother\")", "")
#-----------------------------
nuke.toolbar("Nodes").addMenu("C/3D").addSeparator()
C_menu.addCommand( '3D/Noise Spherical', "nuke.createNode(\"Noise_Spherical\")" , icon="Noise_Spherical.png")

##########################################################################################################################################
nuke.toolbar("Nodes").addMenu("C").addSeparator()
C_menu.addMenu( 'Other',  icon='F_script.png' )
#-----------------------------
C_menu.addCommand( 'Other/Dot Link src', "nuke.createNode(\"Dot_Link_src\")" ,"ctrl+shift+.",  icon="NoOp.png")
C_menu.addCommand( 'Other/Ruler 2D', "nuke.createNode(\"Ruler_2D\")" , icon="Ruler_2D.png")
C_menu.addMenu( 'Other/Controler',  icon='F_effect.png' ) #Sous Menu
C_menu.addCommand( 'Other/Controler/$GUI', "nuke.createNode(\"Control_$gui\")" , icon="Control_$gui.png")
C_menu.addCommand( 'Other/Controler/Disable Nodes', "nuke.createNode(\"Disable_Nodes\")" , icon="Disable_Nodes.png")
C_menu.addCommand( 'Other/Controler/ScanlineRender Ctrl', "nuke.createNode(\"ScanlineRender_Controller\")" , icon="ScanlineRender_Controller.png")
C_menu.addCommand( 'Other/Controler/Knob Ctrl', "nuke.createNode(\"Knobs_Ctrl\")" , icon="04_Knobs_Ctrl.png")
C_menu.addMenu( 'Other/Effect',  icon='F_effect.png' ) #Sous Menu
C_menu.addCommand( 'Other/Effect/Caustic', "nuke.createNode(\"Caustic\")" , icon="Caustic")
C_menu.addCommand( 'Other/Effect/Lightning', "nuke.createNode(\"Lightning\")" , icon="Lightning.png")
C_menu.addCommand( 'Other/Effect/Rain', "nuke.createNode(\"Rain\")" , icon="Rain.png")

CT = '- CGEV Tools .................... OK\n'
nuke.tprint(CT)
##############################           #