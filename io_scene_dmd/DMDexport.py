#-------------------------------------------------------------------------------
#
#       Модуль экспорта DMD-модели в Blender
#       (c) РГУПС, ВЖД 06/12/2018
#       Разработал: Притыкин Д.Е.
#
#-------------------------------------------------------------------------------
import bpy
import bmesh
import os
from .DMD import MultyMesh

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Exporter:

    def __init__(self):
        self.filepath = ""

    def exportModel(self, path):

        self.filepath = path

        dmd_model = MultyMesh()

        objs = bpy.context.selected_objects

        for obj in objs:

            if obj.type == 'MESH':

                from .DMD import Mesh

                print("Process object: " + obj.name)

                md = obj.data

                bpy.ops.object.mode_set(mode='EDIT')
                bm = bmesh.from_edit_mesh(md)
                bmesh.ops.triangulate(bm, faces=bm.faces[:], quad_method=0, ngon_method=0)
                bmesh.update_edit_mesh(md, True)
                bpy.ops.object.mode_set(mode='OBJECT')

                mesh = Mesh()

                for vertex in md.vertices:
                    mesh.vertices.append(list(vertex.co))
                    mesh.vertex_count += 1

                for face in md.polygons:
                    mesh.faces.append(list(face.vertices))
                    mesh.faces_count += 1

                dmd_model.meshes.append(mesh)

        dmd_model.writeToFile(path, dmd_model)