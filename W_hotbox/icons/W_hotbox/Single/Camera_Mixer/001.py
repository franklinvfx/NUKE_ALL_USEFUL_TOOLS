#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Create linked Cam
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('CreateCam').execute()