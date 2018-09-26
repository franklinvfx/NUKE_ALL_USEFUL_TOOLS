#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
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
    
    Oflow = nuke.createNode("OFlow2")
    Oflow.knob('timing2').setExpression(name +'.timing2')
    Oflow.knob('timingOutputSpeed').setExpression(name +'.timingOutputSpeed')
    Oflow.knob('timingInputSpeed').setExpression(name +'.timingInputSpeed')
    Oflow.knob('interpolation').setExpression(name +'.interpolation')
    Oflow.knob('timingFrame2').setExpression(name +'.timingFrame2')
    Oflow.knob('label').setValue('(' + name + ')')
    Oflow.setXpos(postion[0]+200-Oflow.screenWidth()/2)
    Oflow.setYpos(postion[1])
    Oflow.knob('selected').setValue(False)

    Twix = nuke.createNode("OFXcom.revisionfx.twixtorpro_v5")
    Twix.knob('Speed').setExpression(name +'.timingOutputSpeed*100')
    Twix.knob('TimeRetimeMethod').setExpression(name +'.timing2')
    Twix.knob('FrameInterp').setExpression(name +'.interpolation')
    Twix.knob('Frame').setExpression(name +'.timingFrame2')
    Twix.knob('label').setValue('(' + name + ')')
    Twix.setXpos(postion[0]+320-Twix.screenWidth()/2)
    Twix.setYpos(postion[1])
    Twix.knob('selected').setValue(False)

    if i.knob('timing2').value() == 'Frame':
        Twarp = nuke.createNode("TimeWarp")
        Twarp.knob('lookup').setExpression(name +'.timingFrame2')
        Twarp.knob('label').setValue('(' + name + ')')
        Twarp.setXpos(postion[0]+440-Twarp.screenWidth()/2)
        Twarp.setYpos(postion[1])
        Twarp.knob('selected').setValue(False)
    
    emptySelection(selection)