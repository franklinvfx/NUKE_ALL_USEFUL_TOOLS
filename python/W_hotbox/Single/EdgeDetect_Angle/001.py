#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: 4 angle mode
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('Angler').value() == 0:
        i.knob('Angler').setValue(90)
    elif i.knob('Angler').value() == 90:
        i.knob('Angler').setValue(180)
    elif i.knob('Angler').value() == 180:
        i.knob('Angler').setValue(270)
    elif i.knob('Angler').value() == 270:
        i.knob('Angler').setValue(360)
    else:
        i.knob('Angler').setValue(0)
