import tkinter as tk
import math
import numpy as np
import transformations

global_object_width = 1

class Ponto():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    # def xOnView(self, window):
    #     return ((self.x - window.xWmin)/(window.xWmax-window.xWmin))*(window.viewport.xVmax - window.viewport.xVmin)
    
    # def yOnView(self, window):
    #     return (1 - (self.y - window.yWmin)/(window.yWmax-window.yWmin))*(window.viewport.yVmax - window.viewport.yVmin)
    
    # def drawPonto(self, window, cor):
    #     window.viewport.create_oval(self.xOnView(window), self.yOnView(window), self.xOnView(window), self.yOnView(window), width = 1, outline=cor)

    def xNormalizedViewportTransform(self, window):
        return ((self.x + 1)/2) * (window.viewport.xVmax)
        
    def yNormalizedViewportTransform(self, window):
        return (1 - (self.y + 1)/2) * (window.viewport.yVmax)

    def drawNormalizedDot(self, window, cor):
        window.viewport.create_oval(self.xNormalizedViewportTransform(window), self.yNormalizedViewportTransform(window),
                 self.xNormalizedViewportTransform(window), self.yNormalizedViewportTransform(window), width = 1, outline=cor)

class Wireframe():
    def __init__(self, pontos, nome='', tipo='wireframe', cor='black', fechado=False, fill=False):
        self.pontos = pontos
        self.nome = nome
        self.tipo = tipo
        self.cor = cor
        self.fechado = fechado
        self.fill = fill

    def drawConstant(self, viewport):
        for i in range(len(self.pontos) - 1):
            viewport.create_line(self.pontos[i].x, self.pontos[i].y, self.pontos[i+1].x, self.pontos[i+1].y,
                    width = global_object_width, fill=self.cor)
        if self.fechado:
            viewport.create_line(self.pontos[-1].x, self.pontos[-1].y, self.pontos[0].x, self.pontos[0].y,
                    width = global_object_width, fill=self.cor)

    def drawLine(self, p1, p2, window):
        window.viewport.create_line(p1.xNormalizedViewportTransform(window), p1.yNormalizedViewportTransform(window), 
                p2.xNormalizedViewportTransform(window), p2.yNormalizedViewportTransform(window),
                width = global_object_width, fill=self.cor)
    # unused
    def drawObject(self, window):
        if len(self.pontos) == 0:
            return
        if len(self.pontos) == 1:
            self.pontos[0].drawPonto(window, self.cor)
            return

        for i in range(len(self.pontos) - 1):
            window.viewport.create_line(self.pontos[i].xOnView(window), self.pontos[i].yOnView(window), self.pontos[i+1].xOnView(window), 
                    self.pontos[i+1].yOnView(window), width = global_object_width, fill=self.cor)

    # all wireframes are now 3d that use Reta3D lists
    def drawObjectNormalized(self, window): 
        if len(self.pontos) == 1:
            self.pontos[0].drawNormalizedDot(window, self.cor)
            return
        if self.fill: # needs rework
            param = []
            for i in self.pontos:
                param.append(i.xNormalizedViewportTransform(window))
                param.append(i.yNormalizedViewportTransform(window))
            window.viewport.create_polygon(param, fill=self.cor)
            return
        # print(f'{self.pontos[-1].x}, {self.pontos[-1].y}, {self.pontos[0].x}, {self.pontos[0].y}')
        for i in range(len(self.pontos) - 1):
            window.viewport.create_line(self.pontos[i].xNormalizedViewportTransform(window), self.pontos[i].yNormalizedViewportTransform(window), 
                    self.pontos[i+1].xNormalizedViewportTransform(window), self.pontos[i+1].yNormalizedViewportTransform(window), 
                    width = global_object_width, fill=self.cor)
        if self.fechado and len(self.pontos) > 0:
            window.viewport.create_line(self.pontos[-1].xNormalizedViewportTransform(window), self.pontos[-1].yNormalizedViewportTransform(window), 
                    self.pontos[0].xNormalizedViewportTransform(window), self.pontos[0].yNormalizedViewportTransform(window), 
                    width = global_object_width, fill=self.cor)
            
class Ponto3D():
    def __init__(self, x, y, z):
        self.tipo = 'ponto'
        self.x = x
        self.y = y
        self.z = z
    
    def xNormalizedViewportTransform(self, window):
        return ((self.x + 1)/2) * (window.viewport.xVmax)
        
    def yNormalizedViewportTransform(self, window):
        return (1 - (self.y + 1)/2) * (window.viewport.yVmax)

    def drawNormalizedDot(self, window, cor):
        window.viewport.create_oval(self.xNormalizedViewportTransform(window), self.yNormalizedViewportTransform(window),
                self.xNormalizedViewportTransform(window), self.yNormalizedViewportTransform(window), width = 1, fill=self.cor)

class Reta3D(Wireframe):
    def __init__(self, p1, p2, nome='', tipo='reta', cor='black'):
        self.pontos = [p1, p2]
        self.nome = nome
        self.tipo = tipo
        self.cor = cor
        self.fill = False
        self.fechado = False

    def distance_xy_plane(self):
        return math.sqrt((self.pontos[0].x-self.pontos[1].x)**2+(self.pontos[0].y-self.pontos[1].y)**2)

class Objeto3D(Wireframe):
    def __init__(self, retas, nome='', tipo='wireframe', cor='black', fechado=False, fill=False):
        self.nome = nome
        self.tipo = tipo
        self.cor = cor
        self.fechado = fechado
        self.fill = fill
        self.retas = retas
    
    def drawObjectNormalized(self, window):
        for reta in self.retas:
            window.viewport.create_line(reta.pontos[0].xNormalizedViewportTransform(window), reta.pontos[0].yNormalizedViewportTransform(window),
                    reta.pontos[1].xNormalizedViewportTransform(window), reta.pontos[1].yNormalizedViewportTransform(window), width = 1, fill=self.cor)
        # if self.fechado:
        #     window.viewport.create_line(reta[].pontos[0].xNormalizedViewportTransform(window), reta.pontos[0].yNormalizedViewportTransform(window),
        #             reta.pontos[1].xNormalizedViewportTransform(window), reta.pontos[1].yNormalizedViewportTransform(window), width = 1, fill=self.cor)


class Curve(Wireframe):
    def __init__(self, pontos, nome='', tipo='curva', cor='black', fechado=False, fill=False):
        super().__init__(pontos, nome, tipo, cor, False, False)

    def blend(self, step = 0.001):
        mb = [[-1, 3, -3, 1], 
              [3, -6, 3, 0],
              [-3, 3, 0, 0],
              [1, 0, 0, 0]]

        new_pts = []

        i=0
        while i+3 < len(self.pontos):
            # print(f'iterated once more, highest i: {i+3}')
        # for i in range(0, len(self.pontos), 4):
            t = 0
            last = self.pontos[-1]

            p_mat_x = [[self.pontos[i+3].x], [self.pontos[i+2].x], [self.pontos[i+1].x], [self.pontos[i].x]]
            p_mat_y = [[self.pontos[i+3].y], [self.pontos[i+2].y], [self.pontos[i+1].y], [self.pontos[i].y]]
            aux_x = np.matmul(mb, p_mat_x)
            aux_y = np.matmul(mb, p_mat_y)
            while t <= 1:
                t_mat = [t**3, t**2, t, 1]
                coords = [0, 0]
                x = np.matmul(t_mat, aux_x)
                y = np.matmul(t_mat, aux_y)

                # aux1 = np.matmul(aux, p_mat_x)
                coords[0] = x[0]

                # aux2 = np.matmul(aux, p_mat_y)
                coords[1] = y[0]
                new_pts.append(Ponto(coords[0], coords[1]))
                t += step
            
            i+=3
        self.pontos = new_pts
        # for p in self.pontos:
        #     print('(%.1f,%.1f)' % (p.x, p.y))

class BSpline(Curve):
    def __init__(self, pontos, nome='', tipo='curva', cor='black', fechado=False, fill=False):
        super().__init__(pontos, nome, tipo, cor, False, False)

    def blend(self, step = 0.001):
        n_pontos = len(self.pontos)
        min_pontos = 4
        n_iter = int(1 / step)

        blended_points = []
        for i in range(n_pontos):
            lim_sup = i + min_pontos

            if lim_sup > n_pontos:
                break

            pontos_tmp = self.pontos[i:lim_sup]
            delta_x, delta_y = self.calc_params(pontos_tmp, step)
            x = delta_x[0]
            y = delta_y[0]
            blended_points.append(Ponto(x, y))
            for j in range(n_iter):
                x += delta_x[1]
                delta_x[1] += delta_x[2]
                delta_x[2] += delta_x[3]

                y += delta_y[1]
                delta_y[1] += delta_y[2]
                delta_y[2] += delta_y[3]

                blended_points.append(Ponto(x, y))
        self.pontos = blended_points
        # for p in self.pontos:
        #     print('(%.1f,%.1f)' % (p.x, p.y))

    def calc_params(self, points, delta):
        GBS_x = []
        GBS_y = []
        MBS = self.matrix()
        for point in points:
            GBS_x.append(point.x)
            GBS_y.append(point.y)
        GBS_x = np.array([GBS_x]).T
        coef_x = MBS.dot(GBS_x).T[0]
        diff_init_x = self.calc_diff_init(delta, *coef_x)
        GBS_y = np.array([GBS_y]).T
        coef_y = MBS.dot(GBS_y).T[0]
        diff_init_y = self.calc_diff_init(delta, *coef_y)
        return diff_init_x, diff_init_y
    
    def calc_diff_init(self, delta, a, b, c, d):
        delta_2 = delta ** 2
        delta_3 = delta ** 3
        return [
            d,
            a*delta_3 + b*delta_2 + c*delta,
            6*a*delta_3 + 2*b*delta_2,
            6*a*delta_3,
        ]
    
    def matrix(self):
        return np.array(
            [
                [-1/6, 1/2, -1/2, 1/6],
                [1/2, -1, 1/2, 0],
                [-1/2, 0, 1/2, 0],
                [1/6, 2/3, 1/6, 0],
            ]
        )