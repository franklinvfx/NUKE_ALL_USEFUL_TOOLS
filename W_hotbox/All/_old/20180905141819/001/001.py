#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Remove
#
#----------------------------------------------------------------------------------------------------------

def noicon():
  for node in nuke.selectedNodes():
      node["icon"].setValue('') # Remove Icon
noicon()