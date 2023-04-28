from math import *
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt
import time

def Gauss_Seidel(in_filas: int, in_cols:int, u_izq: float, u_der: float, tol: float) -> np.array:
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
    u = np.zeros((in_filas+1, in_columnas+1)) # Matriz orientada en vertical.

    # Iteraciones.
    max_iterations = 20000
    n = 0

    # Cálculo de h
    h1 = 9/in_filas
    h2 = 5/in_columnas
    if h1 != h2:
        print("Error al discretizar la malla, la distancia entre los puntos no es la misma en todas las direcciones.")
        return u, n
    h = h1 # Si h1 = h2 -> Establecemos el valor de h (bien discretizada la placa)

    # Establecemos los valores de contorno. (La matriz está transpuesta)
    u[0, :] = u_izq
    u[in_filas, :] = u_der
    u_arr = -15 # Esta condición es en función de la derivada pero es constante así la definimos fuera del bucle.
    u_ab = np.zeros((in_filas+1,1), float) # Esta matriz de una columna la utilizaremos para guardar las condiciones de frontera del límite inferior.

    # Bucle while hasta que la diferencia de las normas esté por debajo de la tolerancia.
    norma = norm(u)
    norma_anterior = norma + 5 # Nos aseguramos de entrar en el bucle while

    # Agoritmo de Gauss-Seidel
    while fabs(norma - norma_anterior) > tol:
        # Copiar la solución anterior
        u_old = np.copy(u)
        norma_anterior = norm(u_old)

        # Actualizar la solución en los puntos interiores
        for j in range(1, in_columnas):
            for i in range(1, in_filas):
                u[i,j] = 0.25*(u[i-1,j] + u[i,j-1] + u[i,j+1] + u[i+1,j] - h*h*Q/(k*d))

        # Aplicar las condiciones de frontera (tener en cuenta que la matriz está traspuesta)
        u_ab[:,0] = H/k * (u[:, 1] - ur)
        u[1:-1, in_columnas] = 0.25*(2*u[1:-1, -2] + u[:-2, in_columnas] + u[2:, in_columnas] - (h*h*Q/(k*d) - 2*h*u_arr))
        u[1:-1, 0] = 0.25*(2*u[1:-1, 1] + u[:-2, 0] + u[2:, 0] - (h*h*Q/(k*d) + 2*h*u_ab[1:-1,0]))
        u[0, :] = u_izq
        u[in_filas, :] = u_der

        # -----------------------------------------------------------------------------------------
        # OTRA VERSIÓN DEL ALGORITMO CON EL QUE OBTENEMOS LO MISMO: Algo más lenta.
        # for j in range(0, in_columnas+1):
        #     for i in range(1, in_filas):
        #         if j == 0:
        #             u_ab = H/k * (u[i,j] - ur) # Condición de contorno de la fila 0.
        #             u[i,j] = 0.25*(2*u[i,j+1] + u[i-1,j] + u[i+1,j] - (h*h*Q/(k*d) + 2*h*u_ab))
        #         elif j == in_columnas:
        #             u[i,j] = 0.25*(2*u[i,j-1] + u[i-1,j] + u[i+1,j] - (h*h*Q/(k*d) - 2*h*u_arr))
        #         else:
        #             u[i,j] = 0.25*(u[i-1,j] + u[i,j-1] + u[i,j+1] + u[i+1,j] - h*h*Q/(k*d))
        # -----------------------------------------------------------------------------------------

        norma = norm(u)
        n += 1
        if n > max_iterations:
            print(f"El método no converge en {max_iterations} iteraciones con tolerancia = {tol}")
            return u, n
    
    return u, n

def main():
    # Condiciones de contorno
    u_izq = 20
    u_der = 20

    # Dimensiones en las que dividimos.
    in_filas = 25
    in_cols = 45

    # Tolerancia
    tol = 1e-2

    for loop in range(6): # Podemos poner range(8) para hacer los casos 100x180 pero lleva bastante tiempo y cálculo del ordenador.
        print(f"-------------{in_filas}x{in_cols}----------------")
        
        # Obtención de la matriz u que representa la placa con las temperaturas.
        inicio = time.time()
        u, n = Gauss_Seidel(in_filas, in_cols, u_izq, u_der, tol)
        final = time.time()
        u = np.transpose(u)
        np.savetxt("matriz.txt", u, fmt="%5.2f")

        # Representación gráfica de la placa.
        fig, ax = plt.subplots(1,1)
        im = ax.imshow(u, cmap='coolwarm', origin='lower', extent=[0,9,0,5])
        plt.colorbar(im, ax = ax)
        ax.set_title("Temperaturas.")
        ax.set_xlabel("x (cm)")
        ax.set_ylabel("y (cm)")
        ax.set_aspect("equal", "box")
        plt.show()

        # Representación de las líneas isotermas de la placa.
        x = np.linspace(0,9,in_cols+1)
        y = np.linspace(0,5,in_filas+1)
        cs=plt.contour(x,y,u,cmap='coolwarm', origin='lower', negative_linestyles='solid')	
        plt.clabel(cs)
        plt.xlabel("x")
        plt.ylabel("y")
        plt.title("Líneas isotermas.")
        plt.xlim(-0.1,9.1)
        plt.ylim(-0.1,5.1)
        ejes=plt.gca()
        ejes.set_aspect("equal", "box")
        plt.show()

        # Sacamos los datos específicos que se piden
        if in_filas%2 != 0 and in_cols%2 != 0: # En el caso de una discretización impar obtenemos directamente puntos centrales.
            i = int(in_filas/2) 
            j = int(in_cols/2)
            punto_central = u[i,j]
            punto_central_superior = u[in_filas,j]
            punto_central_inferior = u[0, j]
        else: # En el caso par tenemos que hacer una interpolación.
            i = int(in_filas/2) 
            j = int(in_cols/2)
            
            # Tenemos 4 puntos centrales de los que sacaremos el valor medio.
            punto_central_1 = u[i,j-1]
            punto_central_2 = u[i,j]
            centro_1_2 = (punto_central_1 + punto_central_2)/2
            punto_central_3 = u[i-1,j-1]
            punto_central_4 = u[i-1,j]
            centro_3_4 = (punto_central_3 + punto_central_4)/2
            punto_central = (centro_1_2 + centro_3_4)/2

            # Tenemos dos puntos centrales superiores y dos inferiores.
            punto_central_superior_1 = u[in_filas,j-1]
            punto_central_superior_2 = u[in_filas,j]
            punto_central_superior = (punto_central_superior_1 + punto_central_superior_2)/2
            punto_central_inferior_1 = u[0, j-1]
            punto_central_inferior_2 = u[0, j]
            punto_central_inferior = (punto_central_inferior_1 + punto_central_inferior_2)/2

        # Imprimimos los resultados.
        print("CONVERGENCIA:")
        print(f" - Número de iteraciones: {n}")
        print(f" - Tiempo de ejecución (s): {final-inicio:.5f}")
        print()
        print("RESULTADOS NUMÉRICOS:")
        print(f" - Temperatura en el centro de la placa: {punto_central}ºC")
        print(f" - Temperatura en el centro superior de la placa: {punto_central_superior}ºC")
        print(f" - Temperatura en el centro inferior de la placa: {punto_central_inferior}ºC")
        print()

        in_filas += 25
        in_cols += 45
        if loop == 2: # Volvemos a representar las mallas anteriores cambiando la tolerancia
            in_filas = 25
            in_cols = 45
            tol = 1e-3
    
    
if __name__ == "__main__":
    main()
