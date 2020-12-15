bl_info = {
    "name" : "Box_Sim",
    "author" : "Dirk Holst",
    "description" : "",
    "blender" : (2, 82, 7),
    "version" : (0, 0, 1),
    "location" : "VIEW3D",
    "warning" : "",
    "category" : "Generic"
}

import bpy

from . interface import OBJ_PT_maininterface

from . box_sim_4 import Box_sim_4_main

classes = [OBJ_PT_maininterface, Box_sim_4_main]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "main":
     register()
