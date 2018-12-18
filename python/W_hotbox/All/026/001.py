#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: test
# COLOR: #999999
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

import nuke, random

def nodeIsInside (node, backdropNode):
  """Returns true if node geometry is inside backdropNode otherwise returns false"""
  topLeftNode = [node.xpos(), node.ypos()]
  topLeftBackDrop = [backdropNode.xpos(), backdropNode.ypos()]
  bottomRightNode = [node.xpos() + node.screenWidth(), node.ypos() + node.screenHeight()]
  bottomRightBackdrop = [backdropNode.xpos() + backdropNode.screenWidth(), backdropNode.ypos() + backdropNode.screenHeight()]

  topLeft = ( topLeftNode[0] >= topLeftBackDrop[0] ) and ( topLeftNode[1] >= topLeftBackDrop[1] )
  bottomRight = ( bottomRightNode[0] <= bottomRightBackdrop[0] ) and ( bottomRightNode[1] <= bottomRightBackdrop[1] )

  return topLeft and bottomRight

def autoBackdrop():
  '''
  Automatically puts a backdrop behind the selected nodes.

  The backdrop will be just big enough to fit all the select nodes in, with room
  at the top for some text in a large font.
  '''
  selNodes = nuke.selectedNodes()
  if not selNodes:
    return nuke.nodes.BackdropNode()

  # Calculate bounds for the backdrop node.
  bdX = min([node.xpos() for node in selNodes])
  bdY = min([node.ypos() for node in selNodes])
  bdW = max([node.xpos() + node.screenWidth() for node in selNodes]) - bdX
  bdH = max([node.ypos() + node.screenHeight() for node in selNodes]) - bdY

  zOrder = 0
  selectedBackdropNodes = nuke.selectedNodes( "BackdropNode" )
  #if there are backdropNodes selected put the new one immediately behind the farthest one
  if len( selectedBackdropNodes ) :
    zOrder = min( [node.knob( "z_order" ).value() for node in selectedBackdropNodes] ) - 1
  else :
    #otherwise (no backdrop in selection) find the nearest backdrop if exists and set the new one in front of it
    nonSelectedBackdropNodes = nuke.allNodes("BackdropNode")
    for nonBackdrop in selNodes:
      for backdrop in nonSelectedBackdropNodes:
        if nodeIsInside( nonBackdrop, backdrop ):
          zOrder = max( zOrder, backdrop.knob( "z_order" ).value() + 1 )

  # Expand the bounds to leave a little border. Elements are offsets for left, top, right and bottom edges respectively
  left, top, right, bottom = (-10, -80, 10, 10)
  bdX += left
  bdY += top
  bdW += (right - left)
  bdH += (bottom - top)

  n = nuke.nodes.BackdropNode(xpos = bdX,
                              bdwidth = bdW,
                              ypos = bdY,
                              bdheight = bdH,
                              tile_color = int((random.random()*(16 - 10))) + 10,
                              note_font_size=42,
                              z_order = zOrder )

  # revert to previous selection
  n['selected'].setValue(False)
  for node in selNodes:
    node['selected'].setValue(True)

  return n

    