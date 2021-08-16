import math
import numpy as np
import objects


default_matrix = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]
n = len(default_matrix)

def matrix_multiply(mat0, mat1):
    a = np.array(mat0)
    b = np.array(mat1)
    # print(a)
    # print(b)
    mat2 = np.matmul(a, b)
    return mat2

def line_multiply(dot, mat):
    out = [0, 0, 0, 0]
    for i in range(n):
        for j in range(n):
            out[i] += dot[j] * mat[j][i]
    return out

# novo parametro z
def translacao(x, y, z=0, prev_transformation=default_matrix):
    t = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [x, y, z, 1]]
    return matrix_multiply(prev_transformation, t)

# novo parametro sz
def escalonamento(s, sy=False, sz=False, prev_transformation=default_matrix):
    # print(sy, sz)
    e = [[s, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 1]]
    if sy != False:
        e[1][1] = sy
    else:
        e[1][1] = s
        # return matrix_multiply(prev_transformation, e)
    if sz != False:
        e[2][2] = sz
    else:
        e[2][2] = s
    # e = [[s, 0, 0], [0, s, 0], [0, 0, 1]]
    return matrix_multiply(prev_transformation, e)

# novo parametro eixo: x = 0, y = 1, z = 2
def rotacao(anguloDeg, prev_transformation=default_matrix, axis='2'):
    angulo = math.radians(-anguloDeg)
    # print('transforms.rotacao: ', anguloDeg, axis)
    if axis == '2':
        r = [[math.cos(angulo), math.sin(angulo), 0, 0], 
            [-math.sin(angulo), math.cos(angulo), 0, 0], 
            [0, 0, 1, 0],
            [0, 0, 0, 1]]

    elif axis == '0':
        r = [[1, 0, 0, 0], 
            [0, math.cos(angulo), math.sin(angulo), 0],
            [0, -math.sin(angulo), math.cos(angulo), 0],
            [0, 0, 0, 1]]

    elif axis == '1':
        r = [[math.cos(angulo),0, -math.sin(angulo), 0],  
            [0, 1, 0, 0],
            [math.sin(angulo), 0, math.cos(angulo), 0],
            [0, 0, 0, 1]]
    
    # print(r)

    return matrix_multiply(prev_transformation, r)

def decenter(objeto, prev_transformation=default_matrix):
    [cX, cY, cZ] = findCenter(objeto)
    return translacao(cX, cY, cZ, prev_transformation)

def center(objeto, prev_transformation=default_matrix):
    [cX, cY, cZ] = findCenter(objeto)
    return translacao(-cX, -cY, -cZ, prev_transformation)

def findCenter(objeto):
    sumx = 0
    sumy = 0
    sumz = 0
    
    if objeto.tipo != 'wireframe':
        for p in objeto.pontos:
            sumx += p.x
            sumy += p.y
            sumz += p.z    
        n = len(objeto.pontos)    
    
    else:
        for r in objeto.retas:
            sumx += r.pontos[0].x
            sumy += r.pontos[0].y
            sumz += r.pontos[0].z
        n = len(objeto.retas)
    
    return [sumx/n, sumy/n, sumz/n]

def applyTransform(objeto, matriz_transformacao):
    if objeto.tipo == 'reta':
        for p in objeto.pontos:
            # print(f'ponto {p.x}, {p.y}, {p.z}')
            # fazer multiplicacao de matriz
            # print('mtrans')
            # print(matriz_transformacao)
            var = line_multiply([p.x, p.y, p.z, 1], matriz_transformacao)
            # trocar xV yV do ponto
            # print(f'px: {p.x}, py: {p.y}, pz: {p.z}')
            # print(f'multiplied: {var[0]}, {var[1]}, {var[2]}')
            p.x = var[0]
            p.y = var[1]
            p.z = var[2]

    elif objeto.tipo == 'wireframe':       # when dealing with Objeto3D
        for r in objeto.retas:
            var = line_multiply([r.pontos[0].x, r.pontos[0].y, r.pontos[0].z, 1], matriz_transformacao)
            r.pontos[0].x = var[0]
            r.pontos[0].y = var[1]
            r.pontos[0].z = var[2]
    
    else: # ponto
        var = line_multiply([objeto.x, objeto.y, objeto.z, 1], matriz_transformacao)
        objeto.x = var[0]
        objeto.y = var[1]
        objeto.z = var[2]

def transform(objeto, transformacoes, window):
    out = default_matrix
    for t in transformacoes:
        if t[0] == "translacao":
            t[1][0] = round(t[1][0], 2)
            t[1][1] = round(t[1][1], 2)
            t[1][2] = round(t[1][2], 2)
            # descubro novo vetor de translacao relativo ao angulo da tela
            # print(f'{t[1][0]}, {t[1][1]}, {t[1][2]}')
            vector = objects.Reta3D(objects.Ponto3D(0,0,0), objects.Ponto3D(t[1][0], t[1][1], t[1][2]))
            # vector = objects.Objeto3D([objects.Reta3D(objects.Ponto3D(0, 0, 0), vector)])
            aux = rotacao(window.angulo)
            # print(aux.retas)
            applyTransform(vector, aux)
            out = translacao(vector.pontos[1].x, vector.pontos[1].y, vector.pontos[1].z, out)
            # print(f'out:{out}')
        elif t[0] == "escalonamento":
            s = round(t[1][0], 2)
            print('aaa')
            out = center(objeto, out)
            out = escalonamento(s, out)
            out = decenter(objeto, out)
        elif t[0] == "escalonamento_total":
            print('ccc')
            sx = round(t[1][0], 2)
            sy = round(t[1][1], 2)
            sz = round(t[1][2], 2)
            out = escalonamento(sx, sy, sz, out)
        elif t[0] == 'escalonamento_total_centro':
            print('bbb')
            sx = round(t[1][0], 2)
            sy = round(t[1][1], 2)
            sz = round(t[1][2], 2)
            out = center(objeto, out)
            out = escalonamento(sx, sy, sz, out)
            out = decenter(objeto, out)
        elif t[0] == "rotacao":
            if t[1][0] == "1":
                t[1][1] = round(t[1][1], 2)
                out = center(objeto, out)
                out = rotacao(t[1][1], out, t[1][2])
                out = decenter(objeto, out)
            elif t[1][0] == "0":
                t[1][1] = round(t[1][1], 2)
                out = rotacao(t[1][1], out, t[1][2])
            else:
                t[1][1] = round(t[1][1], 2)
                t[1][3] = round(t[1][3], 2)
                t[1][4] = round(t[1][4], 2)
                t[1][5] = round(t[1][5], 2)
                out = translacao(-t[1][3], -t[1][4], -t[1][5], prev_transformation=out)
                out = rotacao(t[1][1], out, t[1][2])
                out = translacao(t[1][3], t[1][4], t[1][5], prev_transformation=out)
    # print('b4')
    # for p in objeto.pontos:
    #     print(f'{p.x}, {p.y}, {p.z}')
    # print('out')
    # print(out)
    # print('transform(b4, out)->')
    applyTransform(objeto, out)
    # print('4ft3r')
    # for p in objeto.pontos:
    #     print(f'{p.x}, {p.y}, {p.z}')
 

    if objeto.nome == 'window':
        objeto.findNormalizingMatrix()  # test
        applyTransform(objeto.view_plane_normal, out)
        # print('is it here?')
        # print(out)
        applyTransform(objeto.view_reference_point, out)
        # print('mah z: ', objeto.view_plane_normal.z)
        objeto.normalizeAll()
    else:
        index = window.objetos.index(objeto)
        window.normalizeObject(index)
    window.viewport.delete('all')
    window.updateObjects()

def getTransformMatrix(transformacoes):
    out = default_matrix
    for t in transformacoes:
        if t[0] == "translacao":
            out = translacao(t[1][0], t[1][1], prev_transformation=out)
        if t[0] == "escalonamento_total":
            out = escalonamento(t[1][0], t[1][1], prev_transformation=out)
        if t[0] == "rotacao":
            if t[1][0] == "0":
                out = rotacao(t[1][1], out)
            else:
                out = translacao(-t[1][2], -t[1][3], prev_transformation=out)
                out = rotacao(t[1][1], out)
                out = translacao(t[1][2], t[1][3], prev_transformation=out)
    
    return out

