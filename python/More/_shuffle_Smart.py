import nuke
import nukescripts

def shuffleAlpha():
    try:
        a = nuke.selectedNode()
        if a.Class() == "Shuffle":
            #a['tile_color'].setValue(4294967295)
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            if a['in'].value() == "rgba" and  r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(4)
                a['green'].setValue(4)
                a['blue'].setValue(4)
                a['alpha'].setValue(4)
                a['label'].setValue("(Alpha)")                  
            else:
                nuke.createNode("") 
        else:
            nuke.createNode("")            
    except:
        nuke.createNode("") 

def shuffleDepth():
    try:
        a = nuke.selectedNode()
        if a.Class() == "Shuffle":
            #a['tile_color'].setValue(1347506687)
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            if a['in'].value() == "rgba" and  r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(4)
                a['green'].setValue(4)
                a['blue'].setValue(4)
                a['alpha'].setValue(4)
                a['label'].setValue("(Depth)")  
                a['in'].setValue("depth")                
            else:
                nukescripts.toggle("disable")
        else:
            nukescripts.toggle("disable")           
    except:
        nukescripts.toggle("disable")
        
        
def shuffleRed():
    try:
        a = nuke.selectedNode()
        name = a['name'].value()
        if a.Class() == "Shuffle":
            #a['tile_color'].setValue(2466250752L)
            name = a['name'].value()
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            lab = a['label'].value()
            if a['in'].value() == "rgba" and r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(1)
                a['green'].setValue(1)
                a['blue'].setValue(1)
                a['alpha'].setValue(1) 
                a['label'].setValue("(Red)")      
            else:
                nukescripts.create_read()

        elif "ID" in name:
            x =a['xpos'].value()
            y = a['ypos'].value()
            print "hallo"
            channel = a['Red'].value()
            s = nuke.nodes.Shuffle()
            s.setXYpos(int(x),int(y+100))
            s.setInput(0,a)##################
            matte = 1
            s['tile_color'].setValue(2466250752L)
            s['red'].setValue(matte)
            s['green'].setValue(matte)
            s['blue'].setValue(matte)
            s['alpha'].setValue(matte)
            s['hide_input'].setValue(1)
            s['note_font_size'].setValue(20)
            s['autolabel'].setValue("nuke.thisNode()['label'].value()")
            s['label'].setValue(channel)
            s['help'].setValue(name)   
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\n"
            m = nuke.PyScript_Knob("showsourse","show source",code)
            s.addKnob(m)
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\nxC = dep.xpos() + dep.screenWidth()/2\nyC = dep.ypos() + dep.screenHeight()/2\nnuke.zoom( 3, [ xC, yC ])\n" 
            m = nuke.PyScript_Knob("jumptosource","jump to source",code)
            s.addKnob(m)
            code = "a = nuke.selectedNode()\nname=a['help'].value()\nname = nuke.toNode(name)\na.setInput(0, name)"
            m = nuke.PyScript_Knob("reconnect","reconnect",code)
            s.addKnob(m)
        else:
            nukescripts.create_read()         
    except:
        nukescripts.create_read()

def shuffleGreen():
    try:
        a = nuke.selectedNode()
        name = a['name'].value()
        if a.Class() == "Shuffle":
            name = a['name'].value()
            #a['tile_color'].setValue(1063467008L)
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            if  a['in'].value() == "rgba" and r == "red" and g == "green" and b == "blue" and aa == "alpha":
                a['red'].setValue(2)
                a['green'].setValue(2)
                a['blue'].setValue(2)
                a['alpha'].setValue(2) 
                a['label'].setValue("(Green)")          
            else:
                nuke.createNode("Grade")
        elif "ID" in name:

            x =a['xpos'].value()
            y = a['ypos'].value()
            print "hallo"
            channel = a['Green'].value()
            s = nuke.nodes.Shuffle()
            s.setXYpos(int(x),int(y+100))
            s.setInput(0,a)
            matte = 2
            s['tile_color'].setValue(1063467008L)
            s['red'].setValue(matte)
            s['green'].setValue(matte)
            s['blue'].setValue(matte)
            s['alpha'].setValue(matte)
            s['hide_input'].setValue(1)
            s['note_font_size'].setValue(20)
            s['autolabel'].setValue("nuke.thisNode()['label'].value()")
            s['label'].setValue(channel)
            s['help'].setValue(name)   
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\n"
            m = nuke.PyScript_Knob("showsourse","show source",code)
            s.addKnob(m)
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\nxC = dep.xpos() + dep.screenWidth()/2\nyC = dep.ypos() + dep.screenHeight()/2\nnuke.zoom( 3, [ xC, yC ])\n" 
            m = nuke.PyScript_Knob("jumptosource","jump to source",code)
            s.addKnob(m)
            code = "a = nuke.selectedNode()\nname=a['help'].value()\nname = nuke.toNode(name)\na.setInput(0, name)"
            m = nuke.PyScript_Knob("reconnect","reconnect",code)
            s.addKnob(m)
        else:
            nuke.createNode("Grade")         
    except:
        nuke.createNode("Grade")
        
def shuffleBlue():
    import nuke
    import nukescripts
    try:
        a = nuke.selectedNode()
        name = a['name'].value()
        if a.Class() == "Shuffle":
            #a['tile_color'].setValue(1027575296L)
            name = a['name'].value()
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            lab = a['label'].value()
            if  a['in'].value() == "rgba" and r == "red" and g == "green" and b == "blue" and aa == "alpha" :
                a['red'].setValue(3)
                a['green'].setValue(3)
                a['blue'].setValue(3)
                a['alpha'].setValue(3)
                a['label'].setValue("(Blue)")
            else:
                nuke.createNode("Blur") 
        elif "ID" in name:
            x =a['xpos'].value()
            y = a['ypos'].value()
            print "hallo"
            channel = a['Blue'].value()
            s = nuke.nodes.Shuffle()
            s.setXYpos(int(x),int(y+100))
            s.setInput(0,a)
            matte = 3
            s['tile_color'].setValue(1027575296L)
            s['red'].setValue(matte)
            s['green'].setValue(matte)
            s['blue'].setValue(matte)
            s['alpha'].setValue(matte)
            s['hide_input'].setValue(1)
            s['note_font_size'].setValue(20)
            s['autolabel'].setValue("nuke.thisNode()['label'].value()")
            s['label'].setValue(channel)
            s['help'].setValue(name)   
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\n"
            m = nuke.PyScript_Knob("showsourse","show source",code)
            s.addKnob(m)
            code = "a = nuke.thisNode()\na['hide_input'].setValue(0)\ndep = a.dependencies(nuke.INPUTS)[0]\na['hide_input'].setValue(1)\nnuke.show(dep)\nxC = dep.xpos() + dep.screenWidth()/2\nyC = dep.ypos() + dep.screenHeight()/2\nnuke.zoom( 3, [ xC, yC ])\n" 
            m = nuke.PyScript_Knob("jumptosource","jump to source",code)
            s.addKnob(m)
            code = "a = nuke.selectedNode()\nname=a['help'].value()\nname = nuke.toNode(name)\na.setInput(0, name)"
            m = nuke.PyScript_Knob("reconnect","reconnect",code)
            s.addKnob(m)
        else:
            nuke.createNode("Blur")                 
    except:
        nuke.createNode("Blur")


def shuffleAlphaFill():
    try:
        a = nuke.selectedNode()
        if a.Class() == "Shuffle":
            #a['tile_color'].setValue(1347506687)
            r = a['red'].value()
            g = a['green'].value()
            b = a['blue'].value()
            aa = a['alpha'].value()
            if a['in'].value() == "rgba" and  r == "red" and g == "green" and b == "blue" and aa == "alpha":
                #a['red'].setValue(4)
                #a['green'].setValue(4)
                #a['blue'].setValue(4)
                a['alpha'].setValue(6)
                a['label'].setValue("(Alpha Fill)")               
            else:
                nukescripts.toggle("")
        else:
            nukescripts.toggle("")           
    except:
        nukescripts.toggle("")
