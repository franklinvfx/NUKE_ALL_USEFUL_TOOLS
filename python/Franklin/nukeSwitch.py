import nuke, sys, subprocess

def versionSwitch():
    nuke.scriptSave() # Save current script
    nukeScript = nuke.root().knob('name').value() # Find current script path
    nukeExe = sys.executable # Find executable path
    if nuke.env['nukex'] == True: # Check Nuke or Nuke X
        nukeProcess = subprocess.Popen([nukeExe, nukeScript]) # Launch Nuke
        print 'Close nukeX and launch nuke'
    else:
        nukeProcess = subprocess.Popen([nukeExe, "--nukex", nukeScript]) # Launch Nuke X
        print 'Close nuke and launch nukeX'
    nuke.executeInMainThread(nuke.scriptExit) # Close current script