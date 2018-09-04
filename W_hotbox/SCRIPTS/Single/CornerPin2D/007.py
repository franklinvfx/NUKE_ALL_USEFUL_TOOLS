#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set to Bbox
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    x = node.input(0).bbox().x()
    y = node.input(0).bbox().y()
    w = node.input(0).bbox().w()
    h = node.input(0).bbox().h()

    node.knob('from1').setValue((x, y))
    node.knob('from2').setValue((x+w, y))
    node.knob('from3').setValue((x+w, y+h))
    node.knob('from4').setValue((x, y+h))