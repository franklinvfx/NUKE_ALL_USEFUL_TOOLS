####pythone code by Pau Rocher###
####bikura at gmail dot com######

import nuke
import nukescripts
import os

class shuffleChannels(nukescripts.PythonPanel):
  def __init__(self, n):
    nukescripts.PythonPanel.__init__(self, 'shuffle channels')
    self.n = n
    self.channels = self.n.channels()

  #def builder(self):
###layers list builder
    self.layers = []
    for i in range ( len ( self.channels ) ):
      if self.channels[i].split('.')[0] not in self.layers :
        self.layers.append ( self.channels[i].split('.')[0] )

#UI######################################################################################################################
    self.tabGroup = nuke.BeginTabGroup_Knob ('tabGroup', '')
    self.addKnob (self.tabGroup)
##layersTab
    self.layersTab = nuke.Tab_Knob ('layersTab', 'layers')
    self.addKnob (self.layersTab)
    
    self.selectedNodeName = nuke.Text_Knob ( 'selectedNodeName', 'selected node: ', '%s, %s node' %( self.n.name(), self.n.Class() ) )
    self.addKnob (self.selectedNodeName)
    
    self.separator = nuke.Text_Knob ( 'separator', '')
    self.addKnob (self.separator)
    
    self.presets = nuke.Enumeration_Knob ('presets', '', ['                   '])
    self.addKnob (self.presets)

    self.savePreset = nuke.PyScript_Knob ('savePreset', 'save preset', 'shuffleChannels.savePreset()')
    #self.addKnob (self.savePreset)
    
    self.removePreset = nuke.PyScript_Knob ('deletePreset', 'delete preset', 'shuffleChannels.deletePreset()')
    #self.addKnob (self.removePreset)
    
    for i in range ( len ( self.layers ) ):
      exec "self.layer%s = ''" %( i )
      exec "self.layer%s = nuke.Boolean_Knob ('layer%s', '%s')" %( i, i, self.layers[i] )
      exec "self.addKnob (self.layer%s)" %i
      exec "self.layer%s.setFlag(4096)" %i
      
    #self.selectAllLayers = nuke.PyScript_Knob ('selectAllLayers', 'select all layers', "shuffleChannels.selectAll()")
    #self.addKnob (self.selectAllLayers)
    #self.selectAllLayers.setFlag(4096)
    
    #self.deselectAllLayers = nuke.PyScript_Knob ('deselectAllLayers', 'deselect all layers', "shuffleChannels.deselectAll()")
    #self.addKnob (self.deselectAllLayers)

##channelsTab
    #self.channelsTab = nuke.Tab_Knob ('channelsTab', 'channels')
    #self.addKnob (self.channelsTab)
    #for i in range ( len ( self.channels ) ):
      #exec "self.channel%s = ''" %( i )
      #exec "self.channel%s = nuke.Boolean_Knob ('channel%s', '%s')" %( i, i, self.channels[i] )
      #exec "self.addKnob (self.channel%s)" %i
      #exec "self.channel%s.setFlag(4096)" %i
    
##prefsTab
    self.prefsTab = nuke.Tab_Knob ('prefsTab', 'preferences')
    self.addKnob (self.prefsTab)
    
    self.unPremult = nuke.Boolean_Knob ('unPremult', 'add unpremult / premult nodes')
    self.addKnob (self.unPremult)
    self.unPremult.setFlag (4096)
    
    self.remove = nuke.Boolean_Knob ('remove', 'add remove node')
    self.addKnob  (self.remove)
    self.remove.setFlag(4096)
  
    self.grade = nuke.Boolean_Knob ('grade', 'add grade node')
    self.addKnob  (self.grade)
    self.grade.setFlag(4096)
    
    self.merge = nuke.Boolean_Knob ('merge', 'add merge node')
    self.addKnob  (self.merge)
    self.merge.setFlag(4096)
    self.operation = nuke.Enumeration_Knob ('operation', '  |    operation', [ 'atop', 'average', 'color-burn', 'color-dodge', 'conjoint-over', 'copy', 'difference', 'disjoint-over', 'divide', 'exclusion', 'from', 'geometric', 'hard-light', 'hypot', 'in', 'mask', 'matte', 'max', 'min', 'minus', 'multiply', 'out', 'over', 'overlay', 'plus', 'screen', 'soft-light', 'stencil', 'under', 'xor'])
    self.addKnob (self.operation)
    self.operation.clearFlag(4096)
    self.operation.setValue('plus')
    
    self.copyAlpha = nuke.Boolean_Knob ('copyAlpha', 'add copyAlpha node')
    self.addKnob  (self.copyAlpha)
    self.copyAlpha.setFlag(4096)
    
    self.noShuffLabel = nuke.Boolean_Knob ('noShuffLabel', 'remove label from Shuffles')
    self.addKnob  (self.noShuffLabel)
    self.noShuffLabel.setFlag(4096)
    
    self.separation = nuke.Double_Knob ('separation', 'separation between nodes')
    self.addKnob (self.separation)
    self.separation.setFlag(4096)
    self.separation.setRange (100, 400)
    self.separation.setDefaultValue ([200])
    
    self.shuffLayersColor = nuke.ColorChip_Knob ('shuffLayersColor', 'Shuffle color')
    self.addKnob (self.shuffLayersColor)
    self.shuffLayersColor.setDefaultValue([nuke.toNode('preferences')['NodeColour05Color'].value()])
    self.shuffLayersColor.setFlag(4096)
    
    self.bdrop = nuke.Boolean_Knob ('bdrop', 'add backDrop')
    self.addKnob  (self.bdrop)
    self.bdrop.setFlag(4096)
    
    self.bdropColor = nuke.ColorChip_Knob ('bdropColor', 'backDrop color')
    self.addKnob (self.bdropColor)
    self.bdropColor.setDefaultValue([926365441])
    
    self.separation01 = nuke.Text_Knob ('separation01', '')
    self.addKnob (self.separation01)
    
    self.EndTab = nuke.EndTabGroup_Knob ('endTabGroup', '')
    self.addKnob ( self.EndTab )
  
    #self.importAllChannels = nuke.PyScript_Knob ('importAllChannels', 'all channels', "print 'function to import all layers'")
    #self.addKnob (self.importAllChannels)
    
  def knobChanged(self, knob):
    if knob == self.presets:
      updateLayersPreset ()
  
  def returnLayers(self):
    return self.layers
  def returnChannels(self):
    return self.channels

  
def getData ():
#gets selected node or not
  try:
    global n
    n = nuke.selectedNode()
  except:
    nuke.message ('Select a node.')
    return
  
#if all good launches the panel########################################################
  layers = shuffleChannels(n).returnLayers()      #returns the layers list
  channels = shuffleChannels(n).returnChannels()  #returns the channels list
  global p
  p = shuffleChannels(n)                          #builds the panel
  windowHeight = len(layers)*20+165               #changes panel dimensions
  if windowHeight > 1000:                         #
    windowHeight = 1000                           #
  p.setMinimumSize (600, windowHeight)            #
  readPrefsFile(p)
  refreshPresetsMenu()
  thePanel = p.showModalDialog()                             #launches the panel
  
  if thePanel == False:
    return
  else:
    pass
  

#beyond this point all happens after the panel has been closed#########################
#creation of the prefs variable 
  prefs = {'unPremult': p.unPremult.value(), 'remove': p.remove.value(), 'grade': p.grade.value(), 'merge': p.merge.value(), 'operation': p.operation.value(), 'copyAlpha': p.copyAlpha.value(), 'noShuffLabel': p.noShuffLabel.value(), 'separation': p.separation.value(), 'shuffLayersColor': p.shuffLayersColor.value(), 'bdrop': p.bdrop.value() , 'bdropColor': p.bdropColor.value()}
##writes the preferences file  
  writePrefsFile(p, str(prefs))
#here I collect what layers have been selected
  layerList = []
  for i in range (len ( layers ) ):
    exec "gate = p.layer%s.value()" %i
    if gate == True :
      layerList.append ( layers[i] )
  
#here it will create a node tree if some layers have been selected
  if len(layerList) > 0:
    buildTree(layerList, prefs)
  else:
    return
  
    
def selectAll():
  layers = shuffleChannels(n).returnLayers()
  for i in range (len(layers)):
    exec "(p.layer%s.setValue(True))" %i
    
def deselectAll():
  layers = shuffleChannels(n).returnLayers()
  for i in range (len(layers)):
    exec "(p.layer%s.setValue(False))" %i

  
def buildTree(layers, prefs):
  
  nukePrefs = nuke.toNode('preferences')
  defGoofyFootValue = nukePrefs['goofy_foot'].value()
  nukePrefs['goofy_foot'].setValue( 0 )
  selNodeXPos = n.xpos()
  selNodeYPos = n.ypos()
  
  n['selected'].setValue(False)
  
  shuffDot0 = nuke.createNode( 'Dot', 'selected False', False)
  shuffDot0['xpos'].setValue(selNodeXPos +  200)
  shuffDot0YPos = int( selNodeYPos +  100 )
  shuffDot0['ypos'].setValue( shuffDot0YPos )
  shuffDot0.setInput(0, n)

#creation of nodes
  for i in range(len(layers)):
    #dots
    newXPos = (prefs['separation']*(i+1))+shuffDot0['xpos'].value()
    exec "shuffDot%s = nuke.createNode('Dot', 'name shuffDot%s xpos %s ypos %s', inpanel=False)" %( i+1, i+1, newXPos , shuffDot0YPos )
    lastDot = i
  exec "shuffDot%s['selected'].setValue(False)" %( len(layers) )
    

    ##shuffles
  for i in range(len(layers)):
    newXPos = (prefs['separation']*(i+1))+shuffDot0['xpos'].value()
    shuf = nuke.createNode ( 'Shuffle', 'name %s in %s selected False xpos %s ypos %s' %( layers[i], layers[i], newXPos-34, shuffDot0YPos+50), False )
    exec "shuf.setInput(0, shuffDot%s)" %(i+1)
    if i == 0:
      shuf['xpos'].setValue(newXPos-34)
      shuf['ypos'].setValue(shuffDot0YPos+50)
    ##color
    if prefs['shuffLayersColor'] != nuke.toNode('preferences')['NodeColour05Color'].value():
      shuf['tile_color'].setValue(prefs['shuffLayersColor'])
    ##label
    if prefs['noShuffLabel'] == True:
      shuf['label'].setValue('') 
    
    #removes
    if prefs['remove'] == True:
      rem = nuke.createNode('Remove', 'operation keep channels rgba selected False xpos %s ypos %s' %( newXPos-34, shuffDot0YPos+88 ), False )
      rem.setInput(0, shuf)
      
    #grades
    if prefs['grade'] == True:
      grad = nuke.createNode('Grade', 'xpos %s ypos %s' %( newXPos-34, shuffDot0YPos+300 ), False)
      
    #merges
    if prefs['merge'] == True:
      if i == 0:
        dotMerge = nuke.createNode('Dot', 'xpos %s ypos %s selected False' %( newXPos, shuffDot0YPos+504 ), False)
      else:
        exec "merge%s = nuke.createNode('Merge', 'operation %s xpos %s ypos %s', False)" %( i, prefs['operation'], newXPos-34, shuffDot0YPos+500 )
        exec "nukescripts.swapAB(merge%s)" %i
        if i == 1 :
          exec "merge%s.setInput (0, dotMerge)" %i
        else:
          exec "merge%s.setInput (0, merge%s)" %( i, i-1)
      
  #copyAlpha
  if prefs['copyAlpha'] == True:
    copyDot = nuke.createNode('Dot', 'xpos %s ypos %s' % ( newXPos+prefs['separation'], shuffDot0YPos ), False)
    exec "copyDot.setInput(0, shuffDot%s)" %(len(layers))
    copyNode = nuke.createNode('Copy', 'xpos %s ypos %s' %( newXPos+prefs['separation']-34, shuffDot0YPos+494 ), False)
    try:
      exec "copyNode.setInput(0, merge%s)" %(len(layers)-1)
    except:
      pass
    copyNode.setInput(1, copyDot)

  #premult
  if prefs['unPremult'] == True:
    unpr = nuke.createNode('Unpremult', 'selected False xpos %s ypos %s channels all' %(shuffDot0.xpos()+50, shuffDot0YPos-10), False)
    unpr.setInput(0, shuffDot0)
    prem = nuke.createNode('Premult', 'selected False xpos %s ypos %s channels all' %(newXPos+prefs['separation']-34, shuffDot0YPos+550), False)
    prem['selected'].setValue(False)
    if prefs['copyAlpha'] == True:
      prem.setInput(0, copyNode)
    elif prefs['merge'] == True:
      exec "prem.setInput(0, merge%s)" %str(len(layers)-1)
      exec "prem['xpos'].setValue(merge%s.xpos())" %str(len(layers)-1)
    elif prefs['grade'] == True:
      prem.setInput(0, grad)
      prem['xpos'].setValue(grad.xpos())
    elif prefs['remove'] == True:
      prem.setInput(0, rem)
      prem['xpos'].setValue(rem.xpos())
    else:
      prem.setInput(0, shuf)
      prem['xpos'].setValue(shuf.xpos())
    shuffDot1.setInput(0, unpr)
  
  #backDrop
  width = 0
  height = 0
  if prefs['bdrop'] == True:
    width = ( prefs['separation'] * (len(layers)+1) )
    if prefs['unPremult'] == True:
      height = 750
    elif prefs['copyAlpha'] == True:
      height = 650
    elif prefs['grade'] == True:
      height = 500
    elif prefs['merge'] == True:
      height = 600
    elif prefs['remove'] == True:
      height = 300
    else:
      height = 250
    if prefs['copyAlpha'] == True:
      width = width + prefs['separation']
      
    
    bd = nuke.createNode('BackdropNode', 'tile_color %s' %( prefs['bdropColor'] ) , False)
    bd['xpos'].setValue( shuffDot0.xpos() - 100)
    bd['ypos'].setValue( shuffDot0.ypos() - 100)
    bd['bdwidth'].setValue( width )
    bd['bdheight'].setValue( height )
    #print 'width = %s , height = %s' %(width, height)
    
##resets prefs to user defined state
  nukePrefs = nuke.toNode('preferences')
  nukePrefs['goofy_foot'].setValue( defGoofyFootValue )
    
    

def readPrefsFile(p):  #reads the preferences file and sets the values on the panel knobs
  try:
    prefsFileR = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'r')
  except:
    prefsFileW = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'w')
    prefsFileW.write ("['prefs', {'none':['none'], 'all': ['all']}]")
    prefsFileW.close()
    return
  prefs = eval(prefsFileR.read())[0]
  for keys in prefs:
    if keys != 'operation':
      exec "p.%s.setValue(%s)" %( keys, prefs[keys] )
    else:
      exec  "p.%s.setValue('%s')" %( keys, prefs[keys] )
      
def writePrefsFile(p, prefs):
  prefsFile = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'r')
  prefsFileContent = eval(prefsFile.read())
  prefsFile.close()
  prefsFile = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'w')
  prefsFile.write ("[%s, %s]" %(prefs, prefsFileContent[1]))
  


  
def savePreset():
  presetName = nuke.getInput('name of preset')
  if presetName == None or '':
    return
  presetLayers = []
  layers = shuffleChannels(n).returnLayers()
  for i in range (len(layers)):
    exec ("selected = p.layer%s.value()") %i
    if selected == True:
      presetLayers.append (layers[i])
  preset = {}
  preset [presetName] = presetLayers
#  print 'and the preset is:  %s' %preset

  prefsFileR = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'r')
  prefsFileContent = eval(prefsFileR.read())
  presetsInFile = prefsFileContent[1]
  presetsInFile [presetName] = presetLayers
  prefsFileW = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'w')
  prefsFileW.write ("[%s, %s]" %(prefsFileContent[0], presetsInFile))
  prefsFileW.close()
  refreshPresetsMenu()
  p.presets.setValue( presetName )

def deletePreset():
  if p.presets.value() not in ['all', 'none']:
    prefsFileR = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'r')
    prefsFileContent = eval(prefsFileR.read())
    presetsInFile = prefsFileContent[1]
    if p.presets.value() not in ['all', 'none']:
      del presetsInFile [ p.presets.value() ]
      prefsFileW = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'w')
      prefsFileW.write ("[%s, %s]" %(prefsFileContent[0], presetsInFile))
    prefsFileW.close()
  
    p.presets.setValue('none')
      
    refreshPresetsMenu()
    


def refreshPresetsMenu():
  prefsFileR = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'r')
  prefsFileContent = eval(prefsFileR.read())
  presetsInFile = prefsFileContent[1]
  list = sorted(presetsInFile.keys())
  list.remove ('all')
  list.remove('none')
  list.insert (0, 'all')
  list.insert (0, 'none')
  p.presets.setValues( list )
  
def updateLayersPreset ():
  prefsFileR = open('%s/.nuke/shufflePanelPrefs.txt' %os.getenv('HOME'), 'r')
  prefsFileContent = eval(prefsFileR.read())
  presetsInFile = prefsFileContent[1]
  
  deselectAll()
  
  chosenPreset = p.presets.value()

  layersInPreset = presetsInFile [ p.presets.value() ]

  layers = shuffleChannels(n).returnLayers()
  
  if p.presets.value() not in ['all', 'none']:
    for i in range (len(layers)):
      #exec "(p.layer%s.setValue(True))" %i
      exec "lay =  (p.layer%s.label())" %i
      if lay in layersInPreset :
        exec "(p.layer%s.setValue(True))" %i
  elif p.presets.value() == 'all':
    selectAll()
  else:
    deselectAll()






