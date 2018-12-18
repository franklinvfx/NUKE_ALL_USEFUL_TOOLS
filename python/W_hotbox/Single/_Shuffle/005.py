#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: <font color="#b30000">R
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    for channel in ['red','green','blue','alpha']:
        i.knob(channel).setValue('red')

    i.knob('tile_color').setValue(2738107647)