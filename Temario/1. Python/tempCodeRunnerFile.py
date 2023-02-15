import numpy as np
import matplotlib.pyplot as plt

a=np.zeros([60,40], float)
num_filas, num_cols = a.shape
print(num_filas, num_cols)
input("Pulse para continuar: ")

for y in range(num_filas):
    for x in range(num_cols):
        a[y,x]=np.exp(-(y-30)**2/200 - (x-20)**2/120)

plt.imshow(a, origin='lower', extent=[0,32.4,0,48.3])
plt.gray()
plt.colorbar()
#ejes=plt.gca() # Get current access (accedemos al método de objetos)
#ejes.set_aspect(0.5)
plt.xlim(3,18)
plt.ylim(5,28)
plt.show()