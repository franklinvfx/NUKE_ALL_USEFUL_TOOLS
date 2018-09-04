import nuke

def Dots():
    nodes = nuke.selectedNodes()
    for selected in nodes:
        selectedX = selected.xpos()
        selectedY = selected.ypos()
        selectedW = selected.screenWidth()
        selectedH = selected.screenHeight()
        A = selected.input(0)
        AX = A.xpos()
        AY = A.ypos()
        AW = A.screenWidth()
        AH = A.screenHeight()
        try:
            B = selected.input(1)
            BX = B.xpos()
            BY = B.ypos()
        except:
            print""
        Dot = nuke.nodes.Dot()
        if B:
            if BX == selectedX:
                t = nuke.selectedNode()
                depB = t.dependencies(nuke.INPUTS)[0]
                try:
                    depA = t.dependencies(nuke.INPUTS)[1]
                except:
                    depA = t.dependencies(nuke.INPUTS)[0]
                x2 = depA['xpos'].value()
                y2 = depA['ypos'].value()
                x2 = int(x2)
                y2 = int(y2)
                x1 = t['xpos'].value()
                y1 = t['ypos'].value()
                x1 = int(x1)
                y1 = int(y1)
                dot = nuke.nodes.Dot()
                dot.setXYpos(x1-100,y1+5)
                dot2 = nuke.nodes.Dot()
                dot2.setXYpos(x1-100,y2+5)
                dot2.setInput(0,depA)
                dot.setInput(0,dot2)
                t.setInput(1,dot)
                nuke.delete(Dot)
            else:
                BX = B.xpos()
                BY = B.ypos()
                BW = B.screenWidth()
                BH = B.screenHeight()
                Dot.setInput(0,B)
                selected.setInput(1,Dot)
                Dot.setXYpos(BX+BW/2-6,selectedY+4)
            if A.Class()== "Dot":
                selected.knob("xpos").setValue(AX-selectedW/2+6)
            else:        
                selected.knob("xpos").setValue(AX)
    ###################################################
        else: 
            Dot.setInput(0,A)
            selected.setInput(0,Dot)        
            Dot.setXYpos(selectedX+selectedW/2-6,AY+AH/2-6)   
    ###################################################
    
