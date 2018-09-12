import nuke, nukescripts, math

try:
    # < Nuke 11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets
except:
    # >= Nuke 11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets

#---------------------------------------------

from menu import pipe_path
'''
nuke.pluginAddPath(path + './icons');
nuke.pluginAddPath(path + './icons/nodes');
nuke.pluginAddPath(path + './Gizmos');
nuke.pluginAddPath(path + './Gizmos/Franklin');
nuke.pluginAddPath(path + './Python');
nuke.pluginAddPath(path + './Python/More');
'''
#---------------------------------------------

import channel_hotbox
nuke.menu('Nuke').findItem('Edit').addCommand('HotBox', 'channel_hotbox.start()', '²')

import autoBackdrop as autoBackdrop
nukescripts.autoBackdrop = autoBackdrop.autoBackdrop
nuke.menu('Nodes').addCommand( 'Other/Backdrop', 'autoBackdrop.autoBackdrop()', 'alt+b', 'Backdrop.png')


##########################################################################################################################################
##########################################################################################################################################
#######                                                      #############################################################################
#######               ADD FRANKLIN TOOLS                     #############################################################################
#######                                                      #############################################################################
##########################################################################################################################################
##########################################################################################################################################


toolbar = nuke.toolbar("Nodes")
F_menu = toolbar.addMenu("Franklin", icon="F_menu.png")

##############################################################
#       TIME        ##########################################
##############################################################
F_menu.addMenu( 'Time', icon='F_time.png' )
##############################################################
F_menu.addCommand( 'Time/TimeCode_F', "nuke.createNode(\"TimeCode_F\")" , icon="F_tcode.png")
F_menu.addCommand( 'Time/FrameRange_Infos', "nuke.createNode(\"FrameRange_Infos\")" , icon="F_framerange_infos.png")
#_____________________________________________________________

##############################################################
#      CHANNEL      ##########################################
##############################################################
F_menu.addMenu( 'Channel',  icon='F_channel.png' )
##############################################################
F_menu.addCommand( 'Channel/ID_Merge', "nuke.createNode(\"ID_Merge\")" , icon="F_idmerge.png")
#_____________________________________________________________

##############################################################
#       COLOR       ##########################################
##############################################################
F_menu.addMenu( 'Color',  icon='F_color.png' )
##############################################################
F_menu.addCommand( 'Color/ColorMerge_F', "nuke.createNode(\"ColorMerge_F\")" , icon="F_colormerge.png")
F_menu.addCommand( 'Color/Normalize_F', "nuke.createNode(\"Normalize_F\")" , icon="F_normalize.png")
F_menu.addCommand( 'Color/Black_Lift', "nuke.createNode(\"BlackLift\")" , icon="F_blacklift.png")
F_menu.addCommand( 'Color/Despill_F', "nuke.createNode(\"Despill_F\")" , icon="F_despill.png")
#_____________________________________________________________

##############################################################
#       FILTER      ##########################################
##############################################################
F_menu.addMenu( 'Filter',  icon='F_filter.png' )
##############################################################
F_menu.addCommand( 'Filter/DirBlur_F', "nuke.createNode(\"DirBlur_F\")" , icon="F_dirblur.png")
F_menu.addCommand( 'Filter/Glow_F', "nuke.createNode(\"Glow_F\")" , icon="F_glow.png")
F_menu.addCommand( 'Filter/Sharpen_F', "nuke.createNode(\"Sharpen_F\")" , icon="F_sharpen.png")
F_menu.addCommand( 'Filter/Bokeh_List', "nuke.createNode(\"Bokeh_List\")" , icon="F_bokeh.png")
#_____________________________________________________________

##############################################################
#     TRANSFORM     ##########################################
##############################################################
F_menu.addMenu( 'Transform',  icon='F_transform.png' )
##############################################################
F_menu.addCommand( 'Transform/CameraShake_F', "nuke.createNode(\"CameraShake_F\")" , icon="F_camerashake.png")
F_menu.addCommand( 'Transform/Transform_Mix', "nuke.createNode(\"Transform_Mix\")" , icon="F_transformmix.png")
F_menu.addCommand( 'Transform/AutoCrop', "nukescripts.autocrop()",  icon="F_autocrop.png")
#_____________________________________________________________

##############################################################
#         3D        ##########################################
##############################################################
F_menu.addMenu( '3D',  icon='F_3D.png' )
##############################################################
F_menu.addMenu( '3D/Position',  icon='Yellow_Folder.png' )  ######################################## Sous Menu ##################
F_menu.addCommand( '3D/Position/Pos_Mask', "nuke.createNode(\"P_Mask\")" , icon="F_pmask.png")
F_menu.addCommand( '3D/Position/Pos_Ramp', "nuke.createNode(\"P_Ramp\")" , icon="F_pramp.png")
nuke.toolbar("Nodes").addMenu("Franklin/3D/Position").addSeparator()
F_menu.addCommand( '3D/Position/Pos_Project', "nuke.createNode(\"P_Project\")" , icon="F_pproject.png")
F_menu.addCommand( '3D/Position/Pos_Object', "nuke.createNode(\"P_Object\")" , icon="F_pobject.png")
nuke.toolbar("Nodes").addMenu("Franklin/3D/Position").addSeparator()
F_menu.addCommand( '3D/Position/Pos_Texture (UPDATE)', "nuke.createNode(\"Position_Texture\")" , icon="Position_Texture.png") #   ( NEED UPDATE)
#-------------------------------------------------------------------------------------------------------------------------------
F_menu.addMenu( '3D/Normals',  icon='Green_Folder.png' ) ########################################### Sous Menu ##################
F_menu.addCommand( '3D/Normals/Normals_Cam', "nuke.createNode(\"Normals_Cam\")" , icon="F_normalcam.png")
#-------------------------------------------------------------------------------------------------------------------------------
F_menu.addMenu( '3D/UV',  icon='Lightblue_Folder.png' )  ########################################### Sous Menu ##################
F_menu.addCommand( '3D/UV/UV_Ramp', "nuke.createNode(\"UV_Ramp\")" , icon="F_uvramp.png")
F_menu.addCommand( '3D/UV/UV_Grid', "nuke.createNode(\"UV_Grid\")" , icon="UV_Grid.png") #                                        ( NEED UPDATE)
F_menu.addCommand( '3D/UV/STMove (UPDATE)', "nuke.createNode(\"STMove\")" , icon="STMove.png") #                                  ( NEED UPDATE)
F_menu.addCommand( '3D/UV/UV_Card', "nuke.createNode(\"UV_Card\")" , icon="") #                                                   ( NEED UPDATE)
#-------------------------------------------------------------------------------------------------------------------------------
F_menu.addMenu( '3D/Depth',  icon='Grey_Folder.png' )    ########################################### Sous Menu ##################
F_menu.addCommand( '3D/Depth/Depth_Ramp (beta)', "nuke.createNode(\"Depth_Ramp\")" , icon="Depth_Ramp.png") #            ( NEED UPDATE)
F_menu.addCommand( '3D/Depth/Depth_Mask (beta)', "nuke.createNode(\"Depth_Mask\")" , icon="Depth_Mask.png") #            ( NEED UPDATE)
#-------------------------------------------------------------------------------------------------------------------------------
F_menu.addMenu( '3D/Deep',  icon='Blue_Folder.png' )     ########################################### Sous Menu ##################
F_menu.addCommand( '3D/Deep/DeepTo_Pos', "nuke.createNode(\"DeepTo_Pos\")" , icon="F_deeptopos.png")
#-------------------------------------------------------------------------------------------------------------------------------
nuke.toolbar("Nodes").addMenu("Franklin/3D").addSeparator()
F_menu.addCommand( '3D/NanRemove', "nuke.createNode(\"NanRemove\")" , icon="F_nanremove.png")
F_menu.addCommand( '3D/Reflections', "nuke.createNode(\"Reflections\")" , icon="F_reflections.png")
F_menu.addCommand( '3D/ScanlineRender_Fade', "nuke.createNode(\"ScanlineRender_Fade\")" , icon="F_scanlinerender.png")
#_____________________________________________________________

nuke.toolbar("Nodes").addMenu("Franklin").addSeparator()
#_____________________________________________________________

##############################################################
#       OTHER       ##########################################
##############################################################
F_menu.addMenu( 'Other',  icon='F_other.png' )
##############################################################
F_menu.addCommand( 'Other/VIEWER INPUT', "nuke.createNode(\"VIEWER_INPUT\")" , icon="F_viewer_input.png")
F_menu.addCommand( 'Other/Dot_Link', "nuke.createNode(\"DotLink\")" , "ctrl+.", icon="F_dotlink.png")

F_menu.addMenu( 'Other/Setup',  icon='F_setup.png' )          ########################################### Sous Menu ##################
F_menu.addCommand( 'Other/Setup/Preserve Bbox', "nuke.createNode(\"Preserve_bbox\")" , "")
#_____________________________________________________________

nuke.toolbar("Nodes").addMenu("Franklin").addSeparator()
#_____________________________________________________________

F_menu.addCommand("Reload F. Tools", 'import Reload as Reload; Reload.reloadMenu()',  icon="F_reload.png")
#_____________________________________________________________


##########################################################################################################################################
##########################################################################################################################################
#######                                                      #############################################################################
#######              CHANGE DEFAULT VALUE                    #############################################################################
#######                                                      #############################################################################
##########################################################################################################################################
##########################################################################################################################################


nuke.knobDefault('Multiply.value', '0' )
nuke.knobDefault('FilterErode.channels', 'rgba' )
nuke.knobDefault("Transform.shutteroffset", "center")
nuke.knobDefault("Tracker3.shutteroffset", "center")
nuke.knobDefault("Tracker4.shutteroffset", "center")
nuke.knobDefault("CornerPin2D.shutteroffset", "center")
nuke.knobDefault("ScanlineRender.shutteroffset", "center")
nuke.knobDefault("Project3D.crop", "false")
nuke.knobDefault("Roto.cliptype", "no clip")
nuke.knobDefault("RotoPaint.cliptype", "no clip")
nuke.knobDefault("Log2Lin.operation", "lin2log")
nuke.knobDefault("PLogLin.operation", "lin to log")
nuke.menu('Nodes').addCommand( "Time/FrameHold", "nuke.createNode('FrameHold')['first_frame'].setValue( nuke.frame() )",  'FrameHold.png')
nuke.knobDefault("Merge.bbox", "3")
nuke.knobDefault("Keymix.bbox", "1")
nuke.knobDefault("EXPTool.mode", "0")
nuke.knobDefault("StickyNote.note_font_size", "40") 
nuke.knobDefault('BackdropNode.note_font_size', '40')
nuke.knobDefault("BackdropNode.note_font", "bold")
#nuke.knobDefault("Read.before", "3")
#nuke.knobDefault("Read.after", "3")
#nuke.knobDefault("Read.on_error", "1")

# Change in Label...
nuke.knobDefault("TimeOffset.label", "[value time_offset]")
nuke.knobDefault("Tracker4.label", "[value transform] / [value reference_frame]")
nuke.knobDefault("Tracker3.label", "[value transform] / [value reference_frame]")


##########################################################################################################################################
##########################################################################################################################################
#######                                                      #############################################################################
#######              ADD TO VIEWER MENU                      #############################################################################
#######                                                      #############################################################################
##########################################################################################################################################
##########################################################################################################################################

import viewerInputNodes

v = nuke.menu("Viewer")
v.addCommand("-", '', '')
m = v.addMenu("IP")

m.addCommand('IP List','nuke.load("viewerInputNodes"), viewerInput()', "Ctrl+Alt+i",  icon="F_ip.png") 
m.addCommand('IP Remove','nuke.load("viewerInputNodes"), viewerInput(ipNode="Remove")', "Ctrl+Alt+Shift+i",  icon="F_ipr.png")



FT = '- Franklin Tools ................ OK'
nuke.tprint(FT)
##############################           #