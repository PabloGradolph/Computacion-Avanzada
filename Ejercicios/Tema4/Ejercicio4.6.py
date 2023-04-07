
import matplotlib.pyplot as plt 
import vpython as vp
import numpy as np
from math import *

def metros(UA: float) -> float:
    # Convierte UA a metros
    res = UA*1.5e11
    return res

def sistema_Yprima(t: float, Y: np.array, Beta: float) -> np.array:

    # Datos necesarios
    Ms = 1.989e30
    G = 6.67e-11
    r = metros(sqrt(Y[0,0]*Y[0,0] + Y[1,0]*Y[1,0]))

    Fg = G*Ms/(r**(Beta+1)) # No es la expresión de la fuerza gravitatoria sino la que usaremos en el sistema.

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Creamos la matriz que vamos a retornar
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[2,0]
    Yprima[1,0] = Y[3,0]
    Yprima[2,0] = (- Fg * (Y[0,0]))*(3.2e7**2) # Último término para pasar de s^2 a años^2.
    Yprima[3,0] = (- Fg * (Y[1,0]))*(3.2e7**2) # Último término para pasar de s^2 a años^2.

    return Yprima

def RK4_sistemas(dt: float, tmin: float, tmax:float, Y0: np.array, Beta) -> list:
    npasos = int((tmax - tmin)/dt)
    t = tmin

    # Inicializamos Y
    Y = Y0

    # Vectores donde iremos guardando los resultados (Además de en los ficheros)
    x = [Y[0,0]]
    y = [Y[1,0]]

    for _ in range(npasos):
        t = t + dt
        k1 = sistema_Yprima(t, Y, Beta)
        k2 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k1, Beta)
        k3 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k2, Beta)
        k4 = sistema_Yprima(t + dt, Y + dt*k3, Beta)
        Y = Y + (dt/6 * (k1 + 2*k2 + 2*k3 + k4))   
        x.append(Y[0,0])
        y.append(Y[1,0])

    return x, y

def main():
    # Datos iniciales.
    Y0 = np.array([[1],[0],[0],[5]], float)
    tmin = 0
    tmax = 2
    dt = 0.001
    Beta = [2,2.01,2.03,2.1,2.5,3]

    for i in Beta:
        x, y = RK4_sistemas(dt, tmin, tmax, Y0, i)

        # Representación en matplotlib
        fig1 = plt.figure("Órbita de la Tierra.")
        ax = fig1.add_subplot(1,1,1)
        ax.plot(x, y, "k", markersize=3)
        ax.plot(0,0, "ok", markersize=5)
        ax.set_ylabel("y (UA)")
        ax.set_xlabel("x (UA)")
        ax.set_ylim(-1.1,1.1)
        ax.set_xlim(-1.1,1.1)
        ax.set_title(f"Órbita de La Tierra alrededor del Sol. Beta = {i}")
        ax.set_aspect("equal")
        plt.show()

        # Representación en vpython
        vp.scene.height = 640 # Para hacer la pantalla cuadrada
        Sol = vp.sphere(pos=vp.vector(0,0,0), radius=0.1, color=vp.color.yellow)
        Tierra = vp.sphere(pos=vp.vector(1,0,0), radius=0.02, color=vp.color.cyan)

        # La siguiente línea crea una curva por donde pasa la tierra
        Tierra.orbita = vp.curve(color=vp.vector(0.3,0.3,0.3))
        for i in range(len(list(x))):
            vp.rate(500)
            Tierra.pos=vp.vector(x[i], y[i], 0)
            Tierra.orbita.append(pos=Tierra.pos)

if __name__ == "__main__":
    main()

