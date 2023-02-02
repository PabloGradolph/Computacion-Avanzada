a=7
b=a.bit_length()
print('a:',a,'  Número de bits:',b)
a=8
b=a.bit_length()
print('a:',a,'  Número de bits:',b)

#------------------------------------

x=3.0
m=x.is_integer()
print('x:', x, '¿Entero?', m)
x=3.1
m=x.is_integer()
print('x:', x, '¿Entero?', m)

#------------------------------------

L=[1,3,5,7,9,1+3j,"hola",[30,31,32]]
print('Esta es la lista que hemos creado:', L)
print('Este es el tercer elemento de la lista:', L[2])
print('Este es el penúltimo elemento de la lista:',L[-2])
print('Aquí están los elementos desde el primero hasta el tercero:',L[:3])
print('Y aquí entre el tercero y el quinto:', L[2:5])
print('Añadimos el número 11 al final de la lista:')
L.append(11)
print(L)
print('Lo añadimos en la posición sexta:')
L.insert(5,11)
print(L)
print('Añadimos los 3 impares siguientes:')
L.extend([13,15,17])
print(L)
print('¿Cuál es la primera ocurrencia del elemento 11? Respuesta:',L.index(11))
print('¿Hemos añadido el número 15 en nuestra lista? Respuesta:',15 in L)
print('¿Y el 19? Respuesta:',19 in L)
print('Vamos a eliminar la palabra hola de nuestra lista:')
L.remove('hola')
print(L)
print('Vamos a eliminar también otros elementos.')
print('Nos quedamos con los impares hasta el 17:')
L.remove(1+3j)
L.remove([30,31,32])
L.remove(11)
print(L)
print('Creamos otra lista, con los números 19 y 21:')
L2=[19,21]
print(L2)
print('Si la multiplicamos por 3:',3*L2)
print('Si sumamos L1 y L2:', L+L2)
print('Para asignar esta concatenación a una nueva lista usamos "list":')
L3=list(L+L2)
print(L3)
print('Podemos sumar todos los elementos de la nueva lista con "sum":')
a=sum(L3)
print('Suma =',a)
print('Valor máximo:',max(L3))
print('Valor mínimo:',min(L3))
print('Número de elementos:',len(L3))
print('Vamos a crear una nueva lista cuyos valores sean la raíz cuadrada')
print('de los elementos de la lista:')
# Es necesario importar la función sqrt del paquete math
from math import sqrt
L4=list(map(sqrt,L3))
print(L4)
print('Para operaciones más sencillas, como multiplicar por 2, es necesario')
print('usar una sintaxis con una función implícita conocida como "lambda":')
L5=list(map(lambda x: 2*x, L3))
print(L5)

#------------------------------------

import numpy as np
from math import *

print('Raíz cuadrada de 3 con la función sqrt del paquete math:',sqrt(3))
print('Raíz cuadrada de 3 con la función sqrt del paquete numpy:',np.sqrt(3))

#------------------------------------

import numpy as np
a=[1, 2, 3, 4, 5]
b=np.array(a, dtype=int)
print('lista:',a)
print('array:',b)
b=np.array(a, float)
print('array con valores reales:',b)
