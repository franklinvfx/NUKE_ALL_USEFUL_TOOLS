#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: <font color="blue">B
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    for channel in ['red','green','blue','alpha']:
        i.knob(channel).setValue('blue')

    i.knob('tile_color').setValue(1061139199)