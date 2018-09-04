def saveImage ():

    ### Getting Lut list from root
    LutList = [n.split(" ")[0] for n in nuke.root()['luts'].toScript().split("\n")]
    Luts = '\n'.join(LutList)

    ### creating panel and assign buttons
    ef = nuke.Panel("Viewer - Save Image As", 420)
    ef.addFilenameSearch("Choose path / file type", "")
    ef.addButton("Cancel")
    ef.addEnumerationPulldown('Channels', "rgb rgba all")
    ef.addEnumerationPulldown('Color Space', Luts)
    ef.addEnumerationPulldown('Exr Type', "16bit-half 32bit-float")
    ef.addButton("ok")
    window=ef.show()

    ### getting values from panel
    exrtype = ef.value('Exr Type')
    channel = ef.value('Channels')
    path = ef.value("Choose path & file type")
    colorSpace = ef.value('Color Space')
    fileType = path.split('.')[-1]

    ### User cancel the oparation
    if window == 0 :
        return

    ### if file format not found
    fileFormat = path.split('/')[-1]
    findDot = ('.')
    for dot in findDot:
        if dot in fileFormat:
            if dot == '.':
            
                ### getting path from user input
                if path == "":
                    nuke.message('no file path selected ')
                if path == "":
                    return
            
                ### getting active node
                curViewer = nuke.activeViewer()
                curNode = curViewer.node()
                acticeVinput = curViewer.activeInput()
                curN = curNode.input(acticeVinput)
            
                ### creating temp write
                w = nuke.createNode("Write")
                w.setName("tempWrite")
                w.setInput(0, curN)
                w['file'].setValue(path)
                w['colorspace'].setValue(colorSpace)
                w['channels'].setValue(channel)
            
                ### if file type is jpg
                if fileType == 'jpg' :
                    w['_jpeg_sub_sampling'].setValue(2)
                    w['_jpeg_quality'].setValue(1)
            
                ### if file type is exr
                if fileType == 'exr' :
                    w['datatype'].setValue(exrtype)
                    w['compression'].setValue(2)
                    w['metadata'].setValue(0)
            
                ### setting current frame for render
                curFrame = nuke.frame()
                if curFrame =="":
                  curFrame = curFrame
            
                ### execute write node
                nuke.execute(nuke.selectedNode(), (int(curFrame)), curFrame)
                name = w.knob('file').value()
                nukescripts.node_delete(popupOnError=True)
            
                ### create Read node
                r = nuke.createNode("Read")
                r['file'].setValue(name)
                curFrame = nuke.frame()
                r['first'].setValue(int(curFrame))
                r['last'].setValue(int(curFrame))
        else:
            nuke.message('forget to choose file format')
            return
