#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: DotLink Camera
#
#----------------------------------------------------------------------------------------------------------


def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection(selection)

for i in selection:

    BGNode = nuke.createNode("DotLink")
    
    postion = [i.xpos()-i.screenWidth()/2,i.ypos()+i.screenHeight()/2]
    BGNode.knob('input_node_2').setValue('Camera')
    BGNode.knob('hide_input').setValue(1)
    BGNode.setXpos(postion[0]-50-BGNode.screenWidth()/2)
    BGNode.setYpos(postion[1]-10+BGNode.screenHeight()/2)

    i.setInput(2,BGNode)

    emptySelection(selection)