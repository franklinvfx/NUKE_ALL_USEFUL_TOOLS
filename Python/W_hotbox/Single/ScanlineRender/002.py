#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: DotLink Setup
#
#----------------------------------------------------------------------------------------------------------


def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection(selection)

for i in selection:

    CamNode = nuke.createNode("DotLink")
    
    postion = [i.xpos()-i.screenWidth()/2,i.ypos()+i.screenHeight()/2]
    CamNode.knob('input_node_2').setValue('Camera')
    CamNode.knob('hide_input').setValue(1)
    CamNode.setXpos(postion[0]-50-CamNode.screenWidth()/2)
    CamNode.setYpos(postion[1]-10+CamNode.screenHeight()/2)
    
    BGNode = nuke.createNode("DotLink")
    BGNode.knob('input_node_2').setValue('Reformat_Undisto')
    BGNode.knob('hide_input').setValue(1)
    BGNode.setXpos(postion[0]+200-BGNode.screenWidth()/2)
    BGNode.setYpos(postion[1]-8+BGNode.screenHeight()/2)

    i.setInput(2,CamNode)
    i.setInput(0,BGNode)
    emptySelection(selection)