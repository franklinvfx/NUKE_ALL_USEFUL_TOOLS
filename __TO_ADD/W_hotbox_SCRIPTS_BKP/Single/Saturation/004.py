#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show value
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('label'). value() == '':
        i.knob('label'). setValue('sat : [value saturation]/ mix :[value mix]')
    else:
        i.knob('label').setValue('')
