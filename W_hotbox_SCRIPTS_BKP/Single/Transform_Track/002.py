#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show filter
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('label'). value() == '[value Mode]':
        i.knob('label'). setValue('[value Mode]/[value knob.filter]')
    else:
        i.knob('label').setValue('[value Mode]')