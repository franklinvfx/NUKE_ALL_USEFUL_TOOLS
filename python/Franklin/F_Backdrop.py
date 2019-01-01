'''
I wrote this script inspired by that of Timur Khodzhaev. http://www.nukepedia.com/python/nodegraph/autobackdrop-replacement/finishdown?miv=1&mjv=2

Copyright (c) 2018 Franklin VFX Co.

'''

import nuke, random, nukescripts, colorsys

def nodeIsInside(node, backdropNode):
    '''
    Returns true if node geometry is inside backdropNode
    otherwise returns false
    '''
    topLeftNode = [node.xpos(), node.ypos()]
    topLeftBackDrop = [backdropNode.xpos(), backdropNode.ypos()]
    bottomRightNode = [node.xpos() + node.screenWidth(),
                       node.ypos() + node.screenHeight()]
    bottomRightBackdrop = [backdropNode.xpos() + backdropNode.screenWidth(),
                           backdropNode.ypos() + backdropNode.screenHeight()]

    topLeft = ((topLeftNode[0] >= topLeftBackDrop[0]) and
               (topLeftNode[1] >= topLeftBackDrop[1]))
    bottomRight = ((bottomRightNode[0] <= bottomRightBackdrop[0]) and
                   (bottomRightNode[1] <= bottomRightBackdrop[1]))

    return topLeft and bottomRight


def F_Backdrop():
    '''
    Automatically puts a backdrop behind the selected nodes.

    The backdrop will be just big enough to fit all the select nodes in,
    with room at the top for some text in a large font.
    '''
    sel = nuke.selectedNodes()
    forced = False

    # if nothing is selected
    if not sel:
        forced = True
        b = nuke.createNode('NoOp')
        sel.append(b)

    # Calculate bounds for the backdrop node.
    bdX = min([node.xpos() for node in sel])
    bdY = min([node.ypos() for node in sel])
    bdW = max([node.xpos() + node.screenWidth() for node in sel]) - bdX
    bdH = max([node.ypos() + node.screenHeight() for node in sel]) - bdY

    zOrder = 0
    selectedBackdropNodes = nuke.selectedNodes("BackdropNode")

    # if there are backdropNodes selected
    # put the new one immediately behind the farthest one
    if len(selectedBackdropNodes):
        zOrder = min([node.knob("z_order").value()
                      for node in selectedBackdropNodes]) - 1
    else:
        # otherwise (no backdrop in selection) find the nearest backdrop
        # if exists and set the new one in front of it
        nonSelectedBackdropNodes = nuke.allNodes("BackdropNode")
        for nonBackdrop in sel:
            for backdrop in nonSelectedBackdropNodes:
                if nodeIsInside(nonBackdrop, backdrop):
                    zOrder = max(zOrder, backdrop.knob("z_order").value() + 1)

    # Expand the bounds to leave a little border.
    # Elements are offsets for left, top, right and bottom edges respectively
    left, top, right, bottom = (-30, -120, 30, 30)
    bdX += left
    bdY += top
    bdW += (right - left)
    bdH += (bottom - top)

    R, G, B = colorsys.hsv_to_rgb(random.random(),
                                  .1+random.random()*.15,
                                  .15 + random.random()*.15)

    n = nuke.nodes.BackdropNode(xpos=bdX, bdwidth=bdW, ypos=bdY,
                                bdheight=bdH,
                                tile_color=int('%02x%02x%02x%02x' % (R*255,
                                                                     G*255,
                                                                     B*255,
                                                                     255), 16),
                                note_font_size=50, z_order=zOrder)

    n.showControlPanel()

    # Buid all knobs for Backdrop
    tab = nuke.Tab_Knob('F_VFX', 'BackdropNode')
    text = nuke.Multiline_Eval_String_Knob('text', 'Text')
    position = nuke.Enumeration_Knob('position', '', ['Left', 'Center'])
    size = nuke.Double_Knob('font_size', 'Font Size') 
    size.setRange(10,100)
    space1 = nuke.Text_Knob('S01', ' ', ' ')
    space2 = nuke.Text_Knob('S02', ' ', ' ')

    grow = nuke.PyScript_Knob('grow', ' <img src="F_scalep.png">', "n=nuke.thisNode()\n\ndef grow(node=None,step=50):\n    try:\n        if not node:\n            n=nuke.selectedNode()\n        else:\n            n=node\n            n['xpos'].setValue(n['xpos'].getValue()-step)\n            n['ypos'].setValue(n['ypos'].getValue()-step)\n            n['bdwidth'].setValue(n['bdwidth'].getValue()+step*2)\n            n['bdheight'].setValue(n['bdheight'].getValue()+step*2)\n    except Exception,e:\n        print('Error:: %s' % e)\n\ngrow(n,50)")
    shrink = nuke.PyScript_Knob('shrink', ' <img src="F_scalem.png">', "n=nuke.thisNode()\n\ndef shrink(node=None,step=50):\n    try:\n        if not node:\n            n=nuke.selectedNode()\n        else:\n            n=node\n            n['xpos'].setValue(n['xpos'].getValue()+step)\n            n['ypos'].setValue(n['ypos'].getValue()+step)\n            n['bdwidth'].setValue(n['bdwidth'].getValue()-step*2)\n            n['bdheight'].setValue(n['bdheight'].getValue()-step*2)\n    except Exception,e:\n        print('Error:: %s' % e)\n\nshrink(n,50)")

    colorandom = nuke.PyScript_Knob('colorandom', ' <img src="ColorBars.png">', "import colorsys, random\nn=nuke.thisNode()\nR,G,B= colorsys.hsv_to_rgb(random.random(),.1+random.random()*.15,.15+random.random()*.15)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ) )")

    red = nuke.PyScript_Knob('red', ' <img src="F_r.png">', "import colorsys\nn=nuke.thisNode()\nR,G,B= [0.0, 0.77, 0.8]\nR,G,B=colorsys.hsv_to_rgb(R,G,B)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ))\n")
    orange = nuke.PyScript_Knob('orange', ' <img src="F_o.png">', "import colorsys\nn=nuke.thisNode()\nR,G,B= [0.1, 0.8, 0.8]\nR,G,B=colorsys.hsv_to_rgb(R,G,B)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ))\n")
    yellow = nuke.PyScript_Knob('yellow', ' <img src="F_y.png">', "import colorsys\nn=nuke.thisNode()\nR,G,B= [0.16, 0.8, 0.8]\nR,G,B=colorsys.hsv_to_rgb(R,G,B)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ))\n")
    green = nuke.PyScript_Knob('green', ' <img src="F_g.png">', "import colorsys\nn=nuke.thisNode()\nR,G,B= [0.33, 0.8, 0.7]\nR,G,B=colorsys.hsv_to_rgb(R,G,B)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ))\n")
    cyan = nuke.PyScript_Knob('cyan', ' <img src="F_c.png">', "import colorsys\nn=nuke.thisNode()\nR,G,B= [0.46, 0.8, 0.7]\nR,G,B=colorsys.hsv_to_rgb(R,G,B)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ))\n")
    blue = nuke.PyScript_Knob('blue', ' <img src="F_b.png">', "import colorsys\nn=nuke.thisNode()\nR,G,B= [0.6, 0.7, 0.76]\nR,G,B=colorsys.hsv_to_rgb(R,G,B)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ))\n")
    darkblue = nuke.PyScript_Knob('darkblue', ' <img src="F_db.png">', "import colorsys\nn=nuke.thisNode()\nR,G,B= [0.67, 0.74, 0.6]\nR,G,B=colorsys.hsv_to_rgb(R,G,B)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ))\n")
    magenta = nuke.PyScript_Knob('magenta', ' <img src="F_m.png">', "import colorsys\nn=nuke.thisNode()\nR,G,B= [0.8, 0.74, 0.65]\nR,G,B=colorsys.hsv_to_rgb(R,G,B)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ))\n")
    pink = nuke.PyScript_Knob('pink', ' <img src="F_p.png">', "import colorsys\nn=nuke.thisNode()\nR,G,B= [0.92, 0.74, 0.8]\nR,G,B=colorsys.hsv_to_rgb(R,G,B)\nn['tile_color'].setValue( int('%02x%02x%02x%02x' % (R*255,G*255,B*255,255), 16 ))\n")

    copyright = nuke.Text_Knob("Ftools","","<font color=\"#1C1C1C\"> Franklin VFX - 2018")

    n.addKnob(tab)
    n['knobChanged'].setValue("try:\n    listenedKnobs = ['text', 'position', 'name']\n    node = nuke.thisNode()\n    name = node.knob('name').value()\n    text = node.knob('text').value()\n    position = node.knob('position').value()\n    position = \"<\" + position + \">\"\n    label = node.knob('label').value()\n    \n    if nuke.thisKnob().name() in listenedKnobs:\n        if text == \"\":\n            if node.knob('position').value() == \"left\":\n                node.knob('label').setValue()\n            else:\n                node.knob('label').setValue(position + name)\n        else:\n            if node.knob('position').value() == \"left\":\n                node.knob('label').setValue(text)\n            else:\n                node.knob('label').setValue(position + text)\n                \n    elif nuke.thisKnob().name() == 'font_size':\n        fontSize = node.knob('font_size').value()\n        node.knob('note_font_size').setValue(fontSize)\nexcept:\n    pass")
    n.addKnob(text)
    n['text'].setFlag(nuke.STARTLINE)
    n.addKnob(size)
    n['font_size'].setValue(50)
    n.addKnob(position)
    n['position'].clearFlag(nuke.STARTLINE)
    n.addKnob(space1)
    n.addKnob(grow)
    n.addKnob(shrink)
    n.addKnob(colorandom)
    n.addKnob(red)
    n.addKnob(orange)
    n.addKnob(yellow)
    n.addKnob(green)
    n.addKnob(cyan)
    n.addKnob(blue)
    n.addKnob(darkblue)
    n.addKnob(magenta)
    n.addKnob(pink)
    n.addKnob(space2)
    n.addKnob(copyright)

    # revert to previous selection
    n['selected'].setValue(True)

    if forced:
        nuke.delete(b)
    else:
        for node in sel:
            node['selected'].setValue(True)
    return n