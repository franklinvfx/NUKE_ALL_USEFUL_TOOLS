#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Cubic/Simon
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    if i.knob('filter'). value() == 'Cubic':
        i.knob('filter'). setValue('Simon')
    else:
        i.knob('filter').setValue('Cubic')