import numpy as np
from collections import defaultdict
from math import *
import matplotlib.pyplot as plt
import itertools
import time

# Variables globales
J = 1.0
kB = 1.0

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
    plt.title("Configuración de los espines.")
    plt.gca().set_aspect("equal")
    plt.grid()
    plt.show()

# Energía local del sitio (i,j)
def energia_sitio(sitios: list, nbhs: defaultdict, espines: dict) -> float:
    energy = 0.0
    for nbh in nbhs[sitios]:
        energy += espines[sitios] * espines[nbh]
    return -J * energy

# Energía total del sistema
def energia_total(sitios: list, nbhs: defaultdict, espines: dict) -> float:
    energy = 0.0
    for site in sitios:
        energy += energia_sitio(site, nbhs, espines)
    return 0.5 * energy # Hay que dividir por 2 debido a que las interacciones se cuentan 2 veces.

# Computa la magnetización total de la red.
def magnetizacion(espines: dict) -> float:
    mag = 0.0
    for spin in espines.values():
        mag += spin
    return mag

# Función para ajustar: ley de potencias.
def ley_potencias(temperatura, beta, tc):
    delta = 0.01  # Valor para limitar la temperatura cerca de tc
    temp_limit = np.where(temperatura <= (tc - delta), temperatura, tc - delta)
    return (tc - temp_limit)**beta

# Función de error para el ajuste.
def error_func(params, temperatura_restringida, magnetizacion_media):
    beta, tc = params
    y_pred = ley_potencias(temperatura_restringida, beta, tc)
    return np.sum((magnetizacion_media - y_pred)**2)

def metropolis(site: tuple, T: float, espines:dict, nbhs: defaultdict):
    #oldSpin = espines[site]
    oldEnergy = energia_sitio(site, nbhs, espines)
    espines[site] *= -1 # Se le da la vuelta al espín
    newEnergy = energia_sitio(site, nbhs, espines) 
    deltaE = newEnergy - oldEnergy # Calculamos la energía necesaria
    if deltaE <= 0: # Si es favorable se lo deja volteado
        pass
    else: # Si no es favorable, le damos la "oportunidad" de voltear mediante un número aleatorio comparandolo con el factor de Boltzmann.
        if np.random.uniform(0, 1) <= np.exp(-deltaE/(kB*T)):
            pass
        else:
            espines[site] *= -1

def paso_montecarlo(T: float, sitios: list, espines: dict, nbhs: defaultdict):
    # Un paso de Monte carlo consiste en recorrer la cantidad de sitios que tenga la red aleatoriamente y en cada elección aplicar el algoritmo de Metrópolis.
    for i in range(len(sitios)):
        int_sitio_random = np.random.randint(0, len(sitios))
        sitio_random = sitios[int_sitio_random]
        metropolis(sitio_random, T, espines, nbhs)

def main():
    print("----------------------------MODELO DE ISING----------------------------")
    print("-> MÉTODO DE MONTECARLO (Algoritmo de metrópolis):")
    print()
    # Condiciones iniciales.
    n = 10 # Número de espines 10x10.
    Tc = 2.27 # Temperatura crítica del modelo de ising (teórica)

    # Definimos todo lo que vamos a usar:
    sitios = list() # Sitios de la red (coordenadas i, j)
    espines = dict() # Diccionario donde las keys son las parejas (i,j) y los valores el espín.  

    for x, y in itertools.product(range(n), range(n)):
        sitios.append((x,y))
    espines = inicializar_spin(sitios, espines) 
    plot_espines(n, espines) # Descomentar si se quiere ver la red de espines iniciales.

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
    print("COMENZANDO LA SIMULACIÓN...")
    start = time.time()
    N = 1000 # Número de espacios temporales.
    T_max = 5.0
    T_min = 0.0
    T_paso = -0.1
    temps = np.arange(T_max, T_min, T_paso) # Definimos las temperaturas con las que vamos a trabajar.
    energias = np.zeros(shape=(len(temps), N))
    magnetizaciones = np.zeros(shape=(len(temps), N))

    for indice_T, T in enumerate(temps): # Enumerate devuelve tuplas (índice, temperatura)
        for i in range(N):
            paso_montecarlo(T, sitios, espines, nbhs)
            energias[indice_T, i] = energia_total(sitios, nbhs, espines)
            magnetizaciones[indice_T, i] = magnetizacion(espines)
        if indice_T==10: # Temperatura = 4.0
            fig1 = plt.figure("Modelo de Ising")
            ax = fig1.add_subplot(2,2,4)
            ax.plot(np.arange(N), magnetizaciones[indice_T, :]/100, color='k')
            ax.grid()
            ax.set_ylabel("Magnetización")
            ax.set_xlabel("Pasos de tiempo")
            ax.set_ylim(-1.1,1.1)
            ax.set_title(f"T=4.0")
        elif indice_T==27: # Temperatura = 2.3
            ax = fig1.add_subplot(2,2,2)
            ax.plot(np.arange(N), magnetizaciones[indice_T, :]/100, color='k')
            ax.grid()
            ax.set_ylabel("Magnetización")
            ax.set_xlabel("Pasos de tiempo")
            ax.set_ylim(-1.1,1.1)
            ax.set_title(f"T=2.25")
        elif indice_T==30: # Temperatura = 2.0
            ax = fig1.add_subplot(2,2,3)
            ax.plot(np.arange(N), magnetizaciones[indice_T, :]/100, color='k')
            ax.grid()
            ax.set_ylabel("Magnetización")
            ax.set_xlabel("Pasos de tiempo")
            ax.set_ylim(-1.1,1.1)
            ax.set_title(f"T=2.0")
        elif indice_T==35: # Temperatura = 1.5
            ax = fig1.add_subplot(2,2,1)
            ax.plot(np.arange(N), magnetizaciones[indice_T, :]/100, color='k')
            ax.grid()
            ax.set_ylabel("Magnetización")
            ax.set_xlabel("Pasos de tiempo")
            ax.set_ylim(-1.1,1.1)
            ax.set_title(f"T=1.5")
    end = time.time()
    plt.show()

    # Cálculo de promedios:
    tau = N // 2
    energia_media = np.mean(energias[:, tau:], axis=1) 
    magnetizacion_media = abs(np.mean(magnetizaciones[:, tau:]/100, axis=1))

    # ---- Cálculo de Beta Temperatura crítica: -----
    # Restringir los valores de temperatura
    temperatura_restringida = np.clip(temps, None, 2.9)  # Ejemplo: límite superior de 2.9

    # Ajuste no lineal utilizando el método de descenso del gradiente
    # Inicializar los parámetros
    beta_inicial = 0.5
    tc_inicial = 2.0
    params_iniciales = np.array([beta_inicial, tc_inicial])

    # Hiperparámetros del descenso del gradiente
    learning_rate = 0.01
    num_iterations = 1000

    # Descenso del gradiente
    params_optimizados = params_iniciales.copy()

    for _ in range(num_iterations):
        gradiente = np.zeros_like(params_optimizados)

        for i, param in enumerate(params_optimizados):
            perturbacion = np.zeros_like(params_optimizados)
            perturbacion[i] = 1e-5

            gradient_pos = error_func(params_optimizados + perturbacion, temperatura_restringida, magnetizacion_media)
            gradient_neg = error_func(params_optimizados - perturbacion, temperatura_restringida, magnetizacion_media)

            gradiente[i] = (gradient_pos - gradient_neg) / (2 * perturbacion[i])

        params_optimizados -= learning_rate * gradiente

    # Obtener los parámetros óptimos del ajuste
    beta_estimado, tc_estimada = params_optimizados

    # Cálculo de la susceptibilidad magnética
    magnetizacion_std = np.std(np.abs(magnetizaciones[:, tau:]), axis=1) # Desviación típica.
    susceptibilidad = magnetizacion_std ** 2 / (kB * temps)

    # Cálculo del calor específico.
    energia_std = np.std(energias[:, tau:], axis=1) # Desviación típica
    calor_especifico = energia_std ** 2 / (kB * temps * temps)

    # Gráficas para la energía total y la magnetización en función de la temperatura.
    fig, ax = plt.subplots(1,1)
    ax.plot(temps, energia_media/100, color='k')
    ax.set_xlabel("Temperatura")
    ax.set_ylabel("Energía")
    ax.grid()
    ax.legend("Energía")
    ax.set_title("Energía media por espín frente a temperatura. Red 10x10")
    plt.show()

    fig, ax = plt.subplots(1,1)
    ax.plot(temps, magnetizacion_media, color='k')
    ax.set_xlabel("Temperatura")
    ax.set_ylabel("Magnetización")
    ax.grid()
    ax.legend("Magnetización")
    ax.set_title("Magnetización frente a temperatura. Red 10x10")
    plt.show()

    # Gráfica para la susceptibilidad magnética
    fig, ax = plt.subplots(1,1)
    ax.plot(temps, susceptibilidad/100, color='k')
    ax.set_xlabel("Temperatura")
    ax.set_ylabel(r"$\chi$")
    ax.grid()
    ax.legend("Susceptibilidad")
    ax.set_title("Susceptibilidad magnética frente a temperatura. Red 10x10")
    plt.show()

    # Gráfica para el calor específico.
    fig, ax = plt.subplots(1,1)
    ax.plot(temps, calor_especifico/100, color='k')
    ax.set_xlabel("Temperatura")
    ax.set_ylabel(r"$C_v$")
    ax.grid()
    ax.legend("Calor específico")
    ax.set_title("Calor específico frente a temperatura. Red 10x10")
    plt.show()

    print()
    print(f"*Tiempo de ejecución (s): {end-start}")
    print()
    print("Resultados de interés:")
    print("Valor estimado de beta:", beta_estimado)
    print("Valor estimado de temperatura crítica:", tc_estimada)

if __name__ == "__main__":
    main()