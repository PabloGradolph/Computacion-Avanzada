#------------------------------------
# Ejercicio 1.1
# Supongamos que conocemos la posición de un punto en el espacio bidimensional en coordenadas
# polares, r, theta. Escribir un programa en Python que transforme dichas coordenadas en coordenadas
# cartesianas. Para ellos, hacer que el programa pregunte al usuario los valores de r y theta, este último 
# en grados, después hacer la correspondiente transformación, y finalmente imprimir los resultados en pantalla.
#------------------------------------

from math import *

# Pedimos los valores de las coordenadas polares.
r = float(input("Introduzca la coordenada r: "))
theta = float(input("Introduzca la coordenada theta (en grados): "))

# Transformamos primero a radianes.
theta = theta * (2*pi/360)

# Convertimos a coordenadas cartesianas e imprimimos los resultados por pantalla.
# X = r sin(theta) e Y = r cos(theta)
x = r * sin(theta)
y = r * cos(theta)
print(f"Las coordenadas cartesianas son: ({x}, {y})")





