# Ejercicio 7.1: Paseos aleatorios bidimensionales.
# Autor: Pablo Gradolph Oliva
# Asignatura: Computación avanzada

import numpy as np
import vpython as vp
import matplotlib.pyplot as plt
from math import *
from random import uniform, choice

def paseo_aleatorio(n: int, pasos: int, long1:bool=True) -> list:
    # n -> número de paseos aleatorios bidimensionales que se desean construir.
    # pasos -> número de pasos que dan estos paseos aleatorios.
    # long1 -> especifica si los pasos han de ser de longitud 1 o no.

    paseos = []

    if long1 == True:
        for _ in range(n):
            paseo = [(0,0,0)] # Lista del paseo vacía.
            x, y = 0, 0

            for _ in range(pasos):
                x_old, y_old = x, y
                theta = uniform(0, 2*pi) # Cálculo del ángulo.
                x, y = x_old + cos(theta), y_old + sin(theta) # La longitud es 1.
                r2 = x*x + y*y
                paseo.append((x,y,r2))
            
            paseos.append(paseo) # Guardamos el paseo en la lista de todos los paseos
    
    else:
        for _ in range(n):
            paseo = [(0,0,0)] # Lista del paseo vacía.
            x, y = 0, 0

            for _ in range(pasos):
                x_old, y_old = x, y
                theta = uniform(0, 2*pi) # Cálculo del ángulo.
                r = uniform(0.5, 2) # Cálculo de la longitud del paso.
                x, y = x_old + r*cos(theta), y_old + r*sin(theta) # La longitud no es 1.
                r2 = x*x + y*y
                paseo.append((x,y,r2))
            
            paseos.append(paseo) # Guardamos el paseo en la lista de todos los paseos

    return paseos

def main():
    n = 500
    pasos = 100
    long1 = True

    for metodo in range(2):
        if metodo == 1: # Variamos entre pasos de longitud 1 y pasos de diferente longitud.
            long1 = False

        paseos = paseo_aleatorio(n, pasos, long1)

        # Tenemos los valores de r^2 separados por cada paseo.
        # Vamos a agrupar esos valores en función del número de pasos.
        erres = []
        for paseo in paseos:
            r_iterable = []
            for coor in paseo:
                r_iterable.append(coor[2])
            erres.append(r_iterable)

        r_promedio = []
        for j in range(len(erres[0])):
            r1 = []
            for i in range(len(erres)):
                r1.append(erres[i][j])
            suma = sum(r1)
            media = suma/len(r1)
            r_promedio.append(media) # En r_promedio tenemos los promedios de r^2 frente al número de pasos.

        # Elegimos aleatoriamente uno de los paseos para ser representado.
        paseo = choice(paseos)

        x, y = [], []
        for coordenada in paseo: # Cada coordenada tiene los valores (x, y, r)
            i = coordenada[0]
            j = coordenada[1]
            x.append(i)
            y.append(j)
        
        # Representamos el paseo aleatorio.
        fig1 = plt.figure("Paseos aleatorio bidimensional longitud del paso 1.")
        ax = fig1.add_subplot(1,2,1)
        ax.plot(x, y, 'k')
        ax.plot(0, 0, 'o', markersize=3, color='red')
        ax.plot(x[-1], y[-1], 'o', markersize=3, color='green')
        ax.set_title("Representación de uno de los paseos aleatorios.")
        ax.set_ylabel("Eje y")
        ax.set_xlabel("Eje x")
        ax.legend(("Paseo","Origen","Punto final"), shadow=True)
        
        # Representamos r^2 en función del número de pasos con el ajuste por mínimos cuadrados correspondiente.
        xn = np.linspace(0,102,101) # Número de pasos
        n = len(xn)
        
        # Aquí el ajuste: Forzando que pase por el origen.
        m = np.linalg.lstsq(xn.reshape(-1,1), r_promedio, rcond=None)[0][0]
        print(f"Pendiente: {m}")
        f = m*xn

        ax = fig1.add_subplot(1,2,2)
        ax.plot(xn, r_promedio,'o', color='k', markersize=1)
        ax.plot(xn, f, color='k', markersize=1)
        ax.set_title("r^2 frente al número de pasos.")
        ax.set_ylabel("<r^2>")
        ax.set_xlabel("Número de pasos")
        plt.show()

        if metodo == 0:
            # Representación del camino escogido en vpython
            vp.scene.height = 640 # Para hacer la pantalla cuadrada
            Caminante = vp.sphere(pos=vp.vector(0,0,0), radius=0.3, color=vp.color.green)
            eje_x = vp.curve(vp.vector(11,0,0), vp.vector(-11,0,0), color=vp.color.yellow)
            eje_y = vp.curve(vp.vector(0,11,0), vp.vector(0,-11,0), color=vp.color.yellow)

            # La siguiente línea crea una curva por donde pasa el caminante.
            Caminante.orbita = vp.curve(color=vp.vector(0.3,0.3,0.3))
            for i in range(len(paseo)):
                vp.rate(6)
                Caminante.pos=vp.vector(paseo[i][0], paseo[i][1], 0)
                Caminante.orbita.append(pos=Caminante.pos)

        elif metodo == 1:
            Caminante2 = vp.sphere(pos=vp.vector(0,0,0), radius=0.3, color=vp.color.red)

            # La siguiente línea crea una curva por donde pasa el caminante.
            Caminante2.orbita = vp.curve(color=vp.vector(3,3,3))
            for i in range(len(paseo)):
                vp.rate(6)
                Caminante2.pos=vp.vector(paseo[i][0], paseo[i][1], 0)
                Caminante2.orbita.append(pos=Caminante2.pos)

if __name__ == "__main__":
    main()