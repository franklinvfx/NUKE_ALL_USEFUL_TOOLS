#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Green/Blue/Red
#
#----------------------------------------------------------------------------------------------------------

#from cgev.ui import messages

for i in nuke.selectedNodes():
    if i.knob('screenType').value() == 'green':
        i.knob('screenType').setValue('blue')
        i.knob('tile_color').setValue(4177919)
    elif i.knob('screenType').value() == 'blue':
        i.knob('screenType').setValue('red')
        i.knob('tile_color').setValue(3204448511)
    else:
        i.knob('screenType').setValue('green')
        i.knob('tile_color').setValue(12517631)
    #messages.splash('Screen type set to : {}'.format(i.knob('screenType').value()))