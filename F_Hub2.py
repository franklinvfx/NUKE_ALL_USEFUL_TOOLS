import nuke, nukescripts, random, colorsys
import webbrowser, os, re, inspect, subprocess, math
import nukescripts.rollingAutoSave
import os.path as op

# Add Directory 
from menu import path



print 'F hub inside load'
    
menubar = nuke.menu("Nuke")                                  
m = menubar.addMenu("&Franklin VFX",  "franklin.png")

def icongreen():
	nuke.message('test vgghghg')

m.addCommand("Node Graph", "F_Hub2.icongreen()")