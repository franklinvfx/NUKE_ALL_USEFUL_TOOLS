# animatedSnap3D.py
# An extension to The Foundry's nukescripts.snap3d module
# to allow snapping to animated geometry
#
# Ivan Busquets - 2011
#
# Updates:
# 03/2012  -  Updated for Nuke 6.3, since the name of the original functions in the snap3d module changed from 6.2 to 6.3
#          -  Cleaned up and grouped animation loop into a single wrapper function
#

import nuke, nukescripts, nuke.geo
from nukescripts import snap3d as s3d

def getFrameRange():
  '''Open a dialog to request a Nuke-style frame range
  @return:  a frameRange object if a valid frame range is entered
                None if frame range is invalid or dialog is cancelled
  '''
  firstFrame = int(nuke.numvalue('root.first_frame'))
  lastFrame = int(nuke.numvalue('root.last_frame'))
  step = 1
  _range = str(nuke.FrameRange(firstFrame,lastFrame,step))
  r = nuke.getInput('Enter Frame Range:', _range)

  try:
    if not r:
      return None
    else:
      return nuke.FrameRange(r)
  except:
    nuke.message('Invalid frame range')
    return None

# Lazy functions to call on "thisNode"  

def translateThisNodeToPointsAnimated():
  return translateToPointsAnimated(nuke.thisNode())
  
def translateRotateThisNodeToPointsAnimated():
  return translateRotateToPointsAnimated(nuke.thisNode())

def translateRotateScaleThisNodeToPointsAnimated():
  return translateRotateScaleToPointsAnimated(nuke.thisNode())

# Lazy functions to determine the vertex selection
# and call animatedSnapFunc with the right arguments

def translateToPointsAnimated(nodeToSnap):
  return animatedSnapFunc(nodeToSnap, s3d.getSelection(), \
                          ["translate"],\
                          ["translate", "xform_order"],\
                          minVertices = 1, snapFunc = s3d.translateToPointsVerified)
    
def translateRotateToPointsAnimated(nodeToSnap):
  return animatedSnapFunc(nodeToSnap, s3d.getSelection(), \
                          ["translate", "rotate"],\
                          ["translate", "rotate", "xform_order", "rot_order"],\
                          minVertices = 1, snapFunc = s3d.translateRotateToPointsVerified)
  
def translateRotateScaleToPointsAnimated(nodeToSnap):
  return animatedSnapFunc(nodeToSnap, s3d.getSelection(),\
                          ["translate", "rotate", "scaling"],\
                          ["translate", "rotate", "scaling", "xform_order", "rot_order"],\
                          minVertices = 3, snapFunc = s3d.translateRotateScaleToPointsVerified)
  
  
# Main wrapper function
def animatedSnapFunc(nodeToSnap, vertexSelection, knobsToAnimate, knobsToVerify, minVertices = 1, snapFunc = s3d.translateToPointsVerified):
  '''A wrapper to call the relevant snap functions within a framerange loop'''
  temp = None
  try:
    s3d.verifyNodeToSnap(nodeToSnap, knobsToVerify)
    
    # verify vertex selection once before the loop
    s3d.verifyVertexSelection(vertexSelection, minVertices)
    
    # now ask for a framerange
    frames = getFrameRange()
   
    if not frames:  return  # Exit eary if cancelled or empty framerange
    
    # Add a CurveTool for the forced-evaluation hack
    temp = nuke.nodes.CurveTool()
    
    # Set the anim flag on knobs
    for knob in [nodeToSnap[x] for x in knobsToAnimate]:
      # reset animated status
      if knob.isAnimated():
        knob.clearAnimated()
      knob.setAnimated()  

    # Set up Progress Task  
    task = nuke.ProgressTask("animatedSnap3D")
    task.setMessage("Matching position of %s to selected vertices" % nodeToSnap.name())
    
    # Loop through the framerange
    for frame in frames:    
      if task.isCancelled():
        break
      
      # Execute the CurveTool node to force evaluation of the tree
      nuke.execute(temp, frame, frame)
      
      # this is repetitive, but the vertex selection needs to be computed again
      # in order to get the vertices at the right context (time)
      vertexSelection = s3d.getSelection()
      
      # this is also repetitive. Selection should be already verified
      # but checking again in case topology has changed between frames
      s3d.verifyVertexSelection(vertexSelection, minVertices)
      
      # Call the passed snap function from the nukescripts.snap3d module
      snapFunc(nodeToSnap, vertexSelection)
    
  except ValueError, e:
    nuke.message(str(e))

  finally:  # delete temp CurveTool node
    if temp:
      nuke.delete(temp)
  



  