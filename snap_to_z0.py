bl_info = {
    "name": "Snap to Z=0",
    "author": "Andrew Sink",
    "version": (1, 0, 1),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tool > Snap to Z=0",
    "description": "Rotate the active face to the build plate and place it at Z=0",
    "category": "3D View",
}

import bpy
import bmesh
from mathutils import Vector, Matrix


class OBJECT_OT_snap_face_to_z0(bpy.types.Operator):
    bl_idname = "object.snap_face_to_z0"
    bl_label = "Snap to Z=0"
    bl_description = "Rotate the active face to face downward and move it to Z=0"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return (
            obj is not None and
            obj.type == 'MESH' and
            context.mode == 'EDIT_MESH'
        )

    def execute(self, context):
        obj = context.active_object

        if obj is None or obj.type != 'MESH':
            self.report({'WARNING'}, "Active object must be a mesh.")
            return {'CANCELLED'}

        if context.mode != 'EDIT_MESH':
            self.report({'WARNING'}, "Must be in Edit Mode.")
            return {'CANCELLED'}

        bm = bmesh.from_edit_mesh(obj.data)
        bm.faces.ensure_lookup_table()

        face = bm.faces.active
        if face is None:
            self.report({'WARNING'}, "No active face. Select a face and make it active.")
            return {'CANCELLED'}

        if not face.select:
            self.report({'WARNING'}, "The active face must also be selected.")
            return {'CANCELLED'}

        local_center = face.calc_center_median().copy()
        local_normal = face.normal.copy()
        local_verts = [v.co.copy() for v in face.verts]

        world_center = obj.matrix_world @ local_center

        normal_matrix = obj.matrix_world.to_3x3().inverted().transposed()
        world_normal = (normal_matrix @ local_normal).normalized()

        target_normal = Vector((0.0, 0.0, -1.0))

        rotation_quat = world_normal.rotation_difference(target_normal)
        rotation_matrix = rotation_quat.to_matrix().to_4x4()

        transform = (
            Matrix.Translation(world_center) @
            rotation_matrix @
            Matrix.Translation(-world_center)
        )

        obj.matrix_world = transform @ obj.matrix_world
        context.view_layer.update()

        rotated_world_verts = [obj.matrix_world @ co for co in local_verts]

        min_z = min(v.z for v in rotated_world_verts)
        obj.location.z -= min_z
        context.view_layer.update()

        self.report({'INFO'}, "Active face snapped to Z=0.")
        return {'FINISHED'}


class VIEW3D_PT_snap_to_z0(bpy.types.Panel):
    bl_label = "Snap to Z=0"
    bl_idname = "VIEW3D_PT_snap_to_z0"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    @classmethod
    def poll(cls, context):
        obj = context.active_object
        return obj is not None and obj.type == 'MESH'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)
        col.label(text="3D Print Placement")
        col.operator("object.snap_face_to_z0", icon='TRIA_DOWN_BAR')


classes = (
    OBJECT_OT_snap_face_to_z0,
    VIEW3D_PT_snap_to_z0,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
