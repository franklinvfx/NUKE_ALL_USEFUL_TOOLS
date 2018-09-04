#BreakOut EXR Layers

import nuke


def createLinkedNode(parentNode, stamp = False):
    #add dot
    if stamp:
        dotNode = nuke.nodes.PostageStamp()
    else:
        dotNode = nuke.nodes.PostageStamp()
        
    label = "Link: <font size = 3 color=\"green\"> [python {nuke.thisNode().input(0).name().replace('.render_main','').replace('_'+nuke.thisNode().input(0).name().split('_')[-1],'') if nuke.thisNode().inputs() else \" - \"}]"
    label += "\n       <font size = 3 color=\"green\"> [python {nuke.thisNode().input(0).name().split('_')[-1] if nuke.thisNode().inputs() and len(nuke.thisNode().input(0).name().split('_')) >1   else \" - \"}]"
    #label += "<font size = 3 color=\"#B40404\"> [python {'\\nHidden Input!!!' if nuke.thisNode()['hide_input'].value() else '\\n'}]"
    dotNode['label'].setValue(label)
    
    #colors         
    dotNode['tile_color'].setValue(0xff00ff)
    dotNode['gl_color'].setValue(0xff00ff)
    dotNode['note_font_color'].setValue(0x595959ff)
    
    if parentNode != None:
        knobInputNodeDefault = parentNode.name()
    else:
        knobInputNodeDefault = ''
    knobInputNode = nuke.String_Knob('input_node_1', 'INPUT', knobInputNodeDefault)        
    dotNode.addKnob(knobInputNode)
    
    knobPython = nuke.PyScript_Knob('python','Input / Reload')
    #knobPython.setCommand("nuke.thisNode().setInput(0,nuke.toNode( nuke.thisNode()['input_node_1'].value()))")
    knobPython.setCommand("def getNode(nodeName):\n nodeToConnect = None\n for node in nuke.allNodes(): \n  if node.name() == nodeName: \n   return node \n\nnuke.thisNode().setInput(0,getNode(nuke.thisNode()['input_node_1'].value()  ))")
    dotNode.addKnob(knobPython)
    
    
    knobHideInput = nuke.Link_Knob("hide_input_1","hide input" )
    knobHideInput.setLink("hide_input")
    dotNode.addKnob(knobHideInput)
    
    if parentNode != None:
        dotNode.setInput( 0, parentNode)
        dotNode.setXYpos(parentNode.xpos()+34, parentNode.ypos()+75 )
    
    return dotNode

def organiceNodes(nodeList):
    
    if len(nodeList) < 3:
        print "please select 3 or more nodes"
        return
    
    parent = nodeList[0]
    childNodes = nodeList[1:]
    
    #calculate the distances
    minydist = 999999999
    for childNode in childNodes:
        ydistance = (childNode.ypos() - parent.ypos())
        if ydistance < minydist:
            minydist = ydistance
    minydist = minydist/3
    
    #add dots on top other nodes at minydist
    dotNodes = []
    for childNode in childNodes:
        dotNode = nuke.nodes.Dot()
        dotNode.setXYpos(childNode.xpos()+34, childNode.ypos()- minydist)
        childNode.setInput(0,dotNode)
        dotNodes.append(dotNode)
    
    dotNodes = sorted(dotNodes, key = lambda node:node.xpos(), reverse =True)
    
    
    for index,dotNode in enumerate(dotNodes):
        if index < len(dotNodes) -1:
            dotNode.setInput(0,dotNodes[index+1])
        else:
            dotNode.setInput(0,parent)
    

def breakoutLayersNode(nodeObj):
    layerNames = []
    for channel in nodeObj.channels():
        layerName = channel.split('.')[0]
        if layerName not in layerNames:
            layerNames.append(layerName)
    nodeList = []
    listToOrganice = []
    
    for layerName in layerNames:
        suffleNodeName = nodeObj.name()+'_'+str(layerName) #+ "_Shuffel"
        shuffleNode = nuke.nodes.Shuffle(name = suffleNodeName , postage_stamp = True)
        shuffleNode.setInput( 0, nodeObj)
        shuffleNode['in'].setValue(layerName)
        #shuffleNode.setXYpos(shuffleNode.xpos()+20, shuffleNode.ypos()+100 )
        linkedNode = createLinkedNode(shuffleNode)
        
        nodeList.append((shuffleNode,linkedNode))
        listToOrganice.append(shuffleNode)
    
    for index, nodeTuple in enumerate(nodeList):        
        for subIndex, node in enumerate(nodeTuple):
            node.setXYpos(node.xpos()+50*index, node.ypos()+(subIndex+1)*50 )
            
    
    
    organiceNodes( [nodeObj] + listToOrganice  )

def breakoutLayers():
    selectedNodes = nuke.selectedNodes()
        
    if len(selectedNodes) > 0 :
        for nodeObj in selectedNodes:
            breakoutLayersNode(nodeObj)    
    else:
        print "Please select one or more nodes to breakout"
        
        
breakoutLayers()