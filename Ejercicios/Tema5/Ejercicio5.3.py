from math import *
import numpy as np
from numpy.linalg import solve, norm
import matplotlib.pyplot as plt

def Gauss_Seidel(in_filas: int, in_cols:int, u_izq: float, u_der: float) -> np.array:
    V = np.zeros((in_filas+1, in_cols+1))

    # Establecemos los valores de contorno
    V[:, 0] = u_izq
    V[:, in_cols] = u_der

    tol = 1e-5

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
        for i in range(0, in_filas+1):
            for j in range(1, in_cols):
                    if i==0:
                        V[i,j] = 0.25 * (V[i,j] + V[i,j-1] + V[i,j+1] + V[i+1,j])
                    elif i==in_filas:
                        V[i,j] = 0.25 * (V[i-1,j] + V[i,j-1] + V[i,j+1] + V[i,j])
                    else:
                        V[i,j] = 0.25 * (V[i-1,j] + V[i,j-1] + V[i,j+1] + V[i+1,j])

        norma = norm(V)
        n += 1
        if n > max_iterations:
            print("El método no converge")
            return V
    
    return V, n


def main():
    # Condiciones de contorno.
    u_izq = -1
    u_der = 1

    # Dimensiones en las que dividimos.
    in_filas = 64
    in_columnas = 128

    print(f"-------------{in_filas}x{in_columnas}----------------")
        
    # Solución por métodos iterativos (Gauss-Seidel)
    V, n = Gauss_Seidel(in_filas, in_columnas, u_izq, u_der)

    # Representación gráfica de la placa
    fig, ax = plt.subplots(1,1)
    im = ax.imshow(V, cmap='gray', origin='lower', extent=[-1,1,-1,1])
    plt.colorbar(im, ax = ax)
    ax.set_title(f"Potencial.")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    x = np.linspace(-1,1,in_columnas+1)
    y = x*0
    ax.plot(x,y,'k', linestyle='--', linewidth=0.5)
    ax.plot(y,x,'k', linestyle='--', linewidth=0.5)
    plt.show()

    x = np.linspace(-1,1,in_columnas+1)
    y = np.linspace(-1,1,in_filas+1)
    cs=plt.contour(x,y,V,colors="k", negative_linestyles='solid')	
    clabels = plt.clabel(cs, inline=True)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.xlim(-1.1,1.1)
    plt.title("Líneas equipotenciales.")
    plt.show()

    print(f"Número de iteraciones: {n}")

if __name__ == "__main__":
    main()