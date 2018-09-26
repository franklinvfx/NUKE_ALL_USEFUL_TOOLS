#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Set input format
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('set_to_input').execute()