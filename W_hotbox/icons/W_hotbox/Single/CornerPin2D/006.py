#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: Convert to Tracker
#
#----------------------------------------------------------------------------------------------------------

'''def cornerPinToTracker():

    cp = nuke.selectedNode()
 
    cp1 = cp['to1'].animations()
    cp2 = cp['to2'].animations()
    cp3 = cp['to3'].animations()
    cp4 = cp['to4'].animations()


    tr = nuke.createNode("Tracker3")
    tr.knob('enable2').setValue('True')
    tr.knob('enable3').setValue('True')
    tr.knob('enable4').setValue('True')
    tr.knob('warp').setValue('srt')
    tr.knob('transform').setValue('match-move')
    tr.knob('use_for1').setValue('all')
    tr.knob('use_for2').setValue('all')
    tr.knob('use_for3').setValue('all')
    tr.knob('use_for4').setValue('all')
    tr.knob('reference_frame').setValue(nuke.frame())
   

    nuke.toNode(tr.knob('name').value())['track1'].copyAnimations(cp1)
    nuke.toNode(tr.knob('name').value())['track2'].copyAnimations(cp2)
    nuke.toNode(tr.knob('name').value())['track3'].copyAnimations(cp3)
    nuke.toNode(tr.knob('name').value())['track4'].copyAnimations(cp4)

cornerPinToTracker()'''

###    Usefull for converting CornerPin node imported from Mocha to tracker node
###    Script set transform mode to matchmove and reference frame to current frame

def cornerPinToTracker():
    anims = []
    cp = nuke.selectedNode()

    for i in range(1, 5):
        if cp['to'+str(i)].isAnimated():
            anims.append(cp['to'+str(i)].animations())

    # define how to access attributes of the tracks knob for Tracker4
    numColumns = 31
    colX = 2
    colY = 3
    colTranslate = 6
    colRotate = 7
    colScale = 8
    numTracker = 0

    tracker = nuke.createNode("Tracker4")
    tracker.setXYpos(cp.xpos()-150, cp.ypos())
    tracker.setInput(0, None)
    tracker.knob('transform').setValue('match-move')
    tracker.knob('label').setValue('From '+cp.name())
    tracker.knob('reference_frame').setValue(nuke.frame())

    # set attributes
    for toX, toY in anims:
        tracker.knob('add_track').execute()
        tracker.knob('tracks').setValue(True, int(numColumns*numTracker)+colTranslate)
        tracker.knob('tracks').setValue(True, int(numColumns*numTracker)+colRotate)
        tracker.knob('tracks').setValue(True, int(numColumns*numTracker)+colScale)

        # keyX.x = frame
        # keyX.y = value
        for keyX in toX.keys():
            tracker.knob('tracks').setValueAt(keyX.y, keyX.x, int(numColumns*numTracker)+colX)
        for keyY in toY.keys():
            tracker.knob('tracks').setValueAt(keyY.y, keyY.x, int(numColumns*numTracker)+colY)
        numTracker += 1

cornerPinToTracker()