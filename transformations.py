import math

default_matrix = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
n = len(default_matrix)

def matrix_multiply(mat0, mat1):
    mat2 = [[0]*3]*3
    for i in range(n):
        cont = 0
        for j in range(n):
            mat2[i][cont] += mat0[i][j] * mat1[j][i]
        cont += 1
    
    return mat2

def line_multiply(dot, mat):
    out = [0, 0, 0]
    for i in range(3):
        for j in range(3):
            out[i] = dot[j] + mat[j][i]
    return out


def translacao(prev_transformation=default_matrix, x, y):
    t = [[1, 0, 0], [0, 1, 0], [x, y, 1]]
    return matrix_multiply(prev_transformation, t)

def escalonamento(prev_transformation=default_matrix, s):
    e = [[s, 0, 0], [0, s, 0], [0, 0, 1]]
    return matrix_multiply(prev_transformation, e)

def rotacao(prev_transformation=default_matrix, angulo):
    r = [[math.cos(angulo), -math.sin(angulo), 0], 
         [math.sin(angulo), math.cos(angulo), 0], 
         [0, 0, 1]]

    return matrix_multiply(prev_transformation, r)

def decenter(prev_transformation, objeto, cX, cY):
    decenter = [[1, 0, 0], [0, 1, 0], [cX, cY, 1]]
    return matrix_multiply(prev_transformation, decenter)

def centerAndBack(prev_transformation=default_matrix, objeto):
    if objeto.pontos.empty(): # checo se não é ponto
        return
    somaX = 0
    somaY = 0
    for i in range(len(objeto.pontos)):
        somaX += objeto.pontos[i].xV
        somaY += objeto.pontos[i].yV
    cX = somaX/len(objeto.pontos)
    cY = somaY/len(objeto.pontos)
    center = [[1, 0, 0], [0, 1, 0], [-cX, -cY, 1]]
    center = matrix_multiply(prev_transformation, center)

def applyTransform(objeto, matriz_transformacao):
    if objeto.pontos.empty(): # checo se não é ponto
        var = [objeto.xV, objeto.yV, 1]
        return line_multiply(var, matriz_transformacao)

    for p in objeto.pontos:
        # fazer multiplicacao de matriz
        var = matrix_multiply([p.xV, p.yV, 1], matriz_transformacao)
        # trocar xV yV do ponto
        p.xV = var[0]
        p.yV = var[1]
    










    

