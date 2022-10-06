import random
import math

class Matriz:
    def __init__(self, filas, columnas, valor=0):
        self.filas = filas
        self.columnas = columnas
        self.matriz = [[]]
        for fila in range(filas):
            for _ in range(columnas):
                self.matriz[fila].append(valor)
            self.matriz.append([])
    
    def __str__(self):
        cadena = ''
        for fila in range(self.filas):
            cadena += str(self.matriz[fila]) + '\n'
        return cadena
    
    def __add__(self, sumando):
        if (self.filas == sumando.filas and self.columnas == sumando.columnas):
            suma = Matriz(self.filas, self.columnas)
            for i in range(self.filas):
                for j in range(self.columnas):
                    suma.matriz[i][j] = self.matriz[i][j] + sumando.matriz[i][j]
            return suma
        print("Las matrices no son del mismo orden")
        return None
    
    def __sub__(self, restando):
        if (self.filas == restando.filas and self.columnas == restando.columnas):
            resta = Matriz(self.filas, self.columnas)
            for i in range(self.filas):
                for j in range(self.columnas):
                    resta.matriz[i][j] = self.matriz[i][j] - restando.matriz[i][j]
            return resta
        print("Las matrices no son del mismo orden")
        return None
            
    def __mul__(self, multiplicando):
        if (type(multiplicando) is int or type(multiplicando) is float):
            return self.multiplicacion_escalar(multiplicando)
        elif (self.columnas == multiplicando.filas):
            return self.multiplicacion_matricial(multiplicando)
        print("Las matrices no se pueden multiplicar")
        return None
            
    def multiplicacion_escalar(self, escalar):
        producto = Matriz(self.filas, self.columnas)
        for i in range(producto.filas):
            for j in range(producto.columnas):
                producto.matriz[i][j] = self.matriz[i][j] * escalar
        return producto
    
    def multiplicacion_matricial(self, otra):
        producto = Matriz(self.filas, otra.columnas)
        for i in range(producto.filas):
            for j in range(producto.columnas):
                for k in range(self.columnas):
                    producto.matriz[i][j] += self.matriz[i][k] * otra.matriz[k][j]
        return producto
    
    def llenar_individual(self):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                entrada = input(f"Valor [{fila}][{columna}]: ")
                try:
                    self.matriz[fila][columna] = int(entrada)
                except:
                    self.matriz[fila][columna] = float(entrada)
        print()
        
    def llenar_aleatorio(self, l_inferior=0, l_superior=10):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                self.matriz[fila][columna] = random.randint(l_inferior, l_superior)
        print()
    
class Transformador:
    def trasladar(self, px, py, tx, ty):
        p = Matriz(1, 3)
        p.matriz = [[px, py, 1]]
        t = Matriz(3, 3)
        t.matriz = [
            [1, 0, 0],
            [0, 1, 0],
            [tx, ty, 1]
        ]
        p_prima = p * t
        return [p_prima.matriz[0][0], p_prima.matriz[0][1]]

    def rotar(self, px, py, angulo, cx=0, cy=0):
        p = Matriz(1, 3)
        p.matriz = [[px, py, 1]]
        c_negativa = Matriz(3, 3)
        c_negativa.matriz = [
            [1, 0, 0],
            [0, 1, 0],
            [-cx, -cy, 1]
        ]
        grados = math.radians(angulo)
        r = Matriz(3, 3)
        r.matriz = [
            [math.cos(grados), math.sin(grados), 0],
            [-math.sin(grados), math.cos(grados), 0],
            [0, 0, 1]
        ]
        c_positiva = Matriz(3, 3)
        c_positiva.matriz = [
            [1, 0, 0],
            [0, 1, 0],
            [cx, cy, 1]
        ]
        p_prima = p * c_negativa * r * c_positiva
        return [p_prima.matriz[0][0], p_prima.matriz[0][1]]

    def escalar(self, px, py, sx, sy, cx=0, cy=0):
        p = Matriz(1, 3)
        p.matriz = [[px, py, 1]]
        c_negativa = Matriz(3, 3)
        c_negativa.matriz = [
            [1, 0, 0],
            [0, 1, 0],
            [-cx, -cy, 1]
        ]
        s = Matriz(3, 3)
        s.matriz = [
            [sx, 0, 0],
            [0, sy, 0],
            [0, 0, 1]
        ]
        c_positiva = Matriz(3, 3)
        c_positiva.matriz = [
            [1, 0, 0],
            [0, 1, 0],
            [cx, cy, 1]
        ]
        p_prima = p * c_negativa * s * c_positiva
        return [p_prima.matriz[0][0], p_prima.matriz[0][1]]
