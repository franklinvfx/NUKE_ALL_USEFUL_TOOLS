#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show Input
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('label'). value() == '':
        i.knob('label'). setValue('input :[value which]')
    else:
        i.knob('label').setValue('')