import nuke

def Bdrop():
    # Smaller backdrops on top of bigger ones
    allNodes = nuke.allNodes('BackdropNode')
    # all.sort(key = lambda x: x.screenHeight() * x.screenWidth(), reverse = True)
    allNodes.sort(key=lambda x: x['bdheight'].value() * x['bdwidth'].value(),
                  reverse=True)

    if int(nuke.env['NukeVersionMajor']) < 9:
        try:
            [b.selectNodes() for b in allNodes if (b in sel or len(sel) == 0)]
        except:  # This will be used for Nuke versions below 6.3v5
            [selectBackdropContents(b) for b in allNodes if (b in sel or len(sel) == 0)]
    else:
        # allNodes.sort(key = lambda x: x.screenHeight() * x.screenWidth(), reverse = False)
        for index, b in enumerate(allNodes):
            b["z_order"].setValue(index)
Bdrop()