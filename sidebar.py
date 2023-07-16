import bpy
from bpy.types import (Panel, Operator)

import struct
import ctypes
import sys
import re
import numpy
import binascii

class CelImport(Operator):
    bl_description = (
        "Imports Celaria Level files into Blender"
    )
    bl_idname = "object.cel_import"
    bl_label = "Celaria Import Operator"

    def execute(self, context):
        self.report({'INFO'}, ":3")
        return {'FINISHED'}

class CelExport(Operator):
    bl_description = (
        "Exports your Blender scene to a Celaria Level File"
    )
    bl_idname = "object.cel_export"
    bl_label = "Export .ecmap"

    filepath: bpy.props.StringProperty(subtype="FILE_PATH")

    def invoke(self, context, event):
        
        bpy.types.WindowManager.fileselect_add(self)
        return {'RUNNING_MODAL'}

    def execute(self, context):
        level_data = []
        camera_start_pos = [0, 0, 0]
        camera_end_pos = [0, 0, 0]

        for ob in bpy.data.objects:
            #self.report({'INFO'}, ob.name)
            try:
                match ob["Object Type"]:
                    case 0: #Cube
                        center = get_center(ob.data.vertices)

                        self.report({'INFO'}, str(rotate_co(center[0],center[2],ob.rotation_euler[2])))

                        object_data = [0]
                        object_data.append(ob["Cube Color"])
                        object_data.append([ #I HATE MATH !!!!!!!!!!!!!!!!!!!!!!! this used to be SOOOOO simple but nOOOOOO you gotta do all this stuff to account for offset centers akld;sfjghfsrtihuoistfrhuk
                            -ob.location[0]-(rotate_co(center[0]*ob.scale[0], center[1]*ob.scale[1], ob.rotation_euler[2])[0]), 
                            ob.location[1]+(rotate_co(center[0]*ob.scale[0], center[1]*ob.scale[1], ob.rotation_euler[2])[1]), 
                            ob.location[2]+(center[2]*ob.scale[2])
                            ])
                        object_data.append([ob.dimensions[0], ob.dimensions[1], ob.dimensions[2]])

                        #self.report({'INFO'}, str(get_center(ob.data.vertices)))

                        object_data.append(numpy.rad2deg(ob.rotation_euler[2]) % 360)
                        if ob["Cube Color"] == 5:
                            object_data.append(ob["Checkpoint ID"])

                        level_data.append(object_data)
                    case 1: #Orb
                        object_data = [1]
                        object_data.append([-ob.location[0],ob.location[1],ob.location[2]])

                        level_data.append(object_data)
                    case 2: #Player
                        object_data = [2]
                        #object_data = [0] #unused byte :3
                        object_data.append([-ob.location[0],ob.location[1],ob.location[2]])

                        object_data.append(numpy.rad2deg(ob.rotation_euler[2]) % 360)

                        level_data.append(object_data)
                    case 3: #Wall
                        center = get_center(ob.data.vertices)

                        object_data = [3]
                        object_data.append([ #I HATE MATH !!!!!!!!!!!!!!!!!!!!!!! this used to be SOOOOO simple but nOOOOOO you gotta do all this stuff to account for offset centers akld;sfjghfsrtihuoistfrhuk
                            -ob.location[0]-(rotate_co(center[0]*ob.scale[0],center[2]*ob.scale[2],ob.rotation_euler[2])[0]), 
                            ob.location[1]+(rotate_co(center[0]*ob.scale[0],center[2]*ob.scale[2],ob.rotation_euler[2])[1]), 
                            ob.location[2]+(center[1]*ob.scale[1])
                            ])
                        object_data.append([ob.dimensions[0], ob.dimensions[1]])

                        object_data.append(numpy.rad2deg(ob.rotation_euler[2]) % 360)

                        level_data.append(object_data)
                    case 4: #Floor
                        center = get_center(ob.data.vertices)

                        object_data = [4]
                        object_data.append([ #I HATE MATH !!!!!!!!!!!!!!!!!!!!!!! this used to be SOOOOO simple but nOOOOOO you gotta do all this stuff to account for offset centers akld;sfjghfsrtihuoistfrhuk
                            -ob.location[0]-(rotate_co(center[0]*ob.scale[0], center[1]*ob.scale[1], ob.rotation_euler[2])[0]), 
                            ob.location[1]+(rotate_co(center[0]*ob.scale[0], center[1]*ob.scale[1], ob.rotation_euler[2])[1]), 
                            ob.location[2]+(center[2]*ob.scale[2])
                            ])
                        object_data.append([ob.dimensions[0], ob.dimensions[1]])

                        object_data.append(numpy.rad2deg(ob.rotation_euler[2]) % 360)

                        level_data.append(object_data)
            except:
                """ try:
                    match ob["Misc. Celaria Type"]:
                        case 0:
                            print("sobbing")
                        case 1:
                            camera_start_pos = [-ob.location[0],ob.location[1],ob.location[2]]
                        case 2:
                            camera_end_pos = [-ob.location[0],ob.location[1],ob.location[2]]
                except: """
                print("that's not a celaria block!")
        #self.report({'INFO'}, ">:3")
        #self.report({'INFO'}, str(camera_start_pos))
        #self.report({'INFO'}, str(camera_end_pos))
        level_hex = [0x63, 0x65, 0x6C, 0x61, 0x72, 0x69, 0x61, 0x5F, 0x65, 0x64, 0x69, 0x04] # celaria_edi and then the version number (4)

        blender_name = re.sub(r'\W+', '', bpy.path.basename(bpy.context.blend_data.filepath.replace(".blend","")))
        level_hex.append(len(blender_name))     #length of name
        for i in blender_name:
            level_hex.append(ord(i))        #name letter by letter
        
        level_hex.append(0x00)         #unused byte :p
        level_hex.append(0x01)         #unused byte ::p
        
        for i in [0x00, 0x00, 0x34, 0x42, 0x00, 0x00, 0x5C, 0x42#,                 #sun position
        #0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x24, 0x40, 0x00, 0x00, 0x00, 0x00, 
        #0x00, 0x00, 0x24, 0x40, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x24, 0x40, 
        #0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 
        #0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]:
        ]:
            level_hex.append(i)

        level_hex.append(double2bin(camera_start_pos[0]))         #preview cam
        level_hex.append(double2bin(camera_start_pos[1]))
        level_hex.append(double2bin(camera_start_pos[2]))
        level_hex.append(double2bin(camera_end_pos[0]))
        level_hex.append(double2bin(camera_end_pos[1]))
        level_hex.append(double2bin(camera_end_pos[2]))

        level_hex.append(f"{swap32(ctypes.c_uint(len(level_data)).value):0{8}x}")       #object count

        for i in level_data:
            level_hex.append(i[0])
            match i[0]:
                case 0: #blocks
                    level_hex.append(i[1])

                    level_hex.append(double2bin(i[2][0]))
                    level_hex.append(double2bin(i[2][1]))
                    level_hex.append(double2bin(i[2][2]))

                    level_hex.append(double2bin(i[3][0]))
                    level_hex.append(double2bin(i[3][1]))
                    level_hex.append(double2bin(i[3][2]))
                    
                    level_hex.append(single2bin(i[4]))

                    if i[1] == 5:
                        level_hex.append(i[5])
                case 1: #sphere
                    level_hex.append(double2bin(i[1][0]))
                    level_hex.append(double2bin(i[1][1]))
                    level_hex.append(double2bin(i[1][2]))
                case 2: #player start
                    level_hex.append(0x00) # unused byte :p

                    level_hex.append(double2bin(i[1][0]))
                    level_hex.append(double2bin(i[1][1]))
                    level_hex.append(double2bin(i[1][2]))

                    level_hex.append(single2bin(i[2]))
                case 3: #barrier wall
                    level_hex.append(0x00) # unused byte :p

                    level_hex.append(double2bin(i[1][0]))
                    level_hex.append(double2bin(i[1][1]))
                    level_hex.append(double2bin(i[1][2]))

                    level_hex.append(double2bin(i[2][0]))
                    level_hex.append(double2bin(i[2][1]))
                    
                    level_hex.append(single2bin(i[3]))
                case 4: #barrier floor
                    level_hex.append(0x00) # unused byte :p

                    level_hex.append(double2bin(i[1][0]))
                    level_hex.append(double2bin(i[1][1]))
                    level_hex.append(double2bin(i[1][2]))

                    level_hex.append(double2bin(i[2][0]))
                    level_hex.append(double2bin(i[2][1]))
                    
                    level_hex.append(single2bin(i[3]))

        #self.report({'INFO'}, str(level_hex))

        level_hexreal = ""
        for i in level_hex:
            if isinstance(i, str):
                level_hexreal += i
            else:
                level_hexreal += f"{i:#0{4}x}"
        level_hexreal = level_hexreal.replace("0x","")

        #self.report({'INFO'}, str(level_hexreal))

        file = open(self.filepath, 'wb')
        file.write(binascii.unhexlify(level_hexreal))

        self.report({'INFO'}, "Level successfully exported!")

        return {'FINISHED'}

class IOPanel(Panel):
    bl_idname = "CELARIA_io"
    bl_label = "Celaria Import/Export"
    bl_region_type = "UI"
    bl_space_type = "VIEW_3D"
    bl_category = "Celaria"

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        #col.operator(CelImport.bl_idname, text="Import", icon="FILEBROWSER")
        col.operator(CelExport.bl_idname, text="Export", icon="FILEBROWSER")

def get_center(vertices):
    average_position = [0,0,0]

    for i in vertices:
        average_position[0] += i.co[0]
        average_position[1] += i.co[1]
        average_position[2] += i.co[2]

    average_position[0] /= len(vertices)
    average_position[1] /= len(vertices)
    average_position[2] /= len(vertices)

    return(average_position)

def rotate_co(x,y,dir):
    return [x*numpy.cos(dir) - y*numpy.sin(dir), x*numpy.sin(dir) + y*numpy.cos(dir)]

def double2bin(fl):
    return (f"{swap64(ctypes.c_uint64.from_buffer(ctypes.c_double(fl)).value):0{16}x}")
    #return (ctypes.c_uint64.from_buffer(ctypes.c_double(fl)).value)

def single2bin(fl):
    return (f"{swap32(ctypes.c_uint32.from_buffer(ctypes.c_float(fl)).value):0{8}x}")
    #return (ctypes.c_uint32.from_buffer(ctypes.c_float(fl)).value)

def swap32(i):
    return struct.unpack("<I", struct.pack(">I", i))[0]
    
def swap64(i):
    return struct.unpack("<Q", struct.pack(">Q", i))[0]

def register():
    #bpy.utils.register_class(CelImport)
    bpy.utils.register_class(CelExport)
    #bpy.utils.register_class(CelExportPath)
    bpy.utils.register_class(IOPanel)

def unregister():
    #bpy.utils.unregister_class(CelImport)
    bpy.utils.unregister_class(CelExport)
    #bpy.utils.unregister_class(CelExportPath)
    bpy.utils.unregister_class(IOPanel)
