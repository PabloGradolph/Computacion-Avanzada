import numpy as np
from math import *
import matplotlib.pyplot as plt

g = 9.8

# Transforma grados a radianes
def radianes(angulo: float) -> float:
    rad = angulo * pi/180
    return rad

# Obtener el segundo valor de la tupla dada por (angulo, alcance)
def obtener_valor(tupla: tuple):
    return tupla[1]

# Devuelve la matriz Y' de cada iteración.
def sistema_Yprima(t: float, Y: np.array) -> np.array:

    # Valores necesarios para las ecuaciones.
    vd, delta = 35, 5.0
    v = sqrt(Y[2,0]*Y[2,0] + Y[3,0]*Y[3,0])
    B2_m = 0.0039 + 0.0058/(1 + exp((v - vd)/delta))

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Creamos la matriz que vamos a retornar
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[2,0]
    Yprima[1,0] = Y[3,0]
    Yprima[2,0] = - B2_m * v * Y[2,0]
    Yprima[3,0] = - g - B2_m * v * Y[3,0]

    return Yprima

# Devuelve la matriz Y' de cada iteración.
def sistema_Yprima_viento(t: float, Y: np.array, direccion: bool) -> np.array:

    # Valores necesarios para las ecuaciones.
    vd, delta = 35, 5.0
    v = sqrt(Y[2,0]*Y[2,0] + Y[3,0]*Y[3,0])
    B2_m = 0.0039 + 0.0058/(1 + exp((v - vd)/delta))
    if direccion == True:
        v_viento = 2.5 # m/s
    else:
        v_viento = - 2.5

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Creamos la matriz que vamos a retornar
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[2,0]
    Yprima[1,0] = Y[3,0]
    Yprima[2,0] = - B2_m * (v - v_viento) * (Y[2,0] - v_viento)
    Yprima[3,0] = - g - B2_m * (v - v_viento) * Y[3,0]

    return Yprima

def RK4_sistemas(dt: float, tmin: float, Y0: np.array, viento: bool, direccion: bool) -> list:

    t = tmin

    # Inicializamos Y y las matrices K
    Y = Y0
    if viento == False:
        k1 = sistema_Yprima(t, Y)
        k2 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k1)
        k3 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k2)
        k4 = sistema_Yprima(t + dt, Y + dt*k3)
    else:
        k1 = sistema_Yprima_viento(t, Y, direccion)
        k2 = sistema_Yprima_viento(t + 0.5*dt, Y + 0.5*dt*k1, direccion)
        k3 = sistema_Yprima_viento(t + 0.5*dt, Y + 0.5*dt*k2, direccion)
        k4 = sistema_Yprima_viento(t + dt, Y + dt*k3, direccion)

    # Vectores donde iremos guardando los resultados (Además de en los ficheros)
    x = [Y[0,0]]
    y = [Y[1,0]]

    while True:
        Y = Y + (dt/6 * (k1 + 2*k2 + 2*k3 + k4))
        t = t + dt
        x.append(Y[0,0])
        y.append(Y[1,0])

        if viento == False:
            k1 = sistema_Yprima(t, Y)
            k2 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k1)
            k3 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k2)
            k4 = sistema_Yprima(t + dt, Y + dt*k3)
        else:
            k1 = sistema_Yprima_viento(t, Y, direccion)
            k2 = sistema_Yprima_viento(t + 0.5*dt, Y + 0.5*dt*k1, direccion)
            k3 = sistema_Yprima_viento(t + 0.5*dt, Y + 0.5*dt*k2, direccion)
            k4 = sistema_Yprima_viento(t + dt, Y + dt*k3, direccion)
        if Y[1,0]<0:
            break

    return x, y

def main():
    # Datos iniciales.
    dt, tmin = 0.1, 0.0
    x0, y0 = 0, 1
    v0 = 49

    alcances = {}
    trayectorias = {}

    # --------- APARTADO A ---------
    print("TRAYECTORIAS PELOTA DE BÉISBOL")
    viento = False
    for angulo in range(30,51):
        # Condición inicial en fucnión del ángulo
        Y0 = np.array([[x0],[y0],[v0*cos(radianes(angulo))],[v0*sin(radianes(angulo))]], float)
        print(f"Ángulo = {angulo}º")

        x, y = RK4_sistemas(dt, tmin, Y0, viento, None)
        xfinal = (x[-2] - (y[-2]/y[-1])*x[-1])/(-(y[-2]/y[-1])+1) # Interpolación.
        alcances[angulo] = xfinal

        x, y = x[:-1], y[:-1] # Quitamos el último valor que está por debajo de y = 0.
        x.append(xfinal) # Añadimos x = xfinal e y = 0 para el último valor.
        y.append(0) # De esta forma la representación gráfica queda correcta.

        print(f"Alcance = {xfinal:.7} m")
        x = np.array(x)
        y = np.array(y)
        trayectorias[angulo] = [x, y]

        print()
    
    # Cálculo de los alcances máximos.
    alcance_max = max(alcances.items(), key=obtener_valor)
    print(f"Alcance máximo:\nÁngulo = {alcance_max[0]} grados --> Alcance = {alcance_max[1]} m")

    fig1 = plt.figure("Trayectoria pelota de béisbol.")
    ax = fig1.add_subplot(1,1,1)
    for key, value in trayectorias.items():
        ax.plot(value[0], value[1], "k", markersize=3)
    ax.grid()
    ax.plot(alcance_max[1],0, "or", markersize=3)
    ax.set_ylabel("Altura y (m)")
    ax.set_xlabel("Alcance x (m)")
    ax.legend((f"Alcance máximo = {alcance_max[1]} m.",f"Ángulo = {alcance_max[0]} grados."), shadow=True)
    ax.set_title(f"Trayectorias pelota de béisbol. Ángulos entre 30º y 50º")
    plt.show()

    # --------- APARTADO B ---------
    # Para el ángulo inicial de 35º incluir el efecto del viento tanto a favor como en contra. Suponiendo una velocidad del viento de 9km/h = 2.5m/s
    # Inluyo las tres gráficas: la del apartado anterior sin el efecto del aire, con el aire a favor y con el aire en contra.
    print()
    print("--------------- Para un ángulo de 35º ------------------")
    trayectorias_2 = {}
    
    # Sin efecto del viento.
    Y0 = np.array([[x0],[y0],[v0*cos(radianes(35))],[v0*sin(radianes(35))]], float)
    x, y = RK4_sistemas(dt, tmin, Y0, viento, None)
    xfinal = (x[-2] - (y[-2]/y[-1])*x[-1])/(-(y[-2]/y[-1])+1) # Interpolación.
    x, y = x[:-1], y[:-1]
    x.append(xfinal) 
    y.append(0)
    x = np.array(x)
    y = np.array(y)
    trayectorias_2["SinViento"] = [x, y]
    print(f"Sin efecto del viento --> Alcance = {xfinal:.7} m")

    # Viento a favor.
    viento, direccion = True, True
    x, y = RK4_sistemas(dt, tmin, Y0, viento, direccion)
    xfinal = (x[-2] - (y[-2]/y[-1])*x[-1])/(-(y[-2]/y[-1])+1) # Interpolación.
    x, y = x[:-1], y[:-1]
    x.append(xfinal) 
    y.append(0)
    x = np.array(x)
    y = np.array(y)
    trayectorias_2["AFavor"] = [x, y]
    print(f"Con el viento a favor --> Alcance = {xfinal:.7} m")

    # Viento en contra.
    direccion = False
    x, y = RK4_sistemas(dt, tmin, Y0, viento, direccion)
    xfinal = (x[-2] - (y[-2]/y[-1])*x[-1])/(-(y[-2]/y[-1])+1) # Interpolación.
    x, y = x[:-1], y[:-1]
    x.append(xfinal) 
    y.append(0)
    x = np.array(x)
    y = np.array(y)
    trayectorias_2["EnContra"] = [x, y]
    print(f"Con el viento en contra --> Alcance = {xfinal:.7} m")

    # Representación gráfica
    fig2 = plt.figure("Trayectoria pelota de béisbol.")
    ax = fig2.add_subplot(1,1,1)
    colores = ["k", "b", "g"]
    for key, value in trayectorias_2.items():
        ax.plot(value[0], value[1], colores[0], markersize=3)
        del colores[0]
    ax.grid()
    ax.set_ylabel("Altura y (m)")
    ax.set_xlabel("Alcance x (m)")
    ax.legend(("Sin efecto del viento","Viento a favor","Viento en contra"), shadow=True)
    ax.set_title(f"Trayectoria para angulo de 35º con distintas condiciones.")
    plt.show()

if __name__ == "__main__":
    main()