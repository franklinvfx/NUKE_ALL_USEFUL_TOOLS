#----------------------------------------------------------------------------------------------------------
#
# AUTOMATICALLY GENERATED FILE TO BE USED BY W_HOTBOX
#
# NAME: Check
#
#----------------------------------------------------------------------------------------------------------

def iconcheck():
  for node in nuke.selectedNodes():
      node["icon"].setValue('F_croixb.png') # Check
    
iconcheck()