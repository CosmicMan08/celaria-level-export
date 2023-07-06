import bpy
from bpy.types import (Panel, Operator, BlendData)

import numpy

def Create_Celaria_Object(color, type):
    bpy.ops.mesh.primitive_cube_add()

    bpy.context.object.name = "Celaria " + color + " Block"

    #bpy.ops.material.new()
    cel_mat = bpy.data.materials.new(name="Celaria " + color)
    cel_mat.use_nodes = True
    #cel_mat.name = "Celaria Mat"
    match type:
        case 0:
            cel_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 1, 1)
            cel_mat.diffuse_color = (1, 1, 1, 1)
        case 1:
            cel_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)
            cel_mat.diffuse_color = (1, 0, 0, 1)
        case 2:
            cel_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 1, 0, 1)
            cel_mat.diffuse_color = (0, 1, 0, 1)
        case 3:
            cel_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 1, 0, 1)
            cel_mat.diffuse_color = (1, 1, 0, 1)
        case 4:
            cel_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (0, 0.5, 1, 1)
            cel_mat.diffuse_color = (0, 0.5, 1, 1)
        case 5:
            cel_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)
            cel_mat.diffuse_color = (1, 0, 0, 1)
    bpy.context.active_object.data.materials.append(cel_mat)

    bpy.context.object["Object Type"] = 0
    bpy.context.object["Cube Color"] = type
    if type == 5:
        bpy.context.object["Checkpoint ID"] = 0

    bpy.context.object.lock_rotation[0] = True
    bpy.context.object.lock_rotation[1] = True

class OBJECT_MT_celaria_submenu(bpy.types.Menu):
    bl_idname = "OBJECT_MT_celaria_submenu"
    bl_label = "Celaria"
    bl_options = {'REGISTER', 'UNDO'}

    def draw(self, context):
        self.layout.operator("object.grey_celaria_block", text="Basic Block", icon="MESH_CUBE")
        self.layout.operator("object.red_celaria_block", text="Goal Block", icon="MESH_CUBE")
        self.layout.operator("object.green_celaria_block", text="Jump Block", icon="MESH_CUBE")
        self.layout.operator("object.yellow_celaria_block", text="Speed Block", icon="MESH_CUBE")
        self.layout.operator("object.blue_celaria_block", text="Ice Block", icon="MESH_CUBE")
        self.layout.operator("object.check_celaria_block", text="Checkpoint Block", icon="MESH_CUBE")
        self.layout.separator()
        self.layout.operator("object.celaria_player", text="Player Spawn", icon="ARMATURE_DATA")
        self.layout.operator("object.celaria_orb", text="Collectible Orb", icon="MESH_ICOSPHERE")
        self.layout.operator("object.celaria_barrier_wall", text="Barrier Wall", icon="MESH_PLANE")
        self.layout.operator("object.celaria_barrier_floor", text="Barrier Floor", icon="MESH_PLANE")
        #self.layout.separator()
        #self.layout.operator("object.celaria_sun", text="Sun", icon="LIGHT_SUN")
        #self.layout.operator("object.celaria_camera_start", text="Camera Start Point", icon="VIEW_CAMERA")
        #self.layout.operator("object.celaria_camera_end", text="Camera End Point", icon="EMPTY_AXIS")


def menu_func(self, context):
    self.layout.menu("OBJECT_MT_celaria_submenu", text="Celaria", icon="MESH_CUBE")
    
def register():
    bpy.utils.register_class(OBJECT_MT_celaria_submenu)

    bpy.utils.register_class(CelGreyBlock)
    bpy.utils.register_class(CelRedBlock)
    bpy.utils.register_class(CelGreenBlock)
    bpy.utils.register_class(CelYellowBlock)
    bpy.utils.register_class(CelBlueBlock)
    bpy.utils.register_class(CelCheckBlock)

    bpy.utils.register_class(CelPlayerSpawn)
    bpy.utils.register_class(CelOrb)
    bpy.utils.register_class(CelBarrierWall)
    bpy.utils.register_class(CelBarrierFloor)

    #bpy.utils.register_class(CelSun)
    #bpy.utils.register_class(CelCameraStart)
    #bpy.utils.register_class(CelCameraEnd)

    bpy.types.VIEW3D_MT_add.append(menu_func)
    
def unregister():
    bpy.utils.unregister_class(OBJECT_MT_celaria_submenu)

    bpy.utils.unregister_class(CelGreyBlock)
    bpy.utils.unregister_class(CelRedBlock)
    bpy.utils.unregister_class(CelGreenBlock)
    bpy.utils.unregister_class(CelYellowBlock)
    bpy.utils.unregister_class(CelBlueBlock)
    bpy.utils.unregister_class(CelCheckBlock)

    bpy.utils.unregister_class(CelPlayerSpawn)
    bpy.utils.unregister_class(CelOrb)
    bpy.utils.unregister_class(CelBarrierWall)
    bpy.utils.unregister_class(CelBarrierFloor)

    #bpy.utils.unregister_class(CelSun)
    #bpy.utils.unregister_class(CelCameraStart)
    #bpy.utils.unregister_class(CelCameraEnd)

    bpy.types.VIEW3D_MT_add.remove(menu_func)

#meta level stuff definitions
class CelSun(Operator):
    bl_description = (
        "Sun for Celaria Import/Export"
    )
    bl_idname = "object.celaria_sun"
    bl_label = "Celaria Sun"

    def execute(self, context):
        bpy.ops.object.light_add(type="SUN")

        bpy.context.object.name = "Celaria Sun"
        
        bpy.context.object["Misc. Celaria Type"] = 0

        bpy.context.object.lock_scale[0] = True
        bpy.context.object.lock_scale[1] = True
        bpy.context.object.lock_scale[2] = True
        return {'FINISHED'}

class CelCameraStart(Operator):
    bl_description = (
        "Camera Start Point for Celaria Import/Export"
    )
    bl_idname = "object.celaria_camera_start"
    bl_label = "Celaria Camera Start"

    def execute(self, context):
        bpy.ops.object.empty_add(type='CUBE')

        bpy.context.object.name = "Celaria Camera Start"
        
        bpy.context.object["Misc. Celaria Type"] = 1

        bpy.context.object.lock_scale[0] = True
        bpy.context.object.lock_scale[1] = True
        bpy.context.object.lock_scale[2] = True

        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        bpy.context.object.lock_rotation[2] = True
        return {'FINISHED'}

class CelCameraEnd(Operator):
    bl_description = (
        "Camera End Point for Celaria Import/Export"
    )
    bl_idname = "object.celaria_camera_end"
    bl_label = "Celaria Camera End"

    def execute(self, context):
        bpy.ops.object.empty_add(type='CUBE')
        bpy.ops.transform.resize(value=(1, 1, 0))

        bpy.context.object.name = "Celaria Camera End"
        
        bpy.context.object["Misc. Celaria Type"] = 2

        bpy.context.object.lock_scale[0] = True
        bpy.context.object.lock_scale[1] = True
        bpy.context.object.lock_scale[2] = True

        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        bpy.context.object.lock_rotation[2] = True
        return {'FINISHED'}

#object definitions
class CelPlayerSpawn(Operator):
    bl_description = (
        "Player Spawn for Celaria Import/Export"
    )
    bl_idname = "object.celaria_player"
    bl_label = "Celaria Player Spawn"

    def execute(self, context):
        bpy.ops.object.empty_add(type='PLAIN_AXES')

        bpy.context.object.name = "Celaria Player"
        
        bpy.context.object["Object Type"] = 2

        bpy.context.object.lock_scale[0] = True
        bpy.context.object.lock_scale[1] = True
        bpy.context.object.lock_scale[2] = True

        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        return {'FINISHED'}

class CelOrb(Operator):
    bl_description = (
        "Collectible Orb for Celaria Import/Export"
    )
    bl_idname = "object.celaria_orb"
    bl_label = "Celaria Orb"

    def execute(self, context):
        bpy.ops.mesh.primitive_ico_sphere_add()

        bpy.context.object.name = "Celaria Orb"

        bpy.ops.material.new()
        bpy.data.materials["Material"].node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0, 0, 1)

        bpy.context.object["Object Type"] = 1

        bpy.context.object.lock_scale[0] = True
        bpy.context.object.lock_scale[1] = True
        bpy.context.object.lock_scale[2] = True

        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        bpy.context.object.lock_rotation[2] = True
        return {'FINISHED'}

class CelBarrierWall(Operator):
    bl_description = (
        "Barriel Wall for Celaria Import/Export"
    )
    bl_idname = "object.celaria_barrier_wall"
    bl_label = "Celaria Barriel Wall"

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add(rotation = (numpy.deg2rad(90),0,0))
        bpy.ops.transform.resize(value=(16, 1, 16))

        bpy.context.object.name = "Celaria Barrier Wall"

        cel_mat = bpy.data.materials.new(name="Celaria Barrier Wall")
        cel_mat.use_nodes = True
        cel_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0.5, 0, 0.5)
        cel_mat.diffuse_color = (1, 0.5, 0, 0.5)
        bpy.context.active_object.data.materials.append(cel_mat)

        bpy.context.object["Object Type"] = 3

        bpy.context.object.lock_scale[2] = True

        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        return {'FINISHED'}

class CelBarrierFloor(Operator):
    bl_description = (
        "Barriel Floor for Celaria Import/Export"
    )
    bl_idname = "object.celaria_barrier_floor"
    bl_label = "Celaria Barriel Floor"

    def execute(self, context):
        bpy.ops.mesh.primitive_plane_add()
        bpy.ops.transform.resize(value=(16, 16, 1))

        bpy.context.object.name = "Celaria Barrier Floor"

        cel_mat = bpy.data.materials.new(name="Celaria Barrier Floor")
        cel_mat.use_nodes = True
        cel_mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = (1, 0.5, 0, 0.5)
        cel_mat.diffuse_color = (1, 0.5, 0, 0.5)
        bpy.context.active_object.data.materials.append(cel_mat)

        bpy.context.object["Object Type"] = 4

        bpy.context.object.lock_scale[2] = True

        bpy.context.object.lock_rotation[0] = True
        bpy.context.object.lock_rotation[1] = True
        return {'FINISHED'}

#block definitions
#i hate that i did it like this but i don't know how else 

class CelGreyBlock(Operator):
    bl_description = (
        "Basic Block for Celaria Import/Export"
    )
    bl_idname = "object.grey_celaria_block"
    bl_label = "Grey Celaria Block"

    def execute(self, context):
        Create_Celaria_Object("Grey", 0)
        return {'FINISHED'}

class CelRedBlock(Operator):
    bl_description = (
        "Goal Block for Celaria Import/Export"
    )
    bl_idname = "object.red_celaria_block"
    bl_label = "Red Celaria Block"

    def execute(self, context):
        Create_Celaria_Object("Red", 1)
        return {'FINISHED'}

class CelGreenBlock(Operator):
    bl_description = (
        "Jump Block for Celaria Import/Export"
    )
    bl_idname = "object.green_celaria_block"
    bl_label = "Green Celaria Block"

    def execute(self, context):
        Create_Celaria_Object("Green", 2)
        return {'FINISHED'}

class CelYellowBlock(Operator):
    bl_description = (
        "Speed Block for Celaria Import/Export"
    )
    bl_idname = "object.yellow_celaria_block"
    bl_label = "Yellow Celaria Block"

    def execute(self, context):
        Create_Celaria_Object("Yellow", 3)
        return {'FINISHED'}

class CelBlueBlock(Operator):
    bl_description = (
        "Ice Block for Celaria Import/Export"
    )
    bl_idname = "object.blue_celaria_block"
    bl_label = "Blue Celaria Block"

    def execute(self, context):
        Create_Celaria_Object("Blue", 4)
        return {'FINISHED'}

class CelCheckBlock(Operator):
    bl_description = (
        "Checkpoint Block for Celaria Import/Export"
    )
    bl_idname = "object.check_celaria_block"
    bl_label = "Checkpoint Celaria Block"

    def execute(self, context):
        Create_Celaria_Object("Checkpoint", 5)
        return {'FINISHED'}