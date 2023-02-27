#------------------------------------
# Clase del 27 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Números aleatorios por el método congruencial lineal.
#------------------------------------

from matplotlib.pyplot import plot, show

# Establecemos las constantes del método

a=1664525
c=1013904223
m=4294967296
N=100		# Número de puntos
x=1		# Semilla
results=[]	# Lista para guardar los valores
for i in range(N):
	x=(a*x+c)%m
	results.append(x)

# Hacemos una gráfica con los resultados:

print(results)
plot(results,"o",markersize="3")
show()

#======================================

from random import *
a=1
lista=["a","e","i","o","u"]
while a!=0:
	print("Número real entre 0 y 1, el 1 no cuenta:", random() )
	print("Número entero entre 0 y 99:", randrange(100) )
	print("Número entero entre 50 y 99:", randrange(50,100) )
	print("Número entero entre 50 y 99, múltiplo de 5:", randrange(50,100,5) )
	print("Número real entre 50 y 100, el 100 no cuenta:", uniform(50,100) )
	print("Elemento al azar de la lista",lista,":", choice(lista) )
	print("Número entero entre 50 y 100, el 100 sí que entra:", randint(50,100) )
	a=int(input("\nPara parar introduce 0, para seguir, cualquier otro número:"))

#======================================

from random import *

seed (42)
for i in range(10):
    print(randrange(100))