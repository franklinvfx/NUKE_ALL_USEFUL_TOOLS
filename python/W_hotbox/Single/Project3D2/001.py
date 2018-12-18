#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: DotLink Camera FrameHold
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
    BGNode.setXpos(postion[0]-200-BGNode.screenWidth()/2)
    BGNode.setYpos(postion[1]-7+BGNode.screenHeight()/2)
    
    FrH = nuke.createNode("FrameHold")
    
    FrH.knob('first_frame').setValue( nuke.frame() )    
    FrH.setXpos(postion[0]-50-FrH.screenWidth()/2)
    FrH.setYpos(postion[1]-23+FrH.screenHeight()/2)
    i.setInput(1,FrH)
    FrH.setInput(0,BGnode)


    emptySelection(selection)