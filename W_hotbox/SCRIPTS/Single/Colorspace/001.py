#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Swap In/Out
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('swap').execute()