#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Preserve Bbox On/Off
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('pbb').value() == (0):
        i.knob('pbb').setValue(1)
    else:
        i.knob('pbb').setValue(0)
