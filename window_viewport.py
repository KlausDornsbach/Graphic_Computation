import tkinter as tk
import objects
import object_display_file
import transformations
import copy
import math

# window
class Window(objects.Objeto3D): # window passa a herdar wireframe
    def __init__(self, viewport):
        self.z_depth = 300
        margin = 10
        self.margin = 10
        list_pontos =  [objects.Ponto3D(-viewport.xVmax/2 - margin, -viewport.yVmax/2 - margin, self.z_depth),# bottom_left
                        objects.Ponto3D(viewport.xVmax/2 + margin, -viewport.yVmax/2 - margin, self.z_depth), # bottom_right
                        objects.Ponto3D(viewport.xVmax/2 + margin, viewport.yVmax/2 + margin, self.z_depth),  # top_right
                        objects.Ponto3D(-viewport.xVmax/2 - margin, viewport.yVmax/2 + margin, self.z_depth)] # top left
        self.width = viewport.xVmax
        self.height = viewport.yVmax
         
        list_retas = [objects.Reta3D(list_pontos[0], list_pontos[1]), objects.Reta3D(list_pontos[1], list_pontos[2]),
                objects.Reta3D(list_pontos[2], list_pontos[3]), objects.Reta3D(list_pontos[3], list_pontos[0])]
        super().__init__(list_retas, 'window', 'wireframe')

        self.viewport = viewport

        # inicializa estrutura de dados de objetos
        self.ODF = object_display_file.ObjectDisplayFile()
        self.objetos = self.ODF.objetos

        self.angulo = 0                # inicializa angulo em 0
        self.angulo_x = 0
        self.angulo_y = 0
        self.normalized_window = objects.Objeto3D(list_retas, 'normalized window', 'wireframe')
        self.normalizing_matrix =[]       # used so I don't need to recalculate on object creation
        self.findNormalizingMatrix()   # find first normalizing matrix
        self.normalizeWindow()         # normalize first time

        self.clipper = Clipper()
        self.line_clipping_method = 'cs'    # initialized as cohen-sutherland
        self.hud_objects = []

        self.view_plane_normal = objects.Ponto3D(0, 0, self.z_depth - 1)
        print('vpn x: ', self.view_plane_normal.x)
        self.view_reference_point = objects.Ponto3D(0, 0, self.z_depth)

    
    def moveWindow(self, direction, step):
        self.viewport.delete('all')

        if direction == 'up':
            transformations.transform(self, [['translacao', [0, self.viewport.yVmax * step/200, 0]]], self)
        elif direction == 'down':
            transformations.transform(self, [['translacao', [0, self.viewport.yVmax * -step/200, 0]]], self)
        elif direction == 'right':
            transformations.transform(self, [['translacao', [self.viewport.xVmax * step/200, 0, 0]]], self)
        elif direction == 'left':
            transformations.transform(self, [['translacao', [self.viewport.xVmax * -step/200, 0, 0]]], self)
        elif direction == 'forth':
            transformations.transform(self, [['translacao', [0, 0, self.viewport.xVmax * -step/200]]], self)
        else:
            transformations.transform(self, [['translacao', [0, 0, self.viewport.xVmax * +step/200]]], self)
    
    def moveWindowAbsolute(self, direction, amount):
        self.viewport.delete('all')

        if direction == 'up':
            transformations.transform(self, [['translacao', [0, amount]]], self)
        elif direction == 'down':
            transformations.transform(self, [['translacao', [0, amount]]], self)
        elif direction == 'right':
            transformations.transform(self, [['translacao', [amount, 0]]], self)
        else:
            transformations.transform(self, [['translacao', [amount, 0]]], self)

    def zoom(self, direction, step):
        self.viewport.delete('all')
        if direction == 'in':
            transformations.transform(self, [['escalonamento_total_centro', [1 - (step/200), 1 - (step/200), 1]]], self)
        else:
            transformations.transform(self, [['escalonamento_total_centro', [1 + (step/200), 1 + (step/200), 1]]], self)
        
        self.findNormalizingMatrix()
        self.normalizeAll()
        self.updateObjects()

    def zoomAbsolute(self, direction, amountX, amountY):
        self.viewport.delete('all')
        if direction == 'in':
            transformations.transform(self, [['escalonamento_total_centro', [1 - amountX/200, 1 - amountY/200, 1]]], self)
        else:
            transformations.transform(self, [['escalonamento_total_centro', [1 + amountX/200, 1 + amountY/200, 1]]], self)
        
        self.findNormalizingMatrix()
        self.normalizeAll()
        self.updateObjects()

    def updateObjects(self):
        for i in self.hud_objects:
            i.drawConstant(self.viewport)
        
        for i in self.ODF.objetos_normalizados:
            # print(i.pontos[0].x)
            
            self.clipper.clip(i, self)
            i.drawObjectNormalized(self)

    def rotate(self, anguloDeg, axis):
        # # transformo window somente
        if axis == '2':
            self.angulo -= anguloDeg
        elif axis == '1':
            self.angulo_y -= anguloDeg
        elif axis == '0':
            self.angulo_x -= anguloDeg
        # 1 is rotation relative to object and 2 is relative to axis z
        print('window.rotate')
        window_only = [['rotacao', ['1', anguloDeg, axis]]]
        # dentro de transform() tenho checagem pra ver se é window
        # que está sendo transformada, então updato tudo e redesenho
        transformations.transform(self, window_only, self)
        print('my new dots:')
        for r in self.retas:
            print(f'x: {r.pontos[0].x}, y: {r.pontos[0].y}, z: {r.pontos[0].z}')
        self.viewport.delete('all')
        self.orthogonalize()
        self.findNormalizingMatrix()
        self.normalizeAll()
        self.updateObjects()

    def orthogonalize(self):
        # move vrp to center
        go_to_center = transformations.translacao(-self.view_reference_point.x, 
                -self.view_reference_point.y, -self.view_reference_point.z)
        self.view_reference_point.x = 0
        self.view_reference_point.y = 0
        self.view_reference_point.z = 0
        print(go_to_center)
        # input()
        # decompose x and y from vpn
        # print('math domain problem', self.view_plane_normal.x)
        x_angle = -self.angulo_x #-math.acos(self.view_plane_normal.x)
        aux = transformations.rotacao(x_angle, go_to_center, '0') # transformations.rotacao(math.degrees(x_angle), go_to_center, '0')

        y_angle = -self.angulo_y # math.acos(self.view_plane_normal.y)
        aux = transformations.rotacao(y_angle, aux, '1')# transformations.rotacao(math.degrees(y_angle), aux, '0')
        self.angulo_x = 0
        self.angulo_y = 0
        transformations.applyTransform(self, aux)
        transformations.applyTransform(self.view_plane_normal, aux) # unneccessary

        for o in self.objetos:
            transformations.applyTransform(o, aux)
        
    #############################  |
    ##   normalizing methods   ##  |
    #############################  v

    def findNormalizingMatrix(self):
        [c_x, c_y, c_z] = transformations.findCenter(self)
        world_transforms = [['translacao', [-c_x, -c_y, -c_z]],
                            ['rotacao', ['0', -(self.angulo)]],
                            ['escalonamento_total', 
                            [1/self.retas[0].distance_xy_plane()*2,
                            1/self.retas[1].distance_xy_plane()*2,
                            1]]
                           ]

        # remember to rotate window in orthogonalization process
        self.normalizing_matrix = transformations.getTransformMatrix(world_transforms)

    def normalizeWindow(self):
        self.normalized_window.retas = copy.deepcopy(self.retas)       # usando deepcopy
        transformations.applyTransform(self.normalized_window, self.normalizing_matrix)

    def normalizeObject(self, index):
        self.ODF.objetos_normalizados[index] = copy.deepcopy(self.objetos[index])
        transformations.applyTransform(self.ODF.objetos_normalizados[index], self.normalizing_matrix)

    def createObjectNormalized(self, obj):
        new_obj = copy.deepcopy(obj)
        transformations.applyTransform(new_obj, self.normalizing_matrix)
        self.ODF.objetos_normalizados.append(new_obj)
        return new_obj  
    
    def normalizeAll(self):
        self.normalizeWindow()

        for i in range(len(self.objetos)):
            self.normalizeObject(i)

    #############################  |
    ##       GUI interface     ##  |
    #############################  v

    def newPonto(self, x, y, z):
        try:
            p = objects.Ponto3D(int(x), int(y), int(z))
            return p
        except ValueError:
            print("NaN")

    def addObject(self, pontos, list_objects_gui_component, nome_gui_component, cor, new_window_gui=0, fechado=False, fill=False, 
                tipo_objeto = "wireframe", curve_type='bezier', curve_step=0.1):

        if tipo_objeto == 'curva':
            if curve_type == 'bezier':
                obj = objects.Curve(pontos, nome=nome_gui_component, cor=cor)
                obj.blend()
            elif curve_type == 'spline':
                obj = objects.BSpline(pontos, nome=nome_gui_component, cor=cor)
                obj.blend()
        elif tipo_objeto == 'ponto':
            obj = pontos[0]
        elif tipo_objeto == 'reta':
            obj = objects.Reta3D(pontos[0], pontos[1])
        else:
            retas = []
            for p in range(len(pontos)-1):
                retas.append(objects.Reta3D(pontos[p], pontos[p+1]))
            if fechado:
                retas.append(objects.Reta3D(pontos[-1], pontos[0]))
            obj = objects.Objeto3D(retas, nome_gui_component, tipo_objeto, cor, fechado, fill)
        
        self.objetos.append(obj)

        nome = nome_gui_component + "[" + tipo_objeto + "]"
        list_objects_gui_component.insert(tk.END, nome)

        normie_obj = self.createObjectNormalized(obj)

        self.clipper.clip(normie_obj, self)

        normie_obj.drawObjectNormalized(self)

        if new_window_gui != 0:
            new_window_gui.destroy()
    

    def addPontoWireframe(self, lista, x, y, z, window):
        try:
            p = objects.Ponto3D(int(x.get()), int(y.get()), int(z.get()))
            x.delete(0, tk.END)
            y.delete(0, tk.END)
            z.delete(0, tk.END)
            lista.append(p)
            # p.drawPonto(window, 'black')
        except ValueError:
            print("NaN")
    
    def chooseClipping(self, method,clipping_window):
        if method == '0':
            self.line_clipping_method = 'cs'
        else:
            self.line_clipping_method = 'lb'
        clipping_window.destroy()

        
# mudar aqui tamanho da viewport
class Viewport(tk.Canvas):
    def __init__(self, parent_container, w, h):
        super().__init__(parent_container, width=w, height=h, bg='white')
        self.xVmax = w
        self.xVmin = 0
        self.yVmax = h
        self.yVmin = 0


#############################
##    clipping methods     ##
#############################

class Clipper():
    def __init__(self):
        self.CENTER = 0b0000
        self.LEFT   = 0b0001
        self.RIGHT  = 0b0010
        self.BOTTOM = 0b0100
        self.TOP    = 0b1000

    def clip(self, obj, window):
        # let the canvas clip the points
        if obj.tipo == 'ponto':
            return self.clippingPontos(obj, window)
        elif obj.tipo == 'reta': 
            if window.line_clipping_method == 'cs':
                return self.cohenSutherland(obj, window)
            if window.line_clipping_method == 'lb':
                return self.liangBarsky(obj, window)
        elif obj.tipo == 'wireframe':
            return self.sutherlandHodgeman(obj, window)
        elif obj.tipo == 'curva':
            self.clippingPontosCurva(obj, window)

    
    def clippingPontos(self, ponto, window):
        x = ponto.pontos[0].x
        y = ponto.pontos[0].y
        margin_x = 2*window.margin/window.viewport.xVmax
        margin_y = 2*window.margin/window.viewport.yVmax

        # print('%d %d %d %d' % (window.viewport.xVmin, window.viewport.yVmin, window.viewport.xVmax, window.viewport.yVmax))

        xmin = -1 + margin_x
        ymin = -1 + margin_y
        xmax = 1 - margin_x
        ymax = 1 - margin_y

        # print('%d %d %d %d' % (xmin, ymin, xmax, ymax))

        should_display = xmin <= x and x <= xmax and ymin <= y and y <= ymax

        if should_display:
            # print('should display point (%.2f, %.2f)' % (x, y))
            return objects.Wireframe([ponto.pontos[0]], '', 'ponto', cor=ponto.cor)
        else:
            ponto.pontos = []
            return 0
    
    def clippingPontosCurva(self, curva, window):
        novos_pontos = []
        # print(type(curva.pontos[0]))
        # for i in range(len(curva.pontos)-1):
        #     result = self.cohenSutherland(objects.Wireframe([curva.pontos[i], curva.pontos[i+1]]), window)
        #     if result == 0:
        #         continue
        #     novos_pontos.append(result)
        # curva.pontos = novos_pontos 
        # novos_pontos = []
        for i in range(len(curva.pontos)):
            ponto = curva.pontos[i]
            x = ponto.x
            y = ponto.y
            margin_x = 2*window.margin/window.viewport.xVmax
            margin_y = 2*window.margin/window.viewport.yVmax

            # print('%d %d %d %d' % (window.viewport.xVmin, window.viewport.yVmin, window.viewport.xVmax, window.viewport.yVmax))

            xmin = -1 + margin_x
            ymin = -1 + margin_y
            xmax = 1 - margin_x
            ymax = 1 - margin_y

            # print('%d %d %d %d' % (xmin, ymin, xmax, ymax))

            should_display = xmin <= x and x <= xmax and ymin <= y and y <= ymax

            if should_display:
                novos_pontos.append(ponto)
                # print('should display point (%.2f, %.2f)' % (x, y))
                # return objects.Wireframe([curva.pontos[0]], '', 'ponto', cor=curva.cor)
        curva.pontos = novos_pontos

    # cohen-sutherland
    def cohenSutherland(self, reta, window):
        p1 = reta.pontos[0]
        p2 = reta.pontos[1]
        region_vector = [self.regionCode(p1, window), self.regionCode(p2, window)]

        if region_vector[0] & region_vector[1] != self.CENTER: # don't draw
            return 0

        if region_vector[0] == region_vector[1]: # draw it all
            return reta
        
        reta.pontos[0] = self.intercept(0, reta, region_vector, window)
        reta.pontos[1] = self.intercept(1, reta, region_vector, window)

        # return doesn't matter
        return objects.Wireframe([p1, p2], '', 'reta', cor=reta.cor)

    def angularCoefficient(self, reta):
        if (reta.pontos[1].x - reta.pontos[0].x) == 0:
            return 2**31
        return (reta.pontos[1].y - reta.pontos[0].y)/(reta.pontos[1].x - reta.pontos[0].x)

    def intercept(self, p, reta, region_vector, window):
        p1 = reta.pontos[p]
        margin_x = 2*window.margin/window.viewport.xVmax
        margin_y = 2*window.margin/window.viewport.yVmax

        if region_vector[p] | self.CENTER == 0b0000:
            return p1

        m = self.angularCoefficient(reta)
        if region_vector[p] & self.RIGHT != 0b0000:
            y_intersect = m*(1 - p1.x) + p1.y
            if y_intersect < 1 and y_intersect > -1:
                return objects.Ponto3D(1 - margin_x, y_intersect, 0)

        elif region_vector[p] & self.LEFT != 0b0000:
            y_intersect = m*(-1 - p1.x) + p1.y
            if y_intersect < 1 and y_intersect > -1:
                return objects.Ponto3D(-1 + margin_x, y_intersect, 0)

        if region_vector[p] & self.TOP != 0b0000:
            x_intersect = (1/m)*(1 - p1.y) + p1.x
            if x_intersect < 1 and x_intersect > -1:
                return objects.Ponto3D(x_intersect, 1 - margin_y, 0)

        elif region_vector[p] & self.BOTTOM != 0b0000:
            x_intersect = (1/m)*(-1 - p1.y) + p1.x
            if x_intersect < 1 and x_intersect > -1:
                return objects.Ponto3D(x_intersect, -1 + margin_y, 0)

    def interceptSutherlandHodgeman(self, p, reta, region_vector, outside, window):
        p1 = reta.pontos[p]
        margin_x = 2*window.margin/window.viewport.xVmax
        margin_y = 2*window.margin/window.viewport.yVmax

        m = self.angularCoefficient(reta)

        if outside == self.RIGHT:
            y_intersect = m*(1 - p1.x - margin_x) + p1.y
            return objects.Ponto3D(1 - margin_x, y_intersect, 0)

        elif outside == self.LEFT:
            y_intersect = m*(-1 - p1.x + margin_x) + p1.y
            return objects.Ponto3D(-1 + margin_x, y_intersect, 0)

        if outside == self.TOP:
            x_intersect = (1/m)*(1 - p1.y - margin_y) + p1.x
            return objects.Ponto3D(x_intersect, 1 - margin_y, 0)

        elif outside == self.BOTTOM:
            x_intersect = (1/m)*(-1 - p1.y + margin_y) + p1.x
            return objects.Ponto3D(x_intersect, -1 + margin_y, 0)

    def regionCode(self, ponto, window):
        margin_x = 2*window.margin/window.viewport.xVmax
        margin_y = 2*window.margin/window.viewport.yVmax
        reg_code = 0b0000   # fully inside
        if ponto.x > 1 - margin_x:     # right
            reg_code = reg_code | 0b0010
        if ponto.x < -1 + margin_x:    # left
            reg_code = reg_code | 0b0001
        if ponto.y > 1 - margin_y:     # top
            reg_code = reg_code | 0b1000
        if ponto.y < -1 + margin_y:    # bottom
            reg_code = reg_code | 0b0100
        return reg_code

    # Sutherland-Hodgeman implementation
    def sutherlandHodgeman(self, wireframe, window):
        pontos = []
        for r in wireframe.retas:
            pontos.append(r.pontos[0])
        region_vector = []
        region_vector = self.updateRegionVector(pontos, window)
        
        # print(len(wireframe.pontos))
        clipped_wireframe = pontos
        clipped_wireframe_aux = []

        OUTSIDE = 0b0001 # start clipping left
        INSIDE = 0b1111 & ~OUTSIDE

        # seq = ['LEFT', 'RIGHT', 'BOTTOM', 'TOP']
        for k in range(4):
            i = -1
            for i in range(i, len(clipped_wireframe) - 1):
                if self.isOut(region_vector[i], OUTSIDE) and self.isOut(region_vector[i+1], OUTSIDE): # out - out
                    pass
                elif not self.isOut(region_vector[i], OUTSIDE) and self.isOut(region_vector[i+1], OUTSIDE): # in out
                    aux = self.interceptSutherlandHodgeman(
                            1, objects.Wireframe([clipped_wireframe[i], clipped_wireframe[i+1]], window),
                            [region_vector[i], region_vector[i+1]], OUTSIDE, window)
                    clipped_wireframe_aux.append(self.interceptSutherlandHodgeman(
                            1, objects.Wireframe([clipped_wireframe[i], clipped_wireframe[i+1]], window),
                            [region_vector[i], region_vector[i+1]], OUTSIDE, window))
                elif self.isOut(region_vector[i], OUTSIDE) and not self.isOut(region_vector[i+1], OUTSIDE): # out in
                    clipped_wireframe_aux.append(self.interceptSutherlandHodgeman(
                            1, objects.Wireframe([clipped_wireframe[i], clipped_wireframe[i+1]], window), 
                            [region_vector[i], region_vector[i+1]], OUTSIDE, window))
                    clipped_wireframe_aux.append(clipped_wireframe[i+1])
                else: 
                    clipped_wireframe_aux.append(clipped_wireframe[i+1])

            clipped_wireframe = clipped_wireframe_aux
            clipped_wireframe_aux = []
            region_vector = self.updateRegionVector(clipped_wireframe, window)
            
            OUTSIDE = OUTSIDE << 1
            INSIDE = 0b1111 & ~OUTSIDE

        if wireframe.fechado == False and (self.regionCode(pontos[0], window) == 0b0000 and 
                                    self.regionCode(pontos[-1], window) != 0b0000) or (
                                    self.regionCode(pontos[-1], window) == 0b0000 and 
                                    self.regionCode(pontos[0], window) != 0b0000):
            clipped_wireframe.pop(0)
# (-100,-100,0),(100,-100,0),(100,100,0),(-100,100,0)
        retas = []
        for p in range(len(clipped_wireframe)-1):
            retas.append(objects.Reta3D(clipped_wireframe[p], clipped_wireframe[p+1]))
        if wireframe.fechado and len(clipped_wireframe)>1: 
            retas.append(objects.Reta3D(clipped_wireframe[0], clipped_wireframe[-1]))
        wireframe.retas = retas


    def updateRegionVector(self, wireframe_dots, window):
        new = []
        for p in wireframe_dots:
            new.append(self.regionCode(p, window))
        return new

    def isOut(self, reg_code, out):
        if reg_code & out != 0b0000:
            return True
        return False

    def liangBarsky(self, reta, window):
        print('call')
        
        pts = reta.pontos
        print(pts[0].x)
        print(pts[0].y)
        print(pts[1].x)
        print(pts[1].y)
        xw_max = 2*window.margin/window.viewport.xVmax
        xw_min = -xw_max
        yw_max = 2*window.margin/window.viewport.yVmax
        yw_min = -yw_max
        print('max')
        print(xw_max)
        
        p = [-(pts[1].x - pts[0].x),
            pts[1].x - pts[0].x,
            -(pts[1].y - pts[0].y),
            pts[1].y - pts[0].y
        ]
        is_pos = []
        is_neg = []
        print(p)
        # print(q)
        i = 0
        while i < 4:
            if p[i] == 0 and p[i+1] == 0:
                # print('case 1')
                is_pos.append(i)
                is_neg.append(i+1)
                i+=1
            elif p[i] < 0:
                # print('case 2')
                is_neg.append(i)
            else:
                is_pos.append(i)
            i+=1
        # print(len(is_neg))
        # print(len(is_pos))
        q = [pts[0].x - xw_min,
            xw_max - pts[0].x,
            pts[0].y - yw_min,
            yw_max - pts[0].y
        ]
        print(q)
        r1 = []
        r2 = []
        for i in range(2):
            if p[is_pos[i]]==0:
                p[is_pos[i]]=0.00001
            if p[is_neg[i]]==0:
                p[is_neg[i]]=0.00001
            r1.append(q[is_pos[i]]/p[is_pos[i]])
            r2.append(q[is_neg[i]]/p[is_neg[i]])

        z1 = max(0, *r1)
        z2 = min(1, *r2)
        print("z1 z2")
        print(z1)
        print(z2)
        # if z1 > z2:       # line is out
        #     pts = []
        #     return
        if z1 > 0:
            print('aqui1')
            print(reta.nome)
            print('p[is_neg[1]]: %.2f, pts[0].y: %.2f, z1: %.2f' % (p[is_neg[1]], pts[0].y, z1))
            pts[0].x = pts[0].x + z1 * p[is_neg[0]]
            pts[0].y = pts[0].y + z1 * p[is_neg[1]]
            print('p[0]: %.2f %.2f' % (pts[0].x, pts[0].y))
        if z2 < 1:
            print('aqui')
            pts[1].x = pts[1].x + z2 * p[is_pos[0]]
            pts[1].y = pts[1].y + z2 * p[is_pos[1]] # ok
            print('p[1]: %.2f %.2f' % (pts[0].x, pts[0].y))


