import tkinter as tk

global_object_width = 1

class Ponto():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def xOnView(self, window):
        return ((self.x - window.xWmin)/(window.xWmax-window.xWmin))*(window.viewport.xVmax - window.viewport.xVmin)
    
    def yOnView(self, window):
        return (1 - (self.y - window.yWmin)/(window.yWmax-window.yWmin))*(window.viewport.yVmax - window.viewport.yVmin)
    
    def drawPonto(self, window, cor):
        window.viewport.create_oval(self.xOnView(window), self.yOnView(window), self.xOnView(window), self.yOnView(window), width = 1, outline=cor)

    def xNormalizedViewportTransform(self, window):
        return ((self.x*(window.viewport.xVmax/2) - window.xWmin)/(window.xWmax-window.xWmin))*(window.viewport.xVmax - window.viewport.xVmin)
        
    def yNormalizedViewportTransform(self, window):
        return (1 - (self.y*(window.viewport.yVmax/2) - window.yWmin)/(window.yWmax-window.yWmin))*(window.viewport.yVmax - window.viewport.yVmin)

    def drawNormalizedDot(self, window, cor):
        window.viewport.create_oval(self.xNormalizedViewportTransform(window), self.yNormalizedViewportTransform(window),
             self.xNormalizedViewportTransform(window), self.yNormalizedViewportTransform(window), width = 1, outline=cor)

class Wireframe():
    def __init__(self, pontos, nome, tipo, cor='black', fechado=False):
        self.pontos = pontos
        self.nome = nome
        self.tipo = tipo
        self.cor = cor
        # if fechado:
        #     self.pontos.append(self.pontos[0])
        self.fechado = fechado
    
    def drawObject(self, window):
        if len(self.pontos) == 1:
            self.pontos[0].drawPonto(window, self.cor)
            return
        
        for i in range(len(self.pontos) - 1):
            window.viewport.create_line(self.pontos[i].xOnView(window), self.pontos[i].yOnView(window), self.pontos[i+1].xOnView(window), 
                self.pontos[i+1].yOnView(window), width = global_object_width, fill=self.cor)

    def drawObjectNormalized(self, window):
        if len(self.pontos) == 1:
            self.pontos[0].drawNormalizedDot(window, self.cor)
            return
        
        for i in range(len(self.pontos) - 1):
            window.viewport.create_line(self.pontos[i].xNormalizedViewportTransform(window), self.pontos[i].yNormalizedViewportTransform(window), 
                self.pontos[i+1].xNormalizedViewportTransform(window), self.pontos[i+1].yNormalizedViewportTransform(window), 
                width = global_object_width, fill=self.cor)
        if self.fechado:
            window.viewport.create_line(self.pontos[-1].xNormalizedViewportTransform(window), self.pontos[-1].yNormalizedViewportTransform(window), 
                self.pontos[0].xNormalizedViewportTransform(window), self.pontos[0].yNormalizedViewportTransform(window), 
                width = global_object_width, fill=self.cor)
            
#############################
##    clipping methods     ##
#############################

# cohen-sutherland
def cohenSutherland(reta, window):
    region_vector = [regionCode(reta.pontos[0]), regionCode(reta.pontos[1])]
    if region_vector[0] & region_vector[1] != 0b0000:
        return 0
    if region_vector[0] == region_vector[1]:
        # draw it all
        pass
    return 0
    


def regionCode(ponto):
    reg_code = 0b0000   # fully inside
    if ponto.x > 1:
        reg_code = reg_code | 0b0010
    if ponto.x < -1:
        reg_code = reg_code | 0b0001
    if ponto.y > 1:
        reg_code = reg_code | 0b1000
    if ponto.y < -1:
        reg_code = reg_code | 0b0100
    return reg_code


