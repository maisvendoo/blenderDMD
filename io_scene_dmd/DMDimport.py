#-------------------------------------------------------------------------------
#
#       Модуль импорта DMD-модели в Blender
#       (c) РГУПС, ВЖД 19/07/2018
#       Разработал: Притыкин Д.Е.
#
#-------------------------------------------------------------------------------
import bpy
import bmesh
import os
from .DMD import MultyMesh

#---------------------------------------------------------------------------
#
#---------------------------------------------------------------------------
def getFileName(path):
    basename = os.path.basename(path)
    tmp = basename.split(".")
    return tmp[0]

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Importer:

    def __init__(self):

        self.dmd = MultyMesh()

    #---------------------------------------------------------------------------
    #
    #---------------------------------------------------------------------------
    def load(self, filepath):
        self.dmd.loadFromFile(filepath)

        for m_idx, m in enumerate(self.dmd.meshes):

            obj_name = getFileName(filepath)
            print("Process new model: ", obj_name)

            md = bpy.data.meshes.new(obj_name + "-" + str(m_idx))
            print("Mesh name: ", md.name)
            print("New mesh created...OK")
            md.from_pydata(m.vertices, [], m.faces)
            print("Loaded data to mesh...OK")
            md.update(calc_edges=True)
            print("Mesh update...OK")

            obj = bpy.data.objects.new(md.name, md)
            print("New scene object creation...OK")
            bpy.context.scene.objects.link(obj)
            print("Link object to scene...OK")


