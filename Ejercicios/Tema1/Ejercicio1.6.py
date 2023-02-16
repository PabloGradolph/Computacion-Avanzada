# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Representar gráficamente varias funciones con distintos tipos de puntos
# y líneas y sus correspondientes leyendas.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0,10,100)
y1, y2, y3, y4, y5, y6, y7 = np.exp(x), np.sin(x), np.cos(x), np.log(x), np.sqrt(x), x**(-1), ((x-3)**2)
l1 = plt.plot(x, y1, "bD--", markersize=3)
l2 = plt.plot(x, y2, "go-", markersize=3)
l3 = plt.plot(x, y3, "ro-", markersize=3) 
l4 = plt.plot(x, y4, "y-.", markersize=3)
l5 = plt.plot(x, y5, "c--", markersize=3)
l6 = plt.plot(x, y6, "ms:", markersize=3)
l7 = plt.plot(x, y7, "k1--", markersize=3)
plt.ylim(-1, 5) 
plt.grid()
plt.xlabel("Eje x")
plt.ylabel("Eje y")
plt.legend( (l1[0], l2[0], l3[0], l4[0], l5[0], l6[0], l7[0]), ("Exponencial", "Seno", "Coseno", "Logaritmo", "Raíz Cuadrada", "1/x", "(x-3)^2"), shadow = True)
plt.title("Gráficas de funciones")
plt.show()