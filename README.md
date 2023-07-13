# celaria-level-export
 A Blender addon for creating and exporting levels to Celaria.

 ![GIF showing a level made in Blender being exported to Celaria.](https://github.com/CosmicMan08/celaria-level-export/blob/main/celaria%20level%20export.gif?raw=true)

 This addon allows you to export your Blender scene to Celaria using several Celaria specific objects in the add menu.

 You can move around, scale, and rotate these blocks; **you cannot edit their mesh in edit mode** however. All changes **must** be done in Object Mode for them to display properly in game.

 ![The add menu in Blender with several Celaria objects.](https://github.com/CosmicMan08/celaria-level-export/blob/main/add%20menu.png?raw=true)

 You can export your scene with the Celaria submenu at the sidebar.

 ![The Celaria section of the sidebar, featuring an "Export" button.](https://github.com/CosmicMan08/celaria-level-export/blob/main/sidebar.png?raw=true)

 Pressing the export menu brings up the file explorer, where it'll let you choose where to save your file 	**(Make sure that the file's extension is ".ecmap"!)** Upon pressing "Export" you should find the exported level in the chosen directory, which you can then open up in Celaria's editor to verify.

### THINGS TO NOTE:

- The red block is functionally two seperate blocks, a goal block and a checkpoint block. I made sure to keep account of this in the addon, and you need to keep account of it when making your levels.

- Checkpoint blocks also store their checkpoint ID, which is the order you need to hit them in. I didn't implement anything to set the ID's automatically, so **be sure to set the ID of each checkpoint in Object Properties>Custom Properties**

- I also didn't implement the preview cam or sun position... i tried to but i couldn't get the preview cam working ingame and i just had no idea where to start with converting the sun's angle in blender to Celaria's format.

- dont use blue blocks. not because theyre broken in the addon or anything, i just hate them and the world would be a better place without them
