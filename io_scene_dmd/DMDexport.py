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

                if obj.material_slots:
                    mat = obj.material_slots[0].material

                    if mat.texture_slots:
                        dmd_model.texture_present = True

                        for f in md.polygons:
                            tex_face = []
                            for uv_layer in md.uv_layers:
                                for i in f.loop_indices:
                                    tex_face.append(i)
                                    uv = uv_layer.data[i].uv
                                    texel = [uv[0], uv[1], 0.0]
                                    dmd_model.tex_vertices.append(texel)
                                    dmd_model.tex_v_count += 1;

                                dmd_model.tex_faces.append(tex_face)
                                dmd_model.tex_f_count += 1;

        dmd_model.writeToFile(path, dmd_model)