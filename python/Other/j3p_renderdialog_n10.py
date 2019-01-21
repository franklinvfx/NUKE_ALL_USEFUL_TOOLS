# Copyright (c) 2010 The Foundry Visionmongers Ltd.  All Rights Reserved.
# Modified by J3P June 18, 2011
# Updated to v2.0 December 28, 2011
# jep@j3pnyc.com

from __future__ import with_statement
import nuke
import nukescripts
import nukescripts.flipbooking as flipbooking
from nukescripts import pyAppUtils
import os
import string
import subprocess
import uuid
import re
#import traceback


##############################################################################
# Skip exisitng
##############################################################################

def skippy():
	n=nuke.thisNode()
	currentFrame = nuke.filename(n,nuke.REPLACE)
	tmpFrame = currentFrame + ".tmp"
	try:
		n['autocrop'].value()
	except:
		autoCropOn=0
	else:
		if n['autocrop'].value() is True:
			autoCropOn=1
			n['autocrop'].setValue(False)
		else:
			autoCropOn=0
	if os.path.exists(currentFrame) or os.path.exists(tmpFrame):
		#print "Frame exists: %s\t skipping..." %currentFrame
		nuke.cancel()
		if autoCropOn == 1:
			n['autocrop'].setValue(True)

		
	else:
		if autoCropOn == 1:
			n['autocrop'].setValue(True)
		else:
			pass
		

##############################################################################
# Make Output
##############################################################################

def make_out(nodes):
	outNodes=[]
	for w in nodes:
		if w.Class() != 'Root':
	  		outNodes.append(w)
	  	else:
	  		outNodes=nuke.allNodes('Write')

  	for n in outNodes:
  		print 'Verifying output path for %s...' %n.name()
		out_dir=os.path.dirname(nuke.filename(n))	
		if os.path.isdir(out_dir):
			print "%s output path exists - skipping..." %n.name()
		else:
			os.umask(0)
			os.makedirs(out_dir)
			print "Creating output directory for %s: %s" %(n.name(),out_dir)


##############################################################################
# Dialogs
##############################################################################

class DialogState:
  def __init__(self):
    self._state = {}

  def get(self, knob, defaultValue = None):
    """Return the given knob's stored last state value.
    If none exists, defaultValue is returned.
    Values are stored in a dict referenced by knob name, so names must be unique!"""
    return self.getValue(knob.name(), defaultValue)

  def save(self, knob):
    """Store the knob's current value as the 'last state' for the next time the dialog is opened.
    Values are stored in a dict referenced by knob name, so names must be unique!"""
    self.saveValue(knob.name(), knob.value())

  def setKnob(self, knob, defaultValue = None):
    """Convenience method for setting a value straight on a knob."""
    knob.setValue(self.get(knob, defaultValue))
  def saveValue(self, id, value):
    """Stores the value with the given id."""
    self._state[id] = value
  def getValue(self, id, defaultValue = None):
    """Recalls the value. If it was not set before, it will return the defaultValue."""
    return self._state.get(id, defaultValue)

_gRenderDialogState = DialogState()
_gFlipbookDialogState = DialogState()

class ExecuteDialog(nukescripts.PythonPanel):
  def _titleString(self):
    return "Execute"

  def _idString(self):
    return "uk.co.thefoundry.ExecuteDialog"

  def _addPreKnobs(self):
    """Add knobs that must appear before the render knobs."""
    return

  def _addPostKnobs(self):
    """Add knobs that must appear after the render knobs."""
    return

  def _getDefaultViews(self):
    oc = nuke.OutputContext()
    allViews = [oc.viewname(i) for i in xrange(1, oc.viewcount())]
    return " ".join(allViews)

  def _addViewKnob(self):
    """Add knobs for view selection."""
    oc = nuke.OutputContext()
    if (oc.viewcount() > 2):
      self._viewSelection = nuke.MultiView_Knob("multi_view", "Views")
      self._viewSelection.fromScript(self._state.get(self._viewSelection, self._getDefaultViews()))
      self.addKnob(self._viewSelection)
      self._viewSelection.clearFlag(nuke.NO_MULTIVIEW)

  def addKnob(self, knob):
    """Add the knob and make sure it cannot be animated."""
    knob.setFlag(nuke.NO_ANIMATION | nuke.NO_MULTIVIEW)
    super(ExecuteDialog, self).addKnob(knob)

  def __init__(self, dialogState, groupContext, nodeSelection = [], exceptOnError = True):
    self._state = dialogState
    self._nodeSelection = nodeSelection
    self._exceptOnError = exceptOnError

    nukescripts.PythonPanel.__init__(self, self._titleString(), self._idString(), False)

    self._viewers = {}
    for n in nuke.allNodes("Viewer", groupContext):
      self._viewers[n.name()] = n
    self._specialRanges = ["input", "global", "custom"]

    self._addPreKnobs()

    # Frame range knobs
    self._rangeEnum = nuke.Enumeration_Knob( "frame_range", "Frame range", self._specialRanges + self._viewers.keys() )
    self._state.setKnob(self._rangeEnum, "input")
    self.addKnob( self._rangeEnum )
    self._frameRange = nuke.String_Knob( "frame_range_string", "")
    self._frameRange.clearFlag(nuke.STARTLINE)
    if self._rangeEnum.value() == "custom":
      self._state.setKnob(self._frameRange, str(nuke.root().frameRange()))
    else:
      self._setFrameRangeFromSource(self._rangeEnum.value())

    self.addKnob(self._frameRange)

    # Proxy
    self._useProxy = nuke.Boolean_Knob("use_proxy", "Use proxy")
    self._useProxy.setFlag(nuke.STARTLINE)
    self._state.setKnob(self._useProxy, nuke.root().proxy())
    self.addKnob(self._useProxy)

    self._addPostKnobs()

    self._continueOnError = nuke.Boolean_Knob("continue", "Continue on error")
    self._state.setKnob(self._continueOnError, True)
    self._continueOnError.setFlag(nuke.STARTLINE)
    self.addKnob(self._continueOnError)
    
    self._addViewKnob()

  def knobChanged( self, knob ):
    self._state.save(knob)
    if (knob == self._frameRange):
      self._rangeEnum.setValue("custom")
      self._state.save(self._rangeEnum)
    if (knob == self._rangeEnum):
      self._setFrameRangeFromSource(knob.value())
      self._state.save(self._frameRange)

  def _setFrameRangeFromSource(self, source):
    if (source == "input"):
      try:
        activeInput = nuke.activeViewer().activeInput()
        self._frameRange.setValue(str(nuke.activeViewer().node().input(activeInput).frameRange()))
      except:
        self._frameRange.setValue(str(nuke.root().frameRange()))
    elif (source == "global"):
      self._frameRange.setValue(str(nuke.root().frameRange()))
    elif (source == "custom"):
      pass
    else:
      self._frameRangeFromViewer(source);

  def _frameRangeFromViewer( self, viewer ):
    """"Set the framerange knob to have the framerange from the given viewer."""
    viewerRange = str(self._viewers[viewer].knob("frame_range").value())
    if viewerRange == "":
      viewerRange = str(self._viewers[viewer].playbackRange())
    self._frameRange.setValue(viewerRange)

  def _selectedViews(self):
    try:
      return self._viewSelection.value().split()
    except AttributeError:
      # If we didn't add the view selection knob, there should be just the one view.
      return [nuke.OutputContext().viewname(1)]

  def addToPane(self):
    nukescripts.PythonPanel.addToPane(self, pane = nuke.thisPane())

  def run(self):
    frame_ranges = nuke.FrameRanges(self._frameRange.value().split(','))
    views = self._selectedViews()
    rootProxyMode = nuke.root().proxy()
    try:
      nuke.Undo().disable()
      nuke.root().setProxy(self._useProxy.value())
      nuke.executeMultiple(self._nodeSelection, frame_ranges, views, continueOnError = self._continueOnError.value())
    except RuntimeError, e:
      if self._exceptOnError or e.args[0][0:9] != "Cancelled":   # TO DO: change this to an exception type
        raise
    finally:
      nuke.root().setProxy(rootProxyMode)
      nuke.Undo().enable()

class RenderDialog(ExecuteDialog):
  def _titleString(self):
    return "Render"

  def _idString(self):
    return "uk.co.thefoundry.RenderDialog"

  def __init__(self, dialogState, groupContext, nodeSelection = [], exceptOnError = True):
    ExecuteDialog.__init__(self, dialogState, groupContext, nodeSelection, exceptOnError)

  def _addPostKnobs(self):
    # Background render stuff
    self._bgRender = nuke.Boolean_Knob("bg_render", "Render in background")
    self._state.setKnob(self._bgRender, False)
    self._bgRender.setFlag(nuke.STARTLINE)
    self.addKnob(self._bgRender)
    self._numThreads = nuke.Int_Knob("num_threads", "Thread limit")
    self._numThreads.setVisible(self._bgRender.value())
    self._state.setKnob(self._numThreads, max(nuke.NUM_CPUS / 2, 1))
    self.addKnob(self._numThreads)
    self._maxMem = nuke.String_Knob("max_memory", "Memory limit")
    self._state.setKnob(self._maxMem, str(max(nuke.memory("max_usage") / 2097152, 16)) + "M")
    self._maxMem.setVisible(self._bgRender.value())
    self.addKnob(self._maxMem)

## Skip existing boolean    
    self._skipExisting = nuke.Boolean_Knob("skip_existing", "Skip existing frames")
    self._state.setKnob(self._skipExisting, False)
    self._skipExisting.setFlag(nuke.STARTLINE)
    self.addKnob(self._skipExisting)
    


  def skipExisting(self):
    return self._skipExisting.value()
    

  def _getBackgroundLimits(self):
    return {
      "maxThreads": self._numThreads.value(), 
      "maxCache": self._maxMem.value() }

  def knobChanged( self, knob ):
    ExecuteDialog.knobChanged(self, knob)

    if (knob == self._bgRender):
      self._numThreads.setVisible(self._bgRender.value())
      self._maxMem.setVisible(self._bgRender.value())

## Hide skip existing if BG render is selected
      if self._bgRender.value() is True:
      	self._skipExisting.setVisible(False)
      else:
      	self._skipExisting.setVisible(True)
      	
      
  def isBackgrounded(self):
    """Return whether the background rendering option is enabled."""
    return self._bgRender.value()
  
  def run(self):
    frame_ranges = nuke.FrameRanges(self._frameRange.value().split(','))
    views = self._selectedViews()
    rootProxyMode = nuke.root().proxy()
    try:
      nuke.Undo().disable()
      nuke.root().setProxy(self._useProxy.value())
      
      if (self.isBackgrounded()):
      	print frame_ranges
      	make_out(self._nodeSelection)
        nuke.executeBackgroundNuke(nuke.EXE_PATH, self._nodeSelection, frame_ranges, views, self._getBackgroundLimits(), continueOnError = self._continueOnError.value())
      else:     
        if(self.skipExisting()):
      	  nuke.addBeforeFrameRender(skippy, nodeClass='Write')
        else:
          nuke.removeBeforeFrameRender(skippy, nodeClass='Write')
        make_out(self._nodeSelection)
        nuke.executeMultiple(self._nodeSelection, frame_ranges, views, continueOnError = self._continueOnError.value())
    except RuntimeError, e:
      if self._exceptOnError or e.args[0][0:9] != "Cancelled":   # TO DO: change this to an exception type
        raise
    finally:
      nuke.root().setProxy(rootProxyMode)
      nuke.Undo().enable()

class FlipbookDialog( RenderDialog ):
  def _titleString( self ):
    return "Flipbook"

  def _idString( self ):
    return "uk.co.thefoundry.FlipbookDialog"

  def __init__(self, dialogState, groupContext, node, takeNodeSettings):
    # Init attributes
    self._node = node
    self._takeNodeSettings = takeNodeSettings

    # init super
    RenderDialog.__init__(self, dialogState, groupContext)

    # Override the initial frame range value
    self._state.setKnob(self._rangeEnum, "input")
    self._setFrameRangeFromSource(self._rangeEnum.value())

    if self._takeNodeSettings:
      self._viewerForSettings.setValue(node.name())
      self.knobChanged(self._viewerForSettings)

  def _addPreKnobs( self ):
    self._flipbookEnum = nuke.Enumeration_Knob( "flipbook", "Flipbook", flipbooking.gFlipbookFactory.getNames() )
    self._state.setKnob(self._flipbookEnum, "FrameCycler")
    self.addKnob( self._flipbookEnum )
    self._viewerForSettings = nuke.Enumeration_Knob("viewer_settings", "Take settings from", ["-"] + self._viewers.keys())
    if not self._takeNodeSettings:
      self._viewerForSettings.setValue("-")
    self.addKnob(self._viewerForSettings)

    self._defaultValues = nuke.PyScript_Knob("default", "Defaults")
    self.addKnob(self._defaultValues)

    # Region of Interest knobs
    self._useRoi = nuke.Boolean_Knob("use_roi", "Enable ROI")
    self._useRoi.setFlag(nuke.STARTLINE)
    self._state.setKnob(self._useRoi, False)
    self.addKnob(self._useRoi)
    self._roi = nuke.BBox_Knob("roi", "Region of Interest")
    self._state.setKnob(self._roi, (0, 0, 0, 0))
    self.addKnob(self._roi)
    self._roi.setVisible(self._useRoi.value())

    # Channel knobs
    self._channels = nuke.Channel_Knob( "channels_knob", "Channels")
    if self._node.Class() == "Write":
      self._channels.setValue(self._node.knob("channels").value())
    else:
      self._state.setKnob(self._channels, "rgba")
    self._channels.setFlag(nuke.STARTLINE | nuke.NO_CHECKMARKS)
    self.addKnob( self._channels )

  def _addPostKnobs( self ):
    super(FlipbookDialog, self)._addPostKnobs()
    # Misc knobs
    self._cleanup = nuke.Boolean_Knob("cleanup", "Delete existing temporary files")
    self._cleanup.setFlag(nuke.STARTLINE)
    self._state.setKnob(self._cleanup, True)
    self.addKnob(self._cleanup)

    # LUT knobs
    self._luts = nuke.Enumeration_Knob("lut", "LUT", nuke.ViewerProcess.registeredNames())
    if self._takeNodeSettings:
      self._state.setKnob(self._luts, self._lutFromViewer(self._viewerForSettings.value()))
    else:
      self._state.setKnob(self._luts, self._lutFromViewer())
    self.addKnob(self._luts)

    self._burnInLUT = nuke.Boolean_Knob("burnin", "Burn in the LUT")
    self._state.setKnob(self._burnInLUT, False)
    self.addKnob(self._burnInLUT)
    
    # Audio knobs
    audioList = []
    audioList.append( "None" )
    for node in nuke.allNodes("AudioRead"):
      audioList.append( node.name() )
    self._audioSource = nuke.Enumeration_Knob( "audio", "Audio", audioList )
    self.addKnob( self._audioSource )
  

  def _getDefaultViews(self):
    return nuke.activeViewer().view()

  def _addViewKnob(self):
    oc = nuke.OutputContext()
    self._views = [oc.viewname(i) for i in xrange(1, oc.viewcount())]
    if (oc.viewcount() > 2):
      supportedViews = self._selectedFlipbook().capabilities()["maximumViews"]
      if (int(supportedViews) > 1):
        self._viewSelection = nuke.MultiView_Knob("views", "Views")
      else:
        self._viewSelection = nuke.OneView_Knob("views", "View", self._views)
      activeView = nuke.activeViewer().view()
      if activeView == "":
        activeView = self._views[0]
      self._state.setKnob(self._viewSelection, activeView)
      self.addKnob(self._viewSelection)
      self._viewSelection.clearFlag(nuke.NO_MULTIVIEW)

  def _selectedFlipbook(self):
    return flipbooking.gFlipbookFactory.getApplication(self._flipbookEnum.value())

  def _lutFromViewer(self, viewerName = ""):
    try:
      if viewerName == "":
        return nuke.ViewerProcess.node().knob("current").value()
      else:
        return nuke.ViewerProcess.node(viewer=viewerName).knob("current").value()
    except AttributeError:
      return "None"

  def _isViewerSettingKnob(self, knob):
    return knob == self._useRoi or knob == self._roi or knob == self._channels or knob == self._useProxy or knob == self._frameRange or knob == self._rangeEnum or knob == self._luts

  def _setKnobAndStore(self, knob, val):
    knob.setValue(val)
    self._state.save(knob)

  def knobChanged(self, knob):
    RenderDialog.knobChanged(self, knob)
    if knob == self._defaultValues:
      self._setKnobAndStore(self._useRoi, False)
      self._setKnobAndStore(self._roi, (0, 0, 0, 0))
      self._roi.setVisible(False)
      self._maxMem.setVisible(False)
      self._numThreads.setVisible(False)
      self._setKnobAndStore(self._viewerForSettings, "-")
      self._setKnobAndStore(self._channels, "rgba")
      self._setKnobAndStore(self._useProxy, False)
      self._setKnobAndStore(self._frameRange, str(nuke.root().frameRange()))
      self._setKnobAndStore(self._rangeEnum, "input")
      self._setKnobAndStore(self._continueOnError, True)
      self._setKnobAndStore(self._bgRender, False)
      self._setKnobAndStore(self._luts, "sRGB")
      self._setKnobAndStore(self._burnInLUT, False)
      self._setKnobAndStore(self._cleanup, True)
      self._setKnobAndStore(self._maxMem, str(max(nuke.memory("max_usage") / 2097152, 16)) + "M")
      self._setKnobAndStore(self._numThreads, max(nuke.NUM_CPUS / 2, 1))
    elif (knob == self._viewerForSettings):
      if self._viewerForSettings.value() != "-":
        viewer = self._viewers[self._viewerForSettings.value()]
        self._setKnobAndStore(self._useRoi, viewer.roiEnabled())
        roi = viewer.roi()
        if roi != None:
          self._roi.fromDict(roi)
          self._state.save(self._roi)
        self._channels.fromScript(viewer.knob("channels").toScript())
        self._state.save(self._channels)
        self._setKnobAndStore(self._useProxy, nuke.root().proxy())
        self._frameRangeFromViewer(viewer.name())
        self._state.save(self._frameRange)
        self._setKnobAndStore(self._rangeEnum, viewer.name())
        self._roi.setVisible(self._useRoi.value())
        self._setKnobAndStore(self._luts, self._lutFromViewer(viewer.name()))
    elif (knob == self._useRoi):
      self._roi.setVisible(self._useRoi.value())
    elif self._isViewerSettingKnob(knob):
      self._viewerForSettings.setValue("-")
      self._state.save(self._viewerForSettings)
    elif knob == self._luts:
      self._burnInLUT.setEnabled(self._luts.value() != "None")

  def _deleteTemporaries(self):
    """Delete all the files in the range to be rendered."""
    temporariesPath = self._getIntermediatePath()
    temporariesPath = temporariesPath .replace("%V", "%s")
    for r in nuke.FrameRanges(self._frameRange.value().split(',')):
      deleteRange = xrange(r.minFrame(), r.maxFrame() + 1)

      for v in self._selectedViews():
        for i in deleteRange:
          if len(self._selectedViews()) > 1: 
            f = temporariesPath % (i, v,)
          else:
            f = temporariesPath % i
          
          if os.access(f, os.F_OK):
            os.remove(f)

  def _getIntermediateFileType(self):
    return _gFlipbookDialogState.getValue('intermediateFormat', 'exr')

  def _getIntermediatePath(self):
    """Get the path for the temporary files. May be filled in using printf syntax."""
    flipbooktmp=""
    if flipbooktmp == "":
      try:
        flipbooktmp = self._selectedFlipbook().cacheDir()
      except:
        try:
          flipbooktmp = os.environ["NUKE_DISK_CACHE"]
        except:
          flipbooktmp = nuke.value("preferences.DiskCachePath")

    if len(self._selectedViews()) > 1:
      flipbookFileNameTemp = "nuke_tmp_flip.%04d.%V." + self._getIntermediateFileType()
    else:
      flipbookFileNameTemp = "nuke_tmp_flip.%04d." + self._getIntermediateFileType()
    flipbooktmpdir = os.path.join(flipbooktmp, "flipbook")
    if not os.path.exists(flipbooktmpdir):
      os.mkdir(flipbooktmpdir)

    if not os.path.isdir(flipbooktmpdir):
      raise RuntimeError("%s already exists and is not a directory, please delete before flipbooking again" % flipbooktmpdir)
    flipbooktmp = os.path.join(flipbooktmpdir, flipbookFileNameTemp)

    if nuke.env['WIN32']:
      flipbooktmp = re.sub(r"\\", "/", str(flipbooktmp))
    return flipbooktmp

  def _requireIntermediateNode(self):
    if self._node.Class() == "Read" or self._node.Class() == "Write":
      flipbookToRun = flipbooking.gFlipbookFactory.getApplication(self._flipbookEnum.value())
      flipbookCapabilities = flipbookToRun.capabilities()

      # Check if we can read it in directly..
      filePath = nuke.filename(self._node)
      # There might be a prefix that overrides the extension, if so, this will
      # confuse the flipbook probably, so just create a render.
      if ':' in filePath:
        readerPrefix = filePath.split(':')[0]
        if len(readerPrefix) > 1: # 1 is a drive letter
          return True
      fileExtension = os.path.splitext(filePath)[1].lower()[1:]
      flipbookSupportsFileType = fileExtension in flipbookCapabilities.get("fileTypes", [])
      if not flipbookSupportsFileType:
        return True

      # Not all flipbooks can handle weird channels
      flipbookSupportsArbitraryChannels = flipbookCapabilities.get("arbitraryChannels", False)
      if self._channels.value() not in set(["rgb", "rgba", "alpha"]) and not flipbookSupportsArbitraryChannels:
        return True
      channelKnob = self._node.knob("channels")
      if channelKnob != None and channelKnob.value() != self._channels.value():
        return True

      if self._burnInLUT.value() and self._burnInLUT.enabled():
        return True

      return False
    else:
      return True

  def _createIntermediateNode(self):
    """Create a write node to render out the current node so that output may be used for flipbooking."""
    flipbooktmp = self._getIntermediatePath()

    fieldname = "file"
    if self._useProxy.value():
      fieldname = "proxy"

    fixup = nuke.createNode("Group", "tile_color 0xff000000", inpanel = False)
    with fixup:
      fixup.setName("Flipbook")
      inputNode = nuke.createNode("Input", inpanel = False)
      shuffle = nuke.createNode("Shuffle", inpanel = False)
      shuffle.knob("in").setValue(self._channels.value())
      write = nuke.createNode("Write", fieldname+" {"+flipbooktmp+"}", inpanel = False)
      write.knob('file_type').setValue(self._getIntermediateFileType())
      write.knob('views').fromScript(" ".join(self._selectedViews()))

      if self._getIntermediateFileType() == "exr": 
        write.knob('compression').setValue("B44")
      if self._burnInLUT.value():
        lut = self._getLUT()
        if lut != "None":
          write.knob('colorspace').setValue(lut)
      outputNode = nuke.createNode("Output", inpanel = False)
    #If called on a Viewer connect fixup node to the one immediately above if exists.
    if self._node.Class() == "Viewer":
      fixup.setInput(0, self._node.input(int(nuke.knob(self._node.fullName()+".input_number"))))
    else:
      fixup.setInput(0, self._node)

    try:
      # Throws exception on render failure
      if (self.isBackgrounded()):
        nuke.executeBackgroundNuke(nuke.EXE_PATH, [write], 
          nuke.FrameRanges(self._frameRange.value().split(',')), self._selectedViews(), 
          self._getBackgroundLimits(), self._continueOnError.value(),
          self._flipbookEnum.value(), self._getOptions(write))
      else:
        nuke.executeMultiple((write,), 
            nuke.FrameRanges(self._frameRange.value().split(',')), self._selectedViews(), 
            self._continueOnError.value())
    except RuntimeError, msg:
      if msg.args[0][0:9] == "Cancelled":
        splitMsg = string.split(msg.args[0])
      
        msg = """Render did not complete, do you want to show the completed range?
Frame range %s contains %s frames but only %s finished.""" % (self._frameRange.value(), splitMsg[3], splitMsg[1])
        if nuke.ask(msg) == False:
          nuke.delete(fixup)
          fixup = None
      else:
        nuke.delete(fixup)
        fixup = None
        nuke.message("Flipbook render failed:\n%s" % (msg.args[0],))
#    except BaseException, be:
#      print be.__class__.__name__
#      traceback.print_exc()
    finally:
      return fixup

  def _getLUT(self):
    return self._luts.value()
    
  def _getAudio(self):
    nukeNode = nuke.toNode( self._audioSource.value() )
    ret = ""
    if nukeNode != None:
      ret = nukeNode["file"].value()
    return ret

  def _getOptions(self, nodeToFlipbook):
    options = { 
    }

    try:
      options['pixelAspect'] = float(nuke.value(nodeToFlipbook.name()+".pixel_aspect"))
    except:
      pass

    try:
      f = nodeToFlipbook.format()
      options['dimensions'] = { 'width' : f.width(), 'height' : f.height() }
    except:
      pass

    # LUT
    if not self._burnInLUT.value():
      inputColourspace = "linear"
      outputColourspace = "linear"
      # Check if we have a different than linear input
      if self._node.Class() == "Read" or self._node.Class() == "Write":
        lut = self._node.knob("colorspace").value()
        # Might be in the format of "default (foo)", if so, get at "foo".
        if lut[:7] == "default":
          lut = lut[9:-1] 
        inputColourspace = lut

      # Check our output
      lut = self._getLUT()
      if lut != "None":
        outputColourspace = lut

      if inputColourspace == outputColourspace:
        options["lut"] = inputColourspace
      else:
        options["lut"] = inputColourspace + "-" + outputColourspace
    # AUDIO
    audioTrack = self._getAudio()
    if audioTrack != "":
      options["audio"] = audioTrack
    
    # ROI
    if self._useRoi.value():
      roi = self._roi.toDict()
      if (roi["r"] - roi["x"] > 0) and (roi["t"] - roi["y"] > 0):
        options["roi"] = bboxToTopLeft(int(nuke.value(nodeToFlipbook.name()+".actual_format.height")), roi)

    return options

  def run(self):
    flipbookToRun = flipbooking.gFlipbookFactory.getApplication(self._flipbookEnum.value())
    if (flipbookToRun):
      if not os.access(flipbookToRun.path(), os.X_OK):
        raise RuntimeError("%s cannot be executed (%s)." % (flipbookToRun.name(), flipbookToRun.path(),) )

      nodeToFlipbook = None
      rootProxyMode = nuke.root().proxy()
      try:
        # Need this to prevent Bug 5295
        nuke.Undo().disable()
        nuke.root().setProxy(self._useProxy.value())

        if self._cleanup.value():
          self._deleteTemporaries()
        calledOnNode = self._node
        if self._node.Class() == "Viewer":
          self._node = self._node.input(int(self._node.knob("input_number").value()))

        runFlipbook = False
        # In many cases we need to create a temporary node and render that.
        if not self._requireIntermediateNode():
          nodeToFlipbook = self._node
          runFlipbook = True
        else:
          nodeToFlipbook = self._createIntermediateNode()
          runFlipbook = not self._bgRender.value()

        if nodeToFlipbook and runFlipbook:
          filename = nuke.filename(nodeToFlipbook)
          if filename is None or filename == "":
            raise RuntimeError("Cannot run a flipbook on '%s', expected to find a filename and there was none." % (nodeToFlipbook.fullName(),))
          flipbookToRun.run(filename, 
              nuke.FrameRanges(self._frameRange.value().split(',')), 
              self._selectedViews(), self._getOptions(nodeToFlipbook))
      finally:
        if self._node != nodeToFlipbook:
          nuke.delete(nodeToFlipbook)
        nuke.root().setProxy(rootProxyMode)
        nuke.Undo().enable()
    else:
        raise RuntimeError("No flipbook called " + self._flipbookEnum.value() + " found. Was it deregistered while the dialog was open?")

def showExecuteDialog(nodesToExecute, exceptOnError = True): 
  """Present a dialog that executes the given list of nodes."""
  groupContext = nuke.root()
  d = ExecuteDialog(_gRenderDialogState, groupContext, nodesToExecute, exceptOnError)
  if d.showModalDialog() == True:
    d.run()

def showRenderDialog(nodesToRender, exceptOnError = True): 
  """Present a dialog that renders the given list of nodes."""
  groupContext = nuke.root()
  myNodesToRender=[]
  for n in nodesToRender:
  	if n.Class()=='Write':
  		myNodesToRender.append(n)
  d = RenderDialog(_gRenderDialogState, groupContext, myNodesToRender, exceptOnError)
  if d.showModalDialog() == True:
    d.run()

def showFlipbookDialog(node, takeNodeSettings = False):
  """Present a dialog that flipbooks the given node."""
  if node is None:
    raise RuntimeError("Can't launch flipbook, require a node.");
  if node.Class() == "Viewer" and node.inputs() == 0:   
    raise RuntimeError("Can't launch flipbook, there is nothing connected to the viewed input.");
    
  groupContext = nuke.root()

  e = FlipbookDialog(_gFlipbookDialogState, groupContext, node, takeNodeSettings)
  if (e.showModalDialog() == True):
    e.run()

def showFlipbookDialogForSelected():
  """Present a dialog that flipbooks the currently selected node."""
  try: 
    showFlipbookDialog(nuke.selectedNode())
  except ValueError, ve:
    raise RuntimeError("Can't launch flipbook, %s." % (ve.args[0]))

def bboxToTopLeft(height, roi):
  """Convert the roi passed from a origin at the bottom left to the top left.
     Also replaces the r and t keys with w and h keys.
     @param height: the height used to determine the top.
     @param roi: the roi with a bottom left origin, must have x, y, r & t keys.
     @result dict with x, y, w & h keys"""
  topLeftRoi = { 
      "x": roi["x"], 
      "y": height - roi["y"] - (roi["t"] - roi["y"]), 
      "w": roi["r"] - roi["x"], 
      "h": roi["t"] - roi["y"] }
  return topLeftRoi

def setRenderDialogDefaultOption(name, value):
  """ Set a particular option to the given value. The type of the value differs per option, giving the wrong value may result in exceptions. The options are read every time the dialog is opened, though not every knob in the dialog has it's value stored."""
  _gRenderDialogState.saveValue(name, value)

def setFlipbookDefaultOption(name, value):
  """ Set a particular option to the given value. The type of the value differs per option, giving the wrong value may result in exceptions. The options are read every time the dialog is opened, though not every knob in the dialog has it's value stored."""
  _gFlipbookDialogState.saveValue(name, value)
