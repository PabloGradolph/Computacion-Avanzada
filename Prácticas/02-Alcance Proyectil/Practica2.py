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

# Devuelve la matriz Y' de cada iteración (sin rozamiento)
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

# Devuelve la matriz Y' de cada iteración (con rozamiento)
def sistema_Yprima_conrozamiento(t: float, Y: np.array) -> np.array:

    v = sqrt(Y[2,0]**2 + Y[3,0]**2)

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Creamos la matriz que vamos a retornar
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[2,0]
    Yprima[1,0] = Y[3,0]
    Yprima[2,0] = - 4e-5*Y[2,0]*(v) #dvx/dt = - B2*v*vx/m // v = sqrt(vx^2 + vy^2)
    Yprima[3,0] = - g - 4e-5*Y[3,0]*(v) #dvy/dt = -g - B2*v*vy/m

    return Yprima

# Devuelve la matriz Y' de cada iteración (con rozamiento y aproximación isoterma)
def sistema_Yprima_isoterma(t: float, Y: np.array) -> np.array:

    y_0 = 1e4
    v = sqrt(Y[2,0]**2 + Y[3,0]**2)

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Creamos la matriz que vamos a retornar
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[2,0]
    Yprima[1,0] = Y[3,0]
    Yprima[2,0] = - exp(-Y[1,0]/y_0)*4e-5*Y[2,0]*(v)
    Yprima[3,0] = - g - exp(-Y[1,0]/y_0)*4e-5*Y[3,0]*(v)

    return Yprima

# Devuelve la matriz Y' de cada iteración (con rozamiento y aproximación adiabática)
def sistema_Yprima_adiabatica(t: float, Y: np.array) -> np.array:
    
    # Valores iniciales
    a, alfa, T = 6.5e-3, 2.5, 300
    v = sqrt(Y[2,0]**2 + Y[3,0]**2)

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Creamos la matriz que vamos a retornar
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[2,0]
    Yprima[1,0] = Y[3,0]
    Yprima[2,0] = - ((1-a*Y[1,0]/T)**alfa)*4e-5*Y[2,0]*(v)
    Yprima[3,0] = - g - ((1-a*Y[1,0]/T)**alfa)*4e-5*Y[3,0]*(v)

    return Yprima

def RK4_sistemas(dt: float, tmin: float, Y0: np.array, roz: bool, aproximacion=None) -> list:

    t = tmin

    # Inicializamos Y y las matrices K
    Y = Y0
    if roz == False: # Distinguimos entre solución con o sin rozamiento
        k1 = sistema_Yprima_sinrozamiento(t, Y)
        k2 = sistema_Yprima_sinrozamiento(t + 0.5*dt, Y + 0.5*dt*k1)
        k3 = sistema_Yprima_sinrozamiento(t + 0.5*dt, Y + 0.5*dt*k2)
        k4 = sistema_Yprima_sinrozamiento(t + dt, Y + dt*k3)
    else: 
        if aproximacion == None:
            k1 = sistema_Yprima_conrozamiento(t, Y)
            k2 = sistema_Yprima_conrozamiento(t + 0.5*dt, Y + 0.5*dt*k1)
            k3 = sistema_Yprima_conrozamiento(t + 0.5*dt, Y + 0.5*dt*k2)
            k4 = sistema_Yprima_conrozamiento(t + dt, Y + dt*k3)
        elif aproximacion == 1:
            k1 = sistema_Yprima_isoterma(t, Y)
            k2 = sistema_Yprima_isoterma(t + 0.5*dt, Y + 0.5*dt*k1)
            k3 = sistema_Yprima_isoterma(t + 0.5*dt, Y + 0.5*dt*k2)
            k4 = sistema_Yprima_isoterma(t + dt, Y + dt*k3)
        elif aproximacion == 2:
            k1 = sistema_Yprima_adiabatica(t, Y)
            k2 = sistema_Yprima_adiabatica(t + 0.5*dt, Y + 0.5*dt*k1)
            k3 = sistema_Yprima_adiabatica(t + 0.5*dt, Y + 0.5*dt*k2)
            k4 = sistema_Yprima_adiabatica(t + dt, Y + dt*k3)
        else:
            print("Error en la entrada del método escogido.")

    # Vectores donde iremos guardando los resultados (Además de en los ficheros)
    x = [Y[0,0]]
    y = [Y[1,0]]

    while True:
        Y = Y + (dt/6 * (k1 + 2*k2 + 2*k3 + k4))
        t = t + dt
        if roz == False: # Distinguimos entre solución con o sin rozamiento
            k1 = sistema_Yprima_sinrozamiento(t, Y)
            k2 = sistema_Yprima_sinrozamiento(t + 0.5*dt, Y + 0.5*dt*k1)
            k3 = sistema_Yprima_sinrozamiento(t + 0.5*dt, Y + 0.5*dt*k2)
            k4 = sistema_Yprima_sinrozamiento(t + dt, Y + dt*k3)
        else: 
            if aproximacion == None:
                k1 = sistema_Yprima_conrozamiento(t, Y)
                k2 = sistema_Yprima_conrozamiento(t + 0.5*dt, Y + 0.5*dt*k1)
                k3 = sistema_Yprima_conrozamiento(t + 0.5*dt, Y + 0.5*dt*k2)
                k4 = sistema_Yprima_conrozamiento(t + dt, Y + dt*k3)
            elif aproximacion == 1:
                k1 = sistema_Yprima_isoterma(t, Y)
                k2 = sistema_Yprima_isoterma(t + 0.5*dt, Y + 0.5*dt*k1)
                k3 = sistema_Yprima_isoterma(t + 0.5*dt, Y + 0.5*dt*k2)
                k4 = sistema_Yprima_isoterma(t + dt, Y + dt*k3)
            elif aproximacion == 2:
                k1 = sistema_Yprima_adiabatica(t, Y)
                k2 = sistema_Yprima_adiabatica(t + 0.5*dt, Y + 0.5*dt*k1)
                k3 = sistema_Yprima_adiabatica(t + 0.5*dt, Y + 0.5*dt*k2)
                k4 = sistema_Yprima_adiabatica(t + dt, Y + dt*k3)

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
    alcances_isotermos = {}
    alcances_adiabaticos = {}
    trayectorias_sinrozamiento = {}
    trayectorias_conrozamiento = {}
    trayectorias_isotermas = {}
    trayectorias_adiabaticas = {}

    # Recorremos todos los ángulos.
    for angulo in range(30,56):
        # Condición inicial en fucnión del ángulo
        Y0 = np.array([[0],[0],[700*cos(radianes(angulo))],[700*sin(radianes(angulo))]], float)
        print(f"Ángulo = {angulo}º")

        # Sin rozamiento.
        rozamiento = False
        x1, y1 = RK4_sistemas(dt, tmin, Y0, rozamiento)
        xfinal = (x1[-2] - (y1[-2]/y1[-1])*x1[-1])/(-(y1[-2]/y1[-1])+1)/1000 # Interpolación.
        alcances_sinrozamiento[angulo] = xfinal
        print(f"Sin rozamiento: Alcance = {xfinal:.7} km")
        x1 = np.array(x1)/1000
        y1 = np.array(y1)/1000
        trayectorias_sinrozamiento[angulo] = [x1, y1]

        # Con rozamiento.
        rozamiento = True
        x2, y2 = RK4_sistemas(dt, tmin, Y0, rozamiento)
        xfinal = (x2[-2] - (y2[-2]/y2[-1])*x2[-1])/(-(y2[-2]/y2[-1])+1)/1000 # Interpolación.
        alcances_conrozamiento[angulo] = xfinal
        print(f"Con rozamiento: Alcance = {xfinal:.7} km")
        x2 = np.array(x2)/1000
        y2 = np.array(y2)/1000
        trayectorias_conrozamiento[angulo] = [x2, y2]

        # Aproximación 1: Isoterma
        rozamiento = True
        aproximacion = 1
        x3, y3 = RK4_sistemas(dt, tmin, Y0, rozamiento, aproximacion)
        xfinal = (x3[-2] - (y3[-2]/y3[-1])*x3[-1])/(-(y3[-2]/y3[-1])+1)/1000 # Interpolación.
        alcances_isotermos[angulo] = xfinal
        print(f"Aproximación Isoterma: Alcance = {xfinal:.7} km")
        x3 = np.array(x3)/1000
        y3 = np.array(y3)/1000
        trayectorias_isotermas[angulo] = [x3, y3]

        # Aproximación 2: Adiabática
        rozamiento = True
        aproximacion = 2
        x4, y4 = RK4_sistemas(dt, tmin, Y0, rozamiento, aproximacion)
        xfinal = (x4[-2] - (y4[-2]/y4[-1])*x4[-1])/(-(y4[-2]/y4[-1])+1)/1000 # Interpolación.
        alcances_adiabaticos[angulo] = xfinal
        print(f"Aproximación Adiabática: Alcance = {xfinal:.7} km")
        x4 = np.array(x4)/1000
        y4 = np.array(y4)/1000
        trayectorias_adiabaticas[angulo] = [x4, y4]

        print()
    
    # Cálculo de los alcances máximos.
    alcance_max1 = max(alcances_sinrozamiento.items(), key=obtener_valor)
    print(f"Alcance máximo sin rozamiento:\nÁngulo = {alcance_max1[0]} grados --> Alcance = {alcance_max1[1]} km")
    
    alcance_max2 = max(alcances_conrozamiento.items(), key=obtener_valor)
    print(f"Alcance máximo con rozamiento:\nÁngulo = {alcance_max2[0]} grados --> Alcance = {alcance_max2[1]} km")

    alcance_max3 = max(alcances_isotermos.items(), key=obtener_valor)
    print(f"Alcance máximo con aproximación isoterma:\nÁngulo = {alcance_max3[0]} grados --> Alcance = {alcance_max3[1]} km")

    alcance_max4 = max(alcances_adiabaticos.items(), key=obtener_valor)
    print(f"Alcance máximo con aproximación adiabática:\nÁngulo = {alcance_max4[0]} grados --> Alcance = {alcance_max4[1]} km")

    # Represento los datos gráficamente:
    # Gráfica sin rozamiento (intervalos de 5º).
    fig1 = plt.figure("Trayectoria del Proyectil.")
    ax = fig1.add_subplot(2,2,1)
    for key, value in trayectorias_sinrozamiento.items():
        if key%5 == 0:
            ax.plot(value[0], value[1], "k", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.set_title(f"Trayectorias proyectil sin rozamiento. Ángulos 30,35,40,45,50 y 55.")

    # Gráfica con rozamiento (intervalos de 5º).
    ax = fig1.add_subplot(2,2,2)
    for key, value in trayectorias_conrozamiento.items():
        if key%5 == 0:
            ax.plot(value[0], value[1], "k", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.set_title(f"Trayectorias proyectil con rozamiento. Ángulos 30,35,40,45,50 y 55.")

    # Gráfica con aproximación isoterma (intervalos de 5º).
    ax = fig1.add_subplot(2,2,3)
    for key, value in trayectorias_isotermas.items():
        if key%5 == 0:
            ax.plot(value[0], value[1], "k", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.set_title(f"Trayectorias proyectil con aproximación isoterma. Ángulos: 30,35,40,45,50 y 55.")

    # Gráfica con aproximación adiabática (intervalos de 5º).
    ax = fig1.add_subplot(2,2,4)
    for key, value in trayectorias_adiabaticas.items():
        if key%5 == 0:
            ax.plot(value[0], value[1], "k", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.set_title(f"Trayectorias proyectil con aproximación adiabática. Ángulos 30,35,40,45,50 y 55.")
    plt.show()

    # Gráfica sin rozamiento (intervalos de 1º).
    fig2 = plt.figure("Trayectoria del Proyectil.")
    ax = fig2.add_subplot(2,2,1)
    for key, value in trayectorias_sinrozamiento.items():
        ax.plot(value[0], value[1], "k", markersize=3)
    ax.plot(alcance_max1[1],0, "or", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.legend((f"Alcance máximo = {alcance_max1[1]} km.",f"Ángulo = {alcance_max1[0]} grados."), shadow=True)
    ax.set_title(f"Trayectorias proyectil sin rozamiento.")

    # Gráfica con rozamiento (intervalos de 1º).
    ax = fig2.add_subplot(2,2,2)
    for key, value in trayectorias_conrozamiento.items():
        ax.plot(value[0], value[1], "k", markersize=3)
    ax.plot(alcance_max2[1],0, "or", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.legend((f"Alcance máximo = {alcance_max2[1]} km.",f"Ángulo = {alcance_max2[0]}º."), shadow=True)
    ax.set_title(f"Trayectorias proyectil con rozamiento.")

    # Gráfica con aproximacion isoterma (intervalos de 1º).
    ax = fig2.add_subplot(2,2,3)
    for key, value in trayectorias_isotermas.items():
        ax.plot(value[0], value[1], "k", markersize=3)
    ax.plot(alcance_max3[1],0, "or", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.legend((f"Alcance máximo = {alcance_max3[1]} km.",f"Ángulo = {alcance_max3[0]}º."), shadow=True)
    ax.set_title(f"Trayectorias proyectil con aproximación isoterma.")

    # Gráfica con aproximacion adiabática (intervalos de 1º).
    ax = fig2.add_subplot(2,2,4)
    for key, value in trayectorias_adiabaticas.items():
        ax.plot(value[0], value[1], "k", markersize=3)
    ax.plot(alcance_max4[1],0, "or", markersize=3)
    ax.grid()
    ax.set_ylabel("Altura y (km)")
    ax.set_xlabel("Alcance x (km)")
    ax.legend((f"Alcance máximo = {alcance_max4[1]} km.",f"Ángulo = {alcance_max4[0]}º."), shadow=True)
    ax.set_title(f"Trayectorias proyectil con aproximación adiabática.")
    plt.show()

if __name__ == "__main__":
    main()