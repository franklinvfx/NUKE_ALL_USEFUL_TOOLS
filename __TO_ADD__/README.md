# FRANKLINVFX - Nuke Tools
Collection of best Nuke Gizmos and Tools.
 
### Table of Contents
**[Installation Instructions](#installation-instructions)**<br>
**[Manual Installation](#manual-installation)**<br>
**[List of Tools](#list-of-tools)**<br>
**[Thanks](#thanks)**

## Installation Instructions
For easy installation of the toolset, we provide a script that will make menu entries for each of our tools and ensure 
they are all part of the Nuke plugin path.

Installation instructions are similar for any OS. However, the paths we are using in the example are formatted for an 
UNIX system (Mac or Linux).

1. Download the full content of the spin_nuke_gizmos repository. If downloaded
as a .ZIP, uncompress the zip in the desired location. For the following steps, we will assume the folder is present 
on disk as: `/my_nuke_gizmos/spin_nuke_gizmos/`.
2. Add the path to the folder in your NUKE_PATH, either via an environment variable ([Defining Nuke plugin path](
https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/defining_nuke_plugin_path.html)) or 
via an existing/new `init.py` file, in which you would add the line: 

    ```python
    nuke.pluginAddPath('/gizmos')
    ```
    
This should be enough to Install the suite of tools.


## Manual Installation
While the default installation is probably ideal for many users, it may not be the best for Studio Environments 
where tools need to be installed in a specific location or for users who already have their own Gizmo loader.

.gizmo files need to be added to the nuke plugin path. See instructions by the foundry: 
- [Loading Gizmos, Plugins, Scripts](
https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/loading_gizmos_plugins_scripts.html)
- [Custom Menus](
https://learn.foundry.com/nuke/content/comp_environment/configuring_nuke/custom_menus_toolbars.html)
 
Please note that a few gizmos are using callbacks to improve on user experience. These callbacks are defined in the 
file `/gizmos/spin_tools/spin_tools_callbacks.py` and would need to be set somewhere, though the tools will function 
without the callbacks as well.

## List of Tools

### 3D
#### Relight
Simpliflied relight node. Only requires a normal map to get started.

This node will not reproduce accurate lighting

### Color
#### Match_Black
Allows you to match Black.
#### Sup
Suppress.

## Thanks
Many of the tools in this collection are based on tools made available freely by the VFX community.

We would like to thank all of the members of the VFX community who made this possible, in particular:
- Frank Rueter, for creating and maintaining Nukepedia.
- Mads Hagbarth, for the innovating techniques shared online and the Blinkscript inspiration.

Please enjoy.
