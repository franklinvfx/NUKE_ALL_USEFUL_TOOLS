import nuke

def Dots():
    nodes = nuke.selectedNodes()
    for selected in nodes:
        selectedX = selected.xpos()
        selectedY = selected.ypos()
        selectedW = selected.screenWidth()
        selectedH = selected.screenHeight()
        try:
            A = selected.input(0)
            AX = A.xpos()
            AY = A.ypos()
            AW = A.screenWidth()
            AH = A.screenHeight()
            AClass = A.Class()
            print " Input 0 found   " + A['name'].value()
        except:

            AX = selected.xpos()
            AY = selected.ypos()
            AW = selected.screenWidth()
            AH = selected.screenHeight()
            AClass = "no classs"
            print " no input0 found   "
        try:
            B = selected.input(1)
            BX = B.xpos()
            BY = B.ypos()
            BW = B.screenWidth()
            BH = B.screenHeight()
            BClass = B.Class()
            print " Input 1 found   " + B['name'].value()
        except:
            BX = selected.xpos()
            BY = selected.ypos()
            BW = selected.screenWidth()
            BH = selected.screenHeight()
            BClass = "no classs"
            print " no input1 found        "
        try:
            C = selected.input(2)
            CX = C.xpos()
            CY = C.ypos()
            CW = C.screenWidth()
            CH = C.screenHeight()
            CClass = C.Class()
            print " Input 2 found   " + C['name'].value()
        except:
            print""
        
        if B and not C:
            Dot = nuke.nodes.Dot()
            print BX,selectedX
            if BX == selectedX or BX-34 == selectedX:
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
                dot.setXYpos(x1-200,y1+5)
                dot2 = nuke.nodes.Dot()
                if BX-34 == selectedX:
                    dot2.setXYpos(x1-200,y2)
                else:
                    dot2.setXYpos(x1-200,y2+5)
                dot2.setInput(0,depA)
                dot.setInput(0,dot2)
                t.setInput(1,dot)
                nuke.delete(Dot)
            else:
                Dot.setInput(0,B)
                selected.setInput(1,Dot)
                Dot.setXYpos(BX+BW/2-6,selectedY+4)
            if A.Class()== "Dot":
                selected.knob("xpos").setValue(AX-selectedW/2+6)
            else:        
                selected.knob("xpos").setValue(AX)
        elif C:
            print "C"
            if "Scanline" in selected.Class():

                if BClass == "no classs":
                    pass
                else:
                    if B.Class()== "Dot":
                        selected.setXYpos(BX-34,selectedY)
                    else:
                        selected.setXYpos(BX,selectedY)

                dot = nuke.nodes.Dot(xpos=CX+CW/2-6, ypos=selectedY+4)
                dot.setInput(0,C)
                selected.setInput(2,dot)

                if AClass == "no classs":
                    pass
                else:
                    dot = nuke.nodes.Dot(xpos=AX+AW/2-6, ypos=selectedY+4)
                    dot.setInput(0,A)
                    selected.setInput(0,dot)
                print "Scanline"
            if "Merge" in selected.Class() or "Roto" in selected.Class()or "Keymix" in selected.Class():
                if A.Class()== "Dot":
                    selected.setXYpos(AX-selectedW/2+6,selectedY)
                else:
                    selected.setXYpos(AX,selectedY)

                if A.Class()== "Dot":
                    dot = nuke.nodes.Dot(xpos=CX+CW/2-6, ypos=selectedY+4)
                else:
                    dot = nuke.nodes.Dot(xpos=CX+CW/2-6, ypos=selectedY+4)
                dot.setInput(0,C)
                selected.setInput(2,dot)
                if B.Class()== "Dot":
                    dot = nuke.nodes.Dot(xpos=BX, ypos=selectedY+4)
                else:
                    dot = nuke.nodes.Dot(xpos=BX+BW/2, ypos=selectedY+4)
                    print "gfdgfdgfd"
                dot.setInput(0,B)
                selected.setInput(1,dot)
                print "Merge"
        else:
            Dot = nuke.nodes.Dot() 
            Dot.setInput(0,A)
            selected.setInput(0,Dot)        
            Dot.setXYpos(selectedX+selectedW/2-6,AY+AH/2-6)   
    ###################################################

