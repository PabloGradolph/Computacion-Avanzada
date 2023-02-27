#------------------------------------
# Clase del 22 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Búsqueda de ceros de una función Bisección, Secante y Newton
#------------------------------------

from math import fabs

def funcion(t: float) -> float:
    pass

def derivada(t: float) -> float:
    pass

# Cálculo de ceros de la función por el método de la bisección
def biseccion(t1: float, t2: float, tol: float) -> float:
    # Definimos el nuevo punto
    t3 = (t1+t2)/2 

    # Número de iteraciones
    n = 1
    while fabs(funcion(t3)) > tol:
        if funcion(t3)*funcion(t1) < 0:
            t2 = t3
        else:
            t1 = t3
        t3 = (t1 + t2)/2
        n += 1

    # Retornamos valor del tiempo y el número de iteraciones.
    return t3, n

def secante(t1: float, t2: float, tol: float) -> float:
    pass

def newton(t1: float, tol: float) -> float:
    t = t1 - funcion(t1)/derivada(t1)
    f = funcion(t)

    # Número de iteraciones
    n = 1
    while fabs(f) > tol:
        t = t - funcion(t)/derivada(t)
        f = funcion(t)
        n += 1
    
    # Retornamos valor del tiempo y el número de iteraciones.
    return t, n