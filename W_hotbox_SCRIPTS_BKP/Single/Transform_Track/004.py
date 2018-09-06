#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show RefFrame
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('label'). value() == '[value Mode]':
        i.knob('label'). setValue('[value Mode]/[value RefFrame]')
    else:
        i.knob('label').setValue('[value Mode]')