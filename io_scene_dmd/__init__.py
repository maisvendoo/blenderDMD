#-------------------------------------------------------------------------------
#
#       Дополнение для работы с моделями DMD для ZDSimulator
#       (c) РГУПС, ВЖД 18/07/2018
#       Разработал: Притыкин Д.Е.
#
#-------------------------------------------------------------------------------

bl_info = {
    "name": "Importer/Exporter DGLEngine DMD models",
    "category": "Import-Export",
    "author": "Dmitry Pritykin",
    "version": (0, 1, 0),
    "blender": (2, 79, 0)
}

import bpy

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class DMDImporter(bpy.types.Operator):
    """DMD models importer"""
    bl_idname = "import_scene.dmd"
    bl_label = "DGLEngine DMD model (*.dmd)"
    bl_options = {'REGISTER', 'UNDO'}

    filepath = bpy.props.StringProperty(subtype='FILE_PATH')

    #---------------------------------------------------------------------------
    #
    #---------------------------------------------------------------------------
    def execute(self, context):
        from .DMDimport import Importer
        dmd_loader = Importer()
        dmd_loader.load(self.filepath)

        return {'FINISHED'}

    #---------------------------------------------------------------------------
    #
    #---------------------------------------------------------------------------
    def invoke(self, context, event):
        context.window_manager.fileselect_add(self)
        return {'RUNNING_MODAL'}

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def menu_import(self, context):
    self.layout.operator(DMDImporter.bl_idname, text=DMDImporter.bl_label)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def register():
    bpy.types.INFO_MT_file_import.append(menu_import)
    bpy.utils.register_class(DMDImporter)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
def unregister():
    bpy.types.INFO_MT_file_import.remove(menu_import)
    bpy.utils.unregister_class(DMDImporter)

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
if __name__ == "__main__":
    register()
