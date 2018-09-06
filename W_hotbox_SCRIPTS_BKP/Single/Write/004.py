#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Batch <font color = "grey">(F8)
#
#----------------------------------------------------------------------------------------------------------

from cgev.pipeline.data import session
from cgev.nuke.tools.nodes import write

man = session.getManager()
write.update(man, False, nuke.selectedNode()['batch2'], nuke.selectedNode())