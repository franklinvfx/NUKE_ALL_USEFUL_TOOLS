#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Rgba/Alpha
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('output').value() == 'rgba':
        i.knob('output').setValue('alpha')
    else:
        i.knob('output').setValue('rgba')