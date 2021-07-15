import tkinter as tk
import objects
import object_display_file
import transformations
import copy

# window
class Window(objects.Wireframe): # window passa a herdar wireframe
    def __init__(self, Xwmin, Ywmin, Xwmax, Ywmax, viewport):
        list_pontos =  [objects.Ponto(-viewport.xVmax/2, -viewport.yVmax/2),# bottom_left
                        objects.Ponto(viewport.xVmax/2, -viewport.yVmax/2), # bottom_right
                        objects.Ponto(viewport.xVmax/2, viewport.yVmax/2),  # top_right
                        objects.Ponto(-viewport.xVmax/2, viewport.yVmax/2)] # top left

        super().__init__(list_pontos, 'window', 'wireframe')

        # window vars
        self.xWmin = Xwmin
        self.yWmin = Ywmin
        self.xWmax = Xwmax
        self.yWmax = Ywmax        

        self.viewport = viewport

        # inicializa estrutura de dados de objetos
        self.ODF = object_display_file.ObjectDisplayFile()
        self.objetos = self.ODF.objetos

        self.angulo = 0                # inicializa angulo em 0
        self.normalized_window = objects.Wireframe(list_pontos, 'normalized window', 'wireframe')
        self.findNormalizingMatrix()   # find first normalizing matrix
        self.normalizeWindow()         # normalize first time
        self.normalizing_matrix        # used so I don't need to recalculate on object creation

        self.clipping_method = 'cs'    # initialized as cohen-sutherland
    
    def moveWindow(self, direction, step):
        self.viewport.delete('all')

        if direction == 'up':
            self.yWmin += step/100 * self.viewport.yVmax
            self.yWmax += step/100 * self.viewport.yVmax
        elif direction == 'left':
            self.xWmin -= step/100 * self.viewport.xVmax
            self.xWmax -= step/100 * self.viewport.xVmax
        elif direction == 'right':
            self.xWmin += step/100 * self.viewport.xVmax
            self.xWmax += step/100 * self.viewport.xVmax
        elif direction == 'down':
            self.yWmin -= step/100 * self.viewport.yVmax
            self.yWmax -= step/100 * self.viewport.yVmax

        self.findNormalizingMatrix()
        self.normalizeAll()
        self.updateObjects()

    def zoom(self, direction, step):
        self.viewport.delete('all')
        #if (self.yWmin - (step/200 * self.viewport.yVmax) < 0.0001) or (self.xWmin - (step/200 * self.viewport.xVmax) < 0.0001):
        #    return
        
        yWmin_save = self.yWmin
        yWmax_save = self.yWmax 
        xWmin_save = self.xWmin
        xWmax_save = self.xWmax
        if direction == 'in':
            self.yWmin += step/200 * self.viewport.yVmax
            self.yWmax -= step/200 * self.viewport.yVmax
            self.xWmin += step/200 * self.viewport.xVmax
            self.xWmax -= step/200 * self.viewport.xVmax
        elif direction == 'out':
            self.yWmin -= step/200 * self.viewport.yVmax
            self.yWmax += step/200 * self.viewport.yVmax
            self.xWmin -= step/200 * self.viewport.xVmax
            self.xWmax += step/200 * self.viewport.xVmax

        if self.xWmax-self.xWmin == 0 or self.yWmax-self.yWmin == 0:
            self.yWmin = yWmin_save
            self.yWmax = yWmax_save
            self.xWmin = xWmin_save
            self.xWmax = xWmax_save

        self.findNormalizingMatrix()
        self.normalizeAll()
        self.updateObjects()
                
    def updateObjects(self):
        for i in self.ODF.objetos_normalizados:
            i.drawObjectNormalized(self)


    def rotate(self, anguloDeg):
        # # transformo window somente
        self.angulo -= anguloDeg
        window_only = [['rotacao', ['1', anguloDeg]]]
        # dentro de transform() tenho checagem pra ver se é window
        # que está sendo transformada, então updato tudo e redesenho
        transformations.transform(self, window_only, self)

    #############################  |
    ##   normalizing methods   ##  |
    #############################  v

    def findNormalizingMatrix(self):
        [c_x, c_y] = transformations.findCenter(self)
        world_transforms = [['translacao', [-c_x, -c_y]],
                            ['rotacao', ['0', -(self.angulo)]],
                            ['escalonamento_total', 
                            [1/(self.xWmax - self.xWmin)*2,
                            1/(self.yWmax - self.yWmin)*2]]
                           ]
        
        self.normalizing_matrix = transformations.getTransformMatrix(world_transforms)

    def normalizeWindow(self):
        self.normalized_window.pontos = copy.deepcopy(self.pontos)       # usando deepcopy
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
        self.normalized_window.pontos = copy.deepcopy(self.pontos)       # usando deepcopy
        transformations.applyTransform(self.normalized_window, self.normalizing_matrix)

        for i in range(len(self.objetos)):
            self.normalizeObject(i)
    

    #############################  |
    ##       GUI interface     ##  |
    #############################  v

    def newPonto(self, x, y):
        try:
            p = objects.Ponto(int(x), int(y))
            return p
        except ValueError:
            print("NaN")
    
    def addObject(self, pontos, list_objects_gui_component, nome_gui_component, cor, new_window_gui=0, fechado=False):
        if len(pontos) == 1:
            tipo_objeto = "ponto"
        elif len(pontos) == 2:
            tipo_objeto = "reta"
        else:
            tipo_objeto = "wireframe"
        
        obj = objects.Wireframe(pontos, nome_gui_component, tipo_objeto, cor, fechado)
        self.objetos.append(obj)
        nome = nome_gui_component + "[" + tipo_objeto + "]"
        list_objects_gui_component.insert(tk.END, nome)
        normie_obj = self.createObjectNormalized(obj)
        normie_obj.drawObjectNormalized(self)
        if new_window_gui != 0:
            new_window_gui.destroy()
    

    def addPontoWireframe(self, lista, x, y, window):
        try:
            p = objects.Ponto(int(x.get()), int(y.get()))
            x.delete(0, tk.END)
            y.delete(0, tk.END)
            lista.append(p)
            p.drawPonto(window, 'black')
        except ValueError:
            print("NaN")

    def chooseClipping(self, clipping, window):
        if clipping == '0':
            self.clipping_method = 'cs'
        elif clipping == '1':
            self.clipping_method = 'lb'
        window.destroy()
        
# mudar aqui tamanho da viewport
class Viewport(tk.Canvas):
    def __init__(self, parent_container, w, h):
        super().__init__(parent_container, width=w, height=h, bg='white')
        self.xVmax = w
        self.xVmin = 0
        self.yVmax = h
        self.yVmin = 0


