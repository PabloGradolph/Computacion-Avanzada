# Escribir un programa que calcule la integral de un círculo de radio r=1 mediante el método de integración de Montecarlo. Probar varios valores de N hasta 10^7. 
# Comparar la eficiencia de realizar este ejercicio en Python y en C++.

import time
from random import *
from math import sqrt, pi, fabs

def circulo_montecarlo(N: int, r: float) -> float:
    # Méodo de montecarlo.
    exitos = 0
    for _ in range(N):
        x = random()
        y = random()
        if y <= sqrt(1-(x*x)):
            exitos += 1

    # Áea del círculo = 4 * Ndentro/Ntotal multiplicado por el área del cuadrado (r*r)
    area = 4 * ((exitos/N) * (r*r))
    return area

def main():
    start = time.time()
    r = 1
    for N in [100, 1000, 10000, 100000, 1000000, 10000000]:
        area = circulo_montecarlo(N, r)
        error = fabs(area - (pi*(r**2)))
        print(f"Área del círculo con {N} intentos = {area}. Error cometido = {error}")
        
    print()
    print(f" * Tiempo de ejecución = {time.time() - start} (s)")

    # En Python tarda alrededor de 3 segundos mientras que en C++ no llega a la centésima de segundo.
    # Ejecutar Ejercicio3.2.cpp para ver la diferencia

if __name__ == "__main__":
    main()