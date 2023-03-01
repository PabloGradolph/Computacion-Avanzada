#------------------------------------
# Clase del 29 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Método de la transformación y método del rechazo.
#------------------------------------

#======= Método de la transformación ==========

# Programa para generar una distribución exponencial a partir de una uniforme por el
# método de la transformación

from random import *
from math import log
import numpy as np
import matplotlib.pyplot as plt

n=1000			# Número de valores
valores=[]		# Lista para guardalos
valores_x=[]	# Guardamos también los valores uniformes

for i in range(n):
	x=random()
	y=-log(x)
	valores_x.append(x)
	valores.append(y)

plt.plot(valores_x,"o", markersize="3")
plt.show()
plt.plot(valores,"o", markersize="3")
plt.show()

#======================================

num_clases=25		# Número de recipientes para el histograma
val_max=5.0		# Máximo valor que vamos a considerar
# Usamos la función histogram de numpy. Devuelve un array con las cuentas de cada clase y
# otro con los límites entre clases. La dimensión de éste último es una unidad mayor que 
# número de clases
cuentas,lims_clases=np.histogram(valores,bins=num_clases,range=(0,val_max),density=True)
# Creamos un array (clases) con valores centrados en cada clase
clases = lims_clases[:-1].copy()    # Copia de lims_clases con el último elemento borrado
clases = clases+(1/2)*val_max/num_clases	     # Sumamos la mitad del tamaño de cada clase
# Creamos el gráfico:
plt.plot(clases,cuentas,"ob", label="Distribución aleatoria")
# Creamos una curva con la distribución teórica y la añadimos al plot
x_teo=np.arange(0,5.1,0.1)
y_teo=np.exp(-x_teo)
plt.plot(x_teo,y_teo,"-r", label="Distribución teórica")
plt.legend()		# Para incluir las leyendas que figuran en los "labels"
plt.xlabel("Valores")
plt.ylabel("Probabilidad")
plt.xlim(0,5)
plt.ylim(-0.02,1.02)
plt.show()

#======================================

num_clases=25		# Número de recipientes para el histograma
val_max=5.0		# Máximo valor que vamos a considerar
plt.hist(valores,num_clases,density=True,width=0.9*val_max/num_clases, label="Distribución aleatoria")
plt.plot(x_teo,y_teo,"-r", label="Distribución teórica")
plt.legend()
plt.xlim(0,5)
plt.ylim(0,1)
plt.show()

#======= Método del rehcazo ==========

# Ejemplo completamente inventado para ver el funcionamiento del método.
from random import *
from math import exp
import numpy as np
import matplotlib.pyplot as plt

# Rango en el que quiero que estén mis números aleatorios.
limite_inferior = -2
limite_superior = 2

def distro(y):
	valor = exp(y)*2*y
	return valor

max_distro = 5
n = 1000
valores = []

i = 0
while i < n:
	y = uniform(limite_inferior, limite_superior)
	test = random() * max_distro # Multiplico por el máximo valor de la función distro(y)
	if test<distro(y):
		valores.append(y)
		i+=1

print(valores)