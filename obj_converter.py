import objects
import window_viewport


class DescritorOBJ:
    def __init__(self):
        self.material_library = {}
        self.default_mtl = Material(0, 0, 0)
        self.material_library['black'] = self.default_mtl

    def fileToWireframe(self, file, window, list_objects_gui_component):
        f = open(file, 'r')

        dot_list = []
        object_name = ''
        object_mtl = 'black'

        for line in f:
            if line[0] == '#':
                continue
            else:
                vec = line.split() # default space split
                if vec[0] == 'v':
                    dot_list.append(objects.Ponto(float(vec[1]), float(vec[2])))
                elif vec[0] == 'mtllib':
                    self.readMaterial('obj_src/' + vec[1])
                elif vec[0] == 'o':
                    object_name = vec[1]
                elif vec[0] == 'usemtl':
                    object_mtl = vec[1]
                else:
                    obj_dots = []
                    for i in vec[1:]:
                        obj_dots.append(dot_list[int(i)-1])
                    tipo = 'wireframe'
                    if obj_dots == 1:
                        tipo = 'ponto'
                    elif obj_dots == 2:
                        tipo = 'reta'
                        # ( pontos, list_objects_gui_component, nome_gui_component, new_window_gui, cor, fechado=False)
                    window.addObject(obj_dots, list_objects_gui_component, object_name, 
                                        self.material_library[object_mtl].color , fechado=True)
                    obj_dots = []


    def wireframeToFile(self, file, object_list_index, window):
        
        pass

    def readMaterial(self, file):
        f = open(file, 'r')

        material_name = ''

        for line in f:
            if line[0] == '#':
                continue
            elif line[0] == '' or line[0] == '\n':
                continue
            else:
                vec = line.split() # default space split
                if vec[0] == 'newmtl':
                    material_name = vec[1]
                elif vec[0] == 'Kd':
                    self.material_library[material_name] = Material(float(vec[1]), float(vec[2]), float(vec[3]))

                    




class Material():
    def __init__(self, r, g, b):
        red = format(int(r*255), '02x')
        green = format(int(g*255),'02x')
        blue = format(int(b*255), '02x')
        self.color = '#' + red + green + blue
