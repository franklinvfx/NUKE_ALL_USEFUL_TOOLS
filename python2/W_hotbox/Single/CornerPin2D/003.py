#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Convert to Matrix
#
#----------------------------------------------------------------------------------------------------------

#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY MAGIC HOTBOX
#
# NAME: To CornerPin Matrix
#
#----------------------------------------------------------------------------------------------------------

#Combines several Transforms nodes into a single one using project first-last frame
#by Magno Borgo 2016
#v01
#Usage: Select the transforms  and run the script
#WARNING: motionblur doesn't work with the transform matrix at this time, use a vector blur.
#Thanks to Ivan Busquets nukepedia article http://www.nukepedia.com/written-tutorials/using-the-nukemath-python-module-to-do-vector-and-matrix-operations/all
#Cornerpin to matrix adapted from Pete O'Connell code.http://community.thefoundry.co.uk/discussion/topic.aspx?f=189&t=98563

def main():
    import nuke
    import math
    #from cgev.common import log

    def applyTransform(x,y,z,node,tMatrix):
        tMatrix.makeIdentity()
        tMatrix.translate(x,y,z)
        tMatrix.transpose()
        node = node * tMatrix
        return node
    
    def checkOrdering(nodes): #inspired on code by Erwan Leroy - 2014
        transforms = 0
        transformList = []
        currentTransforms = 0
        for n in nodes:
    
            parents = True
            currentList = []
            currentList += [n]
            while parents == True:
                p = n.input(0)
                if p:
                   if p not in nodes:
                       parents = False
                   else:
                       n = p
                       currentList += [n]
                else :
                    parents = False
    
            #the node with the biggest number of parents is our last node
            if len(currentList) == len(nodes):
                #transforms = currentTransforms
                transformList = currentList
    
        #We want our first node first though, so we reverse the list
        transformList.reverse()
        return transformList
    
    def transform2DtoMatrix(f,node):
        newMatrix = nuke.math.Matrix4()
        newMatrix.makeIdentity()
        tMatrix = nuke.math.Matrix4()
        tMatrix.makeIdentity()
    
        newMatrix = applyTransform((node['center'].getValueAt(f)[0]*-1),(node['center'].getValueAt(f)[1]*-1),0,newMatrix,tMatrix)
        newMatrix.scale(node['scale'].x_at(f),node['scale'].y_at(f),1)
        newMatrix = applyTransform((node['center'].getValueAt(f)[0]),(node['center'].getValueAt(f)[1]),0,newMatrix,tMatrix)
    
        newMatrix = applyTransform((node['center'].getValueAt(f)[0]*-1),0,0,newMatrix,tMatrix)
        tMatrix.makeIdentity()
        tMatrix[4] = node['skewY'].getValueAt(f)
        newMatrix = newMatrix * tMatrix
        newMatrix = applyTransform((node['center'].getValueAt(f)[0]),0,0,newMatrix,tMatrix)
          
        newMatrix = applyTransform(0,(node['center'].getValueAt(f)[1]*-1),0,newMatrix,tMatrix)
        tMatrix.makeIdentity()
        tMatrix[1] = node['skewX'].getValueAt(f)
        newMatrix = newMatrix * tMatrix      
        newMatrix = applyTransform(0,(node['center'].getValueAt(f)[1]),0,newMatrix,tMatrix)
    
        newMatrix = applyTransform((node['center'].getValueAt(f)[0]*-1),(node['center'].getValueAt(f)[1]*-1),0,newMatrix,tMatrix)
        newMatrix.rotateZ(math.radians(node['rotate'].getValueAt(f))*-1)
        newMatrix = applyTransform((node['center'].getValueAt(f)[0]),(node['center'].getValueAt(f)[1]),0,newMatrix,tMatrix)
        tMatrix.makeIdentity()
        tMatrix.translate(node['translate'].getValueAt(f)[0],node['translate'].getValueAt(f)[1],0)
        tMatrix.transpose()
        newMatrix = newMatrix * tMatrix
        return newMatrix
    
    def cpintomatrix(f,node):
        projectionMatrixTo = nuke.math.Matrix4()
        projectionMatrixFrom = nuke.math.Matrix4()
        to1x = node['to1'].getValueAt(f)[0]
        to1y = node['to1'].getValueAt(f)[1]
        to2x = node['to2'].getValueAt(f)[0]
        to2y = node['to2'].getValueAt(f)[1]
        to3x = node['to3'].getValueAt(f)[0]
        to3y = node['to3'].getValueAt(f)[1]
        to4x = node['to4'].getValueAt(f)[0]
        to4y = node['to4'].getValueAt(f)[1]
        from1x = node['from1'].getValueAt(f)[0]
        from1y = node['from1'].getValueAt(f)[1]
        from2x = node['from2'].getValueAt(f)[0]
        from2y = node['from2'].getValueAt(f)[1]
        from3x = node['from3'].getValueAt(f)[0]
        from3y = node['from3'].getValueAt(f)[1]
        from4x = node['from4'].getValueAt(f)[0]
        from4y = node['from4'].getValueAt(f)[1]
        projectionMatrixTo.mapUnitSquareToQuad(to1x,to1y,to2x,to2y,to3x,to3y,to4x,to4y)
        projectionMatrixFrom.mapUnitSquareToQuad(from1x,from1y,from2x,from2y,from3x,from3y,from4x,from4y)    
        theCornerpinAsMatrix = projectionMatrixTo*projectionMatrixFrom.inverse()
        theCornerpinAsMatrix.transpose()    
        return theCornerpinAsMatrix
        
    def transformstoMatrix(nodes,mode=0):
        #mode 0 creates a cornerpin node with the extra-matrix on it
        #mode 1 returns a matrix based on all the transforms
    
        fRange = nuke.FrameRange('%s-%s' % (nuke.root().firstFrame(), nuke.root().lastFrame()))
        for node in nodes: 
            if node.Class() not in ('Transform','CornerPin2D','Tracker4','Tracker3'):
                if nuke.GUI:
                    msg = 'Unsupported node type: ' + node.Class() + '.\n Selected Node must be Transform, CornerPin, Tracker'
                    nuke.message(msg)
                else:
                    raise TypeError, 'Unsupported node type.\n Selected Node must be Transform, CornerPin, Tracker'
                return
            node.knob('selected').setValue(False)
    
        nodes = checkOrdering(nodes)
    
        if mode == 0:
            newCpin = nuke.createNode('CornerPin2D')
            newCpin['label'].setValue('Matrix')
            newCpin['transform_matrix'].setAnimated()

        frameProgressBar = nuke.ProgressTask('Iterating frames : ')
        frameProgress = 100.0 / max(1.0, nuke.root().lastFrame())

        for f in fRange:
            if frameProgressBar.isCancelled():
                frameProgressBar.setProgress(100)
                nuke.delete(newCpin)
                break

            frameProgressBar.setProgress(int(f * frameProgress))
            frameProgressBar.setMessage(str(f)+'/'+str(nuke.root().lastFrame()))

            mainMatrix = nuke.math.Matrix4()
            mainMatrix.makeIdentity()
            f= float(f)
            for node in nodes:#[::-1]:
                if node.Class() in ('Transform','Tracker4','Tracker3'):
                    mainMatrix = mainMatrix * transform2DtoMatrix(f,node)
                if node.Class() in ('CornerPin2D'):
                    mainMatrix = mainMatrix * cpintomatrix(f,node)
            if mode == 0:
                for n in range(0, len(mainMatrix)):
                    newCpin['transform_matrix'].setValueAt(mainMatrix[n],f,n)

            frameProgressBar.setProgress(int(f * frameProgress))
            frameProgressBar.setMessage(str(f)+'/'+str(nuke.root().lastFrame()))

        if mode == 0:
            try:
                newCpin.knob('selected').setValue(True)
            except:
                pass
        if mode == 1:
            return mainMatrix
    
    transformstoMatrix(nuke.selectedNodes())
main()