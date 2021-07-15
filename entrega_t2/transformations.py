import math
import numpy as np
import objects


default_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
n = len(default_matrix)

def matrix_multiply(mat0, mat1):
    a = np.array(mat0)
    b = np.array(mat1)
    mat2 = np.matmul(a, b)
    return mat2

def line_multiply(dot, mat):
    out = [0, 0, 0]
    for i in range(3):
        for j in range(3):
            out[i] += dot[j] * mat[j][i]
    return out


def translacao(x, y, prev_transformation=default_matrix):
    t = [[1, 0, 0], [0, 1, 0], [x, y, 1]]
    return matrix_multiply(prev_transformation, t)

def escalonamento(s, prev_transformation=default_matrix):
    e = [[s, 0, 0], [0, s, 0], [0, 0, 1]]
    return matrix_multiply(prev_transformation, e)

def rotacao(anguloDeg, prev_transformation=default_matrix):
    angulo = math.radians(anguloDeg)
    r = [[math.cos(angulo), -math.sin(angulo), 0], 
         [math.sin(angulo), math.cos(angulo), 0], 
         [0, 0, 1]]

    return matrix_multiply(prev_transformation, r)

def decenter(objeto, prev_transformation=default_matrix):
    [cX, cY] = findCenter(objeto)
    return translacao(cX, cY, prev_transformation)

def center(objeto, prev_transformation=default_matrix):
    [cX, cY] = findCenter(objeto)
    return translacao(-cX, -cY, prev_transformation)

def applyTransform(objeto, matriz_transformacao):
    for p in objeto.pontos:
        # fazer multiplicacao de matriz
        var = line_multiply([p.x, p.y, 1], matriz_transformacao)
        # trocar xV yV do ponto
        p.x = var[0]
        p.y = var[1]

def findCenter(objeto):
    sumx = 0
    sumy = 0
    for p in objeto.pontos:
        sumx += p.x
        sumy += p.y
    n = len(objeto.pontos)
    return [sumx/n, sumy/n]

def transform(objeto, transformacoes, window, viewport):
    out = default_matrix
    for t in transformacoes:
        if t[0] == "translacao":
            out = translacao(t[1][0], t[1][1], out)
        if t[0] == "escalonamento":
            out = center(objeto, out)
            out = escalonamento(t[1][0], out)
            out = decenter(objeto, out)
        if t[0] == "rotacao":
            if t[1][0] == "1":
                out = center(objeto, out)
                out = rotacao(t[1][1], out)
                out = decenter(objeto, out)
            elif t[1][0] == "0":
                out = rotacao(t[1][1], out)
            else:
                out = translacao(-t[1][2], -t[1][3], out)
                out = rotacao(t[1][1], out)
                out = translacao(t[1][2], t[1][3], out)


    applyTransform(objeto, out)
    viewport.delete('all')
    window.updateObjects()

