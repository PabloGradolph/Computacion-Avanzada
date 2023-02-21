# Derivación numérica. Leer datos a partir del fichero distancia.txt

# Solución analítica: Corresponde a la función s(t) = -70 + 7t + 70exp(-t/10)

#------------------------------------
# IMPORTACIONES
#------------------------------------

import numpy as np
import matplotlib.pyplot as plt
from math import exp, fabs

#------------------------------------
# FUNCIONES
#------------------------------------

# Función que calcula la derivada Analítica de x(t) = -70 + 7t + 70e^(-t/10) respeco a t que es igual a la velocidad.
def velocidad(t:float) -> float:
    return 7 - (7*exp(-t/10))

# Función que calcula la derivada Analítica de v(t) (función anterior) respeco a t que es igual a la aceleración.
def aceleracion(t:float) -> float:
    return 0.7*(exp(-t/10))

# Función que calcula la derivada NUMÉRICA por el método de las diferencias centrales.
def diferencias_centrales(h: float, siguiente: float, anterior: float) -> float:
    return (siguiente - anterior)/(2*h)

# Función que calcula la derivada NUMÉRICA por el método de diferencia hacia adelante.
def diferencia_alante(h: float, siguiente: float, actual: float) -> float:
    return (siguiente - actual)/h

# Función que calcula la derivada NUMÉRICA por el método de diferencia hacia detrás.
def diferencias_atras(h: float, actual: float, anterior: float) -> float:
    return (actual - anterior)/h

def main():
    # Cargamos los datos del fichero y los guardamos en dos vectores
    data = np.loadtxt("distancia.txt")
    tiempo = data[:,0]
    pos = data[:,1]

    # Calculamos la longitud de los vectores leídos.
    if (len(tiempo) == len(pos)):
        n = len(tiempo)
    else:
        print("Error en las longitudes de los vectores leídos del fichero.")

    # Calculamos h y comprobamos que sea correcta en todas las posiciones del vector tiempo.
    tol = 0.0001
    h_anterior = tiempo[1] - tiempo[0]
    for i in range(1, n-1):
        h = tiempo[i+1] - tiempo[i]
        if h - h_anterior > fabs(tol):
            print(f"Hay una variación de h en la posición {i}-{i+1} del fichero.")
        h_anterior = h

    # Calculamos la derivada numérica de las posiciones = velocidades.
    vel = np.zeros([n,1], float)
    for i in range(n):
        if i == 0:
            vel[i] = diferencia_alante(h, pos[i+1], pos[i])
        elif i == n-1:
            vel[i] = diferencias_atras(h, pos[i], pos[i-1])
        else:
            vel[i] = diferencias_centrales(h, pos[i+1], pos[i-1])
    
    # Calculamos la derivada numérica de las velocidades = aceleraciones.
    a = np.zeros([n,1], float)
    for i in range(n):
        if i == 0:
            a[i] = diferencia_alante(h, vel[i+1], vel[i])
        elif i == n-1:
            a[i] = diferencias_atras(h, vel[i], vel[i-1])
        else:
            a[i] = diferencias_centrales(h, vel[i+1], vel[i-1])

    # Hacemos los cálculos ahora de las derivadas analíticas para calcular los errores.
    vel2 = np.zeros([n,1], float)
    for i in range(n):
        vel2[i] = velocidad(tiempo[i])

    a2 = np.zeros([n,1], float)
    for i in range(n):
        a2[i] = aceleracion(vel2[i])
    
    # Cálculo de los errores:
    errores_vel = np.zeros([n,1], float)
    for i in range(n):
        errores_vel[i] = fabs(vel2[i] - vel[i])
    errores_a = np.zeros([n,1], float)
    for i in range(n):
        errores_a[i] = fabs(a2[i] - a[i])

    # Guardamos los resultados en un fichero.
    with open("Sol_DerivacionNumerica.txt", "w", encoding="utf-8") as f:
        f.write("# Resultados Derivación Numérica\n")
        f.write("Tiempo\t Posición\t Velocidad\t Error_velocidad\t Aceleración\t Error_aceleración \n")
        for i in range(n):
            f.write(f"{float(tiempo[i]):.8f}\t {float(pos[i]):.8f}\t {float(vel[i]):.8f}\t {float(errores_vel[i]):.8f}\t {float(a[i]):.8f}\t {float(errores_a[i]):.8f}\n")
    print("Datos guardados en el fichero Sol_DerivacionNumerica.txt")

    # Representamos los resultados gráficamente
    fig1 = plt.figure("Derivación Numérica")
    fig1.subplots_adjust(hspace=0.5, wspace=0.5)

    # Resultados numéricos
    ax = fig1.add_subplot(2,1,1)
    ax.plot(tiempo, pos, "k", markersize=3)
    ax.plot(tiempo, vel, "r", markersize=3)
    ax.plot(tiempo, a, "b", markersize=3)
    ax.set_ylim(-1, 35) 
    ax.grid()
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Valores")
    ax.legend(("Posición", "Velocidad", "Aceleración"), shadow = True)
    ax.set_title("Resultados Numéricos.")

    # Resultados analíticos
    ax = fig1.add_subplot(2,1,2)
    ax.plot(tiempo, pos, "k", markersize=3)
    ax.plot(tiempo, vel2, "r", markersize=3)
    ax.plot(tiempo, a2, "b", markersize=3)
    ax.set_ylim(-1, 35) 
    ax.grid()
    ax.set_xlabel("Tiempo (s)")
    ax.set_ylabel("Valores")
    ax.legend(("Posición", "Velocidad", "Aceleración"), shadow = True)
    ax.set_title("Resultados Analíticos.")
    plt.show()
    
#------------------------------------
# EJECUTAMOS 
#------------------------------------

if __name__ == "__main__":
    main()
