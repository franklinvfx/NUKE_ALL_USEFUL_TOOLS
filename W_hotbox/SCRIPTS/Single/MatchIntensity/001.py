#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Reset ROI
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('resetROI').execute()