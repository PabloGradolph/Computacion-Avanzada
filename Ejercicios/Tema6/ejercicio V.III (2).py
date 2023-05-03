# COMPUTACIÓN AVANZADA - EJERCICIO VI.III
# PABLO TEJERO GARCÍA
# LA ECUACIÓN DE ONDA EN UNA DIMENSIÓN

import numpy as np
import matplotlib.pyplot as plt
from math import *
import random

np.set_printoptions(precision=3)

# Parámetros iniciales

L = 0.64     # Longitud de la cuerda en metros
m = 0.00448  # Masa lineal de la cuerda en kg/m
T = 70       # Tensión en la cuerda en N
dx = 0.08    # Tamaño del paso espacial en metros

# Función que genera el desplazamiento de una onda en base a una condición inicial en un momento temporal concreto
def ecuacion_onda_1d(N: int, r: float, pasos: int) -> np.array:
   
    u = np.zeros((pasos+1,N+1), float)  
    x0 = 0.16
    t = 0

    for i in range(N):

        if i*dx <= 0.16:
            u[t,i] = np.tan(0.006/x0)*(i*dx)

        else:
            u[t,i] = np.tan(0.006/(L - x0))*(L - i*dx)

    for t in range(pasos):
        for i in range(N):
            
            if i == 0 or i == N-1:
                u[t+1,i] = 0
            else:
                u[t+1,i] = -u[t-1, i] + 2*(1-(r*r))*u[t,i] + (r*r)*(u[t,i+1] + u[t,i-1])

    return u

def main():
    
    print()
    r = float(input("Introduzca el parámetro 'r': "))
    t_total = float(input("Introduzca el tiempo (en segundos) que desea estudiar: "))
    print()

    N = int(L / dx)
    
    
    dt = dx/sqrt(T/2*L) # 'lambda' = 2*L
    pasos = int(t_total/dt)

    u = ecuacion_onda_1d(N, r, pasos)

    # Graficamos la solución
    x = np.linspace(0, L, N+1)
    t_graf = random.randint(1, pasos)
    plt.plot(x, u[t_graf,:], marker = 'o', color = 'black', label = f"t = {round(t_graf*dt,3)}")
    plt.plot(x, u[0,:], color = 'blue', label = "t = 0")
    plt.xlabel('Posición (m)')
    plt.ylabel(f'Desplazamiento (m)')
    plt.title(f"Desplazamiento para r = {r} y t = {round(t_graf*dt,3)} (s)")
    plt.legend()
    plt.show()

    # Frecuencia de las vibraciones (Hz):

    mu = m / L
    v = sqrt(T/mu)
    f = v/(2*L)
    print(f)

    # Tensión (N) para una frecuencia de 82.41 Hz:

    f2 = 82.41
    T2 = mu*(f2*(2*L))*(f2*(2*L))
    print(T2)
   
if __name__ == "__main__":
    main()