#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Create linked Grade
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
    node.knob('CrtLnkGrd').execute()