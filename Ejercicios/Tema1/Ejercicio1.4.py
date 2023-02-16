# Ejercicio 1.4

import numpy as np
import matplotlib.pyplot as plt

stm = np.loadtxt("stm.txt", float)
print(f"Número de filas = {np.shape(stm)[0]}")
print(f"Número de columnas = {np.shape(stm)[1]}")

plt.imshow(stm, origin='lower', extent=[0,6.47,0,6.37])
plt.gray()
plt.colorbar()
plt.xlabel("Eje x (nm)")
plt.ylabel("Eje y (nm)")
plt.title("Reconstrucción 7x7 de la superficie de Si(111)")
plt.show()