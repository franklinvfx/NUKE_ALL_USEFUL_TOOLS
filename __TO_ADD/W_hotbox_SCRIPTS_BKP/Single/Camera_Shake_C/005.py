#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Random seed
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('randomize_seedall').execute()