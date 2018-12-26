#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Red
# COLOR: #d61d1d
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
     r = 1 
     g = 0 
     b = 0 
     hexColour = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16) 
     node['tile_color'].setValue( hexColour )