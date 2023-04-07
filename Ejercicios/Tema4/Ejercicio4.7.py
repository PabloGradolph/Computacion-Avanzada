import matplotlib.pyplot as plt 
import vpython as vp
import numpy as np
from math import *

def metros(UA: float) -> float:
    # Convierte UA a metros
    res = UA*1.5e11
    return res

def sistema_Yprima_sinJupiter(t: float, Y: np.array) -> np.array:

    # Datos necesarios
    Ms = 1.989e30
    G = 6.67e-11
    r = metros(sqrt(Y[0,0]*Y[0,0] + Y[1,0]*Y[1,0]))

    Fg = G*Ms/(r**(3)) # No es la expresión de la fuerza gravitatoria sino la que usaremos en el sistema.

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

def sistema_Yprima(t: float, Y: np.array) -> np.array:

    # Datos necesarios
    x_TJ = Y[4,0] - Y[0,0]
    y_TJ = Y[5,0] - Y[1,0]
    r_TJ = sqrt(x_TJ*x_TJ + y_TJ* y_TJ)
    radio_Tierra = sqrt(Y[0,0]*Y[0,0] + Y[1,0]*Y[1,0])
    radio_Jupiter = sqrt(Y[4,0]*Y[4,0] + Y[5,0]*Y[5,0])

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Matriz para las ecuaciones de la Tierra
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[2,0]
    Yprima[1,0] = Y[3,0]
    Yprima[2,0] = (-4*pi*pi*Y[0,0])/(radio_Tierra**3) - (3.8*pi*pi*0.001*(Y[0,0]-Y[4,0]))/(r_TJ**3)
    Yprima[3,0] = (-4*pi*pi*Y[1,0])/(radio_Tierra**3) - (3.8*pi*pi*0.001*(Y[1,0]-Y[5,0]))/(r_TJ**3)

    # Matriz para las ecuaciones de Júpiter
    Yprima[4,0] = Y[6,0]
    Yprima[5,0] = Y[7,0]
    Yprima[6,0] = (-4*pi*pi*Y[4,0])/(radio_Jupiter**3) - (3.8*pi*pi*0.001*(Y[4,0]-Y[0,0]))/(r_TJ**3)
    Yprima[7,0] = (-4*pi*pi*Y[5,0])/(radio_Jupiter**3) - (3.8*pi*pi*0.001*(Y[5,0]-Y[1,0]))/(r_TJ**3)

    return Yprima

def RK4_sistemas(dt: float, tmin: float, tmax:float, Y0: np.array, Jupiter: bool) -> list:
    npasos = int((tmax - tmin)/dt)
    t = tmin

    # Inicializamos Y
    Y = Y0

    # Vectores donde iremos guardando los resultados (Además de en los ficheros)
    x_Tierra = [Y[0,0]]
    y_Tierra = [Y[1,0]]
    if Jupiter == True:
        x_Jupiter = [Y[4,0]]
        y_Jupiter = [Y[5,0]]

    for _ in range(npasos):
        t = t + dt
        if Jupiter == True:
            k1 = sistema_Yprima(t, Y)
            k2 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k1)
            k3 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k2)
            k4 = sistema_Yprima(t + dt, Y + dt*k3)
            Y = Y + (dt/6 * (k1 + 2*k2 + 2*k3 + k4))   
            x_Tierra.append(Y[0,0])
            y_Tierra.append(Y[1,0])
            x_Jupiter.append(Y[4,0])
            y_Jupiter.append(Y[5,0])
        else:
            k1 = sistema_Yprima_sinJupiter(t, Y)
            k2 = sistema_Yprima_sinJupiter(t + 0.5*dt, Y + 0.5*dt*k1)
            k3 = sistema_Yprima_sinJupiter(t + 0.5*dt, Y + 0.5*dt*k2)
            k4 = sistema_Yprima_sinJupiter(t + dt, Y + dt*k3)
            Y = Y + (dt/6 * (k1 + 2*k2 + 2*k3 + k4))   
            x_Tierra.append(Y[0,0])
            y_Tierra.append(Y[1,0])

    if Jupiter == True:
        return x_Tierra, y_Tierra, x_Jupiter, y_Jupiter
    else:
        return x_Tierra, y_Tierra
    
def main():
    # Datos iniciales.
    tmin = 0
    tmax = 3
    dt = 0.001

    # Sin la influencia de Júpiter
    Y0 = np.array([[1],[0],[0],[6.18]], float)
    x_Tierra1, y_Tierra1 = RK4_sistemas(dt, tmin, tmax, Y0, False)
    
    # Representación en matplotlib
    fig2 = plt.figure("Órbita de la Tierra y Júpiter.")
    ax = fig2.add_subplot(1,1,1)
    ax.plot(x_Tierra1, y_Tierra1, "b", markersize=3)
    ax.plot(0,0, "oy", markersize=5)
    ax.set_ylabel("y (UA)")
    ax.set_xlabel("x (UA)")
    ax.grid()
    ax.legend(("Órbita Tierra", "Sol"))
    ax.set_title(f"Órbita de La Tierra alrededor del Sol sin la influencia de Júpiter.")
    ax.set_aspect("equal")
    plt.show()

    # Representación en vpython
    vp.scene.height = 640 # Para hacer la pantalla cuadrada
    Sol = vp.sphere(pos=vp.vector(0,0,0), radius=0.1, color=vp.color.yellow)
    Tierra = vp.sphere(pos=vp.vector(1,0,0), radius=0.01, color=vp.color.cyan)
    Tierra.orbita = vp.curve(color=vp.vector(0.3,0.3,0.3))
    for i in range(len(list(x_Tierra1))):
        vp.rate(400)
        Tierra.pos=vp.vector(x_Tierra1[i], y_Tierra1[i], 0)
        Tierra.orbita.append(pos=Tierra.pos)

    # Con la influencia de Júpiter.
    tmax = 11
    Y0 = np.array([[1],[0],[0],[6.18],[5.2],[0],[0],[2.62]], float)
    x_Tierra, y_Tierra, x_Jupiter, y_Jupiter = RK4_sistemas(dt, tmin, tmax, Y0, True)

    # Representación en matplotlib
    fig2 = plt.figure("Órbita de la Tierra y Júpiter.")
    ax = fig2.add_subplot(1,2,1)
    ax.plot(x_Tierra, y_Tierra, "b", markersize=1)
    ax.plot(x_Jupiter, y_Jupiter, "r", markersize=1)
    ax.plot(0,0, "oy", markersize=5)
    ax.set_ylabel("y (UA)")
    ax.set_xlabel("x (UA)")
    ax.grid()
    ax.legend(("Órbita Tierra", "Órbita Júpiter", "Sol"))
    ax.set_title(f"Órbitas de La Tierra y Júpiter alrededor del Sol.")
    ax.set_aspect("equal")

    ax = fig2.add_subplot(1,2,2)
    ax.plot(x_Tierra1, y_Tierra1, "g", markersize=1)
    ax.plot(x_Tierra, y_Tierra, "b", markersize=1)
    ax.plot(0,0, "oy", markersize=5)
    ax.set_ylabel("y (UA)")
    ax.set_xlabel("x (UA)")
    ax.grid()
    ax.legend(("Órbita Tierra sin Júpiter","Órbita Tierra con Júpiter", "Sol"))
    ax.set_title(f"Órbita de La Tierra alrededor del Sol con y sin la influencia de Júpiter.")
    ax.set_aspect("equal")
    plt.show()

    # Representación en vpython
    Jupiter = vp.sphere(pos=vp.vector(5.2,0,0), radius=0.05, color=vp.color.red)
    Tierra = vp.sphere(pos=vp.vector(1,0,0), radius=0.01, color=vp.color.cyan)

    # La siguiente línea crea una curva por donde pasan la tierra y Júpiter.
    # --- AL AMPLIAR SE PUEDE VER LA DIFERENCIA ENTRE LAS ÓRBITAS. ---
    Tierra.orbita = vp.curve(color=vp.vector(0.3,0.3,0.3))
    Jupiter.orbita = vp.curve(color=vp.vector(0.3,0.3,0.3))
    for i in range(len(list(x_Tierra))):
        vp.rate(600)
        Tierra.pos=vp.vector(x_Tierra[i], y_Tierra[i], 0)
        Jupiter.pos = vp.vector(x_Jupiter[i], y_Jupiter[i], 0)
        Tierra.orbita.append(pos=Tierra.pos)
        Jupiter.orbita.append(pos=Jupiter.pos)

if __name__ == "__main__":
    main()