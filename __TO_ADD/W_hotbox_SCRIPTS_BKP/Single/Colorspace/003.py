#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show Conversion
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('label'). value() == '':
        i.knob('label'). setValue('[value colorspace_in] to [value colorspace_out]')
    else:
        i.knob('label').setValue('')