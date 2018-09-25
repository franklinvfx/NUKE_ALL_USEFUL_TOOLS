#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: DotLink CG
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
    BGNode.knob('MM_easySearch').setValue('CG')
    BGNode.knob('hide_input').setValue(1)
    BGNode.setXpos(postion[0]+80-BGNode.screenWidth()/2)
    BGNode.setYpos(postion[1]-70+BGNode.screenHeight()/2)

    i.setInput(0,BGNode)

    emptySelection(selection)