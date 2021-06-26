import tkinter as tk

global_object_width = 1

class Ponto():
    def __init__(self, x, y, window):
        self.x = x
        self.y = y
        self.xV = self.xOnView(window)
        self.yV = self.yOnView(window)        
        self.nome = ''
        self.cor = 'black'
        self.tipo = 'ponto'

    def xOnView(self, window):
        var = ((self.x - window.xWmin)/(window.xWmax-window.xWmin))*(window.viewport.xVmax - window.viewport.xVmin)
        return var

    def yOnView(self, window):
        var = (1 - (self.y - window.yWmin)/(window.yWmax-window.yWmin))*(window.viewport.yVmax - window.viewport.yVmin)
        return var
    
    def updateView(self, window):
        self.xV = self.xOnView(window)
        self.yV = self.yOnView(window)
    
    def atualizaPonto(self, viewport, window):
        self.updateView(window)
        viewport.create_oval(self.xV, self.yV, self.xV, self.yV, width = 1, fill=self.cor)

class Object():
    def __init__(self, pontos, nome, tipo, cor='black'):
        self.pontos = pontos
        self.nome = nome
        self.tipo = tipo
        self.cor = cor
    
    def drawLine(self, p1, p2, viewport, window):
        p1.updateView(window)
        p2.updateView(window)
        viewport.create_line(p1.xV, p1.yV, p2.xV, p2.yV, width = global_object_width, fill=self.cor)

    def updateAndDrawObject(self, viewport, window):
        if self.tipo == 'ponto':
            self.pontos[0].atualizaPonto(viewport, window)
        elif self.tipo == 'reta':
            self.drawLine(self.pontos[0], self.pontos[1], viewport, window)
        elif self.tipo == 'wireframe':
            self.drawWireframe(viewport, window)

class Wireframe(Object):
    def __init__(self, pontos, nome, tipo, fechado, cor='black'):
        super().__init__(pontos, nome, tipo='wireframe', cor='black')
        self.fechado = fechado
    
    def drawWireframe(self, viewport, window):
        if len(self.pontos) == 1:
            self.pontos[0].atualizaPonto(viewport, window)
            return
        pFinal = self.pontos[-1]
        for i in range(len(self.pontos)):
            self.pontos[i].updateView(window)
        for i in range(len(self.pontos)-1): # desenho
            viewport.create_line(self.pontos[i].xV, self.pontos[i].yV, self.pontos[i+1].xV, self.pontos[i+1].yV, width = global_object_width, fill=self.cor)
        if self.fechado: # se é fechado desenho ultima reta
            viewport.create_line(pFinal.xV, pFinal.yV, self.pontos[0].xV, self.pontos[0].yV, width = 1, fill=self.cor)

            
