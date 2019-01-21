
import nuke

# val = []

# if val == True:
# 	val = False
# 	menubar = nuke.menu("Nuke")
# 	m = menubar.addMenu("Franklin",  "franklin.png")
# 	m.addMenu('Debug', "F_node.png")
# 	m.addCommand('Debug/Yes', F_callbackTrace(), "F_nodetools.png")






# def _cb(name):
#   nuke.tprint(name + " " + nuke.thisNode().name())

# def _cbk(name):
#   nuke.tprint(name + " " + nuke.thisNode().name() + "." + nuke.thisKnob().name())

# nuke.addOnUserCreate(_cb, ("onUserCreate"))
# nuke.addOnCreate(_cb, ("onCreate"))
# nuke.addOnScriptLoad(_cb, ("onScriptLoad"))
# nuke.addOnScriptSave(_cb, ("onScriptSave"))
# nuke.addOnScriptClose(_cb, ("onScriptClose"))
# nuke.addOnDestroy(_cb, ("onDestroy"))
# nuke.addKnobChanged(_cbk, ("knobChanged"))
# nuke.addUpdateUI(_cb, ("updateUI"))
# nuke.addAutolabel(_cb, ("autolabel"))
# nuke.addBeforeRender(_cb, ("beforeRender"))
# nuke.addBeforeFrameRender(_cb, ("beforeFrameRender"))
# nuke.addAfterFrameRender(_cb, ("afterFrameRender"))
# nuke.addAfterRender(_cb, ("afterRender"))
# nuke.addRenderProgress(_cb, ("renderProgress"))
# nuke.addFilenameFilter(lambda s: nuke.tprint("filenameFilter('"+s+"')"))





def _cb(name):
	pass

def _cbk(name):
  pass

nuke.addOnUserCreate(_cb, ("onUserCreate"))
nuke.addOnCreate(_cb, ("onCreate"))
nuke.addOnScriptLoad(_cb, ("onScriptLoad"))
nuke.addOnScriptSave(_cb, ("onScriptSave"))
nuke.addOnScriptClose(_cb, ("onScriptClose"))
nuke.addOnDestroy(_cb, ("onDestroy"))
nuke.addKnobChanged(_cbk, ("knobChanged"))
nuke.addUpdateUI(_cb, ("updateUI"))
nuke.addAutolabel(_cb, ("autolabel"))
nuke.addBeforeRender(_cb, ("beforeRender"))
nuke.addBeforeFrameRender(_cb, ("beforeFrameRender"))
nuke.addAfterFrameRender(_cb, ("afterFrameRender"))
nuke.addAfterRender(_cb, ("afterRender"))
nuke.addRenderProgress(_cb, ("renderProgress"))
nuke.addFilenameFilter(lambda s: nuke.tprint("filenameFilter('"+s+"')"))









# 	nuke.load("Reload"); reloadSpecific("Franklin", "F_callbackTrace")

# else:
# 	val = True
# 	menubar = nuke.menu("Nuke")
# 	m = menubar.addMenu("Franklin",  "franklin.png")
# 	m.addMenu('Debug', "F_node.png")
# 	m.addCommand('Debug/None', F_callbackTrace(), "F_nodetools.png")
# 	nuke.load("Reload"); reloadSpecific("Franklin", "F_callbackTrace")