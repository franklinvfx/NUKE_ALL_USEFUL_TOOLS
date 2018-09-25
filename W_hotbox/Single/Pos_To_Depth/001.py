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
    
    DeepNode = nuke.createNode("DotLink")
    DeepNode.knob('input_node_2').setValue('CG')
    DeepNode.knob('hide_input').setValue(1)
    DeepNode.setXpos(postion[0]+80-DeepNode.screenWidth()/2)
    DeepNode.setYpos(postion[1]-75+DeepNode.screenHeight()/2)

    i.setInput(1,CamNode)
    i.setInput(0,DeepNode)
    emptySelection(selection)