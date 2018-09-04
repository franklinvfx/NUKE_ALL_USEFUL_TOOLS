#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: BBox Union/B
#
#----------------------------------------------------------------------------------------------------------

'''for i in nuke.selectedNodes():
    if i.knob('bbox'). value() == 'union':
        i.knob('bbox'). setValue('B')
    else:
        i.knob('bbox').setValue('union')'''

for i in nuke.selectedNodes():
    if i.knob('bbox'). value() != 'union':
        i.knob('bbox'). setValue('union')
    else:
        i.knob('bbox').setValue('B')