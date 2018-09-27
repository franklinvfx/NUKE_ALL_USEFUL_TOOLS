#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show mix
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('label'). value() == '':
        i.knob('label'). setValue('mix :[value mix]')
    else:
        i.knob('label').setValue('')