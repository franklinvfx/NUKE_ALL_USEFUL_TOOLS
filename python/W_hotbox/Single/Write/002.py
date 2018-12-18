#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Batch <font color = "grey">(F8)
#
#----------------------------------------------------------------------------------------------------------

#man = session.getManager()
#write.update(man, False, nuke.selectedNode()['batch2'], nuke.selectedNode())

for node in nuke.selectedNodes():
    node.knob('Render').execute()