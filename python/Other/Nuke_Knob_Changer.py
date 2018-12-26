import nuke
import nukescripts

class KnobChanger(nukescripts.PythonPanel):
    def __init__(self):
        nukescripts.PythonPanel.__init__( self, 'Knob Changer', 'com.0hufx.KnobChanger')
        
        self.nodeSel = nuke.Enumeration_Knob('nodeSel', 'Apply to', ['All Nodes', 'Selected Nodes'])
        self.addKnob( self.nodeSel )
        self.Update = nuke.PyScript_Knob('update','Update')
        self.addKnob( self.Update )
        self.nodesChange = nuke.Enumeration_Knob('nodesChange', 'Nodes', [])
        self.addKnob( self.nodesChange )
        self.NodeKnobs = nuke.Enumeration_Knob('nodeKnobs', 'Knob', [])
        self.addKnob( self.NodeKnobs )
        self.TypeKnob = nuke.EvalString_Knob('TypeKnob', '')
        self.addKnob( self.TypeKnob )
        self.TypeKnob.setEnabled( False )
        self.EnableTypeKnob = nuke.Boolean_Knob('EnableTypeKnob','Type Knob Name')
        self.addKnob( self.EnableTypeKnob )
        self.KnobValue = nuke.EvalString_Knob('Value', 'New Value')
        self.addKnob( self.KnobValue )
        self.Execute = nuke.PyScript_Knob('execute','Execute')
        self.addKnob( self.Execute )

       
    def knobChanged ( self, knob ):

        if self.EnableTypeKnob.value() == True:
            #print 'Enabled'
            self.TypeKnob.setEnabled(True)
            self.NodeKnobs.setEnabled(False)
            KnobToChange = self.TypeKnob.value()
        else:
            #print 'Disabled'
            self.TypeKnob.setEnabled(False)
            self.NodeKnobs.setEnabled(True)
            KnobToChange = self.NodeKnobs.value()

        print KnobToChange

        if self.nodeSel.value() == 'All Nodes':
            x = nuke.allNodes()
        else:
            x = nuke.selectedNodes()

        Names = []

        for y in x:
                Names.append( y.Class() )

        Names = set(Names)
        Names = list(Names)
        #print Names
        self.nodesChange.setValues( Names )

        NodeToChange = self.nodesChange.value()
        
       #print NodeToChange

        NKnobs = []
        for i in nuke.allNodes(NodeToChange):
            NKnobs = sorted(i.knobs()) 

        self.NodeKnobs.setValues( NKnobs )
        kv = self.KnobValue.value()

        if knob == self.Execute:
            if self.nodeSel.value() == 'All Nodes':
                try:
                    for c in nuke.allNodes(NodeToChange):
                        c[KnobToChange].setValue(kv)
                except TypeError:
                    try:
                        try:
                            kv = float(kv)
                            for c in nuke.allNodes(NodeToChange):
                                c[KnobToChange].setValue(kv)
                        except TypeError:
                            nuke.message('Invalid Value')
                    except ValueError:
                        nuke.message('Invalid Value')
            else:
                try:
                    for c in nuke.selectedNodes(NodeToChange):
                        c[KnobToChange].setValue(kv)
                except TypeError:
                    try:
                        try:
                            kv = float(kv)
                            for c in nuke.selectedNodes(NodeToChange):
                                c[KnobToChange].setValue(kv)
                        except TypeError:
                            nuke.message('Invalid Value')
                    except ValueError:
                        nuke.message('Invalid Value')
						
def knobpanshow():
	KnobChanger().show()
		
def addknobManager():
    global knobManager
    knobManager = KnobChanger()
    return knobManager.addToPane()