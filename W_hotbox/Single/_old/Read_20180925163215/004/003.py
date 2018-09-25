#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Frame range hold/black
#
#----------------------------------------------------------------------------------------------------------

from cgev.ui import messages

for node in nuke.allNodes('Read'):
    if node.knob('before').value() != 'hold':
        node.knob('before').setValue('hold')
        node.knob('after').setValue('hold')
    else:
        node.knob('before').setValue('black')
        node.knob('after').setValue('black')
    messages.splash('Frame range set to : {}'.format(node.knob('before').value()))