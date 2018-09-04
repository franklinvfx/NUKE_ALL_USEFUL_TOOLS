#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Linear WorkFlow
#
#----------------------------------------------------------------------------------------------------------


def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection(selection)

for i in selection:

    BGNode = nuke.createNode("Colorspace")
    BGNode2 = nuke.createNode("Colorspace")
    postion = [i.xpos()-i.screenWidth()/2,i.ypos()+i.screenHeight()/2]

    BGNode.setXpos(postion[0]+100+BGNode.screenWidth()/2)
    BGNode.setYpos(postion[1]-100+BGNode.screenHeight()/2)

    BGNode2.setXpos(postion[0]-100+BGNode2.screenWidth()/2)
    BGNode2.setYpos(postion[1]-100+BGNode2.screenHeight()/2)
    i.setInput(0,BGNode)
    i.setInput(1,BGNode2)
    emptySelection(selection)