# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
# Escribir un programa que utilice una función para imprimir en pantalla los 
# elementos impares de un array de 10 elementos.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - 
import numpy as np

def impares_array(array: np.array):
    print()
    print("ELEMENTOS IMPARES INTRODUCIDOS:")
    for i in array:
        if i%2 != 0:
            print(i)

def main():
    lista = []
    for i in range(1,11):
        number = int(input(f"Inserte el elemento {i} --> "))
        lista.append(number)
    array = np.array(lista, int)
    impares_array(array)

if __name__ == "__main__":
    main()

    
