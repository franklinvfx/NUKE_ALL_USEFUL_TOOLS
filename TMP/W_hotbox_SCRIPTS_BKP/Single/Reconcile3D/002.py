#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Add Axis
#
#----------------------------------------------------------------------------------------------------------


def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection(selection)

for i in selection:

    BGNode = nuke.createNode("Axis2")
    
    postion = [i.xpos()-i.screenWidth()/2,i.ypos()+i.screenHeight()/2]
    BGNode.setXpos(postion[0]-50-BGNode.screenWidth()/2)
    BGNode.setYpos(postion[1]-61+BGNode.screenHeight()/2)

    i.setInput(2,BGNode)

    emptySelection(selection)