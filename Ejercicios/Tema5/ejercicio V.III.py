# COMPUTACIÓN AVANZADA - EJERCICIO V.III
# PABLO TEJERO GARCÍA
# ECUACIONES DE LAPLACE Y POISSON - EL POTENCIAL ELÉCTRICO

import numpy as np
import matplotlib.pyplot as plt
import time

# -------------------- DISTRIBUCIÓN DE POTENCIAL ELÉCTRICO Y CAMPO ELÉCTRICO EN UNA PLACA DE UN METRO CUADRADO -------------------- #

# Función que genera una malla de puntos NxN a partir de una entrada N
# Además, la matriz genera el correspondiente parámetro 'h' en base a la entrada dada
def malla_puntos(N: int) -> np.array:
    
    x = np.linspace(0, 1, N)
    y = np.linspace(0, 1, N)

    X, Y = np.meshgrid(x, y)

    # Parámetro 'h' empleado para discretizar la malla creada
        # Todos los puntos se encuentran separados entre sí por una distancia 'h'
        # Con el aumento de 'h' aumenta la precisión a la par que el tiempo de ejecución
        
    h = 1/(N-1)

    return X, Y, h

def potencial_electrico_poisson(N: int, h: float, X: np.array, Y: np.array, V: np.array) -> np.array:
    
    # Matriz 'rho' = Matriz de densidad de carga eléctrica en la malla.
    rho = np.zeros((N, N))
    rho[(X >= 0.6) & (X <= 0.8) & (Y >= 0.6) & (Y <= 0.8)] = 1
    rho[(X >= 0.2) & (X <= 0.4) & (Y >= 0.2) & (Y <= 0.4)] = -1

    # En este caso, no hay carga eléctrica fuera de las condiciones de contorno.
    # Por tanto, la ecuación de Poisson queda reducida a una ecuación de Laplace.    
    
    # Mayor eficiencia del código
    # 10000 iteraciones logran un equilibrio entre precisión en el gráfico y ejecución veloz
    for _ in range(10000):
       V[1:-1, 1:-1] = 0.25 * (V[1:-1, 2:] + V[1:-1, :-2] + V[2:, 1:-1] + V[:-2, 1:-1] + h**2 * rho[1:-1, 1:-1])

    '''
    Método simple, aumentando drásticamente el tiempo de ejecución:

    for _ in range(10000):
        for i in range(1, N-1):
                for j in range(1, N-1):
                    V[i, j] = 0.25 * (V[i-1, j] + V[i+1, j] + V[i, j-1] + V[i, j+1] + h**2 * rho[i, j])
    
    '''

    return V

def campo_electrico_laplace(N: int, h: float, V: np.array) -> np.array:

    # El campo eléctrico, basado en la ecuación de Laplace, consiste en el gradiente del potencial eléctrico

    # Generación de matrices de campo eléctrico, una por cada derivada parcial
    # Mismas dimensiones frente a la matriz de potencial (y, por tanto, frente a la malla NxN)
    Ex = np.zeros((N, N))
    Ey = np.zeros((N, N))

    # Cálculo de la derivada en todos los puntos a excepción de los bordes
    # Se emplea el método de diferencias finitas centradas
    Ex[:, 1:-1] = -(V[:, 2:] - V[:, :-2]) / (2 * h)
    Ey[1:-1, :] = -(V[2:, :] - V[:-2, :]) / (2 * h)

    return Ex, Ey

def main():

    print()
    print("DISTRIBUCIÓN DE POTENCIAL ELÉCTRICO Y CAMPO ELÉCTRICO EN UNA PLACA DE UN METRO CUADRADO")
    print()
    print("A continuación, introduzca el parámetro 'N' empleado para la generación de la malla 'NxN'.")
    print("La precisión del cálculo aumentará con el aumento de 'N'.")
    print()

    N = int(input(" Introduzca el parámetro N: "))
    
    print()
    print(f"N = {N}")
    print(f"PLACA = {N}x{N}")
    print()

    tiempo_inicial = time.perf_counter()
    
    # Generación de la malla en base al parámetro 'N' 
    # Con su correspondiente parámetro 'h'
    X, Y, h = malla_puntos(N)    

    # Generación de una matriz de potencial con las mismas dimensiones que la malla
    V = np.zeros((N, N))

    # Definición de las condiciones de frontera
    V[(X >= 0.6) & (X <= 0.8) & (Y >= 0.6) & (Y <= 0.8)] = 1
    V[(X >= 0.2) & (X <= 0.4) & (Y >= 0.2) & (Y <= 0.4)] = -1

    V = potencial_electrico_poisson(N, h, X, Y, V)
    Ex, Ey = campo_electrico_laplace(N, h, V)

    tiempo_final = time.perf_counter()

    tiempo_total = tiempo_final - tiempo_inicial
    print(f"Tiempo de ejecución: {round(tiempo_total, 2)} segundos.")
    print()

    # -------------------------- POTENCIAL ELÉCTICO: 'IMSHOW' -------------------------- #

    plt.imshow(V, origin='lower', extent=(0, 1, 0, 1), cmap = 'magma')
    plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Potencial eléctrico')
    plt.show()

    # ------------------------ LÍNEAS EQUIPOTENCIALES: 'CONTOUR' ------------------------ #
    
    cs = plt.contour(X, Y, V, 10, cmap = 'magma')
    plt.clabel(cs)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Líneas equipotenciales')
    plt.show()

    # ---------------------------- CAMPO ELÉCTRICO: 'QUIVER' ---------------------------- #
    
    # Mostramos sólo una de cada cinco flechas
    mask = np.zeros((N, N))
    mask[::5, ::5] = 1  
    
    plt.quiver(X[mask==1], Y[mask==1], Ex[mask==1], Ey[mask==1], scale = 4, cmap='cool', pivot='mid', headwidth = 1.5)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Campo eléctrico')
    plt.show()

main()




