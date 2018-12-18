#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Crop/UnCrop
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('crop_to_format'). value() == 0:
        i.knob('crop_to_format'). setValue(1)
    else:
        i.knob('crop_to_format').setValue(0)