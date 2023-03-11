# Ecuaciones diferenciales de orden superior. Trayectoria de un proyectil.

import numpy as np
from math import *
import matplotlib.pyplot as plt

# El valor de la solución exacta (calculada de forma analítica) es el siguiente:
sol_exacta = 43301.27019/1000 # Dividimos entre 1000 para km.
g = 9.8

# Cálculo de error relativo
def errores(exacto: float, obtenido: float):
    Ea = fabs(exacto - obtenido)
    Er = fabs(Ea/exacto)
    return Er

# Devuelve la matriz Y' de cada iteración (en nuestro caso)
def sistema_Yprima(t: float, Y: np.array) -> np.array:

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Creamos la matriz que vamos a retornar
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[2,0]
    Yprima[1,0] = Y[3,0]
    Yprima[2,0] = 0.0
    Yprima[3,0] = -g

    return Yprima

def Euler_sistemas(dt: float, tmin: float, Y0: np.array, tol=10e-4) -> list:
    # Inicializamos las variables
    t = tmin
    Y = Y0

    # Vectores donde iremos guardando los resultados (Además de en los ficheros)
    x = [Y[0,0]]
    y = [Y[1,0]]

    while True:
        Y = Y + dt*(sistema_Yprima(t, Y))
        t = t + dt
        x.append(Y[0,0])
        y.append(Y[1,0])
        if Y[1,0]<0:
            break

    return x, y

def RK4_sistemas(dt: float, tmin: float, Y0: np.array) -> list:
    t = tmin

    # Inicializamos Y y las matrices K
    Y = Y0
    k1 = sistema_Yprima(t, Y)
    k2 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k1)
    k3 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k2)
    k4 = sistema_Yprima(t + dt, Y + dt*k3)

    # Vectores donde iremos guardando los resultados (Además de en los ficheros)
    x = [Y[0,0]]
    y = [Y[1,0]]

    while True:
        Y = Y + (dt/6 * (k1 + 2*k2 + 2*k3 + k4))
        t = t + dt
        k1 = sistema_Yprima(t, Y)
        k2 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k1)
        k3 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k2)
        k4 = sistema_Yprima(t + dt, Y + dt*k3)   
        x.append(Y[0,0])
        y.append(Y[1,0])
        if Y[1,0]<0:
            break

    return x, y 

def main():
    # Datos iniciales.
    Y0 = np.array([[0],[0],[700*cos(pi/6)],[350]], float)
    tmin = 0

    # Calculamos para distintos valores de dt
    dt = 0.0001
    while dt<2:
        print()
        # Método de Euler.
        print(f"Euler para un dt = {dt}")
        x1, y1 = Euler_sistemas(dt, tmin, Y0)
        xfinal = (x1[-2] - (y1[-2]/y1[-1])*x1[-1])/(-(y1[-2]/y1[-1])+1)/1000
        print(f"Sol = {xfinal:.7} --> Error relativo = {errores(sol_exacta, xfinal):.7}")
        x1 = np.array(x1)/1000
        y1 = np.array(y1)/1000
        # Valor máximo de y
        posicion = np.where(y1 == np.amax(y1))
        ymax1 = (float(x1[posicion]), np.amax(y1))

        # Método Runge-Kutta 4º orden
        print(f"Runge-Kutta para un dt = {dt}")
        x2, y2 = RK4_sistemas(dt, tmin, Y0)
        xfinal = (x2[-2] - (y2[-2]/y2[-1])*x2[-1])/(-(y2[-2]/y2[-1])+1)/1000 # Interpolación
        print(f"Sol = {xfinal:.7} --> Error relativo = {errores(sol_exacta, xfinal):.7}")
        x2 = np.array(x2)/1000
        y2 = np.array(y2)/1000
        posicion = np.where(y2 == np.amax(y2))
        ymax2 = (float(x2[posicion]), np.amax(y2))

        # Representamos gráficamente
        fig1 = plt.figure("Trayectoria del Proyectil.")
        ax = fig1.add_subplot(2,1,1)
        ax.plot(x1, y1, "k", markersize=3)
        ax.plot(sol_exacta,0, "og", markersize=5)
        ax.plot(ymax1[0], ymax1[1], "or", markersize=5)
        ax.text(ymax1[0]-4.5, ymax1[1]-1, f"({ymax1[0]}, {ymax1[1]})", fontsize=10, color="black")
        ax.grid()
        ax.set_ylabel("Altura y (km)")
        ax.set_xlabel("Alcance x (km)")
        ax.legend(("Trayectoria obtenida", "Alcance teórico", "Altura máxima"), shadow=True)
        ax.set_title(f"Trayectoria proyectil. Método Euler con dt = {dt}")

        ax = fig1.add_subplot(2,1,2)
        ax.plot(x2, y2, "k", markersize=3)
        ax.plot(sol_exacta,0, "og", markersize=5)
        ax.plot(ymax2[0], ymax2[1], "or", markersize=5)
        ax.text(ymax2[0]-4.5, ymax2[1]-1, f"({ymax2[0]}, {ymax2[1]})", fontsize=10, color="black")
        ax.grid()
        ax.set_ylabel("Altura y (km)")
        ax.set_xlabel("Alcance x (km)")
        ax.legend(("Trayectoria obtenida", "Alcance teórico", "Altura máxima"), shadow=True)
        ax.set_title(f"Trayectoria proyectil. Método Runge-Kutta con dt = {dt}")
        plt.show()

        # Vamos aumentando dt (he elegido ir multiplicandolo por 5)
        dt = dt*5

if __name__ == "__main__":
    main()