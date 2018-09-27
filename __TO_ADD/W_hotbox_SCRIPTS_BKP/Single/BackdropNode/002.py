#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Center
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    n="<center>"
    i.knob('label').setValue(n+i.knob('label').value())