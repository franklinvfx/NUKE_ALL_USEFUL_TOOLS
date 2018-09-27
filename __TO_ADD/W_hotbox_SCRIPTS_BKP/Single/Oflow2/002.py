#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Reset input range
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('resetInputRange').execute()