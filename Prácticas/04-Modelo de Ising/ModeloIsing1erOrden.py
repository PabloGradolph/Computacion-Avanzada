import numpy as np
from collections import defaultdict
from math import *
import matplotlib.pyplot as plt
import itertools

# Variables globales
J = 1.0
kB = 1.0 
mu = 1.0

# Inicializa los espines de la red a un valor arbitrario.
def inicializar_spin(sitios: list, espines: dict) -> np.array:
    for spin in sitios:
        espines[spin] = np.random.choice([-1, 1])
    return espines

# Función para la visualización de los espines.
def plot_espines(n: int, espines: dict):
    plt.figure()
    colors = {1: "red", -1: "blue"}
    for site, spin in espines.items():
        x, y = site
        plt.quiver(x, y, 0, spin, pivot="middle", color=colors[spin])
    plt.xticks(range(-1,n+1))
    plt.yticks(range(-1,n+1))
    plt.title("Configuración inicial de los espines.")
    plt.gca().set_aspect("equal")
    plt.grid()
    plt.show()

# Energía local del sitio (i,j) de primer orden
def energia_sitio_primer_orden(H:float, sitios: list, nbhs: defaultdict, espines: dict) -> float:
    energy = 0.0
    for nbh in nbhs[sitios]:
        energy += espines[sitios] * espines[nbh] - mu*H*espines[sitios]
    return energy

# Energía total del sistema de primer orden.
def energia_total_primer_orden(H: float, sitios: list, nbhs: defaultdict, espines: dict) -> float:
    energy = 0.0
    for site in sitios:
        energy += energia_sitio_primer_orden(H, site, nbhs, espines)
    return 0.5 * energy

# Computa la magnetización total de la red.
def magnetizacion(espines: dict) -> float:
    mag = 0.0
    for spin in espines.values():
        mag += spin
    return mag

# Función del algorimto de metrópolis primer orden.
def metropolis_primer_orden(H: float, site: tuple, T: float, espines:dict, nbhs: defaultdict):
    oldEnergy = energia_sitio_primer_orden(H, site, nbhs, espines)
    espines[site] *= -1 # Se le da la vuelta al espín
    newEnergy = energia_sitio_primer_orden(H, site, nbhs, espines) 
    deltaE = newEnergy - oldEnergy # Calculamos la energía necesaria
    if deltaE <= 0: # Si es favorable se lo deja volteado
        pass
    else: # Si no es favorable, le damos la "oportunidad" de voltear mediante un número aleatorio comparandolo con el factor de Boltzmann.
        if np.random.uniform(0, 1) <= np.exp(-deltaE/(kB*T)):
            pass
        else:
            espines[site] *= -1

# Función para la simulación de montecarlo que llama a la función del algorimto de metrópolis en cada paso.
def paso_montecarlo(H: float, T: float, sitios: list, espines: dict, nbhs: defaultdict):
    # Un paso de Monte carlo consiste en recorrer la cantidad de sitios que tenga la red aleatoriamente y en cada elección aplicar el algoritmo de Metrópolis.
    for i in range(len(sitios)):
        int_sitio_random = np.random.randint(0, len(sitios))
        sitio_random = sitios[int_sitio_random]
        metropolis_primer_orden(H, sitio_random, T, espines, nbhs)

def main():
    # Estudiamos ahora el modelo de Ising de primer orden: (en presencia de un campo magnético externo.)
    print("----------------------------MODELO DE ISING----------------------------")
    print("MODELO DE ISING DE 1er ORDEN")
    print("->Datos:")
    print("   -Tamaño de la red: 10x10")
    print("   -Número de pasos de montecarlo: 1000")
    print("   -Temperaturas: 0º - 5º")

    n = 10 # Número de espines 10x10.
    sitios = list() # Sitios de la red (coordenadas i, j)
    espines = dict() # Diccionario donde las keys son las parejas (i,j) y los valores el espín.  

    for x, y in itertools.product(range(n), range(n)):
        sitios.append((x,y))
    espines = inicializar_spin(sitios, espines) 
    plot_espines(n, espines)

    nbhs = defaultdict(list) # Recorremos todos los sitios y agregamos en su lista de nbhs los sitios vecinos. Tenemos en cuenta que el sistema
                             # tiene condiciones periódicas de frontera.
    for site in espines:
        x, y = site
        if x + 1 < n:
            nbhs[site].append(((x + 1) % n, y))
        if x - 1 >= 0:
            nbhs[site].append(((x - 1) % n, y))
        if y + 1 < n:
            nbhs[site].append((x, (y + 1) % n))
        if y - 1 >= 0:
            nbhs[site].append((x, (y - 1) % n))
    
    # Comenzamos la simulación:
    print()
    print("COMENZANDO LA SIMULACIÓN...")
    N = 1000 # Número de espacios temporales.
    
    Hs = np.linspace(-10,10.1,20)
    Hs = list(Hs)

    temperaturas = [5.0, 4.0, 2.5, 2.0, 1.0]
    magnetizaciones = np.zeros(shape=(len(Hs), N))

    for T in temperaturas:

        for indice_H, H in enumerate(Hs):
            for i in range(N):
                paso_montecarlo(H, T, sitios, espines, nbhs)
                magnetizaciones[indice_H, i] = magnetizacion(espines)

        magnetizacion_media = np.mean(magnetizaciones/100, axis=1)
        fig, ax = plt.subplots(1,1)
        ax.plot(Hs, magnetizacion_media, 'o-', color='k')
        ax.set_xlabel("H")
        ax.set_ylabel("Magnetización")
        ax.grid()
        ax.legend("Magnetización")
        ax.set_title(f"T={T}")
        plt.show()
        
    print("FIN DE LA SIMULACIÓN")

if __name__ == "__main__":
    main()