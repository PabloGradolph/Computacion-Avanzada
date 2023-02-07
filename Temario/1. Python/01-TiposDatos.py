# - - - - - - - - - - - - - - - - - - - - - - - - 
# Clase 31 de enero de 2023.
# Autor: Pablo Gradolph Oliva
# Contenido: Tipos de datos en Python
# - - - - - - - - - - - - - - - - - - - - - - - - 

# Esto es un comentario

print('Hola \
mundo')

#------------------------------------

a=5
print('El valor de a es',a)
print('El tipo de a es',type(a))
a=a/3
print('El nuevo valor de a es',a)
print('El nuevo tipo de a es',type(a))
a=3+5j
print('El nuevo valor de a es',a)
print('El nuevo tipo de a es',type(a))
a="Hola"
print('El nuevo valor de a es',a)
print('El nuevo tipo de a es',type(a))
a=a/3

#------------------------------------

a=1.1
b=2.2
c=a+b
print(c)

#------------------------------------

a=8/3
print('a =',a, ' Dato original')
print()
b=int(a)
print('b =',b, ' Truncado con int()')
print()
c=round(a)
print('c =',c, ' Redondeado con round()')
print()
d=float(c)
print('d =',d, ' Entero transformado en real')
print()
e=complex(c)
print('e =',e, ' Entero transformado en complejo')
print()
f=str(e)
print('f =',f, ' Complejo transformado en texto')
print()
print('Al intentar dividir un texto por un número, dará un error:')
print()
print(f/2)

#------------------------------------

a="Al olmo viejo, hendido por el rayo\
y en su mitad podrido,\
con las lluvias de abril y el sol de mayo\
algunas hojas verdes le han salido."
print('Sin saltos de línea:')
print()
print(a)
print()

a="""Al olmo viejo, hendido por el rayo
y en su mitad podrido,
con las lluvias de abril y el sol de mayo
algunas hojas verdes le han salido."""
print('Con saltos de línea:')
print()
print(a)