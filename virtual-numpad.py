bl_info = {
    "name": "Virtual Numpad for Blender",
    "author": "Benoît G. & ChatGPT",
    "version": (1, 3),
    "blender": (4, 4, 0),
    "location": "View3D > Sidebar > Tool Tab",
    "description": "A virtual numpad for folks that don't have one.  Viewport > Tools tab.",
    "category": "3D View",
}

import bpy
import math

class VIEW3D_PT_virtual_numpad(bpy.types.Panel):
    bl_label = "Virtual Numpad"
    bl_idname = "VIEW3D_PT_virtual_numpad"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        col = layout.column(align=True)

        # First row
        row = col.row(align=True)
        op = row.operator("view3d.view_axis", text="7\n↖")
        op.type = 'TOP'
        op = row.operator("view3d.view_orbit_updown", text="8\n↑")
        op.direction = 'UP'
        row.operator("view3d.view_opposite", text="9\n⇄")

        # Second row
        row = col.row(align=True)
        op = row.operator("view3d.view_orbit_leftright", text="4\n←")
        op.direction = 'LEFT'
        row.operator("view3d.view_persportho", text="5")
        op = row.operator("view3d.view_orbit_leftright", text="6\n→")
        op.direction = 'RIGHT'

        # Third row
        row = col.row(align=True)
        op = row.operator("view3d.view_axis", text="1\n↙")
        op.type = 'FRONT'
        op = row.operator("view3d.view_orbit_updown", text="2\n↓")
        op.direction = 'DOWN'
        op = row.operator("view3d.view_axis", text="3\n→")
        op.type = 'RIGHT'

        # Fourth row
        row = col.row(align=True)
        cam_op = row.operator("view3d.view_camera", text="0\nCam")
        row.operator("view3d.view_selected", text=".")

        # Fifth row (misc numpad functions)
        row = col.row(align=True)
        row.operator("view3d.localview", text="/")
        row.operator("view3d.virtual_zoom", text="+").delta = 1
        row.operator("view3d.virtual_zoom", text="-").delta = -1

# Custom Operators

class VIEW3D_OT_opposite_view(bpy.types.Operator):
    """View from opposite direction (Numpad 9)"""
    bl_idname = "view3d.view_opposite"
    bl_label = "Opposite View"

    def execute(self, context):
        bpy.ops.view3d.view_orbit(angle=math.pi, type='ORBITLEFT')
        return {'FINISHED'}

class VIEW3D_OT_orbit_updown(bpy.types.Operator):
    """Orbit Up/Down like Numpad 8/2"""
    bl_idname = "view3d.view_orbit_updown"
    bl_label = "Orbit Up/Down"
    direction: bpy.props.EnumProperty(
        items=[
            ('UP', "Up", ""),
            ('DOWN', "Down", "")
        ]
    )

    def execute(self, context):
        angle = math.radians(15)
        direction = 'ORBITUP' if self.direction == 'UP' else 'ORBITDOWN'
        bpy.ops.view3d.view_orbit(angle=angle, type=direction)
        return {'FINISHED'}

class VIEW3D_OT_orbit_leftright(bpy.types.Operator):
    """Orbit Left/Right like Numpad 4/6"""
    bl_idname = "view3d.view_orbit_leftright"
    bl_label = "Orbit Left/Right"
    direction: bpy.props.EnumProperty(
        items=[
            ('LEFT', "Left", ""),
            ('RIGHT', "Right", "")
        ]
    )

    def execute(self, context):
        angle = math.radians(15)
        direction = 'ORBITLEFT' if self.direction == 'LEFT' else 'ORBITRIGHT'
        bpy.ops.view3d.view_orbit(angle=angle, type=direction)
        return {'FINISHED'}

class VIEW3D_OT_virtual_zoom(bpy.types.Operator):
    """Zoom in/out like Numpad + / -"""
    bl_idname = "view3d.virtual_zoom"
    bl_label = "Virtual Zoom"
    delta: bpy.props.IntProperty()

    def execute(self, context):
        for _ in range(abs(self.delta)):
            bpy.ops.view3d.zoom(delta=self.delta)
        return {'FINISHED'}

classes = (
    VIEW3D_PT_virtual_numpad,
    VIEW3D_OT_opposite_view,
    VIEW3D_OT_orbit_updown,
    VIEW3D_OT_orbit_leftright,
    VIEW3D_OT_virtual_zoom,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
