#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Bokeh List
#
#----------------------------------------------------------------------------------------------------------


def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()

emptySelection(selection)

for i in selection:

    BGNode = nuke.createNode("Bokeh_List")
    
    postion = [i.xpos()-i.screenWidth()/2,i.ypos()+i.screenHeight()/2]
    BGNode.setXpos(postion[0]-20-BGNode.screenWidth()/2)
    BGNode.setYpos(postion[1]-23+BGNode.screenHeight()/2)

    i.setInput(1,BGNode)
    i.knob('filter_type').setValue('image')
    i.knob('filter_channel').setValue('rgba.red')

    emptySelection(selection)