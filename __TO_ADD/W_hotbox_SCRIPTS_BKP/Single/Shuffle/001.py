#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Create OCIO 3D Mask
#
#----------------------------------------------------------------------------------------------------------

if nuke.root().knob('colorManagement').value() == 'OCIO':

    OCIOColorspace = nuke.createNode('OCIOColorSpace')
    OCIOColorspace.setName('OCIO 3D Mask')

    workingspace = nuke.root().knob('workingSpaceLUT').value()
    OCIOColorspace.knob('in_colorspace').setValue(workingspace)
    OCIOColorspace.knob('out_colorspace').setValue('Aliases/lin_rec709')
else:
    nuke.message('This action only works with colorspace set to OCIO !')