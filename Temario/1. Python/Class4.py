#------------------------------------
# Clase del 6 de febrero de 2023
#------------------------------------

#In[0]

import numpy as np
from math import *

print('Raíz cuadrada de 3 con la función sqrt del paquete math:',sqrt(3))
print('Raíz cuadrada de 3 con la función sqrt del paquete numpy:',np.sqrt(3))

#In[1]

a=[1, 2, 3, 4, 5]
b=np.array(a, dtype=int)
print('lista:',a)
print('array:',b)
b=np.array(a, float)
print('array con valores reales:',b)

#In[2]

import numpy as np
a=np.zeros(3,float)
b=np.ones(4,int)
c=np.empty(5,str)
print(a)
print(b)
print(c)
a[0]=np.pi
a[1]=np.sqrt(2)
a[2]=np.e
print(a)

#In[3]

import numpy as np
x1 = np.array([[1, 2, 3], [4, 5, 6]], int)
print('Matriz:')
print(x1)
print('Segundo elemento de la primera fila:')
print(x1[0, 1])
print('Segunda fila:')
print(x1[1,:])

a1=[2, 4, 6, 8]
a2=[3, 6, 9, 12]
a3=[5, 10, 15, 20]

x2=np.array([a1,a2,a3], int)
print('Otra matriz:')
print(x2)

#In[4]

import numpy as np

x1=np.zeros([3,4],int)
print('array bidimensional de ceros:')
print(x1)
print()

x2=np.ones([2,3,4],int)
print('array tridimensional de unos:')
print(x2)

#In[5]

import numpy as np
from math import sqrt

a1=np.array([2, 4, 6, 8], int)
a2=np.array([3, 6, 9, 12], int)

print('Array 1:',a1)
print('Array 2:',a2)
print('Suma de dos arrays:',a1+a2)
print('Producto de dos arrays:',a1*a2)
print('Producto del array 1 por pi:', a1*np.pi)
print('Producto escalar:', np.dot(a1,a2))
print('Raíz cuadrada del array 2:',np.sqrt(a2))

print('Mismo resultado obtenido con map:')
a4=np.array(list(map(sqrt,a2)),float)
print(a4)


# Ejemplo:
from math import *
import numpy as np

lista1=[1,2,3]
lista2=[3,4,5]

a=np.array([lista1,lista2],int)

print(a)
print(np.size(a))
print(np.shape(a))
print(len(a))

#In[6]

import numpy as np

a1=np.array([2, 4, 6, 8], int)
a2=a1

print('a1:')
print(a1)
print('a2:')
print(a2)
print()
print('Cambiamos el primer elemento de a1, a1[0]=777.')
a1[0]=777     # Cambiamos un elemento del array a1
print()

#Observamos que se ha cambiado en a1 y en a2
print('a1:')
print(a1)
print('a2:')
print(a2)

print()
print('Haciendo una copia con np.copy:')
print()
a1=np.array([2, 4, 6, 8], int)
a2=np.copy(a1)

a1[0]=777
print('a1:')
print(a1)
print('a2:')
print(a2)

print()
print('Conversión de a1 en una lista:')
lista=list(a1)
print(lista)