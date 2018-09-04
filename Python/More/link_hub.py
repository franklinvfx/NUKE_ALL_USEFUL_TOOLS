
# Philippe HUBERDEAU


import nuke, nukescripts
import inspect, os, re, webbrowser


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

def createLinkContainer():
    try:
        sel = nuke.selectedNode()
        nukescripts.clear_selection_recursive()
    except Exception:
        sel = nuke.thisNode()
    link = nuke.createNode("PostageStamp")
    link.setInput(0,sel)
    if link.input(0)==None:      # so connection failed, the selection is a 3d node and postageStamp can't connect
        nukescripts.node_delete(popupOnError=True)
        link = nuke.createNode("NoOp")     # NoOp can connect to 3d nodes
        link['tile_color'].setValue(0xff0000ff) # dark red to indicate relation to 3D node
    else:
        #link = nuke.createNode("PostageStamp")
        link['postage_stamp'].setValue(True)
        link['tile_color'].setValue(0xff0000ff)
        link['note_font_size'].setValue(10)
        link['note_font_color'].setValue(0x400ff)
    return link
def linkDressing(_link):
    _link['note_font_size'].setValue(10)
    _link['hide_input'].setValue(False)
	

def renameByFamily(_thisNode, _lnklbl):
    ''' _lnklblh has two possible values : "Linked_" or "Src_" to know which type of node run the script '''
    oldname = _thisNode.name().split(_lnklbl)[-1] + "0" # little hack to avoid no number at the end
    # num = re.search('\d+', oldname).group(0)
    # oldname = oldname.split(num)[0]
    oldname = ("_").join(oldname.split("_")[:-1])   # rip the last characters after "_"
    newname = nuke.getInput("New Name", oldname)
    family = []
    link_class = []
    for ps in nuke.allNodes("PostageStamp"):
        link_class.append(ps)
    for ps in nuke.allNodes("NoOp"):
        link_class.append(ps)        
    for ps in link_class:
        psname = ps.name().split("Linked_")[-1] + "0"
        # num = re.search('\d+', psname).group(0)
        # psname = psname.split(num)[0]
        psname = ("_").join(psname.split("_")[:-1])   # rip the last characters after "_"
        if psname == oldname:
            family.append(ps)
    for link in family:
        link.setName("Linked_"+newname)
    if _lnklbl=="Linked_":
        _thisNode.input(0).setName("Src_"+newname)
    else:
        _thisNode.setName("Src_"+newname)

def selectByFamily(_thisNode, _lnklbl):
    ''' _lnklblh has two possible values : "Linked_" or "Src_" to know which type of node runs the script '''
    family_name = _thisNode.name().split(_lnklbl)[-1] + "0" # little hack to avoid zero number for the regex
    num = re.search('\d+', family_name).group(0)
    family_name = family_name.split(num)[0]
    family = []
    link_class = []
    nukescripts.clear_selection_recursive()
    for ps in nuke.allNodes("PostageStamp"):
        link_class.append(ps)
    for ps in nuke.allNodes("NoOp"):
        link_class.append(ps)
    for ps in link_class:
        psname = ps.name().split("Linked_")[-1] + "0"
        num = re.search('\d+', psname).group(0)
        psname = psname.split(num)[0]
        if psname == family_name:
            family.append(ps)
    for link in family:
        link.setSelected(True)
    if _lnklbl=="Linked_":
        _thisNode.input(0).setSelected(True)
    else:
        _thisNode.setSelected(True)
        
def reconnectSelected():
    for psl in nuke.selectedNodes():
        try:
            psl.input(0).name()            # it has a connection so no need to reconnect
            nuke.message("Link does already have a connection!!!")
        except Exception:
            if psl.Class()=="PostageStamp":
                if "Linked_" in psl.name() and psl.Class()=="PostageStamp":
                    for ps in nuke.allNodes("PostageStamp"):
                        if ps.name().split("Src_")[-1] in psl.name().split("Linked_")[-1]:
                            psl.setInput(0,ps)
                            break
            elif psl.Class()=="NoOp":
                if "Linked_" in psl.name() and psl.Class()=="NoOp":
                    for ps in nuke.allNodes("NoOp"):
                        if ps.name().split("Src_")[-1] in psl.name().split("Linked_")[-1]:
                            psl.setInput(0,ps)
                            break
            
def addLabelOptions(_label):
    _label['note_font_color'].setValue(0)
    _label['tile_color'].setValue(0x7fff00ff)
    _label['postage_stamp'].setValue(False)
    _label['note_font_size'].setValue(10)

    pybut = nuke.PyScript_Knob("create_link", "Create New Link")
    library = os.path.basename(inspect.getfile(inspect.currentframe())).split(".")[0]
    pybut.setCommand( '''nukescripts.clear_selection_recursive()
link = '''+library+ '''.createLinkContainer()
link.setInput(0,nuke.thisNode())
link.setXYpos(nuke.thisNode().xpos()+100,nuke.thisNode().ypos()+80)
link.setName(nuke.thisNode().name().replace("Src","Linked"))
'''+library+".addLinkOptions(link)\n"+library + ".linkDressing(link)\n")
    _label.addKnob(pybut)

    pybut = nuke.PyScript_Knob("RenameAllSame", "Rename Serie")
    pybut.setCommand(library + ".renameByFamily(nuke.thisNode(), 'Src_')")
    _label.addKnob(pybut)
    
    pybut = nuke.PyScript_Knob("selectByFamily", "Select by family")
    pybut.setCommand(library + ".selectByFamily(nuke.thisNode(), 'Src_')")

    knobdivide = nuke.Text_Knob("divName"," "," ")
    _label.addKnob(knobdivide)

    knobHide = nuke.Link_Knob("hide_input_1","Hide Input" )
    knobHide.setLink("hide_input")
    _label.addKnob(knobHide)

    knobPostage = nuke.Link_Knob("postage_stamp_1","Postage Stamp" )
    knobPostage.setLink("postage_stamp")
    _label.addKnob(knobPostage)

	
    _label['User'].setName("Source")
    return _label

    
def addLinkOptions(_link):
    _link['note_font_size'].setValue(10)
    _link['hide_input'].setValue(True)

    pybut = nuke.PyScript_Knob("duplicate", "Duplicate")
    library = os.path.basename(inspect.getfile(inspect.currentframe())).split(".")[0]
    pybut.setCommand( library + ".copyKeepInputs([nuke.thisNode()])" )


    pybut = nuke.PyScript_Knob("RenameAllSame", "Rename Serie")
    pybut.setCommand(library + ".renameByFamily(nuke.thisNode(), 'Linked_')")
    _link.addKnob(pybut)

    pybut = nuke.PyScript_Knob("selectByFamily", "Select by family")
    pybut.setCommand(library + ".selectByFamily(nuke.thisNode(), 'Linked_')")

    
    pybut = nuke.PyScript_Knob("ReconnectSelected", "Reconnect Selected")
    pybut.setCommand( library + ".reconnectSelected()")
    _link.addKnob(pybut)
    
    pybut = nuke.PyScript_Knob("toggle_disable_All_Postages", "Postages\n Stamp")
    pybut.setCommand('''value = nuke.thisNode()['postage_stamp'].value()
for ps in nuke.allNode()("PostageStamp"):
    ps['postage_stamp'].setValue(not value)''')

    
    pybut = nuke.PyScript_Knob("toggle_hide_All_inputs", "Hide\n Inputs")
    pybut.setCommand('''value = nuke.thisNode()['hide_input'].value()
for ps in nuke.allNodes("PostageStamp"):
    ps['hide_input'].setValue(not value)''')

    
    pybut = nuke.PyScript_Knob("go_to_src", "Go to Source Node")
    pybut.setCommand('''prev = nuke.thisNode().input(0)
nuke.zoom( 1, [ prev.xpos(), prev.ypos() ])''')
    _link.addKnob(pybut)

    knobdivide = nuke.Text_Knob("divName"," "," ")
    _link.addKnob(knobdivide)

    knobHide = nuke.Link_Knob("hide_input_1","Hide Input" )
    knobHide.setLink("hide_input")
    _link.addKnob(knobHide)

    knobPostage = nuke.Link_Knob("postage_stamp_1","Postage Stamp" )
    knobPostage.setLink("postage_stamp")
    _link.addKnob(knobPostage)

    
    #_link.setXYpos( src.xpos(), src.ypos()+100 )
    #_link.autoplace()
    _link['User'].setName("Link")
    return _link


def linkTools():
    class NAMER( nukescripts.PythonPanel):
        def __init__( self, _node ):
            self.node = _node
            nukescripts.PythonPanel.__init__( self, 'Namer', 'Namer')
            self.pulldown = nuke.Enumeration_Knob("GetFrom","GetFrom",["inHouseLayerPass", "name", "filename", "label"])
            parent = self.node
            try:     # to avoid error when selected node is connected to nothing
                while parent.Class()!="Read" or parent.input(0):
                    parent = parent.input(0)
                self.filename = parent['file'].value().split("/")[-1].split(".")[0].replace("-","_")
            except Exception:
                self.filename = ""
            if self.node.Class()=="Read":
                self.label = nuke.String_Knob("name","Re-name", self.node.name())
                self.pulldown.setValue( "name" )
            else:
                self.label = nuke.String_Knob("name","Re-name",self.node.name())
                self.pulldown.setValue( "name" )
            self.addKnob(self.label)
            

        def knobChanged(self,knob):
            if nuke.thisKnob().name() == "GetFrom":
                if nuke.thisKnob().value()=="name":
                    self.label.setValue( self.node.name() )
                elif nuke.thisKnob().value()=="filename":
                    if self.filename:
                        self.label.setValue( self.filename )
                    else:
                        self.label.setValue( "" )
                elif nuke.thisKnob().value()=="label":
                    self.label.setValue( self.node['label'].value() )
                elif nuke.thisKnob().value()=="inHouseLayerPass":
                    if self.filename:
                        self.label.setValue( "_".join(self.filename.split("_")[5:]) )
                    else:
                        self.label.setValue( "" )
    class LABELCHOOSER( nukescripts.PythonPanel):
        def __init__( self ):
            nukescripts.PythonPanel.__init__( self, 'labelchooser', 'labelchooser')
            labels_list = []
            for ps in nuke.allNodes("PostageStamp"):
                if "Src_" in ps.name():
                    realname = ps.name().split("Src_")[-1]
                    if "_" in realname:
                        prefixe = realname.split("_")[0]
                    else:
                        prefixe = realname
                    labels_list.append(prefixe+"/"+realname)
            self.pulldown = nuke.CascadingEnumeration_Knob("labelchooser","Choose a Label", labels_list)
            self.addKnob(self.pulldown)
    try:
        src = nuke.selectedNode()
        # nukescripts.clear_selection_recursive()
        namer = NAMER(src)
        result = namer.showModalDialog()
        if result:
            label = createLinkContainer()
            # label.hideControlPanel()
            label.setXYpos(src.xpos()+110,src.ypos()+60)
            label.setInput(0, src)
            name = namer.label.value()
            link = createLinkContainer()
            link.setInput(0, label)
            addLabelOptions(label)
            link.setXYpos(label.xpos()+0,label.ypos()+80)
            label.setName( "Src_" + name)
            link.setName( "Linked_" + name)
            label.hideControlPanel()
            label.setSelected(True)
            addLinkOptions(link)
			
			


			
    except Exception:                 # if nothing is selected create a link from all labels available
        label_chooser = LABELCHOOSER()
        result = label_chooser.showModalDialog()
        if result:
            nukescripts.clear_selection_recursive()
            nuke.toNode( "Src_" + label_chooser.pulldown.value().split("/")[-1] ).setSelected(True)
            link = createLinkContainer()
            link.setName( "Linked_" + label_chooser.pulldown.value().split("/")[-1] + "_")
            for ps in nuke.allNodes("PostageStamp"):
                if ps.name().split("Src_")[-1] in link.name().split("Linked_")[-1]:
                    link.setInput(0,ps)
                    break
            addLinkOptions(link)
			
