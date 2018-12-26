import nuke

def selectDependencies(nodeBase):
    nodeBase['selected'].setValue(True)
    for node in nodeBase.dependencies():
        if node not in nuke.selectedNodes():
            selectDependencies(node)
        
def selectDependent(nodeBase):
    nodeBase['selected'].setValue(True)
    for node in nodeBase.dependent():
        if node not in nuke.selectedNodes():
            selectDependent(node)

def getAllDependencies(nodeBase,nodeType=None):
    relatedNodes = set()
    if nodeType == None or nodeBase.Class() == nodeType :
        relatedNodes.add(nodeBase)
    for node in nodeBase.dependencies():
        relatedNodes=relatedNodes.union( getAllDependencies(node,nodeType) )
    return relatedNodes

def isUsedBackdrop(backdrop, nodes):
    left = backdrop.xpos()
    top = backdrop.ypos() + 20
    right = left + backdrop['bdwidth'].value() - 20
    bottom = top + backdrop['bdheight'].value() - 20
    for node in nodes:
        if (node.xpos() > left and
            node.xpos() < right and
            node.ypos() > top and
            node.ypos() < bottom):
            return True
    return False

def selectRelatedBackdrops(relatedNodes):
    for bdnode in nuke.allNodes("BackdropNode"):
        if isUsedBackdrop(bdnode, relatedNodes):
            bdnode.setSelected(True)

n = nuke.thisNode()
v = nuke.allNodes("Viewer")  
all = nuke.allNodes()

def selectrelated():
    for node in nuke.selectedNodes():
        selectDependencies(node)
    selectRelatedBackdrops(nuke.selectedNodes())
    n.setSelected(True)

        
selectrelated()