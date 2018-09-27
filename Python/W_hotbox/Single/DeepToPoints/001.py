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
    CamNode.knob('MM_easySearch').setValue('Camera')
    CamNode.knob('hide_input').setValue(1)
    CamNode.setXpos(postion[0]-10-CamNode.screenWidth()/2)
    CamNode.setYpos(postion[1]-65+CamNode.screenHeight()/2)
    
    DeepNode = nuke.createNode("DotLink")
    DeepNode.knob('MM_easySearch').setValue('Deep')
    DeepNode.knob('hide_input').setValue(1)
    DeepNode.setXpos(postion[0]+150-DeepNode.screenWidth()/2)
    DeepNode.setYpos(postion[1]-65+DeepNode.screenHeight()/2)

    i.setInput(1,CamNode)
    i.setInput(0,DeepNode)
    emptySelection(selection)