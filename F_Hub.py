import nuke, nukescripts, random, colorsys
import webbrowser, os, re, inspect, subprocess, math
import nukescripts.rollingAutoSave
import os.path as op

# Add Directory 
from menu import path
nuke.pluginAddPath(path + './icons');
nuke.pluginAddPath(path + './icons/nodes');
nuke.pluginAddPath(path + './icons/grapichs');
nuke.pluginAddPath(path + './Python');
nuke.pluginAddPath(path + './Python/More');

#______________________________________________________________________________

import JFX_nodeScaler   #
import breakoutLayers   #
import rotoToTrack      #
import viewerInputNodes #
import superSwap        #
import shuffle_Smart    #

import gifwriter_ui

#______________________________________________________________________________


# Add Shortcuts
explorer = 'ctrl+r'                # open in explorer the folder of the selected (read or write)
create_dir = 'ctrl+alt+w'          # create directory from selected Read node

last_propertie = 'v'               # keep only the last propertie open (close all others)
last3_propertie = 'shift+v'        # keep only the 3 last properties open (close all others)
#--------------------------------------------------------------------------------------------
shuffle = 'alt+k'                  # create a Shuffle node
merge = 'm'                        # create a Merge node
keymix = 'shift+k'                   # create a Keymix node
multiply = 'shift+m'               # create a Multiply node
erode = 'e'                        # create a Erode (filter) node
tracker = 'alt+t'                  # create a Tracker node
transform = 't'                    # create a Merge node
#--------------------------------------------------------------------------------------------
duplicate_node = 'alt+v'           # duplicate the node and keep inputs
swap = 'shift+x'                   # options on multiple nodes (Grade, Transform, Ramp, Shuffle, CornerPin2D, Mirror, FrameHold, Blur, ColorCorrect, Grade)

sc_nodes = 'alt+1'                 # change the scale between nodes in the node graph
mir_nodes = 'alt+0'                # mirror on nodes in the node graph
do_nodes = 'alt+.'                 # intelligent dots

red_nodes = 'ctrl+shift+r'         # node tile color to red
green_nodes = 'ctrl+shift+g'       # node tile color to green
blue_nodes = 'ctrl+shift+b'        # node tile color to blue
cyan_nodes = 'ctrl+shift+e'        # node tile color to cyan
magenta_nodes = 'ctrl+shift+f'     # node tile color to magenta
yellow_nodes = 'ctrl+shift+v'      # node tile color to yellow
customcolor_nodes = 'ctrl+shift+c' # node tile color to default color

outline_ico = 'ctrl+alt+shift+a'   #
topline_ico = 'ctrl+alt+shift+z'   #
grey_ico = 'ctrl+alt+shift+e'      #
zebra_ico = 'ctrl+alt+shift+r'     #
check_ico = 'ctrl+alt+shift+t'     #
arrow_ico = 'ctrl+alt+shift+y'     #
custom_ico = 'ctrl+alt+shift+u'    #

upscale_name = 'ctrl+alt++'        #
downscale_name = 'ctrl+alt+-'      #
nodefont_black = 'ctrl+alt+e'      #
nodefont_red = 'ctrl+alt+r'        #
nodefont_white = 'ctrl+alt+t'      #

########################################################################    ## ##  #####  ##  #  #   #         ######    
menubar = nuke.menu("Nuke")                                     ########    # # #  #      # # #  #   #         #          
m = menubar.addMenu("&Franklin VFX",  "franklin.png")           ########    #   #  ###    # # #  #   #         ###       
########################################################################    #   #  #####  #  ##  #####         # 

m.addMenu('Node Graph', "F_node.png")    # Dossier 
m.addCommand('Node Graph/Scale Tool', JFX_nodeScaler.ScaleNodes, sc_nodes, "F_nodetools.png") #######################################################################################
m.addCommand('Node Graph/Mirror', 'mirrorNodes.mirrorNodes( nuke.selectedNodes(), direction="x" )', mir_nodes, "F_mirror.png") #######################################################################################
m.addMenu("Node Graph").addSeparator()   #######
m.addCommand('Node Graph/Dots','Dots.Dots()', do_nodes, "Dot.png") #######################################################################################
m.addMenu("Node Graph").addSeparator()   #######
m.addMenu('Node Graph/Customize', "F_customnode.png")    # Dossier 

m.addMenu('Node Graph/Customize/Color', "F_ccolornode.png")   # Dossier  
m.addCommand("Node Graph/Customize/Color/Red", lambda: batchTileColor(4278190335), red_nodes, 'F_rn.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Color/Green", lambda: batchTileColor(16711935), green_nodes, 'F_gn.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Color/Blue", lambda: batchTileColor(65535), blue_nodes, 'F_bn.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Color/Cyan", lambda: batchTileColor(16777215), cyan_nodes, 'F_cn.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Color/Magenta", lambda: batchTileColor(4278255615), magenta_nodes, 'F_mn.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Color/Yellow", lambda: batchTileColor(4294902015), yellow_nodes, 'F_yn.png', shortcutContext=2)
m.addMenu("Node Graph/Customize/Color").addSeparator()   #######
m.addCommand("Node Graph/Customize/Color/Custom", lambda: batchTileColor(), customcolor_nodes, 'F_ccolornode.png', shortcutContext=2)

####
m.addMenu('Node Graph/Customize/Advance', "F_nodeadvance.png")    # Dossier  
m.addCommand("Node Graph/Customize/Advance/Outline", "F_Hub.icongreen()", outline_ico, 'F_outlineon.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Advance/Topline", "F_Hub.iconline()", topline_ico, 'F_toplineon.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Advance/Grey", "F_Hub.icongrey()", grey_ico, "")
m.addCommand("Node Graph/Customize/Advance/Zebra", "F_Hub.iconzebrar()", zebra_ico, 'F_zebraon.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Advance/Mark", "F_Hub.iconcroixb()", check_ico, 'F_markon.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Advance/Arrow", "F_Hub.iconarrow()", arrow_ico, 'F_arrowon.png', shortcutContext=2)
m.addMenu("Node Graph/Customize/Advance").addSeparator()   #######
#### 
m.addMenu('Node Graph/Customize/Advance/More', "F_scalep.png")    # Dossier   
m.addCommand("Node Graph/Customize/Advance/More/On Left", "F_Hub.fdoticon()", custom_ico, 'F_fon.png', shortcutContext=2)
m.addCommand("Node Graph/Customize/Advance/More/On Right", "F_Hub.ficon()", 'F_fon.png')
m.addMenu("Node Graph/Customize/Advance").addSeparator()     #######
m.addCommand("Node Graph/Customize/Advance/Remove", "F_Hub.noicon()", "F_scalem.png")
####
m.addMenu("Node Graph/Customize/Font", "F_text.png")    # Dossier  
m.addCommand("Node Graph/Customize/Font/Increase Size", "F_Hub.changeNodeFontSize(4)", upscale_name, "F_scalep.png", shortcutContext=2)
m.addCommand("Node Graph/Customize/Font/Decrease Size", "F_Hub.changeNodeFontSize(-4)", downscale_name, "F_scalem.png", shortcutContext=2)
m.addCommand("Node Graph/Customize/Font/-", "", "")
m.addCommand("Node Graph/Customize/Font/To Black", "F_Hub.textToBlack()", nodefont_black, "F_textb.png", shortcutContext=2)
m.addCommand("Node Graph/Customize/Font/-", "", "")
m.addCommand("Node Graph/Customize/Font/To Red", "F_Hub.textToRed()", nodefont_red, "F_textr.png", shortcutContext=2)
m.addCommand("Node Graph/Customize/Font/Select all Red", "F_Hub.selectRedTextNodes()")
m.addCommand("Node Graph/Customize/Font/-", "", "")
m.addCommand("Node Graph/Customize/Font/To White", "F_Hub.textToWhite()", nodefont_white, "F_textw.png", shortcutContext=2)
m.addCommand("Node Graph/Customize/Font/Select all White", "F_Hub.selectWhiteTextNodes()")
#######################################################################################
m.addMenu("Properties Pane", "F_prop.png")   # Dossier 
m.addCommand("Properties Pane/Keep Last", "F_Hub.ClosePropertiesButLast(1)", last_propertie, "F_pan1.png")
m.addCommand("Properties Pane/Keep 3 Last", "F_Hub.ClosePropertiesButLast(3)", last3_propertie, "F_pan3.png")
#######################################################################################
m.addMenu('Viewer', "F_viewer.png")
m.addMenu("Viewer/Input Process", "F_ip.png")   # Dossier 
m.addCommand('Viewer/Input Process/Create','nuke.load("viewerInputNodes"), viewerInput()', "Ctrl+Alt+i", "F_list.png") #######################################################################################
m.addCommand('Viewer/Input Process/Remove','nuke.load("viewerInputNodes"), viewerInput(ipNode="Remove")', "Ctrl+Alt+Shift+i", "F_delete.png") #######################################################################################
m.addMenu("Viewer").addSeparator()   #######
####
m.addMenu("Viewer/Go to Node", "F_go.png")   # Dossier 
m.addCommand("Viewer/Go to Node/Active Node", "F_Hub.goToActiveNode()","Ctrl+0", "F_active.png")
m.addMenu("Viewer/Go to Node").addSeparator()   #######
m.addCommand("Viewer/Go to Node/In Viewer 1", "F_Hub.goToActiveNthNode(1)", "ctrl+1")
m.addCommand("Viewer/Go to Node/In Viewer 2", "F_Hub.goToActiveNthNode(2)", "ctrl+2")
m.addCommand("Viewer/Go to Node/In Viewer 3", "F_Hub.goToActiveNthNode(3)", "ctrl+3")
m.addCommand("Viewer/Go to Node/In Viewer 4", "F_Hub.goToActiveNthNode(4)", "ctrl+4")
m.addCommand("Viewer/Go to Node/In Viewer 5", "F_Hub.goToActiveNthNode(5)", "ctrl+5")
m.addCommand("Viewer/Go to Node/In Viewer 6", "F_Hub.goToActiveNthNode(6)", "ctrl+6")
m.addCommand("Viewer/Go to Node/In Viewer 7", "F_Hub.goToActiveNthNode(7)", "ctrl+7")
m.addCommand("Viewer/Go to Node/In Viewer 8", "F_Hub.goToActiveNthNode(8)", "ctrl+8")
m.addCommand("Viewer/Go to Node/In Viewer 9", "F_Hub.goToActiveNthNode(9)", "ctrl+9")
####
m.addMenu("Viewer").addSeparator()   #######
m.addCommand("Viewer/Viewer Up", "F_Hub.navUp()","Shift+Up", "F_up.png")
m.addCommand("Viewer/Viewer Down", "F_Hub.navDown()","Shift+Down", "F_down.png")
m.addMenu("Viewer").addSeparator()   #######
m.addCommand("Viewer/Which Buffer", "F_Hub.whichBuffer()","Ctrl+Shift+h", "F_markg.png")
m.addSeparator()
#######################################################################################
m.addMenu("Read - Write", "F_explorer.png")
m.addMenu('Read - Write/Read',  'F_read.png') # Dossier #######
m.addCommand("Read - Write/Read/Set Project From Read", "F_Hub.setProjectBoundsFromRead()",  'F_set.png')
m.addCommand('Read - Write/Read/Open Read in Explorer','F_Hub.Revealexplr()', explorer,  'F_explore.png', shortcutContext=2)
m.addCommand('Read - Write/Read/Rename Tool', 'import batchrenamer; batchrenamer.main()',  'F_superswap.png') #######################################################################################
####
m.addMenu('Read - Write/Read All',  'F_read.png') # Dossier #######
m.addCommand('Read - Write/Read All/Reload All', 'F_Hub.readReload()',  'F_reload.png')
m.addCommand('Read - Write/Read All/Reload All Geo', 'F_Hub.geoReload()',  'F_reloadgeo.png')
m.addCommand('Read - Write/Read All/Cache To Always', "F_Hub.cacheLocalSelected()",  'F_cache.png')
####
m.addMenu('Read - Write/Read All/Missing Frames',  'F_markg.png') # Dossier #######
m.addCommand("Read - Write/Read All/Missing Frames/Error", 'F_Hub.setError()',  'F_error.png')
m.addCommand("Read - Write/Read All/Missing Frames/Black", 'F_Hub.black()',  'F_black.png')
m.addCommand("Read - Write/Read All/Missing Frames/Checkerboard", 'F_Hub.checkerboard()',  'F_checker.png')
m.addCommand("Read - Write/Read All/Missing Frames/Nearest frame", 'F_Hub.nearestFrame()',  'F_nearest.png')
####
m.addMenu("Read - Write").addSeparator()   #######
m.addMenu('Read - Write/Write',  'F_write.png') # Dossier #######
m.addCommand("Read - Write/Write/Create Folder for Selected Write", "F_Hub.createDirForSelectedWrites()", create_dir,  'F_folder.png') 
####
m.addMenu("Read - Write").addSeparator()   #######
m.addCommand('Read - Write/EXR To Camera', 'F_Hub.fetchMetaCamToTransform()',  'Camera.png')
#######################################################################################
m.addMenu('Knobs', "F_knob.png")    # Dossier 
m.addCommand('Knobs/Set Value', 'F_Hub.setValue()',  "F_setv.png")
m.addCommand('Knobs/Set Expression', 'F_Hub.setExpression()',  "F_sete.png")
#######################################################################################
m.addSeparator()
#import breakoutLayers
import shuffleChannels
import multiChannelSplit
m.addCommand('Break Out v2', multiChannelSplit.MultiChannelSplit) #######################################################################################
m.addCommand('Break Out', shuffleChannels.getData, '') #######################################################################################
m.addCommand('Backdrop Re-Order UPDATE', 'F_Hub.reArrangeBDsByArea()', 'Ctrl+Alt+b')
m.addCommand('Roto To Track', rotoToTrack.Roto_to_Trackers) #######################################################################################
#######################################################################################
m.addSeparator()
m.addMenu('Additional Shortcuts', "F_short.png")   # Dossier 
m.addCommand('Additional Shortcuts/Shuffle', "nuke.createNode( \'Shuffle\' )", shuffle, "Shuffle.png", shortcutContext=2)
m.addCommand('Additional Shortcuts/Merge      Smart', 'F_Hub.mergeThis()', merge, "F_merge.png", shortcutContext=2)
m.addCommand('Additional Shortcuts/KeyMix', "nuke.createNode( \'Keymix\' )", keymix, "Keymix.png", shortcutContext=2)
m.addMenu("Additional Shortcuts").addSeparator()   #######
m.addCommand('Additional Shortcuts/Multiply', "nuke.createNode( \'Multiply\' )", multiply, "ColorMult.png", shortcutContext=2)
m.addCommand('Additional Shortcuts/FilterErode', "nuke.createNode( \'FilterErode\' )", erode, "FilterErode.png", shortcutContext=2)
m.addCommand("Additional Shortcuts/Tracker", "nuke.createNode(\"Tracker4\")", tracker, "Tracker.png", shortcutContext=2)
m.addCommand('Additional Shortcuts/Transform  Smart', 'F_Hub.transformThis()', transform, "F_transformg.png", shortcutContext=2)
m.addMenu("Additional Shortcuts").addSeparator()   #######
m.addCommand("Additional Shortcuts/Duplicate", "F_Hub.copyKeepInputs(nuke.selectedNodes())", duplicate_node, "F_duplicate.png", shortcutContext=2)
m.addCommand("Additional Shortcuts/Super Swap", 'import superSwap as superSwap; superSwap.swapper()', swap, "F_superswap.png", shortcutContext=2) #######################################################################################
#######################################################################################
#m.addSeparator()
#m.addCommand("My Web Site !", "F_Hub.infos()",  "F_markg.png")

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################


def setError():
	selection = nuke.allNodes("Read")
	for i in selection:
		i.knob("on_error").setValue("error")
		
def black():
	selection = nuke.allNodes("Read")
	for i in selection:
		i.knob("on_error").setValue("black")
		
def checkerboard():
	selection = nuke.allNodes("Read")
	for i in selection:
		i.knob("on_error").setValue("checherboard")

def nearestFrame():
	selection = nuke.allNodes("Read")
	for i in selection:
		i.knob("on_error").setValue("nearest frame")

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def transformThis(): 
    try: 
        if 'render_mode' in nuke.selectedNode().knobs(): 
            return nuke.createNode( 'TransformGeo' )
        elif 'Deep' in nuke.selectedNode().Class(): 
            return nuke.createNode( "DeepTransform")
        else:
            nuke.createNode( 'Transform' )   
    except: 
        return nuke.createNode( 'Transform' ) 

def smMerge(nodeType):
    a = nuke.selectedNodes()
    al = []
    for node in a:
        al.append(node['xpos'].value())
        al.sort()
        al.reverse()


    amm =  len(al)
    new = [None]*amm
    p = 0
    while p< amm:   
        a = nuke.selectedNodes()
        for one in a:
            pos = one['xpos'].value()
            if pos == al[p]:
                new.insert(p,one)
        #print new[:amm]
        p+=1

    q=1
    merges = []
    for node in new[:amm]: 
        if q==1:
            followed = node
            q+=1
        else:
            if nodeType== "MergeGeo":
                follower = nuke.nodes.MergeGeo()
                #merges.append(follower)
            if nodeType== "MergeMat":
                follower = nuke.nodes.MergeMat()
                #merges.append(follower)
            if nodeType== "DeepMerge":
                follower = nuke.nodes.DeepMerge()
                #merges.append(follower)
            if nodeType== "Merge2":
                follower = nuke.nodes.Merge2()
                #merges.append(follower)
            follower.setInput(0,followed)
            follower.setInput(1,node)
            followed = follower
            merges.append(follower)
    for node in nuke.allNodes():
        node.setSelected(False)
    for node in merges:
        node.setSelected(True)

def mergeThis():
    import nuke 
    try: 
        if 'shadow_override' in nuke.selectedNode().knobs() or 'Camera' in nuke.selectedNode().Class() or 'render_mode' in nuke.selectedNode().knobs() or 'Light' in nuke.selectedNode().Class() or 'DisplaceGeo' in nuke.selectedNode().Class() or 'Axis' in nuke.selectedNode().Class():
            if len(nuke.selectedNodes())==1:
                return nuke.createNode( "MergeGeo")
            else:
                smMerge("MergeGeo")

        elif 'MergeMat' in nuke.selectedNode().Class() or 'project_on' in nuke.selectedNode().knobs() or 'Mat' in nuke.selectedNode()['name'].value(): 
             if len(nuke.selectedNodes())==1:
                return nuke.createNode( "MergeMat")
             else:
                smMerge("MergeMat")
        elif 'Deep' in nuke.selectedNode().Class() and "DeepHoldout" not in nuke.selectedNode()['name'].value() and "DeepToImage" not in nuke.selectedNode()['name'].value(): 
             if len(nuke.selectedNodes())==1:
                return nuke.createNode( "DeepMerge")
             else:
                smMerge("DeepMerge")
        else: 
            raise ValueError 
    except: 
         if len(nuke.selectedNodes())<=1:
            return nuke.createNode( "Merge2")

         else:
            smMerge("Merge2")

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
	
def readReload () :
    [i.knob('reload').execute() for i in nuke.allNodes() if i.Class()=='Read']
	
def geoReload () :
    [i.knob('reload').execute() for i in nuke.allNodes() if i.Class()=='ReadGeo2']
	
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################	

def setValue():
	selNodes = nuke.selectedNodes()

	panel = nuke.Panel("Change Value")
	panel.addSingleLineInput("Knob", '...')
	panel.addSingleLineInput("Value", '...')
	panel.addBooleanCheckBox("Value is a number?", False)
	panel.show()

	kVal = panel.value("Knob")
	vVal = panel.value("Value")
	num = panel.value("Value is a number?")

	if num == True:
		 f = float(vVal)
		 if not vVal == "...":
			 for s in selNodes:
				 s[kVal].setValue(f)

	elif  num == False:
		if not vVal == "...":
			for s in selNodes:
				s[kVal].setValue(vVal) 

def setExpression():
	selNodes = nuke.selectedNodes()

	panel = nuke.Panel("Set Expression")
	panel.addSingleLineInput("Knob", '...')
	panel.addSingleLineInput("Expression", '...')
	panel.show()

	kVal = panel.value("Knob")
	eVal = panel.value("Expression")

	for s in selNodes:
		if not s[kVal].isAnimated():
			s[kVal].setExpression(eVal)

		else:
			if nuke.ask('One or more of the selected knobs already has an expression, replace?'):
				s[kVal].setExpression(eVal)

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def icongreen():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_greyg.png') # Green Outline
	  
def iconline():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_yeline.png') # Yellow Line on Top
	  	  
def icongrey():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_grey.png') # Full Grey
	  
def iconcroixb():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_croixb.png') # White Mark
	  
def iconzebrar():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_zebrar.png') # Red Zebra
	  
def iconarrow():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_arrow.png') # Arrow
	  
def ficon():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_onnode.png') # F on Right

def fdoticon():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_ondot.png') # F on Left

def moreicon():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_head.png') # CUSTOM MORE
	  
def noicon():
  for node in nuke.selectedNodes():
      node["icon"].setValue('') # No ICON

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
		
def Revealexplr():
    a=nuke.selectedNode()
    b=a['file'].value()
    u=os.path.split(b)[0]
    u = os.path.normpath(u)
    cmd = 'explorer "%s"' % (u)
    os.system(cmd)

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def setProjectBoundsFromRead():
    try:
        sel = nuke.selectedNode()
    except Exception:
        nuke.message("Please select a Read Node")
        return
    if sel.Class()=="Read":
        nuke.root()['first_frame'].setValue( sel['first'].value() )
        nuke.root()['last_frame'].setValue( sel['last'].value() )
        nuke.root()['format'].setValue( sel['format'].value() )
    else:
        nuke.message("Please select a Read Node")

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def togglePreviousNode() :
  global main
  global prev
  av = nuke.activeViewer()
  try :
   ai = av.activeInput()
   avn = av.node()
   curr = avn.input(ai)
   try :
    if main :
     if not(curr==main or curr==prev):
      del main
   except :
    main = avn.input(ai)
   if main == curr :
    prev = curr.input(0)
    nuke.connectViewer( ai, prev )
   else :
    nuke.connectViewer( ai, main )
    prev = main.input(0)
    del main
  except :
     print 'no active viewer'
	 
def navDown() : 
  av = nuke.activeViewer()
  ai = av.activeInput()
  avn = av.node()
  curr = avn.input(ai)
  nextlist = curr.dependent()
  next = nextlist[0]
  nuke.connectViewer( ai, next )
  
def navUp() : 
  av = nuke.activeViewer()
  ai = av.activeInput()
  avn = av.node()
  curr = avn.input(ai)
  prev = curr.input(0)
  nuke.connectViewer( ai, prev )
  
def goToActiveNode():
    av = nuke.activeViewer()
    ai = av.activeInput()
    avn = av.node().input(ai)
    nuke.zoom( 1, [ avn.xpos(), avn.ypos() ] )
	
def goToActiveNthNode(nth):
    av = nuke.activeViewer()
    if nth-1<0:
        avn = av.node().input(9)   
    else: 
        avn = av.node().input(nth-1)
    nuke.zoom( 1, [ avn.xpos(), avn.ypos() ] )
	
def whichBuffer():
	av = nuke.activeViewer()
	try :
		ai = int(av.activeInput()) + 1
		if ai == 10:
			ai = 0
		nuke.message( "Current Buffer : "+str(ai) )
	except Exception:
		pass
    
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def readFromWrite():
    read_list = []
    sel_list = nuke.selectedNodes()
    for sel in sel_list:
        if sel.Class() in ['Write', 'Read']:
            filepath =  sel['file'].evaluate()
            filenamebase =  filepath.split('/')[-1].split('.')[0]
            ext = filepath.split('.')[-1]
            dirpath = op.dirname( filepath )
            print nuke.getFileNameList( dirpath )
            for elt in nuke.getFileNameList( dirpath ):
                if filenamebase in elt and elt.split('.')[-1].split(' ')[0] == ext:
                    read = nuke.createNode('Read')
                    read['file'].fromUserText( dirpath + '/' + elt )
                    read.setXYpos(sel.xpos()+50,sel.ypos()+20)
                    read_list.append(read)
    for read in read_list:
        read.setSelected(True)
'''
def writeFromRead():
    description = "_" + nuke.getInput('add description to unify your files\n(it will add it also to a new directory)', 'draft')
    for read in nuke.selectedNodes():
        nukescripts.clear_selection_recursive()
        read.setSelected(True)
        filepath = read['file'].value()
        dirpath = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        if read.Class()=="Read":
            padding = filename.split(".")[-2]
            write = nuke.createNode("Write")
            #write['beforeRender'].setValue( "beforeRenderActions()" )
            write.setName("Write_from_" + read.name())
            write['file'].setValue( dirpath + description + "/" + filename.replace("."+padding, description+"."+padding))
'''
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def createDirForSelectedWrites():
    for sel in nuke.selectedNodes():
        if sel.Class()=="Write" or sel.Class()=="WriteGeo":
            dirpath = os.path.dirname( sel['file'].value() ) + '/'
            if not os.path.exists(dirpath):
                ask = nuke.ask("Create this path ? \n" + dirpath)
                if ask:
                    os.makedirs(dirpath)
            else:
                nuke.message("Path already exists")
        else:
            nuke.message("Create path ONLY for Write nodes")

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def cacheLocalSelected():
    for n in nuke.selectedNodes():
        try:
            n['cacheLocal'].setValue('always')
        except Exception:
            pass
			
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
			
def changeNodeFontSize(_multiplier):
    bd = []
    nodes = nuke.selectedNodes()
    for node in nodes:
        if node.Class()=="BackdropNode":
            bd.append(node)
    if bd!=[]:
        nodes = bd
    for node in nodes:
        node['note_font_size'].setValue(node['note_font_size'].value()+1*_multiplier)

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def textToRed():
    for n in nuke.selectedNodes():
        n['note_font_color'].setValue(0xaf0505ff)
		
def textToWhite():
    for n in nuke.selectedNodes():
        n['note_font_color'].setValue(4294967295)
		
def textToBlack():
    for n in nuke.selectedNodes():
        n['note_font_color'].setValue(0)
		
def selectRedTextNodes():
    for n in nuke.allNodes():
        if n['note_font_color'].value() == 0xaf0505ff:
            n['selected'].setValue(True)
			
def selectWhiteTextNodes():
    for n in nuke.allNodes():
        if n['note_font_color'].value() == 4294967295:
            n['selected'].setValue(True)

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def ClosePropertiesButLast(n) :
    p = nuke.toNode("preferences")
    max = p['maxPanels'].value()
    p['maxPanels'].setValue(n)
    p['maxPanels'].setValue(max)
	
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def selectDependencies():
    selectedNode = nuke.selectedNode()
    depNodes = selectedNode.dependencies()
    for depNode in depNodes:
     depNode.setSelected( True )
	 
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
	
def infos():
    webbrowser.open("http://www.franklinvfx.com")

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def copyKeepInputs(node_list):
    dst_list = []
    for src in node_list:
        xpos = src.xpos()
        ypos = src.ypos()
        nukescripts.clear_selection_recursive()
        src.setSelected(True)
        nuke.nodeCopy(nukescripts.cut_paste_file())
        nukescripts.clear_selection_recursive()
        dst = nuke.nodePaste(nukescripts.cut_paste_file())
        for input in range(src.inputs()):
            dst.setInput(input,src.input(input))                
        dst.setXYpos(xpos+30, ypos+30)
        dst_list.append(dst)
    nukescripts.clear_selection_recursive()
    for dst in dst_list:
        dst.setSelected(True)

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################
		
global transform_keyword

def translate(_axis, _exr, _frame, _view):
    list=_exr.metadata(transform_keyword, _frame, _view)
    if transform_keyword=="exr/worldToCamera":   # so it's an Arnold Cam 
        list = matrixToList( mayaToNukeMatrixConv( listToMatrix(list), "translate") )
    if (list==None):
        return 0
    else:
        if transform_keyword=="exr/worldToCamera":   # so it's an Arnold Cam 
            if _axis=="x":
                return list[3]
            elif _axis=="y":
                return list[7]
            elif _axis=="z":
                return list[11]
        else:                           # else it might be a V-ray Cam, who seriously use Mental Ray yet !?
            if _axis=="x":
                return list[12]
            elif _axis=="y":
                return list[13]
            elif _axis=="z":
                return list[14]

def rotation(_axis, _exr, _frame, _view): 
    list = _exr.metadata(transform_keyword, _frame, _view)
    if transform_keyword=="exr/worldToCamera":   # so it's an Arnold Cam 
        list = matrixToList( mayaToNukeMatrixConv( listToMatrix(list), "rotate" ) )
    if (list==None):
        print 'NoneType'
        return 0
    else:
        list.pop(15)
        list.pop(14)
        list.pop(13)
        list.pop(12)
        list.pop(11)
        list.pop(7)
        list.pop(3)     
        M=mat3(list)
        swappedM=mat3(list)
        
        if transform_keyword=="exr/worldToCamera":   # so it's an Arnold Cam 
            swappedM.setRow(2,M.getRow(2)*-1.0)
            swappedM.setRow(0,M.getRow(0)*-1.0)
        else:
            swappedM.setRow(1,M.getRow(2)*-1.0)
            swappedM.setRow(2,M.getRow(1))

        eulerAngles=swappedM.toEulerXYZ()
        if _axis=="x":
            return -math.degrees(eulerAngles[0])
        elif _axis=="y":
            if transform_keyword=="exr/worldToCamera":   # so it's an Arnold Cam 
                return math.degrees(eulerAngles[1])
            else:
                return -math.degrees(eulerAngles[1])
        elif _axis=="z":
            return -math.degrees(eulerAngles[2])

def listToMatrix(list):
    m = nuke.math.Matrix4()
    try: 
        for i in range(16):
            m[i] = list[i]
    except:
        raise
    return m
    
def matrixToList(mat):
    list = []
    try: 
        for i in range(16):
            list.append( mat[i] )
    except:
        raise
    return list
        
def mayaToNukeMatrixConv( m, _TrsRot ):
    flipZ=nuke.math.Matrix4()
    flipZ.makeIdentity()
    if _TrsRot=="translate":
        flipZ.scale(1,1,-1)
        m.transpose()
    m=m*flipZ
    m = m.inverse()
    return m
        
def fetchMetaCamToTransform():
    exr = nuke.selectedNode()
    global transform_keyword
    if exr.metadata('exr/arnold')==None:   # "It's not an Arnold EXR so let's go with a V-ray one !"
        focal_keyword = "exr/cameraFocalLength"
        haperture_keyword = "exr/cameraAperture"
        transform_keyword = "exr/cameraTransform"
    else:                                                    # else it might be a V-ray Cam, who seriously use Mental Ray yet !?
        focal_keyword = "exr/CameraFocalLength"
        haperture_keyword = "exr/CameraFilmApertureHorizontal"
        transform_keyword = "exr/worldToCamera"
        
    first_frame = exr["first"].value()
    last_frame = exr["last"].value()
    cam = nuke.createNode("Camera2", "name EXRcam")
    cam['label'].setValue("from " + exr['file'].value().split("/")[-1].split("%")[0] + "\n" + exr.metadata('input/ctime'))
    if len(nuke.views()) > 1:
        cam['translate'].splitView()
        cam['rotate'].splitView()
    cam['rot_order'].setValue('XYZ')
    for view in nuke.views():
        for cur_frame in range(first_frame, last_frame + 1):
            task = nuke.ProgressTask( 'Baking camera from metadata')
            if task.isCancelled():
              break
            task.setMessage( 'processing frame %s' % cur_frame )
            k = cam['focal']
            k.setAnimated(0, view)
            a = k.animations(view)
            focal = exr.metadata(focal_keyword, cur_frame, view)
            # if exr.metadata('exr/arnold')!=None:
                # focal = focal*10
            print "focal : ", focal
            a[0].setKey(cur_frame, focal)
            #cam['near'].setValue(exr.metadata('exr/clipNear', cur_frame, view))
            #cam['far'].setValue(exr.metadata('exr/clipFar', cur_frame, view))
            cam['haperture'].setValue(exr.metadata(haperture_keyword))
            cam['vaperture'].setValue(exr.metadata(haperture_keyword)*exr.metadata('input/height')/exr.metadata('input/width'))
            kt = cam['translate']
            kt.setAnimated(0, view)
            cam_aniX = cam['translate'].animations(view)[0]
            cam_aniX.setKey(cur_frame, translate("x",exr, cur_frame, view))
            kt.setAnimated(1, view)
            cam_aniY = cam['translate'].animations(view)[1]
            cam_aniY.setKey(cur_frame, translate("y", exr, cur_frame, view))
            kt.setAnimated(2, view)
            cam_aniY = cam['translate'].animations(view)[2]
            cam_aniY.setKey(cur_frame, translate("z", exr, cur_frame, view))
            kr = cam['rotate']
            kr.setAnimated(0, view)
            cam_aniX = cam['rotate'].animations(view)[0]
            cam_aniX.setKey(cur_frame, rotation("x", exr, cur_frame, view))
            kr.setAnimated(1, view)
            cam_aniY = cam['rotate'].animations(view)[1]
            cam_aniY.setKey(cur_frame, rotation("y", exr, cur_frame, view))
            kr.setAnimated(2, view)
            cam_aniY = cam['rotate'].animations(view)[2]
            cam_aniY.setKey(cur_frame, rotation("z", exr, cur_frame, view))
            task.setProgress( int(cur_frame/last_frame*100 ) )
         		 
#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def batchTileColor(nukeHex = None):
    if nukeHex == None:
        nukeHex = nuke.getColor()
    for node in nuke.selectedNodes():
        node.knob('tile_color').setValue(nukeHex)

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################

def killViewers():
    for v in nuke.allNodes("Viewer"):
        nuke.delete(v)
nuke.addOnScriptLoad(killViewers)

#####################################################################################################################################
#####################################################################################################################################
#####################################################################################################################################