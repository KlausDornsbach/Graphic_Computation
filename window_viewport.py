import tkinter as tk
import objects
import object_display_file

# window
class Window():
    def __init__(self, Xwmin, Ywmin, Xwmax, Ywmax, viewport):
        # window vars
        self.xWmin = Xwmin
        self.yWmin = Ywmin
        self.xWmax = Xwmax
        self.yWmax = Ywmax
        self.viewport = viewport
        # inicializa estrutura de dados de objetos
        self.ODF = object_display_file.ObjectDisplayFile()
        self.objetos = self.ODF.objetos
    
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


        self.updateObjects()
                
    def updateObjects(self):
        for i in self.objetos:
            i.updateAndDrawObject(self.viewport, self)

    
        

# mudar aqui tamanho da viewport
class Viewport(tk.Canvas):
    def __init__(self, parent_container, w, h):
        super().__init__(parent_container, width=w, height=h, bg='white')
        self.xVmax = w
        self.xVmin = 0
        self.yVmax = h
        self.yVmin = 0
