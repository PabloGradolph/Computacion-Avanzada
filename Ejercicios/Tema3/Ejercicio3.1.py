# Generación de números aleatorios siguiendo ciertas distribuciones de probabilidad.
# Siguiendo los métodos de la transformación y del rechazo.

#======= Apartado A ==========
from random import random, uniform
from math import exp, pi, sqrt, fabs
import numpy as np
import matplotlib.pyplot as plt

# Py = 3/2 * y^2 con "y" entre [-1,1]:

# Rango en el que quiero que estén mis números aleatorios.
limite_inferior = -1
limite_superior = 1

# Cantidad de números aleatorios que quiero generar y máximo que alcanza la distribución.
n = 10000
max_distro = 3/2

# ------------------------------
# Método de la transformación:
# ------------------------------

# Para este método conviene que la función de distribución esté normalizada a 1. En este caso
# si que está normalizada. (Calcular integral entre -1 y 1 en valor absoluto).
valores=[]		
valores_x=[]

for i in range(n):
	x=uniform(-(2**5/9)**(1/4),(2**5/9)**(1/4)) # Normalizada
	y=(2*fabs(x))**(1/3) # Ecuación tras aplicar el método de la transformación.
	valores_x.append(x)
	if x>0:
		valores.append(y)
	else:
		valores.append(-y)

# Descomentar si se quieren ver los puntos generados.
# plt.plot(valores_x, "o", markersize="3")
# plt.show()
# plt.plot(valores, "o", markersize="3")
# plt.show()

# Representamos gráficamente los resultados.
num_clases = 25
cuentas,lims_clases=np.histogram(valores,bins=num_clases,range=(-1,max_distro),density=True)
clases = lims_clases[:-1].copy()
clases = clases+(1/2)*max_distro/num_clases
plt.plot(clases,cuentas,"ob", label="Distribución aleatoria")
x_teo=np.arange(-1,1.1,0.1)
y_teo= 3/2 * ((x_teo)**2)
plt.plot(x_teo,y_teo,"-r", label="Distribución teórica")
plt.title("MÉTODO TRANSFORMACIÓN APARTADO A")
plt.legend()
plt.xlabel("Valores")
plt.ylabel("Probabilidad")
plt.xlim(-1.1,1.1)
plt.ylim(-1,2)
plt.show()

# ------------------------------
# Método del rechazo:
# ------------------------------

# Función de distribución.
def distro(y):
    return 3/2 * (y*y)

valores = []
i = 0
while i < n:
	y = uniform(limite_inferior, limite_superior)
	test = random() * max_distro # Multiplico por el máximo valor de la función distro(y)
	if test<distro(y):
		valores.append(y)
		i+=1

# Descomentar si se quieren ver los puntos generados.
# plt.plot(valores, "o", markersize="3")
# plt.show()

# Representamos gráficamente los resultados.
num_clases = 25
cuentas,lims_clases=np.histogram(valores,bins=num_clases,range=(-1,1),density=True)
clases = lims_clases[:-1].copy()
clases = clases+(1/2)*max_distro/num_clases
plt.plot(clases,cuentas,"ob", label="Distribución aleatoria")
x_teo=np.arange(-1,1.1,0.1)
y_teo= 3/2 * ((x_teo)**2)
plt.plot(x_teo,y_teo,"-r", label="Distribución teórica")
plt.legend()
plt.title("MÉTODO RECHAZO APARTADO A")
plt.xlabel("Valores")
plt.ylabel("Probabilidad")
plt.xlim(-1.1,1.1)
plt.ylim(-1,2)
plt.show()

#======= Apartado B ==========

# Py = 1/sqrt(pi)*exp(-(y-1)**2) con "y" entre [-3,5]:

for n in [100,1000,10000]:
	# Rango en el que quiero que estén mis números aleatorios.
	limite_inferior = -3
	limite_superior = 5

	# Cantidad de números aleatorios que quiero generar y máximo que alcanza la distribución.
	max_distro = 1/sqrt(pi)

	# Función de distribución.
	def distro(y):
		return (1/sqrt(pi)) * exp(-((y-1)**2))

	valores = []
	i = 0
	while i < n:
		y = uniform(limite_inferior, limite_superior)
		test = random() * max_distro # Multiplico por el máximo valor de la función distro(y)
		if test<distro(y):
			valores.append(y)
			i+=1

	# Descomentar si se quieren ver los puntos generados.
	# plt.plot(valores, "o", markersize="3")
	# plt.show()

	# Representamos gráficamente los resultados.
	num_clases = 25
	cuentas,lims_clases=np.histogram(valores,bins=num_clases,range=(-3,5),density=True)
	clases = lims_clases[:-1].copy()
	clases = clases+(1/2)*max_distro/num_clases
	plt.plot(clases,cuentas,"ob", label="Distribución aleatoria")
	x_teo=np.arange(-3,5.1,0.1)
	y_teo= np.exp(-((x_teo-1)**2)) * (1/np.sqrt(pi)) 
	plt.plot(x_teo,y_teo,"-r", label="Distribución teórica")
	plt.legend()
	plt.title(f"MÉTODO RECHAZO CON {n} VALORES GENERADOS")
	plt.xlabel("Valores")
	plt.ylabel("Probabilidad")
	plt.xlim(-3.1,5.1)
	plt.ylim(-0.25,0.75)
	plt.show()
