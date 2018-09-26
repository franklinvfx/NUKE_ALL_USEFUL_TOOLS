#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Reset
# COLOR: #db0000
# TEXTCOLOR: #111111
#
#----------------------------------------------------------------------------------------------------------

def noicon():
  for node in nuke.selectedNodes():
      node["icon"].setValue('') # Remove Icon
      node['note_font_size'].setValue(11)
noicon()