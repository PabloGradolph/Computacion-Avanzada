from math import *
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt

def Gauss_Seidel(in_filas: int, in_cols:int, u_izq: float, u_der: float) -> np.array:
    # Constantes
    d = 0.5
    Q = 0.6
    k = 0.16
    H = 0.073
    ur = 25

    # Intercambio de filas y columnas para la matriz
    in_columnas = in_filas
    in_filas = in_cols 

    # Matriz solución
    u = np.zeros((in_filas+1, in_columnas+1))

    # Iteraciones.
    max_iterations = 10000
    n = 0

    # Cálculo de h
    h1 = 9/in_filas
    h2 = 5/in_columnas
    if h1 != h2:
        print("Error al discretizar la malla, la distancia entre los puntos no es la misma en todas las direcciones.")
        return u, n
    h = h1 # Si h1 = h2 -> Establecemos el valor de h (bien discretizada la placa)

    # Establecemos los valores de contorno.
    u[0, :] = u_izq
    u[in_filas, :] = u_der
    u_arr = -15 # Esta condición es en función de la derivada pero es constante así la definimos fuera del bucle.

    # Tolerancia/Epsilon
    tol = 1e-2

    # Bucle while hasta que la diferencia de las normas esté por debajo de la tolerancia.
    norma = norm(u)
    norma_anterior = norma + 5 # Nos aseguramos de entrar en el bucle while

    # Agoritmo de Gauss-Seidel
    while fabs(norma - norma_anterior) > tol:
        # Copiar la solución anterior
        u_old = np.copy(u)
        norma_anterior = norm(u_old)

        # Actualizar la solución en los puntos interiores
        for j in range(0, in_columnas+1):
            for i in range(1, in_filas):
                if j == 0:
                    u_ab = H/k * (u[i,j] - ur) # Condición de contorno de la fila 0.
                    u[i,j] = 0.25*(2*u[i,j+1] + u[i-1,j] + u[i+1,j] - (h*h*Q/(k*d) + 2*h*u_ab))
                elif j == in_columnas:
                    u[i,j] = 0.25*(2*u[i,j-1] + u[i-1,j] + u[i+1,j] - (h*h*Q/(k*d) - 2*h*u_arr))
                else:
                    u[i,j] = 0.25*(u[i-1,j] + u[i,j-1] + u[i,j+1] + u[i+1,j] - h*h*Q/(k*d))

        # Aplicar las condiciones de frontera
        norma = norm(u)
        n += 1
        if n > max_iterations:
            print("El método no converge")
            return u, n
    
    return u, n

def main():
    # Condiciones de contorno
    u_izq = 20
    u_der = 20

    # Dimensiones en las que dividimos.
    in_filas = 50
    in_cols = 90

    print(f"-------------{in_filas}x{in_cols}----------------")

    u, n = Gauss_Seidel(in_filas, in_cols, u_izq, u_der)
    u = np.transpose(u)
    np.savetxt("matriz.txt", u, fmt="%5.2f")
    fig, ax = plt.subplots(1,1)
    im = ax.imshow(u, cmap='gray', origin='lower', extent=[0,9,0,5])
    plt.colorbar(im, ax = ax)
    ax.set_title("Temperaturas.")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_aspect("equal", "box")
    plt.show()

    print(f"Número de iteraciones: {n}")
    
if __name__ == "__main__":
    main()
