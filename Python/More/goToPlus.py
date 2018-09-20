import nuke
import nukescripts
import re


def goToPlus():
    '''
    Allows you to directly enter simple math signs to
    go to a frame without explicity requiring you to
    enter the current frame number before it.
    '''

    '''class GoToPlusPanel(nukescripts.PythonPanel):
        def __init__(self):
            nukescripts.PythonPanel.__init__(self, 'Go To Plus')
            self.cFrame = nuke.frame()
            self.goto = nuke.String_Knob('goto', '')
            self.result = nuke.Text_Knob('result', 'result :')

            for knob in (self.goto, self.result):
                self.addKnob(knob)

        def knobChanged(self, knob):
            print knob.name()+', value : '+str(knob.value())
            if knob.name() == self.goto.name():
                self.result = 'result : '+str(knob.value())

    panel = GoToPlusPanel()
    panel.showModalDialog()'''

    cFrame = nuke.frame()

    p = nuke.Panel('Go to Frame Plus')
    p.addSingleLineInput('', '')
    # p.addExpressionInput('Go to frame', cFrame)
    p.show()

    goTo = p.value('')
    pat1 = re.compile('\+|-|\*|\/')

    if goTo == '':
        return
    elif goTo[0].isdigit() == True and pat1.search(goTo) == None:
        nuke.frame(int(goTo))
    elif goTo[0].isdigit() == True and pat1.search(goTo) != None:
        try:
            nuke.frame(eval(goTo))
        except Exception, e:
            raise RuntimeError(e)
    else:
        try:
            nuke.frame(eval(str(int(cFrame)) + goTo))
        except Exception, e:
            raise RuntimeError(e)
