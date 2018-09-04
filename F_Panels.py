import nuke, nukescripts, math

try:
    # < Nuke 11
    import PySide.QtCore as QtCore
    import PySide.QtGui as QtGui
    import PySide.QtGui as QtGuiWidgets
except:
    # >= Nuke 11
    import PySide2.QtCore as QtCore
    import PySide2.QtGui as QtGui
    import PySide2.QtWidgets as QtGuiWidgets

from menu import path

nuke.pluginAddPath(path + './icons');

nuke.pluginAddPath(path + './Python');
nuke.pluginAddPath(path + './Python/More');

##########################################################################################################################################
##########################################################################################################################################
#######                                                      #############################################################################
#######                   ADD PANNELS                        #############################################################################
#######                                                      #############################################################################
##########################################################################################################################################
##########################################################################################################################################


p = nuke.menu("Pane")
#------------------------------
p.addCommand( '-', "", icon="F_toolset.png")
#------------------------------
 
import BackdropManager
from BackdropManager import addBackdropManager
p.addCommand( 'Backdrop Manager', addBackdropManager,  icon='Backdrop.png')
nukescripts.registerPanel('com.ohufx.Backdrop', addBackdropManager )
 
#------------------------------

import capture  
def addCaptureManager(): 
    Capture = capture.captureNodePanel() 
    return Capture.addToPane() 
p.addCommand('ToolSet Manager', addCaptureManager,  icon="F_toolset.png") 
nukescripts.registerPanel('com.0hufx.Capture', addCaptureManager )

#------------------------------

import Nuke_Knob_Changer  
def addKnobChanger(): 
    KnobChanger = Nuke_Knob_Changer.KnobChanger() 
    return KnobChanger.addToPane() 
p.addCommand('Knob Manager', addKnobChanger,  icon="F_knob.png") 
nukescripts.registerPanel('com.0hufx.KnobChanger', addKnobChanger )

#------------------------------
p.addCommand('-', '', '') 
#------------------------------

import DiskCachePanel 
def addDiskCachePanelManager(): 
    DiskCache = DiskCachePanel.addPanel() 
    return DiskCachePanel.addToPane() 
p.addCommand('Disk Cache', addDiskCachePanelManager,  icon="F_cache.png") 
nukescripts.registerPanel('com.0hufx.DiskCache', addDiskCachePanelManager )

#------------------------------

import IconPanel 
def addIconPanel(): 
    IconP = IconPanel.addIconPanel() 
    return IconP.addToPane() 
p.addCommand('Icon Panel', addIconPanel,  icon="AllPlugins.png") 
nukescripts.registerPanel('com.ohufx.IconPanel', addIconPanel )

#------------------------------

import SearchReplacePanel
def addSRPanel():
        myPanel = SearchReplacePanel.SearchReplacePanel()
        return myPanel.addToPane()
nuke.menu('Pane').addCommand('Search Replace', addSRPanel,  icon="F_superswap.png")
nukescripts.registerPanel('com.ohufx.SearchReplace', addSRPanel)