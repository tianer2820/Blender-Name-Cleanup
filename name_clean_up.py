bl_info = {
    "name": "Name Clean Up",
    "author": "tianer2820",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "F3 Search Menu > cleanup",
    "description": "Easily reformat object names, mesh names and image names",
    "warning": "",
    "doc_url": "",
    "category": "User Interface",
}




import bpy
from bpy import data as D
from mathutils import *
from math import *



def format_name(name: str) -> str:
    name = name.lower()
    name = name.replace('-', ' ')
    name = name.replace('_', ' ')
    name = name.strip()
    last_c = None
    new_name = ''
    for c in name:
        if not last_c is None:
            if c == last_c == ' ':
                continue
        new_name += c
        last_c = c
    return new_name



class LowerObjectNames(bpy.types.Operator):
    """Rename all selected objects to lower case"""
    bl_idname = "cleanup.lower_object_names"
    bl_label = "Lower object names"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return len(context.view_layer.objects.selected) > 0

    def execute(self, context):
        self.all_lower(context)
        return {'FINISHED'}
    
    def all_lower(self, context: bpy.types.Context):
        count = 0
        objs = context.view_layer.objects.selected
        for obj in objs:
            obj: bpy.types.Object
            name = obj.name
            new_name = format_name(name)
            if obj.name != new_name:
                count += 1
            obj.name = new_name

        self.report({'INFO'}, 'renamed {} objects'.format(count))


class LowerImageNames(bpy.types.Operator):
    """Rename all images to lower case"""
    bl_idname = "cleanup.lower_image_names"
    bl_label = "Lower image names"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return True

    def execute(self, context):
        self.lower_img_names(context)
        return {'FINISHED'}
    
    def lower_img_names(self, context: bpy.types.Context):
        count = 0
        images = context.blend_data.images
        for img in images:
            img: bpy.types.Image
            name = img.name
            new_name = format_name(name)
            if img.name != new_name:
                count += 1
            img.name = new_name
        self.report({'INFO'}, 'renamed {} materials'.format(count))


class SyncMeshNames(bpy.types.Operator):
    """Rename all selected objects to lower case"""
    bl_idname = "cleanup.sync_mesh_names"
    bl_label = "Sync mesh names"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return len(context.view_layer.objects.selected) > 0

    def execute(self, context):
        self.sync_mesh_names(context)
        return {'FINISHED'}
    
    def sync_mesh_names(self, context: bpy.types.Context):
        count = 0
        objs = context.view_layer.objects.selected
        for obj in objs:
            obj: bpy.types.Object
            name = obj.name
            mesh = obj.data
            if mesh.users == 1:
                if mesh.name != name:
                    count += 1
                mesh.name = name
        self.report({'INFO'}, 'renamed {} meshs'.format(count))


class SyncMaterialNames(bpy.types.Operator):
    """Rename all selected objects to lower case"""
    bl_idname = "cleanup.sync_material_names"
    bl_label = "Sync material names"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return len(context.view_layer.objects.selected) > 0

    def execute(self, context):
        self.sync_material_names(context)
        return {'FINISHED'}
    
    def sync_material_names(self, context: bpy.types.Context):
        count = 0
        objs = context.view_layer.objects.selected
        for obj in objs:
            obj: bpy.types.Object
            name = obj.name
            mat_slots = obj.material_slots
            for slot in mat_slots:
                slot: bpy.types.MaterialSlot
                if slot.material is not None:
                    if slot.material.users == 1:
                        if slot.material.name != name:
                            count += 1
                        slot.material.name = name
        self.report({'INFO'}, 'renamed {} materials'.format(count))


class DoAllFormattings(bpy.types.Operator):
    """Do all formattings"""
    bl_idname = "cleanup.do_all_formattings"
    bl_label = "Do all formattings"

    @classmethod
    def poll(cls, context: bpy.types.Context):
        return len(context.view_layer.objects.selected) > 0

    def execute(self, context):
        self.do_all(context)
        return {'FINISHED'}
    
    def do_all(self, context: bpy.types.Context):
        bpy.ops.cleanup.lower_object_names()
        bpy.ops.cleanup.lower_image_names()
        bpy.ops.cleanup.sync_mesh_names()
        bpy.ops.cleanup.sync_material_names()



classes = [
    LowerObjectNames,
    SyncMeshNames,
    SyncMaterialNames,
    LowerImageNames,
    DoAllFormattings,
]

def register():
    for c in classes:
        bpy.utils.register_class(c)


def unregister():
    for c in reversed(classes):
        bpy.utils.unregister_class(c)


if __name__ == "__main__":
    register()
