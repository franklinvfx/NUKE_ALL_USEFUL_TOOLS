#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Create Cam
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('create_camera').execute()