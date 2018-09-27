#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show samples
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('label'). value() == '':
        i.knob('label'). setValue('Samples : [value samples]')
    else:
        i.knob('label').setValue('')
