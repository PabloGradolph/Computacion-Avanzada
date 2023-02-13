from math import sqrt, fabs
from timeit import default_timer
from itertools import product
import numpy as np

def constante_madelung(L: float) -> float:
    # Del enunciado sacamos la fórmula para M que procedemos a programar.
    # Primero inicializamos en cero la constante.
    M = 0
    bucle = list(product(np.arange(-L, L+1),repeat=3))
    bucle.remove((0,0,0)) # Evitamos dividir por cero

    for h in bucle:
        i,j,k = h[0],h[1],h[2]   
        M += (1/sqrt(i*i + j*j + k*k)) if (i+j+k)%2 == 0 else -(1/sqrt(i*i + j*j + k*k))
    
    return M

def errores(exacto: float, obtenido: float):
    # Cálculo de los errores absoluto y relativo
    Ea = fabs(exacto - obtenido)
    Er = fabs(Ea/exacto)*100
    return Ea, Er

def main():
    inicio = default_timer()
    Mexacta = -1.74756

    # Para L = 20
    Mobtenida = constante_madelung(20)
    Ea, Er = errores(Mexacta, Mobtenida)
    print(f"Para L = 20 --> M = {Mobtenida}; Error absoluto = {Ea}; Error relativo = {Er}%")

    # Para L = 50
    Mobtenida = constante_madelung(50)
    Ea, Er = errores(Mexacta, Mobtenida)
    print(f"Para L = 50 --> M = {Mobtenida}; Error absoluto = {Ea}; Error relativo = {Er}%")

    # Para L = 100
    Mobtenida = constante_madelung(100)
    Ea, Er = errores(Mexacta, Mobtenida)
    print(f"Para L = 100 --> M = {Mobtenida}; Error absoluto = {Ea}; Error relativo = {Er}%")

    # Para L = 200
    Mobtenida = constante_madelung(200)
    Ea, Er = errores(Mexacta, Mobtenida)
    print(f"Para L = 200 --> M = {Mobtenida}; Error absoluto = {Ea}; Error relativo = {Er}%")

    fin = default_timer()
    print()
    print(f"* Tiempo de ejecución del programa (s) = {fin - inicio}")

if __name__ == "__main__":
    main()