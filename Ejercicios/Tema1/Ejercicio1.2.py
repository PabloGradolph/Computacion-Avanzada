# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Escribir un programa para transformar las coordenadas cilíndricas (r, θ, z) 
# de un punto en el espacio en coodenadas cartesianas (x, y, z) y que 
# además calcule la distancia al origen. Utilizar para ello una función. 
# Comprobar que el programa da el resultado correcto con el punto (1, 𝜋/4, 2)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

from math import *

def transformacion(coordenadas: tuple) -> tuple:
    # Guardamos las coordenadas polares
    r = coordenadas[0]
    theta = coordenadas[1]
    z = coordenadas[2]

    # Transformamos
    x = r*cos(theta)
    y = r*sin(theta)
    cartesianas = (x,y,z)

    # Calculamos la distancia y devolvemos los datos
    distancia = sqrt((x*x)+(y*y)+(z*z))
    return cartesianas, distancia

def main():
    # Probamos con el ejemplo del enunciado
    coordenadas = (1,pi/4,2)
    cartesianas, distancia = transformacion(coordenadas)
    print(f"Las coordenadas cartesianas son {cartesianas} y la distancia al origen es {distancia} u^2")

if __name__ == "__main__":
    main()
