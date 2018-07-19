#-------------------------------------------------------------------------------
#
#       Класс для работы с моделями DMD
#       (c) РГУПС, ВЖД 18/07/2018
#       Разработал: Притыкин Д.Е.
#
#-------------------------------------------------------------------------------

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class FileContainer:

    def __init__(self):
        self.dmd_text = []
        self.line_index = 0
        self.length = 0

    #---------------------------------------------------------------------------
    #
    #---------------------------------------------------------------------------
    def load(self, filepath):
        try:
            f = open(filepath, 'rt')
            self.dmd_text = f.read().split('\n')
            self.line_index = 0
            self.length = len(self.dmd_text)

            print("Loaded file ", filepath, " with ", self.length, " lines")

            return True

        except Exception as ex:
            print(ex)
            return False

    #---------------------------------------------------------------------------
    #
    #---------------------------------------------------------------------------
    def getLine(self):
        line = ""
        if self.line_index <= self.length - 1:
            line = self.dmd_text[self.line_index]
            self.line_index += 1
            return line
        else:
            return None

    #---------------------------------------------------------------------------
    #
    #---------------------------------------------------------------------------
    def eof(self):
        return self.line_index > self.length - 1

#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class Mesh:

    def __init__(self):
        self.vertices = []
        self.faces = []
        self.faset_normals = []
        self.smooth_normals = []
        self.width = 0.0
        self.height = 0.0
        self.depth = 0.0
        self.vertex_count = 0
        self.faces_count = 0
        self.fextent = 0.0
        self.fextentX = 0.0
        self.fextentY = 0.0
        self.fextentZ = 0.0
        self.scale_type = 0
        self.parent = None


#-------------------------------------------------------------------------------
#
#-------------------------------------------------------------------------------
class MultyMesh:

    def __init__(self):
        self.meshes = []
        self.current_frame = 0
        self.fextent = 0.0
        self.fextentX = 0.0
        self.fextentY = 0.0
        self.scale_type = 0
        self.fall_smooth = 0
        self.fall_scale = 1
        self.tex_vertices = []
        self.tex_faces = []
        self.tex_v_count = 0
        self.tex_f_count = 0
        self.texture_present = False

    #---------------------------------------------------------------------------
    #
    #---------------------------------------------------------------------------
    def readNextMesh(self, dmd_cont):

        mesh = Mesh()

        line = dmd_cont.getLine()

        while (line != "numverts numfaces") and line is not None:
            line = dmd_cont.getLine()

        line = dmd_cont.getLine()
        geom_data = line.split(" ")

        tmp = []
        for gd in geom_data:
            try:
                tmp.append(int(gd))
            except ValueError:
                pass

        mesh.vertex_count = tmp[0]
        mesh.faces_count = tmp[1]

        line = dmd_cont.getLine()

        for i in range(0, mesh.vertex_count):
            line = dmd_cont.getLine()
            vertex_data = line.strip('\t').split(" ")
            try:
                x = float(vertex_data[0])
                y = float(vertex_data[1])
                z = float(vertex_data[2])
                mesh.vertices.append([x, y, z])
            except Exception as ex:
                print(ex)
                return

        line = dmd_cont.getLine()
        line = dmd_cont.getLine()

        for i in range(0, mesh.faces_count):
            line = dmd_cont.getLine()
            face_data = line.rstrip('\t').split(" ")
            face = []
            for f in face_data:
                try:
                    face.append(int(f) - 1)
                except Exception as ex:
                    print(ex)
                    return

            mesh.faces.append(face)

        mesh.parent = self
        self.meshes.append(mesh)

        print("Loaded: ", mesh.vertex_count, " vertices ", mesh.faces_count, " faces")

    #---------------------------------------------------------------------------
    #
    #---------------------------------------------------------------------------
    def readTextureBlock(self, dmd_cont):
        line = dmd_cont.getLine()
        line = dmd_cont.getLine()
        tex_data = line.split(" ")

        tmp = []
        for td in tex_data:
            try:
                tmp.append(int(td))
            except ValueError:
                pass

        self.tex_v_count = tmp[0]
        self.tex_f_count = tmp[1]

        line = dmd_cont.getLine()

        if line != "Texture vertices:":
            self.texture_present = False
            print("Texture is't present")
            return

        for i in range(0, self.tex_v_count):
            line = dmd_cont.getLine()
            vertex = line.strip('\t').split(" ")
            try:
                x = float(vertex[0])
                y = float(vertex[1])
                z = float(vertex[2])
                self.tex_vertices.append([x, y, z])
            except Exception as ex:
                print(ex)
                return

        line = dmd_cont.getLine()
        line = dmd_cont.getLine()

        for i in range(0, self.tex_f_count):
            line = dmd_cont.getLine()
            face_data = line.strip('\t').split(" ")
            face = []
            for f in face_data:
                try:
                    face.append(int(f) - 1)
                except Exception as ex:
                    print(ex)
                    return
            self.tex_faces.append(face)

        self.texture_present = True

        print("Loaded texture data about ", self.tex_v_count, " vertices ", self.tex_f_count, " faces")

    #---------------------------------------------------------------------------
    #
    #---------------------------------------------------------------------------
    def loadFromFile(self, filepath):
        dmd_cont = FileContainer()
        dmd_cont.load(filepath)

        line = dmd_cont.getLine()
        while  line is not None:
            if line == "New object":
                self.readNextMesh(dmd_cont)

            if line == "New Texture:":
                self.readTextureBlock(dmd_cont)

            line = dmd_cont.getLine()



