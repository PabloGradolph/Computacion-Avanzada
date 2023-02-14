#------------------------------------
# Clase del 14 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Gráficos de Densidad y Representación gráfica en 3D
# (uso de matplotlib y vpython)
#------------------------------------

#In[0]
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
ejes=plt.gca() # Get current access (accedemos al método de objetos)
ejes.set_aspect(0.5)
plt.xlim(3,18)
plt.ylim(5,28)
plt.show()

# In[1]:

import numpy as np
import vpython as vp
vp.sphere(radius=0.5, pos=vp.vector(0.5,-1.0,0.0),color=vp.vector(1,1,1))

s=vp.sphere()
s.pos=vp.vector(2,-1,0)
s.radius=0.3
s.color=vp.vector(1,1,0)