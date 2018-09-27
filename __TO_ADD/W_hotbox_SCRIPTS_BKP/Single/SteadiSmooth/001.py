#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Show filter
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('label'). value() == 'Smooth: [value Stab]%':
        i.knob('label'). setValue('Smooth: [value Stab]% / [value knob.filter]')
    else:
        i.knob('label').setValue('Smooth: [value Stab]%')