#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Green
#
#----------------------------------------------------------------------------------------------------------

for node in nuke.selectedNodes():
     r = 0 
     g = 1 
     b = 0 
     hexColour = int('%02x%02x%02x%02x' % (r*255,g*255,b*255,1),16) 
     node['tile_color'].setValue( hexColour )