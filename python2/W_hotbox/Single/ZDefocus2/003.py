#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Toggle Anamorphic
#
#----------------------------------------------------------------------------------------------------------

for i in nuke.selectedNodes():
    i.knob('aspect').setValue(1.5-i.knob('aspect').value())