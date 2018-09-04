#
#  Created by Tyler Lockard [lockardvfx@gmail.com] tylerlockard.com
#  11/7/14
#
#  "Batch Renamer" removes all the hassle from jumping out of nuke, launching a batch 
#  rename program, probably messing up a few times, jumping back into Nuke and updating 
#  your read node... That takes like, a whole minute. That's just too long.
#
#  With a simple UI, we can do all that in Nuke. I'll also update your Read node for you!


import os
import nuke
import nukescripts



class BatchRenamePanel(nukescripts.PythonPanel):
    '''
    The dialog panel where we're going to grab all of
    our information. 
    '''
    def __init__(self, sequence):
        nukescripts.PythonPanel.__init__(self, 'Batch Renamer')
        
        # Set our window width based on the filename length
        self.file = os.path.basename(sequence)
        self.setMinimumSize( len(self.file)*10+200, 200 )
        
        # Make some knobs!
        self.seq = sequence
        self.shot = nuke.Text_Knob('shot', 'Source: ', '<span style="color:orange">' + self.seq)
        self.div1 = nuke.Text_Knob('break', '')
        self.div2 = nuke.Text_Knob('break', '')
        self.blank1 = nuke.Text_Knob('break', '', ' ')
        self.blank2 = nuke.Text_Knob('break', '', ' ')
        self.find= nuke.String_Knob('find:', 'Find this:', '')
        self.previewFind = nuke.Text_Knob('previewFind', '', self.file)
        self.replace= nuke.String_Knob('replace', 'Replace with:', '')
        self.previewReplace = nuke.Text_Knob('previewReplace', '', self.file)
        
        # Add Knobs
        self.addKnob(self.shot)
        self.addKnob(self.div1)
        self.addKnob(self.find)
        self.addKnob(self.previewFind)
        self.addKnob(self.blank1)
        self.addKnob(self.replace)
        self.addKnob(self.previewReplace)
        self.addKnob(self.div2)
        self.addKnob(self.blank2)
    
    
    def knobChanged(self, knob):
        '''
        Refreshes the preview text whenever the find 
        and replace fields are changed
        '''
        try:
            self.update = self.file.split(self.find.value())
            self.highlight = '<span style="color:orange">' + self.find.value() + '</span>'
            self.update = self.highlight.join(self.update)
            self.previewFind.setValue(self.update)
            self.update = self.file.split(self.find.value())
            self.highlight = '<span style="color:orange">' + self.replace.value() + '</span>'
            self.update = self.highlight.join(self.update)
            self.previewReplace.setValue(self.update)
        except:
            pass


def batchRename(node, sequence, find, replace):
    '''
    Takes an image sequence and runs a mass-rename 
    based on the feedback from the dialog panel.
    '''
    from glob import glob
    ext = "." + sequence.split('.')[-1]
    dir = os.path.dirname(sequence)
    frames = glob( dir + "/*" + ext )
    for f in frames:
        r = dir + '/' + os.path.basename(f).replace(find, replace)
        os.rename(f, r)
    node['file'].setValue( dir + '/' + os.path.basename(sequence).replace(find, replace) )
    nuke.message("Batch rename successful! \n\nI updated the read node for you.")


def main():
    '''
    If we have a read node selected, lets run the 
    batch rename!
    '''
    try:
        # Grab the selected node's file input
        node = nuke.selectedNode()
        sequence = node['file'].value()
    except:
        nuke.message("Select a read node first")
        return
    
    # Check if we have a Read node selected
    if node.Class() != "Read":
        nuke.critical("\nYou fool, I can't rename a \"%s\" node!" %node.Class())
        return
    
    # Good to go, display dialog
    p = BatchRenamePanel(sequence)
    result = p.showModalDialog()
    
    # Run the batch rename with what we've collected
    if result == True:
        batchRename(node, sequence, p.find.value(), p.replace.value())


