#------------------------------------
# Clase del 28 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Histogramas con Python.
#------------------------------------

#======= Histogramas en Python ==========

from random import *
import numpy as np
import matplotlib.pyplot as plt
from math import log

n=10000			# Número de valores
valores=[]		# Lista para guardalos

for i in range(n):
    x=uniform(0,5) # Número aleatorio entre 0 y 5
    valores.append(x)

num_clases=25		# Número de recipientes para el histograma
val_max=5.0		# Máximo valor que vamos a considerar
# Usamos la función histogram de numpy. Devuelve un array con las cuentas de cada clase y
# otro con los límites entre clases. La dimensión de éste último es una unidad mayor que 
# número de clases
cuentas,lims_clases=np.histogram(valores,bins=num_clases,range=(0,val_max),density=True)
# density = True/False en función de si representamos frecuencia(False) o probabilidad(True).
# Creamos un array (clases) con valores centrados en cada clase
clases = lims_clases[:-1].copy()   # Copia de lims_clases con el último elemento borrado
clases = clases+(1/2)*val_max/num_clases	     # Sumamos la mitad del tamaño de cada clase
# Creamos el gráfico:
plt.plot(clases,cuentas,"ob", label="Distribución aleatoria")
# Creamos una curva con la distribución teórica y la añadimos al plot
x_teo=np.arange(0,5.1,0.1)
y_teo=0.2*np.ones(len(x_teo),float)
plt.plot(x_teo,y_teo,"-r", label="Distribución teórica")
plt.legend()		# Para incluir las leyendas que figuran en los "labels"
plt.xlabel("Valores")
plt.ylabel("Probabilidad")
plt.xlim(0,5)
plt.ylim(-0.02,1.02)
#plt.ylim(0,n/5) # Para density = False
plt.show()

#==== Histogramas con matplotlib ============

num_clases=25		# Número de recipientes para el histograma
val_max=5.0		# Máximo valor que vamos a considerar
plt.hist(valores,num_clases,density=True,width=0.9*val_max/num_clases, label="Distribución aleatoria")
plt.plot(x_teo,y_teo,"-r", label="Distribución teórica")
plt.legend()
plt.xlim(0,5)
plt.ylim(0,1)
plt.show()