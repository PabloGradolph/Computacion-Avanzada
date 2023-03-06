#------------------------------------
# Resolución de ecuaciones diferenciales con condiciones iniciales por el método de Euler.
# Escribir un programa en Python para resolver la ecuación que describe la desintegración radiactiva por el método de Euler:
# Generar un fichero de datos y un gráfico para 𝜏=1 con 100 pasos de tiempo de 0.05 s. Tomar N(t=0)=100.
# Comparar con la solución exacta. Explorar cómo cambia la precisión al variar el tamaño del paso de tiempo, por ejemplo para valores de 0.2 s y 0.5 s.
# Reescalar el tiempo para abordar el problema del 235U.
#------------------------------------

#------------------------------------
# IMPORTACIONES
#------------------------------------

from math import exp
import matplotlib.pyplot as plt
import numpy as np

#------------------------------------
# FUNCIONES
#------------------------------------

# Función para generar nombres de ficheros.
def file_name(xmin: float, xmax: float, h: float, metodo: str) -> str:
    fname = f"{metodo}_tmin"
    fname += f"{xmin:.2f}_tau"
    fname += f"{xmax:.1f}_h"
    fname += f"{h:.2f}_"
    fname += ".txt"
    return fname
    
# Función que devuelve el valor de dy/dx para un cierto valor de x y de y.
# En este caso adaptando las variables a t y N.
def y_prima(N: float, tau: float) -> float:
    return - (N/tau)

# Devuelve el valor exacto de la función "y" que tratamos de calcular en el punto x.
# En nuestro caso el número "N" en el tiempo t.
def sol_exacta(t: float) -> float:
    return 100/exp(t)

# Función para la resolución de una ecuación diferencial por el método de Euler.
def euler(h: float, xmin: float, y0: float, tau: float):
    # Inicializamos x e y
    x, y = xmin, y0

    fname = file_name(xmin,tau,h,"Euler")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"#Datos para h = {h}\n")
        f.write("t\t\t\tN\t\t\tSolución Exacta\n")
        if tau == 1:
            f.write(f"{x:.3f}\t{y:.5f}\t{sol_exacta(x):.5f}\n")
        else: # Si tau vale 10e9 cambia la solución exacta de la ecuación diferencial.
            f.write(f"{x:}\t{y:.5f}\t{sol_exacta(x/(10**9)):.5f}\n")
        for _ in range(100):
            x = x + h
            y = y + (h*y_prima(y, tau))
            if tau == 1:
                f.write(f"{x:.3f}\t{y:.5f}\t{sol_exacta(x):.5f}\n")
            else: # Si tau vale 10e9 cambia la solución exacta de la ecuación diferencial.
                f.write(f"{x:}\t{y:.5f}\t{sol_exacta(x/(10**9)):.5f}\n")

    print(f"Fichero de salida: {fname}")

def main():
    # Datos iniciales
    h = [0.05, 0.2, 0.5]
    t0 = 0
    y0 = 100
    tau = 1
   
    # Hacemos un bucle para cada valor de h
    for i in h:
        euler(i, t0, y0, tau)
    
    # Cambiamos el valor tau para el caso del 235U
    tau = 10e9
    h = [tau/100000, tau/10000, tau/1000]
    for i in h:
        euler(i, t0, y0, tau)
    
    # Representamos los resultados gráficamente
    fig1 = plt.figure("MÉTODO DE EULER: EDOs")

    # Primera parte del ejercicio:

    # Datos para tau = 1
    h = [0.05, 0.20, 0.50]
    for i in range(1,4):
        h2 = str(h[i-1])
        if i>1:
            data = np.loadtxt(f"Euler_tmin0.00_tau1.0_h{h2}0_.txt", float, skiprows=2)
        else:
            data = np.loadtxt(f"Euler_tmin0.00_tau1.0_h{h2}_.txt", float, skiprows=2)
        tiempo = data[:,0]
        N = data[:,1]
        sol = data[:,2]
        
        ax = fig1.add_subplot(2,3,i)
        ax.plot(tiempo, N, "k", markersize=3)
        ax.plot(tiempo, sol, "r", markersize=3)
        ax.grid()
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("N")
        ax.legend(("Resultado Euler", "Solución Exacta"), shadow = True)
        ax.set_title("Resultados tau=1 h="+h2)
    
    # Segunda parte del ejercicio:

    # Datos para tau = 10^9. Problema del 235U
    h = [100000.0, 1000000.0, 10000000.0]
    for i in range(1,4):
        h2 = str(h[i-1])
        data = np.loadtxt(f"Euler_tmin0.00_tau10000000000.0_h{h2}0_.txt", float, skiprows=2)
        tiempo = data[:,0]
        N = data[:,1]
        sol = data[:,2]
        
        ax = fig1.add_subplot(2,3,i+3)
        ax.plot(tiempo, N, "k", markersize=3)
        ax.plot(tiempo, sol, "r", markersize=3)
        ax.grid()
        ax.set_xlabel("Tiempo (años)")
        ax.set_ylabel("N")
        ax.legend(("Resultado Euler", "Solución Exacta"), shadow = True)
        ax.set_title("Resultados tau=10^9 h="+h2)
    plt.show()

    # Los resultados para el 235U no se aproximan correctamente, igual he aplicado mal un tema de escalas. En este caso no veo el error.
    # O igual el método de Euler no es lo suficientemente preciso para aproximarlo.

#------------------------------------
# EJECUTAMOS
#------------------------------------

if __name__ == "__main__":
    main()