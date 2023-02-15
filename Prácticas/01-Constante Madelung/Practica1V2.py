# Versión 2 del cálculo de la constante de madelung tratando de optimizar el código al máximo.

from math import sqrt, fabs
from timeit import default_timer
from itertools import product   
import numpy as np

def constante_madelung(L: float) -> float:
    
    # Primero inicializamos en cero la constante.
    M = 0

    # Creamos todas las posibles coordenadas con la función product de la librería itertools
    bucle = list(product(np.arange(-L, L+1),repeat=3))
    bucle.remove((0,0,0)) # Evitamos dividir por cero quitando la coordenada (0,0,0)

    for coordenada in bucle:
        i,j,k = coordenada[0],coordenada[1],coordenada[2] 
        M += ((-1)**(fabs(i+j+k))) * (1/sqrt(i*i + j*j + k*k)) # fabs(i+j+k) porque no se admiten potencias negativas.
    
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
    # Otra forma más eficiente que la versión 1, pero con tiempo de ejecución similar a la planteada con el bucle "for h in bucle" es la siguiente:
    # Comenta el bucle for entero y ejecuta/descomenta la siguiente línea comentada:
    # M = sum(map(lambda coor: ((-1)**(fabs(coor[0]+coor[1]+coor[2]))) * (1/sqrt(coor[0]*coor[0] + coor[1]*coor[1] + coor[2]*coor[2])), bucle))
    # - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
    
    return M 

def errores(exacto: float, obtenido: float):
    # Cálculo de los errores absoluto y relativo
    Ea = fabs(exacto - obtenido)
    Er = fabs(Ea/exacto)*100
    return Ea, Er 


def main():
    inicio = default_timer()
    Mexacta = -1.74756

    for L in [20,50,100,200]:
        Mobtenida = constante_madelung(L)
        Ea, Er = errores(Mexacta, Mobtenida)
        print(f"Para L = {L} --> M = {Mobtenida}; Error absoluto = {Ea}; Error relativo = {Er}%")

    fin = default_timer()
    print()
    print(f"* Tiempo de ejecución del programa (s) = {fin - inicio}")

if __name__ == "__main__":
    main()