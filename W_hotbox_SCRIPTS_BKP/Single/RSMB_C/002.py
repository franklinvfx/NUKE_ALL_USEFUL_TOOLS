#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: GUI On/Off
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('Render').value() == 0:
        i.knob('Render').setValue(1)
    else:
        i.knob('Render').setValue(0)