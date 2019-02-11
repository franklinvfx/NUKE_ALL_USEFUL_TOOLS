import nuke, nukescripts
import os
import multiprocessing
import time
import platform

def cmdExecute():
    Nwrite = nuke.selectedNode()
    NName = Nwrite['name'].value()
    fRange = nuke.activeViewer().node()['frame_range'].getValue()

    #Get list of available CPU threads
    actThd = multiprocessing.cpu_count()
    thds = ""
    thd = range(1, actThd+1)
    for n in thd:
        thds += str(n) + " "

    #Check if selected node is executable
    if Nwrite.Class() not in ['Write', 'DeepWrite', 'WriteGeo', 'WriteTank', 'SmartVector']:
        nuke.message('Selected node is not executable via CMD!') #making sure selected node is executable
    else:
        i = nuke.Panel('Render settings')
        i.addSingleLineInput('first', nuke.root().firstFrame())
        i.addSingleLineInput('last', nuke.root().lastFrame())
        i.addEnumerationPulldown( 'threads', thds )
        i.addBooleanCheckBox('Save new version', 0)
        i.addBooleanCheckBox('NukeX', 0)
        i.addBooleanCheckBox('Close Nuke', 0)
        if i.show():
            try:
                nuke.scriptSave("")
                ret = [int(i.value('first')), int(i.value('last'))]
                rThd = int(i.value('threads'))
                sav = i.value('Save new version')
                X = i.value('NukeX')
                nukeQuit = i.value('Close Nuke')

                if X == 1:
                    args = '"' + nuke.env["ExecutablePath"] + '"' + " --nukex" \
                       + " -i -m " + str(rThd) \
                       + " -X " + NName \
                       + " -F " + str(ret[0]) + '-' + str(ret[1]) \
                       + " " + '"' + nuke.scriptName() + '"' #Quote unquote for spaces in BAT
                else:
                    args = '"' + nuke.env["ExecutablePath"] + '"' \
                       + " -i -m " + str(rThd) \
                       + " -X " + NName \
                       + " -F " + str(ret[0]) + '-' + str(ret[1]) \
                       + " " + '"' + nuke.scriptName() + '"' #Quote unquote for spaces in BAT

                #identify OS
                if platform.system() == "Windows":
                    startCMD = "start cmd /k " + '"' + args + '"' #Quote unquote in case both paths have spaces
                    print args
                if platform.system() == "Linux":
                    startCMD = "gnome-terminal -x " +  args #Quote unquote in case both paths have spaces
                os.popen(startCMD)

                #save new version
                if sav == 1:
                    nukescripts.script_and_write_nodes_version_up()

                #quit
                if nukeQuit == 1:
                    nuke.scriptExit()

            except:
                nuke.message('Invalid input')

#Add to menu and assign shortcut key
nodeMenu = nuke.menu('Nuke').findItem('Render')
nodeMenu.addCommand('Execute using Command Prompt', 'cmdExecute.cmdExecute()', 'F6')
