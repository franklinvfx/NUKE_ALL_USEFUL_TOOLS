#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Fill Alpha
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('in').setValue('rgba')
    i.knob('alpha').setValue('white')

    i.knob('tile_color').setValue(4278124287)