#------------------------------------
# Clase del 8 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Funciones y comienzo de representación gráfica con Python
# (uso de matplotlib)
#------------------------------------

#In[0]
import numpy as np

def funcion1(a):
    b=np.array(a,int)
    c=b*2
    d=list(c)
    return b,d      # Devuelve un array con los elementos de la lista de
                    # entrada y una lista cuyos elementos están multiplicados
                    # por dos

lista1=[1,3,5,7,9]
abc=np.array(lista1,int)

array1,lista2 = funcion1(lista1)
#array1,lista2 = funcion1(abc)

print('Lista original:',lista1)
#print('array original:', abc)
print('Lista convertida en array:',array1)
print('Lista con los elementos duplicados:',lista2)

# Ejemplo: función sin argumentos ni retorno:

def imprime_ok():
    print('No hay errores')

def imprime_error(a):
    print('Se ha detectado un error')
    print('El valor de',a,'no es correcto')
	
a=2+2
if a==4:
    imprime_ok()
else:
    imprime_error(a)

#In[1]

import numpy as np

def duplicar(a):
    b=a*2
    return b

lista1=[1,3,5,7,9]

lista2 = list(map(duplicar,lista1))

print('Lista con los elementos duplicados:',lista2)