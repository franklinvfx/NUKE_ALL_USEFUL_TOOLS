def IPNodesList():
  IPNodes=['Diffuse Color', 'Saturation', 'Mirror', 'Grain Check', 'Grid']
  return IPNodes

def getActiveViewerNode():
  return nuke.activeViewer().node().knob('input_process_node').getValue()

def viewerInput(ipNode=None, openPanel=False): 
  '''Creates or deletes a VIEWER_INPUT node and sets the active viewer to it'''
  IPNodes=IPNodesList()
  IPName=getActiveViewerNode()

  IPList = ['{%s}' % l for l in IPNodes]
  if not ipNode: # panel to select the appropriate IP mode if ipNode not set via menu.py
    p=nuke.Panel('Input Process',300)
    p.addEnumerationPulldown('IP Node',' '.join(IPList))
    p.addBooleanCheckBox('Open Panel', True)
    pp=p.show()
    if pp:
      ipNode=p.value('IP Node')
      openPanel=p.value('Open Panel')
    else:
      return
  if 'Remove'==ipNode:
    removeExistingNode(IPName)
    restoreArchivedNode(IPName)
    return

  makeViewerNode(ipNode, openPanel, IPName=IPName)
  nuke.activeViewer().node().knob('input_process').setValue(True)

def makeViewerNode(ipNode, openPanel, IPName=''): # select which VIEWER_INPUT to create from either the panel above or via menu.py
    removeExistingNode(IPName)

    if 'Mirror'== ipNode:
      n=mirrorIP(openPanel)
    #elif 'Normalize'== ipNode:
      #n=normalizeIP(openPanel)
    #elif 'Grid'== ipNode:
      #n=gridIP(openPanel)
    elif 'Diffuse Color'== ipNode:
      n=colorIP(openPanel)
	#elif 'Noise'== ipNode:
      #n=noiseIP(openPanel)
    elif 'Grain Check'== ipNode:
      n=noiseIP(openPanel)
    elif 'Saturation'== ipNode:
      n=overIP(openPanel)

    n['name'].setValue(IPName)
    n['label'].setValue(ipNode)
    n.setXYpos(nuke.activeViewer().node().xpos()+100, nuke.activeViewer().node().ypos()+0)
    return

def removeExistingNode(IPName):
    IPNodes=IPNodesList()
    for i in nuke.allNodes():
        i['selected'].setValue(False)
        if IPName == i['name'].value():
            if i['label'].value() not in IPNodes:
              i['name'].setValue('ARCHIVED_'+IPName)
              print 'found existing IP node - archiving'
              return
            print 'deleting old viewer input node'
            if 'Auto Shuffle' in i['label'].value():
              removeViewerKnobChanged()
            i['selected'].setValue(True)
            nukescripts.node_delete(popupOnError=True)
    return

def restoreArchivedNode(IPName):
    for i in nuke.allNodes():
        if 'ARCHIVED_'+IPName == i['name'].value():
          print 'resoring archived IP node'
          i['name'].setValue(IPName)
          nuke.activeViewer().node().knob('input_process').setValue(False)

    return

def mirrorIP(openPanel=False):
  n=nuke.createNode('Mirror', inpanel=openPanel)
  n['Horizontal'].setValue(True)
  n['tile_color'].setValue(15151515)
  n['hide_input'].setValue(True)
  return n
  
def gridIP(openPanel=False):
  n=nuke.createNode('Grid', inpanel=openPanel)
  n['tile_color'].setValue(15151515)
  n['hide_input'].setValue(True)
  return n
'''
def hsvIP(openPanel=False):
  hsv=nuke.createNode('Colorspace', inpanel=False)
  
  hsv['colorspace_out'].setValue('HSV')
  hsv['selected'].setValue(True)
  hsv['selected'].setValue(True)
  
  n=nuke.collapseToGroup(show=openPanel)
  return n
'''  
def overIP(openPanel=False):
  n=nuke.createNode('Saturation', inpanel=openPanel)
  n['saturation'].setValue(2)
  n['tile_color'].setValue(15151515)
  n['hide_input'].setValue(True)
  return n

def normalizeIP(openPanel=False):
  nDot=nuke.createNode('Dot', inpanel=False)
  maxD=nuke.createNode('Dilate', inpanel=False)
  minD=nuke.createNode('Dilate', inpanel=False)
  maxBB=nuke.createNode('CopyBBox', inpanel=False)
  minBB=nuke.createNode('CopyBBox', inpanel=False)
  fromMinMax=nuke.createNode('Merge2', inpanel=False)
  fromMinIn=nuke.createNode('Merge2', inpanel=False)
  mDivide=nuke.createNode('Merge2', inpanel=False)

  maxD.setInput(0,nDot)
  minD.setInput(0,nDot)
  maxBB.setInput(0,maxD)
  maxBB.setInput(1,nDot)
  minBB.setInput(0,minD)
  minBB.setInput(1,nDot)
  fromMinMax.setInput(0,maxBB)
  fromMinMax.setInput(1,minBB)
  fromMinIn.setInput(0,nDot)
  fromMinIn.setInput(1,minBB)
  mDivide.setInput(0,fromMinMax)
  mDivide.setInput(1,fromMinIn)

  maxD.setName('DilateMax')
  maxD['size'].setExpression('max(input.format.w, input.format.h)')
  minD.setName('DilateMin')
  minD['size'].setExpression('-max(input.format.w, input.format.h)')
  fromMinMax['operation'].setValue('from')
  fromMinIn['operation'].setValue('from')
  mDivide['operation'].setValue('divide')


  nDot['selected'].setValue(True)
  maxD['selected'].setValue(True)
  minD['selected'].setValue(True)
  maxBB['selected'].setValue(True)
  minBB['selected'].setValue(True)
  fromMinMax['selected'].setValue(True)
  fromMinIn['selected'].setValue(True)
  mDivide['selected'].setValue(True)

  n=nuke.collapseToGroup(show=openPanel)
  
  group = nuke.selectedNode()
  group['tile_color'].setValue(15151515)
  group['hide_input'].setValue(True)

  return n

def colorIP(openPanel=False):

  gra=nuke.createNode('Grade', inpanel=False)
  matrixR=nuke.createNode('ColorMatrix', inpanel=False)
  matrixG=nuke.createNode('ColorMatrix', inpanel=False)
  matrixB=nuke.createNode('ColorMatrix', inpanel=False)
  divideR=nuke.createNode('Merge2', inpanel=False)
  divideG=nuke.createNode('Merge2', inpanel=False)
  divideB=nuke.createNode('Merge2', inpanel=False)
  addchan=nuke.createNode('AddChannels', inpanel=False)
  copyG=nuke.createNode('Copy', inpanel=False)
  copyB=nuke.createNode('Copy', inpanel=False)
  copyA=nuke.createNode('Copy', inpanel=False)

  matrixR.setInput(0,gra)
  matrixG.setInput(0,gra)
  matrixB.setInput(0,gra)
  divideR.setInput(0,matrixR)
  divideR.setInput(1,gra)
  divideG.setInput(0,matrixG)
  divideG.setInput(1,gra)
  divideB.setInput(0,matrixB)
  divideB.setInput(1,gra)
  addchan.setInput(0,gra)
  copyG.setInput(0,divideR)
  copyG.setInput(1,divideG)
  copyB.setInput(0,copyG)
  copyB.setInput(1,divideB)
  copyA.setInput(0,copyB)
  copyA.setInput(1,addchan)

  gra.setName('Franklin')
  gra['gamma'].setExpression('-parent.gamma_1+1')
  matrixR['matrix'].setValue('111000000')
  matrixG['matrix'].setValue('000111000')
  matrixB['matrix'].setValue('000000111')
  divideR['operation'].setValue('divide')
  divideG['operation'].setValue('divide')
  divideB['operation'].setValue('divide')
  addchan['channels'].setValue('rgba.alpha')
  copyG['from0'].setValue('rgba.green')
  copyG['to0'].setValue('rgba.green')
  copyB['from0'].setValue('rgba.blue')
  copyB['to0'].setValue('rgba.blue')
 
  gra['selected'].setValue(True)
  matrixR['selected'].setValue(True)
  matrixG['selected'].setValue(True)
  matrixB['selected'].setValue(True)
  divideR['selected'].setValue(True)
  divideG['selected'].setValue(True)
  divideB['selected'].setValue(True)
  addchan['selected'].setValue(True)
  copyG['selected'].setValue(True)
  copyB['selected'].setValue(True)
  copyA['selected'].setValue(True)

  c = nuke.collapseToGroup(show=openPanel)
  
  group = nuke.selectedNode()
  with group:
      firstab = nuke.Tab_Knob("firsTab","Franklin")
      group.addKnob(firstab)
      gamma_1 = nuke.Double_Knob("gamma_1", "Contrast")
      group.addKnob(gamma_1)

  group['gamma_1'].setValue(0.4)
  group['tile_color'].setValue(15151515)
  group['hide_input'].setValue(True)
  
  return c
  


def noiseIP(openPanel=False):

  logA=nuke.createNode('Log2Lin', inpanel=False)
  logB=nuke.createNode('Log2Lin', inpanel=False)
  blurr=nuke.createNode('Blur', inpanel=False)
  diff=nuke.createNode('Merge2', inpanel=False)
  gra=nuke.createNode('Grade', inpanel=False)
  matrixR=nuke.createNode('ColorMatrix', inpanel=False)
  matrixG=nuke.createNode('ColorMatrix', inpanel=False)
  matrixB=nuke.createNode('ColorMatrix', inpanel=False)
  divideR=nuke.createNode('Merge2', inpanel=False)
  divideG=nuke.createNode('Merge2', inpanel=False)
  divideB=nuke.createNode('Merge2', inpanel=False)
  copyG=nuke.createNode('Copy', inpanel=False)
  copyB=nuke.createNode('Copy', inpanel=False)
  switchh=nuke.createNode('Switch', inpanel=False)

  logB.setInput(0,logA)
  blurr.setInput(0,logB)
  diff.setInput(0,logB)
  diff.setInput(1,blurr)
  gra.setInput(0,diff)
  matrixR.setInput(0,gra)
  matrixG.setInput(0,gra)
  matrixB.setInput(0,gra)
  divideR.setInput(0,matrixR)
  divideR.setInput(1,gra)
  divideG.setInput(0,matrixG)
  divideG.setInput(1,gra)
  divideB.setInput(0,matrixB)
  divideB.setInput(1,gra)
  copyG.setInput(0,divideR)
  copyG.setInput(1,divideG)
  copyB.setInput(0,copyG)
  copyB.setInput(1,divideB)
  switchh.setInput(0,gra)
  switchh.setInput(1,copyB)


  logA['operation'].setValue('lin2log')
  logB['operation'].setValue('lin2log')
  logB['mix'].setExpression('parent.contrast')
  blurr['size'].setValue(3)
  diff['operation'].setValue('difference')
  gra.setName('Franklin')
  gra['multiply'].setValue(8)
  matrixR['matrix'].setValue('111000000')
  matrixG['matrix'].setValue('000111000')
  matrixB['matrix'].setValue('000000111')
  divideR['operation'].setValue('divide')
  divideG['operation'].setValue('divide')
  divideB['operation'].setValue('divide')
  copyG['from0'].setValue('rgba.green')
  copyG['to0'].setValue('rgba.green')
  copyB['from0'].setValue('rgba.blue')
  copyB['to0'].setValue('rgba.blue')
  switchh['which'].setExpression('parent.mode')
  
  logA['selected'].setValue(True)
  logB['selected'].setValue(True)
  blurr['selected'].setValue(True)
  diff['selected'].setValue(True)
  gra['selected'].setValue(True)
  matrixR['selected'].setValue(True)
  matrixG['selected'].setValue(True)
  matrixB['selected'].setValue(True)
  divideR['selected'].setValue(True)
  divideG['selected'].setValue(True)
  divideB['selected'].setValue(True)
  copyG['selected'].setValue(True)
  copyB['selected'].setValue(True)
  switchh['selected'].setValue(True)

  c = nuke.collapseToGroup(show=openPanel)
  group = nuke.selectedNode()
  mod = nuke.Enumeration_Knob("mode", "Mode", ["Normal", "Color"])
  contrast = nuke.Double_Knob("contrast", "Contrast")
  
  with group:
      firstab = nuke.Tab_Knob("firsTab","Franklin")
      group.addKnob(firstab)
      group.addKnob(mod)
      group.addKnob(contrast)


  group['contrast'].setValue(0.5)
  group['tile_color'].setValue(15151515)
  group['hide_input'].setValue(True)
  
  return c

def removeViewerKnobChanged():
  for i in nuke.allNodes('Viewer'):
    i['knobChanged'].setValue('')
  return
