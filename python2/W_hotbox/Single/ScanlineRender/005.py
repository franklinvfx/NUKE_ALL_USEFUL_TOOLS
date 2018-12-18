#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Output P/N channels
#
#----------------------------------------------------------------------------------------------------------

nuke.tcl("add_layer", "position position.red position.green position.blue")
nuke.tcl("add_layer", "normals normals.red normals.green normals.blue")

for i in nuke.selectedNodes():
    i.knob('output_shader_vectors').setValue(1)
    i.knob('P_channel').setValue('position')
    i.knob('N_channel').setValue('normals')