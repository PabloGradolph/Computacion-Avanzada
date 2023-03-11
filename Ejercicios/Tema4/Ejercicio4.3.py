import numpy as np
from math import *
import matplotlib.pyplot as plt

g = 9.8

# Cálculo de error relativo
def errores(exacto: float, obtenido: float):
    Ea = fabs(exacto - obtenido)
    Er = fabs(Ea/exacto)
    return Er

# Transforma grados a radianes
def radianes(angulo: float) -> float:
    rad = angulo * pi/180
    return rad

# Obtener el segundo valor de la tupla dada por (angulo, alcance)
def obtener_valor(tupla: tuple):
    return tupla[1]

# Devuelve la matriz Y' de cada iteración (en nuestro caso)
def sistema_Yprima_sinrozamiento(t: float, Y: np.array) -> np.array:

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

# Devuelve la matriz Y' de cada iteración (en nuestro caso)
def sistema_Yprima_conrozamiento(t: float, Y: np.array) -> np.array:

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Creamos la matriz que vamos a retornar
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[2,0]
    Yprima[1,0] = Y[3,0]
    Yprima[2,0] = - 4*10e-5*Y[2,0]*(sqrt(Y[2,0]**2 + Y[3,0]**2)) #dvx/dt = - B2*v*vx/m // v = sqrt(vx^2 + vy^2)
    Yprima[3,0] = - g - 4*10e-5*Y[3,0]*(sqrt(Y[2,0]**2 + Y[3,0]**2)) #dvy/dt = -g - B2*v*vy/m

    return Yprima

def RK4_sistemas(dt: float, tmin: float, Y0: np.array, roz: bool) -> list:
    t = tmin

    # Inicializamos Y y las matrices K
    Y = Y0
    if roz == True: # Distinguimos entre solución con o sin rozamiento
        k1 = sistema_Yprima_conrozamiento(t, Y)
        k2 = sistema_Yprima_conrozamiento(t + 0.5*dt, Y + 0.5*dt*k1)
        k3 = sistema_Yprima_conrozamiento(t + 0.5*dt, Y + 0.5*dt*k2)
        k4 = sistema_Yprima_conrozamiento(t + dt, Y + dt*k3)
    elif roz == False:
        k1 = sistema_Yprima_sinrozamiento(t, Y)
        k2 = sistema_Yprima_sinrozamiento(t + 0.5*dt, Y + 0.5*dt*k1)
        k3 = sistema_Yprima_sinrozamiento(t + 0.5*dt, Y + 0.5*dt*k2)
        k4 = sistema_Yprima_sinrozamiento(t + dt, Y + dt*k3)

    # Vectores donde iremos guardando los resultados (Además de en los ficheros)
    x = [Y[0,0]]
    y = [Y[1,0]]

    while True:
        Y = Y + (dt/6 * (k1 + 2*k2 + 2*k3 + k4))
        t = t + dt
        if roz == True: # Distinguimos entre solución con o sin rozamiento
            k1 = sistema_Yprima_conrozamiento(t, Y)
            k2 = sistema_Yprima_conrozamiento(t + 0.5*dt, Y + 0.5*dt*k1)
            k3 = sistema_Yprima_conrozamiento(t + 0.5*dt, Y + 0.5*dt*k2)
            k4 = sistema_Yprima_conrozamiento(t + dt, Y + dt*k3)
        elif roz == False:
            k1 = sistema_Yprima_sinrozamiento(t, Y)
            k2 = sistema_Yprima_sinrozamiento(t + 0.5*dt, Y + 0.5*dt*k1)
            k3 = sistema_Yprima_sinrozamiento(t + 0.5*dt, Y + 0.5*dt*k2)
            k4 = sistema_Yprima_sinrozamiento(t + dt, Y + dt*k3) 
        x.append(Y[0,0])
        y.append(Y[1,0])
        if Y[1,0]<0:
            break

    return x, y 

def main():
    # Datos iniciales.
    dt, tmin = 0.1, 0.0

    # Guardamos los alcances y las trayectorias
    alcances_sinrozamiento = {}
    alcances_conrozamiento = {}
    trayectorias_sinrozamiento = {}
    trayectorias_conrozamiento = {}

    # Recorremos todos los ángulos.
    for angulo in range(30,56):
        # Condición inicial en fucnión del ángulo
        Y0 = np.array([[0],[0],[700*cos(radianes(angulo))],[700*sin(radianes(angulo))]], float)
        print(f"Ángulo = {angulo}")

        # Sin rozamiento.
        rozamiento = False
        x1, y1 = RK4_sistemas(dt, tmin, Y0, rozamiento)
        xfinal = (x1[-2] - (y1[-2]/y1[-1])*x1[-1])/(-(y1[-2]/y1[-1])+1)/1000 # Interpolación.
        alcances_sinrozamiento[angulo] = xfinal
        print(f"Sin rozamiento: Sol = {xfinal:.7}")
        x1 = np.array(x1)/1000
        y1 = np.array(y1)/1000
        trayectorias_sinrozamiento[angulo] = [x1, y1]

        # Con rozamiento.
        rozamiento = True
        x2, y2 = RK4_sistemas(dt, tmin, Y0, rozamiento)
        xfinal = (x2[-2] - (y2[-2]/y2[-1])*x2[-1])/(-(y2[-2]/y2[-1])+1)/1000 # Interpolación.
        alcances_conrozamiento[angulo] = xfinal
        print(f"Con rozamiento: Sol = {xfinal:.7}")
        x2 = np.array(x2)/1000
        y2 = np.array(y2)/1000
        trayectorias_conrozamiento[angulo] = [x2, y2]

        print()
    
    # Gráficas sin rozamiento (intervalos de 5º).
    fig1 = plt.figure("Trayectoria del Proyectil.")
    ax = fig1.add_subplot(1,1,1)
    for key, value in trayectorias_sinrozamiento.items():
        if key%5 == 0:
            ax.plot(value[0], value[1], "k", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.set_title(f"Trayectorias proyectil sin rozamiento. Ángulos 30,35,40,45,50 y 55 grados.")
    plt.show()

    # Gráficas sin rozamiento (intervalos de 5º).
    fig2 = plt.figure("Trayectoria del Proyectil.")
    ax = fig2.add_subplot(1,1,1)
    for key, value in trayectorias_conrozamiento.items():
        if key%5 == 0:
            ax.plot(value[0], value[1], "k", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.set_title(f"Trayectorias proyectil con rozamiento. Ángulos 30,35,40,45,50 y 55 grados.")
    plt.show()

    # Cálculo de los alcances máximos.
    alcance_max1 = max(alcances_sinrozamiento.items(), key=obtener_valor)
    print(f"Alcance máximo sin rozamiento:\nÁngulo = {alcance_max1[0]} grados --> Alcance = {alcance_max1[1]} km")
    
    alcance_max2 = max(alcances_conrozamiento.items(), key=obtener_valor)
    print(f"Alcance máximo sin rozamiento:\nÁngulo = {alcance_max2[0]} grados --> Alcance = {alcance_max2[1]} km")

    # Gráficas sin rozamiento (intervalos de 1º).
    fig3 = plt.figure("Trayectoria del Proyectil.")
    ax = fig3.add_subplot(1,1,1)
    for key, value in trayectorias_sinrozamiento.items():
        ax.plot(value[0], value[1], "k", markersize=3)
    ax.plot(alcance_max1[1],0, "or", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.legend((f"Alcance máximo = {alcance_max1[1]} km.",f"Ángulo = {alcance_max1[0]} grados."), shadow=True)
    ax.set_title(f"Trayectorias proyectil sin rozamiento.")
    plt.show()

    # Gráficas sin rozamiento (intervalos de 5º).
    fig4 = plt.figure("Trayectoria del Proyectil.")
    ax = fig4.add_subplot(1,1,1)
    for key, value in trayectorias_conrozamiento.items():
        ax.plot(value[0], value[1], "k", markersize=3)
    ax.plot(alcance_max2[1],0, "or", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.legend((f"Alcance máximo = {alcance_max2[1]} km.",f"Ángulo = {alcance_max2[0]} grados."), shadow=True)
    ax.set_title(f"Trayectorias proyectil con rozamiento.")
    plt.show()

if __name__ == "__main__":
    main()