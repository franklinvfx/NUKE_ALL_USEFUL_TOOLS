#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: A
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    for channel in ['red','green','blue','alpha']:
        i.knob(channel).setValue('alpha')

    i.knob('tile_color').setValue(4278124287)