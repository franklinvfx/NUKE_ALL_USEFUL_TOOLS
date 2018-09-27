#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Create Write
#
#----------------------------------------------------------------------------------------------------------

import nukescripts

def writeFromRead():
    description = ""
    for read in nuke.selectedNodes():
        #nukescripts.clear_selection_recursive()
        read = nuke.selectedNode()
        #read.setSelected(True)
        filepath = read['file'].value()
        colorspace = read['colorspace'].value()
        dirpath = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        #if read.Class()=="Read":
            
        padding = filename.split(".")[-2]
        write = nuke.createNode("Write")
        write.setName("Write_from_" + read.name())
        write['file'].setValue( dirpath + description + "/" + filename.replace("."+padding, description+"."+padding))
        write['colorspace'].setValue(colorspace)
        write['create_directories'].setValue('true')
        
        #postion = [read.xpos()-read.screenWidth()/2,read.ypos()+read.screenHeight()/2]
        #write.setXpos(postion[0]+200)
        #write.setYpos(postion[1]-25)
        
        nodePos = ( nuke.selectedNode().xpos(), nuke.selectedNode().ypos()) 
        
        nuke.nodeCopy('%clipboard%')
        n = nuke.selectedNode()
        nuke.delete(n)
        
        nuke.selectAll() 
        nuke.invertSelection()
                
        for node in nuke.allNodes():
            node.setSelected(False)
        
        nuke.nodePaste('%clipboard%')
                
        nodesToPlace = sorted( nuke.selectedNodes(), key=lambda node: node.ypos())
        
        for index,node in enumerate(nodesToPlace):
            node.setXYpos(nodePos[0]+100, nodePos[1])
        
writeFromRead()

