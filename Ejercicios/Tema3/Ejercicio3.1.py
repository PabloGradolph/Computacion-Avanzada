# Generación de números aleatorios siguiendo ciertas distribuciones de probabilidad.
# Siguiendo los métodos de la transformación y del rechazo.

#======= Apartado A ==========
from random import *
from math import exp
import numpy as np
import matplotlib.pyplot as plt

# Py = 3/2 * y^2 con y entre [-1,1]:

# Rango en el que quiero que estén mis números aleatorios.
limite_inferior = -1
limite_superior = 1

# Cantidad de números aleatorios que quiero generar.
n = 1000

# Método de la transformación:
# Para este método conviene que la función de distribución esté normalizada a 1. En este caso
# si qu está normalizada. (Calcular integral entre -1 y 1 en valor absoluto).
valores=[]		
valores_x=[]

# Método del rechazo:
# Función de distribución.
def distro(y):
    return 3/2 * y*y

max_distro = 3/2
valores = []
i = 0
while i < n:
	y = uniform(limite_inferior, limite_superior)
	test = random() * max_distro # Multiplico por el máximo valor de la función distro(y)
	if test<distro(y):
		valores.append(y)
		i+=1

# Mostramos los valores que se han generado siguiendo la distribución.
plt.plot(valores, "o", markersize="3")
plt.show()

num_clases = 25
cuentas,lims_clases=np.histogram(valores,bins=num_clases,range=(0,max_distro),density=True)
clases = lims_clases[:-1].copy()
clases = clases+(1/2)*max_distro/num_clases
plt.plot(clases,cuentas,"ob", label="Distribución aleatoria")
x_teo=np.arange(-1,1.1,0.1)
y_teo= 3/2 * ((x_teo)**2)
plt.plot(x_teo,y_teo,"-r", label="Distribución teórica")
plt.legend()
plt.xlabel("Valores")
plt.ylabel("Probabilidad")
plt.xlim(-1.1,1.1)
plt.ylim(-2,2)
plt.show()

#======= Apartado B ==========