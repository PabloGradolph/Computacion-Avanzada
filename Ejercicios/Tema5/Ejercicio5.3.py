# Tenemos la ecuación 0.25 * (V[i-1,j] + V[i,j-1] + V[i,j+1] + V[i+1,j]) + (p(i,j)*h^2)/4

from math import *
import numpy as np
from numpy.linalg import norm
import matplotlib.pyplot as plt

def matriz_ro(N: int) -> np.array:
    ro = np.zeros((N+1, N+1), float)
    pos = int(N/5)

    # Establecemos las condiciones iniciales a la matriz ro (variarán según el problema planteado)
    for i in range(N):
        for j in range(N):
            # Situamos la carga positiva
            if pos*3 <= i <= pos*4 and pos*3 <= j <= pos*4:
                ro[i,j] = 1
            
            # Situamos la carga negativa
            if pos <= i <= pos*2 and pos <= j <= pos*2:
                ro[i,j] = -1
    
    return ro

def Gauss_Seidel(ro: np.array, N: int, v_izq: float, v_der: float, v_arr: float, v_ab: float) -> np.array:
    V = np.zeros((N+1, N+1))

    # Sacamos el valor de h, teniendo en cuenta que la placa tiene 1metro lado.
    h = 1/N # Total/número de divisiones.

    # Establecemos los valores de contorno
    V[0, :] = v_arr
    V[N, :] = v_ab
    V[:, 0] = v_izq
    V[:, N] = v_der

    tol = 1e-5
    print(f"Tolerancia = {tol}")

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

        # Actualizar la solución en los puntos interiores.
        # Solución más eficiente en tiempo pero requiere un mayor número de iteraciones.
        # V[1:-1, 1:-1] = 0.25 * (V[1:-1, 2:] + V[1:-1, :-2] + V[2:, 1:-1] + V[:-2, 1:-1]) + h**2 * ro[1:-1, 1:-1] / 4 

        for i in range(1, N):
            for j in range(1, N):
                V[i,j] = 0.25*(V[i-1,j] + V[i,j-1] + V[i,j+1] + V[i+1,j]) + h**2 * ro[i, j] / 4

        norma = norm(V)
        n += 1
        if n > max_iterations:
            print("El método no converge")
            return V, n
    
    return V, n

def campo_electrico(N: int, V: np.array) -> np.array:
    h = 1/N
    row = np.shape(V)[0]
    col = np.shape(V)[1]

    Ex = np.zeros((row, col)) # Matriz para el campo eléctrico en el eje x.
    Ey = np.zeros((row, col)) # Matriz para el campo eléctrico en el eje y.

    for i in range(row): # Recordamos que componente y -> i (filas)
        for j in range(col): # Recordamos que componente x -> j (columnas)
            # Componente y del campo eléctrico.
            if i == 0:
                Ey[i,j] = - (V[i+1,j]-V[i,j])/(h)
            elif i == col-1:
                Ey[i,j] = - (V[i,j]-V[i-1,j])/(h)
            else:
                Ey[i,j] = - (V[i+1,j]-V[i-1,j])/(2*h)
            
            # Componente x del campo eléctrico.
            if j == 0:
                Ex[i,j] = - (V[i,j+1]-V[i,j])/(h)
            elif j == col-1:
                Ex[i,j] = - (V[i,j]-V[i,j-1])/(h)
            else:
                Ex[i,j] = - (V[i,j+1]-V[i,j-1])/(2*h)

    return Ex,Ey   

def main():
    # Condiciones de contorno.
    v_izq = 0
    v_der = 0
    v_ab = 0
    v_arr = 0

    # Dimensiones en las que dividimos.
    N = 100

    print(f"-------------{N}x{N}----------------")
        
    # Solución por métodos iterativos (Gauss-Seidel)
    ro = matriz_ro(N)
    V, n = Gauss_Seidel(ro, N, v_izq, v_der, v_arr, v_ab)
    V = np.transpose(V) # Tenemos que transponer la matriz por el tema de la relación coordenadas -> índices (i,j)
    
    # Representación gráfica de la placa.
    fig, ax = plt.subplots(1,1)
    im = ax.imshow(V, cmap='gray', extent=[0,1,0,1], origin="lower")
    plt.colorbar(im, ax = ax)
    ax.set_title("Potencial.")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    x = np.linspace(0,1,N+1)
    y = np.ones(N+1)
    y = y*0.5
    ax.plot(x,y,'k', linestyle='--', linewidth=0.5)
    ax.plot(y,x,'k', linestyle='--', linewidth=0.5)
    ax.set_aspect("equal", "box")
    plt.show()

    # Representación de las líneas equipotenciales.
    x = np.linspace(0,1,N+1)
    y = np.linspace(0,1,N+1)
    levels = [-0.007, -0.002, 0.002, 0.007]
    cs=plt.contour(x,y,V,colors="k", origin="lower",levels=levels, negative_linestyles='solid')	
    plt.clabel(cs)
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title("Líneas equipotenciales.")
    ejes=plt.gca()
    ejes.set_aspect("equal", "box")
    plt.show()

    # Representación de las líneas de campo eléctrico.
    Ex,Ey = campo_electrico(N, V) # Matrices completas, tenemos que coger solo algunos valores para ver bien el gráfico.
    Ex_reducida = np.zeros((int(N/5)+1, int(N/5)+1), float)
    Ey_reducida = np.zeros((int(N/5)+1, int(N/5)+1), float)
    for i in range(N):
        for j in range(N):
            if i%5 == 0 and j%5 == 0:
                Ex_reducida[int(i/5),int(j/5)] = Ex[i,j]
                Ey_reducida[int(i/5),int(j/5)] = Ey[i,j]
    
    # Ya están reducidas así que representamos.
    x = np.linspace(0,1,int(N/5)+1)
    y = np.linspace(0,1,int(N/5)+1)
    plt.quiver(x,y,Ex_reducida,Ey_reducida)
    plt.title("Campo eléctrico.")
    plt.xlabel("x")
    plt.ylabel("y")
    ejes=plt.gca()
    ejes.set_aspect("equal", "box")
    plt.show()

    print(f"Número de iteraciones: {n}")

if __name__ == "__main__":
    main()