#------------------------------------
# Clase del 7 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Condicionales y Bucles en Python
#------------------------------------

#In[0]

a=8
if a%2==0 and a%3!=0:
    print('Número par e indivisible por 3')
elif a%2==0 and a%3==0:
    print('Número par y múltiplo de 3')
elif a%2!=0 and a%3==0:
    print('Número impar y múltiplo de 3')
else:
    print('Número impar e indivisible por 3')

#In[1]

a=8
if a%2==0:
    if a%3!=0:
        print('Número par e indivisible por 3')
    else:
        print('Número par y múltiplo de 3')
elif a%2!=0:
    if a%3!=0:
        print('Número impar y múltiplo de 3')
    else:
        print('Número impar e indivisible por 3')

#In[2]

a=8
b=11
c=13
if a < b < c:
    print('Los valores están ordenados crecientemente')
if 0 < a < 10:
    print('El valor "a" está comprendido entre 0 y 10')

#In[3]

for i in [3.14, 'Juan', 21]:
    print(i)
print ('fin del bucle for')

for i in 'Pepito':
    print('Letra',i)
print ('fin del bucle for')

a=1
b=0
for i in 'Pepito':
    b=b+1
    a=a*b
    print(a)
print ('fin del bucle for')


# Ejemplo:

import numpy as np

a = np.arange(5.0)
print(a)
for i in a:
	print(i)

#In[4]

import numpy as np
a=np.linspace(0,5,11)
for i in range(11):
    print(a[i])
print('Con once elementos:')
a=np.linspace(0,5,11)
for i in range(10):
    print(a[i])