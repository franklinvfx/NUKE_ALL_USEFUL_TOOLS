#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Missing frames error/black
#
#----------------------------------------------------------------------------------------------------------

from cgev.ui import messages

for node in nuke.allNodes('Read'):
    if node.knob('on_error').value() != 'black':
       node.knob('on_error').setValue('black')
    else:
        node.knob('on_error').setValue('error')
    messages.splash('Missing frames set to : {}'.format(node.knob('on_error').value()))