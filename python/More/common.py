#
# Python code by Timur Khodzhaev
#
# - www.chimuru.com
# - chimuru@gmail.com
#
# List of functions:

# topInput() - returns knob value of the first node of the certain class found upstream of the node pipe
# topInputKnob() - returns knob of the first node of the certain class found upstream of the node pipe
# topInputNode(node,ch_class,input=0) - returns node from upstream

# ensureMatrix() - make sure returned vbalue is always a Matrix
# ensureFloat() - make sure returned value is always Float
# getKnobViews(knob) - return list of views for the knob
# animCurveMinMax(curve) - returns min/max values on animated curve (minValue frame number , minValue, maxValue frame number, maxValue)
# getTrackNames(node) - Returns a list of tracks in a Tracker4 node

# emptyInput(node,start_input=0) - returns first empty input
# nonEmptyInput(node,start_input=0) - returns first non empty input
# shiftConnections(node,start=0) - shifts connection pipes


# Finds node of certain class in the input pipe upstream and if there is a knob
# specified returns its value
import nuke
import re
import os

def topInput(node,input,ch_class,knob,ch_frame):
    if node:
        input_node=node.input(input)
        if input_node:
            if input_node.Class() == ch_class :
                if input_node.knob(knob):
                    return input_node[knob].getValueAt(ch_frame)
            else:
                if input_node.Class()=='JoinViews':
#                    print nuke.views()
#                    print nuke.thisView()
                    current_view=nuke.views().index(nuke.thisView())
                    return topInput(input_node,current_view,ch_class,knob,ch_frame)
                else:
                    return topInput(input_node,0,ch_class,knob,ch_frame)
        else:
            return None

# Finds node of certain class in the input pipe upstream and if there is a knob
# specified returns its object

def topInputKnob(node,ch_class,knob,input=0):
    if node:
        input_node=node.input(input)
        if input_node:
            if nodeClass(input_node) == ch_class :
                if input_node.knob(knob):
                    return input_node[knob]
            else:
                if nodeClass(input_node)=='JoinViews':
#                    print nuke.views()
#                    print nuke.thisView()
                    current_view=nuke.views().index(nuke.thisView())
                    return topInputKnob(input_node,current_view,ch_class,knob)
                else:
                    return topInputKnob(input_node,ch_class,knob)
        else:
            return None

# Finds node of certain class in the input pipe upstream and 
# returns node onject

def topInputNode(node,ch_class,input=0):
    if node:
        input_node=node.input(input)
        if input_node:
            if nodeClass(input_node) == ch_class :
                return input_node
            else:
                if nodeClass(input_node)=='JoinViews':
#                    print nuke.views()
#                    print nuke.thisView()
                    current_view=nuke.views().index(nuke.thisView())
                    return topInputNode(input_node,current_view,ch_class)
                else:
                    return topInputNode(input_node,ch_class)
        else:
            return None

##########################################################
#
# Volume Holdout matrix knob work abound
# in matrix node direct expression is used to refer to the certain element in the array
# of the transfrom matrix. When there is no object returned there is an exception raised 
# because None object is unsubscriptable
# this function is workaroud to make sure returned value is always a list or 0

def ensureMatrix(value):
    if (type(value) is list):
        return value
    else:
        return [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
def ensureFloat(value):
    if (type(value) is float):
        return value
    else:
        return 0

#########################################################
#
# Returns a list of view for knob
# parse toScript of the knob to get named views
#

def getKnobViews(knob):
    if knob:
        s=knob.toScript()
        pt=re.compile('\w+\s\{')
        ss=re.findall(pt,s)
        result =[]
        for i in ss:
#            ss=i.lstrip(' ').split(' ')[0]
            if i:
                if not(i in result):
                    result.append(i[0:-2])
        return result


#########################################################
#
# Returns a node Class even for Group nodes
# by default Nuke returns Group for all Group nodes
# this script reads aditional knob nodeClass and returns its value 
#

def nodeClass(node):
    if node:
        if ( 'nodeClass' in node.knobs().keys() ) :
            return node['nodeClass'].value()
        else:
            return node.Class()



#########################################################
#
# Returns a 4 values for a animated curve with min and max values
# (minValue frame number , minValue, maxValue frame number, maxValue)
# 
#

def animCurveMinMax(curve):
    try:
        minX,minY=1000000000000,1000000000000
        maxX,maxY=-100000000000,-1000000000000
        for i in curve.keys():
            if i.y<minY:
                minX,minY=i.x,i.y
            if i.y>maxY:
                maxX,maxY=i.x,i.y
        return minX,minY,maxX,maxY

    except Exception,e:
        print('Error:: %s' % e)

#########################################################
#
# Returns a list of tracks in a Tracker4 node
# its actually parse toScript so it could break on Nuke version up
# 
#
def getTrackNames(node):
    k=node['tracks']
    s=node['tracks'].toScript().split(' \n} \n{ \n ')
    s.pop(0)
    ss=str(s)[2:].split('\\n')
    ss.pop(-1)
    ss.pop(-1)
    outList=[]
    for i in ss:
        outList.append(i.split('"')[1])
    return outList


#########################################################
#
# Functions to work with help buttons in nodes
# returns url for specified node
#
# Uses nodeClass function from this module
#

def getHelpUrl(node=None):

    # url will be used in case of unknown class or node is not provided

    mySite='www.chimuru.com'

    # Check if there is override for default value
    if os.getenv('TK_HELP_URL'):
        mySite=os.getenv('TK_HELP_URL')

    if node:
        # Reading os environment variable to find file with help urls
        if os.getenv('TK_HELP_FILE'):
            helpFile=os.getenv('TK_HELP_FILE')

            # opening help Settings file to read settings
            settings=[]
            if os.path.isfile( helpFile ):
                prefFile = open(helpFile,"r")
                prefContent = prefFile.readlines()
                prefFile.close()

                for i in prefContent:
                    key,value= i.rstrip().split('::')
                    settings.append((key,value))  
         
            ndClass=nodeClass(node)

            # Look through list of values from settings to see if there a url for that node
            url=mySite
            for key,value in settings:
                if ndClass==key:
                    url=value

        # if help settings file is not defined return my site            
        else:
            url=mySite

    # if no node provided return my site
    else:
        url=mySite

    return url

#########################################################
#
# Functions to work with input pipes
#
# returns first empty input pipe starting from start_input pipe
#
def emptyInput(node,start_input=0):
    inputs=node.inputs()
    for input in range(start_input,inputs):
        if node.input(input)==None:
            return input
    return None

#########################################################
#
# Functions to work with input pipes
#
# returns first not empty input pipe starting from start_input pipe
#
def nonEmptyInput(node,start_input=0):
    inputs=node.inputs()
    for input in range(start_input,inputs):
        if node.input(input)!=None:
            return input
    return None

#########################################################
#
# Functions to work with input pipes
#
# shifts connection pipes to get rid of empty connections
# made for CountSheet rewiring but might be usefull for 3dScenes and merges as well
#
def shiftConnections(node,start=0):
    inputs=node.inputs()
    for input in range(start,inputs):
        node.setInput(input, node.input(input+1))
    if emptyInput(node)==start:
            shiftConnections(node, start)
    if emptyInput(node):
         shiftConnections(node, emptyInput(node))
    return node

#
# Functions to find file in plugin path folders
#
# looks through all folders and returns path list if file is found
#
def where(filename):
    file_list=[]
    for path in nuke.pluginPath():
        check_file='%s%s%s' % (path, os.sep, filename)
        if os.path.isfile( check_file ):
            file_list.append(check_file)
    if file_list:
        file_list.reverse()

    return file_list

