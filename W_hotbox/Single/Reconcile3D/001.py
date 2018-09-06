#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Dotlink Setup
#
#----------------------------------------------------------------------------------------------------------


def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection(selection)

for i in selection:

    CamNode = nuke.nodePaste("//stora/diska/global/templatesProd/11_Other/06_Dot_Link.nk")
    
    postion = [i.xpos()-i.screenWidth()/2,i.ypos()+i.screenHeight()/2]
    CamNode.knob('input_node_2').setValue('Camera')
    CamNode.knob('hide_input').setValue(1)
    CamNode.setXpos(postion[0]+200-CamNode.screenWidth()/2)
    CamNode.setYpos(postion[1]-8+CamNode.screenHeight()/2)
    
    ImgNode = nuke.nodePaste("//stora/diska/global/templatesProd/11_Other/06_Dot_Link.nk")
    ImgNode.knob('input_node_2').setValue('Master_Undisto')
    ImgNode.knob('hide_input').setValue(1)
    ImgNode.setXpos(postion[0]+72+ImgNode.screenWidth()/2)
    ImgNode.setYpos(postion[1]-100+ImgNode.screenHeight()/2)
    
    BGNode = nuke.createNode("Axis2")
    BGNode.setXpos(postion[0]-50-BGNode.screenWidth()/2)
    BGNode.setYpos(postion[1]-10+BGNode.screenHeight()/2)
    

    i.setInput(1,CamNode)
    i.setInput(0,ImgNode)
    i.setInput(2,BGNode)
    emptySelection(selection)