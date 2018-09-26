#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Arrow
#
#----------------------------------------------------------------------------------------------------------

#nuke.pluginAddPath('./icons/FT/nodes');
#nuke.pluginAddPath('./icons/FT/color');

def iconarrow():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_arrow.png') # Arrow
iconarrow()