# Escribir un programa en Python que calcule la velocidad de un ciclista en función del 
# tiempo mediante los métodos de Euler y Runge-Kutta según la ecuación:
# dv/dt = P/mv
# Añadir la resistencia del aire en el apartado b.

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

# Variables globales
p, m = 400, 70

# Función para generar nombres de ficheros.
def file_name(tmin: float, tmax: float, h: float, metodo: str) -> str:
    fname = f"{metodo}_tmin"
    fname += f"{tmin:.2f}_tmax"
    fname += f"{tmax:.1f}_h"
    fname += f"{h:.2f}_"
    fname += ".txt"
    return fname

# Devuelve el valor de dv/dt
def funcion(v: float) -> float:
    return p/(m*v)

# Función que devuelve la solución exacta de la ecuación sin rozamiento.
def sol_exacta(t: float) -> float:
    return sqrt(16 + 2*p*t/m)

# Función que incluye rozamiento (apartado b)
def funcion_b(v: float) -> float:
    C, ro, A = 0.5, 1.225, 0.33
    return p/(m*v) - (C*ro*A*(v*v)/(2*m))

# Método de Euler para resolver ecuaciones diferenciales con condiciones iniciales.
def euler(dt: float, tmin: float, tmax: float, v0: float):
    # Número de pasos:
    npasos = int((tmax - tmin)/dt)
    t, v = tmin, v0

    fname = file_name(tmin, tmax, dt, "Euler")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"#Datos para dt = {dt}. Método Euler.\n")
        f.write("t\t\t\tv\t\t\tSolución Exacta\n")
        f.write(f"{t:.3f}\t{v:.5f}\t{sol_exacta(t):.5f}\n")
        for _ in range(npasos):
            t = t + dt
            v = v + dt*funcion(v)
            f.write(f"{t:.3f}\t{v:.5f}\t{sol_exacta(t):.5f}\n")
    
    print(f"Fichero de salida: {fname}")

# Método de Runge-Kutta de 4º orden para resolver ecuaciones diferenciales (Esta función la uso para el apartado a)
def RK4(dt: float, tmin: float, tmax: float, v0):
    # Definimos el número de pasos
    npasos = int((tmax - tmin)/dt)

    t, v = tmin, v0
    fname = file_name(tmin, tmax, dt, "RK4")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"#Datos para dt = {dt}. Método RK4\n")
        f.write("t\t\t\tv\t\t\tSolución Exacta\n")
        f.write(f"{t:.3f}\t{v:.5f}\t{sol_exacta(t):.5f}\n")
        for _ in range(npasos):
            t = t + dt
            k1 = funcion(v)
            k2 = funcion(v + 0.5*k1*dt)
            k3 = funcion(v + 0.5*k2*dt)
            k4 = funcion(v + k3*dt)
            v = v + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
            f.write(f"{t:.3f}\t{v:.5f}\t{sol_exacta(t):.5f}\n")
    
    print(f"Fichero de salida: {fname}")

# Método de Runge-Kutta de 4º orden para resolver ecuaciones diferenciales (Esta función la uso para el apartado a)
def RK4_b(dt: float, tmin: float, tmax: float, v0) -> float:
    # Definimos el número de pasos
    npasos = int((tmax - tmin)/dt)

    t, v = tmin, v0
    fname = file_name(tmin, tmax, dt, "RK4_b")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"#Datos para dt = {dt}. Método RK4\n")
        f.write("t\t\t\tv\n")
        f.write(f"{t:.3f}\t{v:.5f}\n")
        for _ in range(npasos):
            t = t + dt
            k1 = funcion_b(v)
            k2 = funcion_b(v + 0.5*k1*dt)
            k3 = funcion_b(v + 0.5*k2*dt)
            k4 = funcion_b(v + k3*dt)
            v = v + (dt/6)*(k1 + 2*k2 + 2*k3 + k4)
            f.write(f"{t:.3f}\t{v:.5f}\n")

    print(f"Fichero de salida: {fname}")

def main():
    # ===========Apartado A ===========
    # Datos iniciales
    tmin, tmax = 0, 200
    v0 = 4
    dt = [0.5, 0.2, 0.05] # Probamos para distintos valores de dt
    for h in dt:
        euler(h, tmin, tmax, v0)
        RK4(h, tmin, tmax, v0)

    # Representamos gráficamente
    fig1 = plt.figure("Velocidad Ciclista en función del tiempo sin rozamiento.")

    # Gráficos Euler.
    for i in range(3):
        dt2 = str(dt[i])
        if i<2:
            data = np.loadtxt(f"Euler_tmin0.00_tmax200.0_h{dt2}0_.txt", float, skiprows=2)
        else:
            data = np.loadtxt(f"Euler_tmin0.00_tmax200.0_h{dt2}_.txt", float, skiprows=2)
        tiempo = data[:,0]
        v = data[:,1]
        sol = data[:,2]
        
        ax = fig1.add_subplot(2,3,i+1)
        ax.plot(tiempo, v, "k", markersize=3)
        ax.plot(tiempo, sol, "r", markersize=3)
        ax.grid()
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("v")
        ax.legend(("Resultado Euler", "Solución Exacta"), shadow = True)
        ax.set_title("Resultados Euler dt="+dt2)
    
    # Gráficos Runge-Kutta 4º orden.
    for i in range(3):
        dt2 = str(dt[i])
        if i<2:
            data = np.loadtxt(f"RK4_tmin0.00_tmax200.0_h{dt2}0_.txt", float, skiprows=2)
        else:
            data = np.loadtxt(f"RK4_tmin0.00_tmax200.0_h{dt2}_.txt", float, skiprows=2)
        tiempo = data[:,0]
        v = data[:,1]
        sol = data[:,2]
        
        ax = fig1.add_subplot(2,3,i+4)
        ax.plot(tiempo, v, "k", markersize=3)
        ax.plot(tiempo, sol, "r", markersize=3)
        ax.grid()
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("v")
        ax.legend(("Resultado RK4", "Solución Exacta"), shadow = True)
        ax.set_title("Resultados RK4 dt="+dt2)
    plt.show()

    # ===========Apartado B ===========
    # La velocidad terminal teórica se corresponde con v = 15.81818503 m/s
    h = 0.05 # Hacemos este apartado para un h = 0.05
    RK4_b(h, tmin, tmax, v0)

    # Representamos los resultados gráficamente.
    vmax = np.array([15.81818503 for _ in range(200)])
    data = np.loadtxt(f"RK4_b_tmin0.00_tmax200.0_h0.05_.txt", float, skiprows=2)
    tiempo = data[:,0]
    v = data[:,1]
    plt.plot(tiempo, v, "k", markersize=3, label="Resultado RK3")
    plt.plot(vmax, "r", markersize=2, label="Velocidad terminal")
    plt.grid()
    plt.xlabel('tiempo')
    plt.ylabel('velocidad')
    plt.title("Velocidad Ciclista en función del tiempo y velocidad terminal.")
    plt.legend(shadow=True)
    plt.show()

    # Vemos como la velocidad terminal obtenida se corresponde con la teórica.
    # Es un resultado bastante realista en media de un ciclista aficionado, ya que para profesionales esta velocidad es baja.

if __name__ == "__main__":
    main()
