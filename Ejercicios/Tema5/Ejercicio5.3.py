# Tenemos la ecuación 0.25 * (V[i-1,j] + V[i,j-1] + V[i,j+1] + V[i+1,j]) + (p(i,j)*h^2)/4

from math import *
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt

def matriz_ro(in_filas: int, in_cols:int) -> np.array:
    ro = np.zeros((in_filas+1, in_cols+1), float)

    # Establecemos las condiciones iniciales a la matriz ro (variarán según el problema planteado)
    for i in range(in_filas):
        for j in range(in_cols):
            # Situamos la carga positiva
            if 19 <= i <= 39 and 59 <= j <= 79:
                ro[i,j] = 1
            
            # Situamos la carga negativa
            if 59 <= i <= 79 and 19 <= j <= 39:
                ro[i,j] = -1
    
    return ro

def Gauss_Seidel(ro: np.array, in_filas: int, in_cols:int, v_izq: float, v_der: float, v_arr: float, v_ab: float) -> np.array:
    V = np.zeros((in_filas+1, in_cols+1))

    # Sacamos el valor de h, teniendo en cuenta que la placa tiene 1metro lado.
    h = 1/100 # Total/número de divisiones.

    # Establecemos los valores de contorno
    V[0, :] = v_arr
    V[in_filas, :] = v_ab
    V[:, 0] = v_izq
    V[:, in_cols] = v_der

    tol = 1e-4

    # Por si acaso no converge el método.
    max_iterations = 10000
    n = 0
    
    # Bucle while hasta que la diferencia de las normas esté por debajo de la tolerancia.
    norma = norm(V)
    norma_anterior = norma + 5 # Nos aseguramos de entrar en el bucle while

    # Agoritmo de Gauss-Seidel
    while fabs(norma - norma_anterior) > tol:
        # Copiar la solución anterior
        u_old = np.copy(V)
        norma_anterior = norm(u_old)

        # Actualizar la solución en los puntos interiores
        for i in range(1, in_filas):
            for j in range(1, in_cols):
                V[i,j] = 0.25 * (V[i-1,j] + V[i,j-1] + V[i,j+1] + V[i+1,j]) + (ro[i,j]*h*h)/4

        norma = norm(V)
        n += 1
        if n > max_iterations:
            print("El método no converge")
            return V
    
    return V, n

def main():
    # Condiciones de contorno.
    v_izq = 0
    v_der = 0
    v_ab = 0
    v_arr = 0

    # Dimensiones en las que dividimos.
    in_filas = 100
    in_columnas = 100

    print(f"-------------{in_filas}x{in_columnas}----------------")
        
    # Solución por métodos iterativos (Gauss-Seidel)
    ro = matriz_ro(in_filas, in_columnas)
    V, n = Gauss_Seidel(ro, in_filas, in_columnas, v_izq, v_der, v_arr, v_ab)
    
    # Representación gráfica de la placa
    fig, ax = plt.subplots(1,1)
    im = ax.imshow(V, cmap='gray', extent=[0,1,0,1])
    plt.colorbar(im, ax = ax)
    ax.set_title("Potencial.")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    x = np.linspace(0,1,in_columnas+1)
    y = x*0
    ax.plot(x,y,'k', linestyle='--', linewidth=3)
    ax.plot(y,x,'k', linestyle='--', linewidth=3)
    plt.show()

    x = np.linspace(0,1,in_columnas+1)
    y = np.linspace(0,1,in_filas+1)
    levels = [-0.011, -0.007, -0.002, 0.002, 0.007, 0.011]
    cs=plt.contour(x,y,V,colors="k",levels=levels, negative_linestyles='solid')	
    plt.clabel(cs, inline=True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-0.1,1.1)
    plt.title("Líneas equipotenciales.")
    plt.show()

    print(f"Número de iteraciones: {n}")

if __name__ == "__main__":
    main()