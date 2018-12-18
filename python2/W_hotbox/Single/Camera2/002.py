#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: CameraSmoother
#
#----------------------------------------------------------------------------------------------------------


def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection(selection)

for i in selection:

    BGNode = nuke.nodePaste("//stora/diska/global/templatesProd/09_3D/06_Camera/03_Camera_Smoother.nk")
    
    postion = [i.xpos()-i.screenWidth()/2,i.ypos()+i.screenHeight()/2]
    BGNode.setXpos(postion[0]+60-BGNode.screenWidth()/2)
    BGNode.setYpos(postion[1]+50+BGNode.screenHeight()/2)

    BGNode.setInput(0,i)

    emptySelection(selection)