#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: <font color="green">G
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    for channel in ['red','green','blue','alpha']:
        i.knob(channel).setValue('green')

    i.knob('tile_color').setValue(729426943)