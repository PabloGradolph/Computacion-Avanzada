from math import *
import numpy as np
from numpy.linalg import solve, norm
import matplotlib.pyplot as plt
import time

def construir_sistema(in_filas: int, in_cols:int , u_izq: float, u_der: float, u_arr: float, u_ab: float) -> np.array:
    
    # Dividimos la malla
    incognitas = (in_cols - 1) * (in_filas - 1)

    # Matrices para el sistema.
    A = np.zeros([incognitas, incognitas], float)
    b = np.zeros(incognitas, float)
    
    # Creamos A
    for i in range(incognitas):
        for j in range(incognitas):
            if i == j: # Elementos diagonal
                A[i,j] = -4
            elif i == j+1 and (i) % (in_cols-1) != 0:
                A[i,j] = 1
            elif i == j-1 and (i+1) % (in_cols-1) != 0:
                A[i,j] = 1
            elif j == i + in_cols - 1 or i == j + in_cols - 1:
                A[i,j] = 1
    
    # Creamos b
    for i in range(incognitas):
        if (i+1) % (in_cols-1) == 0 and i != 0:
            b[i] = - u_der

    # Si se quieren ver las matrices creadas para hacer comprobaciones.
    # print(A)
    # np.savetxt("matriz.txt", A, fmt="%5.2f")
    # print()
    # print(b)

    return A, b

def Gauss_Seidel(in_filas: int, in_cols:int, u_izq: float, u_der: float, u_arr: float, u_ab: float) -> np.array:
    u = np.zeros((in_filas+1, in_cols+1))

    # Establecemos los valores de contorno
    u[0, :] = u_arr
    u[in_filas, :] = u_ab
    u[:, 0] = u_izq
    u[:, in_cols] = u_der

    tol = 1e-2

    # Por si acaso no converge el método.
    max_iterations = 10000
    n = 0
    
    # Bucle while hasta que la diferencia de las normas esté por debajo de la tolerancia.
    norma = norm(u)
    norma_anterior = norma + 5 # Nos aseguramos de entrar en el bucle while

    # Agoritmo de Gauss-Seidel
    while fabs(norma - norma_anterior) > tol:
        # Copiar la solución anterior
        u_old = np.copy(u)
        norma_anterior = norm(u_old)

        # Actualizar la solución en los puntos interiores
        for i in range(1, in_filas):
            for j in range(1, in_cols):
                u[i,j] = 0.25*(u[i-1,j] + u[i,j-1] + u[i,j+1] + u[i+1,j])

        norma = norm(u)
        n += 1
        if n > max_iterations:
            print("El método no converge")
            return u
    
    return u, n

def main():
    # Condiciones de contorno.
    u_izq, u_ab, u_arr = 0, 0, 0
    u_der = 100

    # Dimensiones con las que empezamos.
    in_filas = 4
    in_columnas = 8

    for _ in range(5): # Se pude poner hasta 6 para conseguir 128x256 pero tarda unos 15 minutos.
        print(f"-------------{in_filas}x{in_columnas}----------------")
        inicio_directo = time.time()

        # Solución directa.
        A, b = construir_sistema(in_filas, in_columnas, u_izq, u_der, u_arr, u_ab)
        x = solve(A, b)
        final_directo = time.time()
        x = list(x)

        placa = np.zeros([in_filas + 1, in_columnas + 1], float)
        for i in range(in_filas+1):
            for j in range(in_columnas+1):
                if j == in_columnas:
                    placa[i,j] = u_der
                elif i != 0 and j != 0 and i != in_filas:
                    placa[i,j] = x[0]
                    x.pop(0)
        
        # Solución por métodos iterativos (Gauss-Seidel)
        inicio_iterativo = time.time()
        u, n = Gauss_Seidel(in_filas, in_columnas, u_izq, u_der, u_arr, u_ab)
        final_iterativo = time.time()

        # Representación gráfica de la placa
        fig, ax = plt.subplots(1,2)
        im = ax[0].imshow(placa, cmap='gray')
        plt.colorbar(im, ax = ax[0])
        ax[0].set_title(f"Solución directa. {in_filas}x{in_columnas}")
        im = ax[1].imshow(u, cmap='gray')
        plt.colorbar(im, ax = ax[1])
        ax[1].set_title(f"Solución métodos iterativos. {in_filas}x{in_columnas}")
        plt.show()

        print(f"*Tiempo de ejecución directo (s): {final_directo-inicio_directo}")
        print(f"*Tiempo de ejecución iterativo (s): {final_iterativo-inicio_iterativo}")
        print(f"Número de iteraciones: {n}")
        i,j = int(in_filas/2), int(in_columnas/2)
        print(f"Tempertura en el centro de la placa: Directo -> {placa[i,j]} ; Iterativo -> {u[i,j]}")
        print()

        in_filas *= 2
        in_columnas *= 2

if __name__ == "__main__":
    main()