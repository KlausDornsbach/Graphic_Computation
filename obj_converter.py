import objects
import window_viewport
import os
import copy

class DescritorOBJ:
    def __init__(self):
        self.material_library = {}
        self.default_mtl = Material(0, 0, 0)
        self.material_library['black'] = self.default_mtl

    def fileToWireframe(self, window, list_objects_gui_component, file):
        f = open(file, 'r')

        dot_list = []
        object_name = ''
        object_mtl = 'black'

        fech = False

        for line in f:
            if line[0] == '#' or line[0] == '\n':
                continue
            else:
                vec = line.split() # default space split
                if vec[0] == 'v':
                    dot_list.append(objects.Ponto3D(float(vec[1]), float(vec[2]), float(vec[3])))
                elif vec[0] == 'mtllib':
                    self.readMaterial('src/' + vec[1])
                elif vec[0] == 'o':
                    object_name = vec[1]
                elif vec[0] == 'usemtl':
                    object_mtl = vec[1]
                elif vec[0] == 'w':
                    window_center = dot_list[int(vec[1])-1] # (x,y)
                    window_size = dot_list[int(vec[2])-1] # (x,y) | x=width and y=height

                    # Move window to adjust its center (if necessary)

                    if window_center.x > 0:
                        delta_x = window_center.x - 0
                        window.moveWindowAbsolute('right', delta_x)
                    elif window_center.x < 0:
                        delta_x = 0 - window_center.x
                        window.moveWindowAbsolute('left', delta_x)
                    
                    if window_center.y > 0:
                        delta_y = window_center.y - 0
                        window.moveWindowAbsolute('up', delta_y)
                    elif window_center.y < 0:
                        delta_y = 0 - window_center.y
                        window.moveWindowAbsolute('down', delta_y)

                    # Zoom window to adjust its size (if necessary)
                    
                    if window_size.x > window.width:
                        delta_x = (window_size.x - window.width)/2
                        window.zoomAbsolute('out', delta_x, 0)
                    elif window_size.x < window.width:
                        delta_x = (window.width - window_size.x)/2
                        window.zoomAbsolute('in', delta_x, 0)

                    if window_size.y > window.height:
                        delta_y = (window_size.y - window.height)/2
                        window.zoomAbsolute('out', 0, delta_y)
                    elif window_size.y < window.height:
                        delta_y = (window.height - window_size.y)/2
                        window.zoomAbsolute('in', 0, delta_y)
                
                else:
                    if vec[0] == 'f':
                        fech = True
                    obj_dots = []
                    for i in vec[1:]:
                        obj_dots.append(copy.deepcopy(dot_list[int(i)-1]))
                    print(object_name)
                    print(' '.join(['(%d, %d, %d)' % (p.x, p.y, p.z) for p in obj_dots]))
                    # print(fech)
                    # addObject já transforma em retas os pontos passados
                    window.addObject(obj_dots, list_objects_gui_component, object_name,
                                        self.material_library[object_mtl].color, fechado=fech, tipo_objeto='wireframe')
                    obj_dots = []
                    fech = False
        f.close()


    def wireframeToFile(self, window, object_list, file):
        f = open(file, 'w+')

        writable_mtlib_file = file.split('.')

        f.write('mtllib %s.mtl\n' % str(writable_mtlib_file[0]))
        # f.write('v 0.0 0.0 0.0\n') # centro da window
        # f.write('v %.1f %.1f 0.0\n' % (window.xWmax, window.yWmax)) # tamanho da window
        # f.write('o window\n')
        # f.write('w 1 2\n')

        # vertices_count = 2
        vertices_count = 0

        colors = []

        for obj in object_list:
            f.write('o %s\n' % (obj.nome))
            
            if obj.cor not in colors:
                colors.append(obj.cor)
                color_number = len(colors)
            else:
                color_number = colors.index(obj.cor) + 1

            f.write('usemtl color_%d\n' % (color_number))

            vertices_for_obj = []
            for p in obj.pontos:
                f.write('v %.1f %.1f 0.0\n' % (p.x, p.y))
                vertices_count += 1
                vertices_for_obj.append(str(vertices_count))

            if obj.tipo == 'ponto':
                f.write('p %s\n' % ' '.join(vertices_for_obj))
            elif obj.tipo == 'reta':
                f.write('l %s\n' % ' '.join(vertices_for_obj))
            elif obj.tipo == 'wireframe':
                f.write('l %s\n' % ' '.join(vertices_for_obj))

        f.close()

        f_mtl = open('out/%s.mtl' % file, 'w+')

        for i in range(len(colors)):
            hex_color = colors[i]
            color = hex_to_material_color(hex_color)
            f_mtl.write('newmtl color_%d\n' % (i+1))
            f_mtl.write('Kd %.6f %.6f %.6f\n\n' % (color[0], color[1], color[2]))

        f_mtl.close()

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

                    
def hex_to_material_color(hex_color):
    hex_color = hex_color.lstrip('#')
    lv = len(hex_color)
    return tuple(int(hex_color[i:i + lv // 3], 16) / 255 for i in range(0, lv, lv // 3))



class Material():
    def __init__(self, r, g, b):
        red = format(int(r*255), '02x')
        green = format(int(g*255),'02x')
        blue = format(int(b*255), '02x')
        self.color = '#' + red + green + blue
