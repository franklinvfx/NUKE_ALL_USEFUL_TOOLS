#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Alpha/Rgb...
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('Channel').value() == 'Alpha':
        i.knob('Channel').setValue('rgba')
    elif i.knob('Channel').value() == 'rgba':
        i.knob('Channel').setValue('All')
    else:
        i.knob('Channel').setValue('Alpha')
