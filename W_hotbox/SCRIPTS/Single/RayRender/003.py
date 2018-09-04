#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: AOV preset
#
#----------------------------------------------------------------------------------------------------------

nuke.tcl("add_layer", "position position.red position.green position.blue")
nuke.tcl("add_layer", "normals normals.red normals.green normals.blue")
nuke.tcl("add_layer", "motion motion.u motion.v ")
nuke.tcl("add_layer", "diffuse diffuse.red diffuse.green diffuse.blue")
nuke.tcl("add_layer", "specular specular.red specular.green specular.blue")
nuke.tcl("add_layer", "reflection reflection.red reflection.green reflection.blue")
nuke.tcl("add_layer", "emissive emissive.red emissive.green emissive.blue")


for i in nuke.selectedNodes():
    i.knob('output_shader_vectors').setValue(1)
    i.knob('AOV_Point').setValue('position')
    i.knob('AOV_Normal').setValue('normals')
    i.knob('AOV_Motion').setValue('motion')
    i.knob('AOV_Direct_Diffuse').setValue('diffuse')
    i.knob('AOV_Direct_Specular').setValue('specular')
    i.knob('AOV_Reflection').setValue('reflection')
    i.knob('AOV_Emissive').setValue('emissive')