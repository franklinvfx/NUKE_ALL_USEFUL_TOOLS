#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: <img src="\\stora\diska\global\templatesProd\Other_images\decrease_bt.png">
#
#----------------------------------------------------------------------------------------------------------

def changeNodeFontSize(_multiplier):
    bd = []
    nodes = nuke.selectedNodes()
    for node in nodes:
        if node.Class()=="BackdropNode":
            bd.append(node)
    if bd!=[]:
        nodes = bd
    for node in nodes:
        node['note_font_size'].setValue(node['note_font_size'].value()+1*_multiplier)

changeNodeFontSize(-4)