bl_info = {
    "name": "Snap to Z0",
    "author": "OpenAI",
    "version": (1, 0, 0),
    "blender": (4, 0, 0),
    "location": "View3D > Sidebar > Tool > Snap to Z0",
    "description": "Rotate the active face to the build plate and move it to Z=0",
    "category": "3D View",
}

import bpy
import bmesh
from mathutils import Vector, Matrix


def get_active_face_bmesh(obj):
    if obj is None or obj.type != 'MESH':
        return None, "Active object must be a mesh."

    if bpy.context.mode != 'EDIT_MESH':
        return None, "Must be in Edit Mode."

    bm = bmesh.from_edit_mesh(obj.data)
    bm.faces.ensure_lookup_table()

    face = bm.faces.active
    if face is None:
        return None, "No active face. Select a face and make it active."

    if not face.select:
        return None, "The active face must also be selected."

    return face, None


class OBJECT_OT_snap_face_to_z0(bpy.types.Operator):
    bl_idname = "object.snap_face_to_z0"
    bl_label = "Snap to Z0"
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
        face, error = get_active_face_bmesh(obj)

        if error:
            self.report({'WARNING'}, error)
            return {'CANCELLED'}

        # Local-space face center
        local_center = face.calc_center_median()

        # World-space center
        world_center = obj.matrix_world @ local_center

        # Proper normal transform for world space
        normal_matrix = obj.matrix_world.to_3x3().inverted().transposed()
        world_normal = (normal_matrix @ face.normal).normalized()

        target_normal = Vector((0.0, 0.0, -1.0))

        # If the face normal is already aligned, this will be identity
        rotation_quat = world_normal.rotation_difference(target_normal)
        rotation_matrix = rotation_quat.to_matrix().to_4x4()

        # Rotate object around the selected face center in world space
        transform = (
            Matrix.Translation(world_center) @
            rotation_matrix @
            Matrix.Translation(-world_center)
        )

        obj.matrix_world = transform @ obj.matrix_world
        context.view_layer.update()

        # Recompute face vertex world positions after rotation
        rotated_world_verts = [obj.matrix_world @ v.co for v in face.verts]

        # Since the face should now be horizontal, move it so it sits on Z=0
        min_z = min(v.z for v in rotated_world_verts)
        obj.location.z -= min_z
        context.view_layer.update()

        self.report({'INFO'}, "Active face snapped to Z=0.")
        return {'FINISHED'}


class VIEW3D_PT_snap_to_z0(bpy.types.Panel):
    bl_label = "Snap to Z0"
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