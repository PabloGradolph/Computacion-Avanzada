# Difuja la red cristalina del NaCl en 3 dimensiones con vpython.

import vpython as vp
import numpy as np
from itertools import product

# Datos iniciales del problema
red = 5*5.64
radio_Na = 1.15
radio_Cl = 1.67
distancia = 2.82

# Array con elementos esfera 11x11x11 (cantidad de átomos que habrá)
atomos = np.empty((11,11,11), vp.sphere)

# Creamos la lista de coordenadas (centradas) para ello dividimos la red entera entre 2 (mismo espacio a cada lado del 0)
coor_inicial = -(red/2)
coordenadas = []
for h in range(11):
    coordenada = coor_inicial + h*distancia
    coordenadas.append(coordenada)

# Tenemos la lista de coordenadas para una recta, creamos aquí todas las combinaciones posibles para coordenadas en el espacio.
coordenadas = list(product(coordenadas,repeat=3))

contador = 0 # El contador nos ayudará a ir representando un átomo de cada tipo.
for i in range(11):
    for j in range(11):
        for k in range(11):
            coor = coordenadas[0] # Cogemos la primera coordenada donde irá representada la esfera
            if contador%2==0: # Si el contador es par representamos un cloro.
                # Cloros
                atomos[i,j,k] = vp.sphere(pos=vp.vector(coor[0],coor[1],coor[2]), radius=radio_Cl, color=vp.vector(0,1,0))
            else: # Si el contador es impar representamos un sodio.
                # Sodios
                atomos[i,j,k] = vp.sphere(pos=vp.vector(coor[0],coor[1],coor[2]), radius=radio_Na, color=vp.vector(1,1,1))
            contador += 1
            del coordenadas[0] # Borramos la coordenada que hemos cogido para poder coger la siguiente.
