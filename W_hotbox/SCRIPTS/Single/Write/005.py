#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Batch <font color = "grey">Version Up
#
#----------------------------------------------------------------------------------------------------------

from cgev.ui import messages
from cgev.pipeline.data import session
from cgev.nuke.tools.nodes import write

prev = nuke.selectedNode().knob('revision').value() + 1
nuke.selectedNode().knob('revision').setValue(prev)

messages.splash('Increment version to \'\' {}'.format(int(nuke.selectedNode().knob('revision').value())) + ' \'\'')

man = session.getManager()
write.update(man, False, nuke.selectedNode()['batch2'], nuke.selectedNode())