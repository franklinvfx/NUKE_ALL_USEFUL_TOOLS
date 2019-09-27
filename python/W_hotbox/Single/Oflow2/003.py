#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Convert
#
#----------------------------------------------------------------------------------------------------------

def emptySelection(selection):
    for i in selection:
        i.knob('selected').setValue(False)

selection = nuke.selectedNodes()
name = nuke.selectedNode().name()

emptySelection(selection)

for i in selection:
    postion = [i.xpos()-i.screenWidth()/2,i.ypos()]
    
    kro = nuke.createNode("Kronos")
    kro.knob('timing2').setExpression(name +'.timing2')
    kro.knob('input.first').setExpression(name +'.input.first')
    kro.knob('input.last').setExpression(name +'.input.last')
    kro.knob('timingOutputSpeed').setExpression(name +'.timingOutputSpeed')
    kro.knob('timingInputSpeed').setExpression(name +'.timingInputSpeed')
    kro.knob('interpolation').setExpression(name +'.interpolation')
    kro.knob('timingFrame2').setExpression(name +'.timingFrame2')
    # kro.knob('label').setValue('(' + name + ')')
    kro.setXpos(postion[0]+200-kro.screenWidth()/2)
    kro.setYpos(postion[1])
    kro.knob('selected').setValue(False)
    
    try:
        Twix = nuke.createNode("OFXcom.revisionfx.twixtorpro_v5")
        Twix.knob('Speed').setExpression(name +'.timingOutputSpeed*100')
        Twix.knob('TimeRetimeMethod').setExpression(name +'.timing2')
        Twix.knob('FrameInterp').setExpression(name +'.interpolation')
        Twix.knob('Frame').setExpression(name +'.timingFrame2')
        Twix.knob('label').setValue('(' + name + ')')
        Twix.setXpos(postion[0]+440-Twix.screenWidth()/2)
        Twix.setYpos(postion[1])
        Twix.knob('selected').setValue(False)
    except:
        pass

    if i.knob('timing2').value() == 'Frame':
        Twarp = nuke.createNode("TimeWarp")
        Twarp.knob('lookup').setExpression(name +'.timingFrame2')
        Twarp.knob('label').setValue('(' + name + ')')
        Twarp.setXpos(postion[0]+320-Twarp.screenWidth()/2)
        Twarp.setYpos(postion[1])
        Twarp.knob('selected').setValue(False)
    
    emptySelection(selection)