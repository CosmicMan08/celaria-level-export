bl_info = {
        "name": "Celaria Level Editor",
        "description": "Tool for importing, editing, and exporting levels for Celaria.",
        "author": "CosmicMan08",
        "version": (1, 1),
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
    from . import sidebar
    from . import objects
    properties.register()
    sidebar.register()
    objects.register()

def unregister():
    from . import properties
    from . import sidebar
    from . import objects
    properties.unregister()
    sidebar.unregister()
    objects.unregister()

if __name__ == '__main__':
    register()
