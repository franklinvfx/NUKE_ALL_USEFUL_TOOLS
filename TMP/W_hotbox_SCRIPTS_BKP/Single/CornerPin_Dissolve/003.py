#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Create CP linked
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('create_cornerpin').execute()