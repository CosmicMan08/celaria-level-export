bl_info = {
        "name": "Celaria Level Editor",
        "description": "Tool for importing, editing, and exporting levels for Celaria.",
        "author": "CosmicMan08",
        "version": (1, 0),
        "blender": (3, 3, 0),
        "location": "3DView",
        #"warning": "", # used for warning icon and text in add-ons panel
        #"wiki_url": "http://my.wiki.url",
        #"tracker_url": "http://my.bugtracker.url",
        "support": "COMMUNITY",
        "category": "Import-Export"
        }

import bpy

def register():
    from . import properties
    from . import ui
    from . import objects
    properties.register()
    ui.register()
    objects.register()

def unregister():
    from . import properties
    from . import ui
    from . import objects
    properties.unregister()
    ui.unregister()
    objects.unregister()

if __name__ == '__main__':
    register()
