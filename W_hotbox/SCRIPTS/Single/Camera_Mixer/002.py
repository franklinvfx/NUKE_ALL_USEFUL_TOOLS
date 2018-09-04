#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Create baked Cam
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('CreateBakedCam').execute()