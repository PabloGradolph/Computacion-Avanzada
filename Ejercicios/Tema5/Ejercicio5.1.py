# Queremos resolver u'' = u.
# Tenemos los siguiente datos: u'(1) = 1.17520, u'(3) = 10.0178
# La ecuación es del tipo: u'' = p(x)*u' + q(x)*u + r(x) con x en [a,b]
# Vamos a tener en cuenta estos polinomios para resolver la ecuación diferencial
# Por el método de las diferencias finitas llegando a una matriz tridiagonal.

from math import *
import numpy as np
import matplotlib.pyplot as plt

def uReal(x: float) -> float:
    '''Devuelve el valor real de la función en cada punto
    para comparar con los resultados numéricos al final.'''
    
    if x<1 or x>3:
        print("Valor x fuera de las condiciones de contorno.")
    elif x == 1 or x == 3:
        return sinh(x)
    else:
        return cosh(x)

# Polinomios p(x), q(x) y r(x) de nuestra ecuación diferencial:
def pol_p(x: float) -> float:
    p = 0
    return p

def pol_q(x: float) -> float:
    q = 1
    return q

def pol_r(x: float) -> float:
    r = 0
    return r
# --------------------------------------------

def sol_tridiagonales(A: np.array, b: np.array) -> np.array:
    '''Resuelve sistemas lineales en los que la matriz
    A pasada como argumento es una matriz tridiagonal.'''

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(A)[0]
    col = np.shape(A)[1]

    # Vamos a comprobar que la matriz A sea tridiagonal para poder continuar.
    is_tridiagonal = True

    # Todos los elementos de fuera de las 3 diagonales principales son 0.
    for i in range(row):
        if is_tridiagonal == False:
            break
        for j in range(col):
            if i!=j and i-j!=1 and i-j!=-1:
                if A[i,j]!=0:
                    is_tridiagonal = False
                    break
    
    # Solo continuamos si la matriz A tiene todos los elementos de fuera de la diagonal son 0.
    if is_tridiagonal == False:
        print("La matriz A pasada como argumento no es tridiagonal.")
        return A
    else:
        # Comprobamos la diagonal principal
        suma = 0
        for i in range(row):
            suma = suma + fabs(A[i,i])
        if suma == 0:
            is_tridiagonal = False
        
        # Comprobamos la diagonal de abajo
        suma = 0
        for i in range(row-1):
            suma = suma + fabs(A[i,i+1])
        if suma == 0:
            is_tridiagonal = False
        
        # Comprobamos la diagonal de arriba
        suma = 0
        for i in range(row):
            suma = suma + fabs(A[i,i-1])
        if suma == 0:
            is_tridiagonal = False
    
    if is_tridiagonal == False:
        print("La matriz A pasada como argumento no es tridiagonal.")
        return A
    else:
        # Si llegamos a este punto sabemos que la matriz A es tridiagonal.
        # Ahora comprobamos que el número de columnas de A sea igual al número de filas de b.
        brows = np.shape(b)[0]
        iguales = False
        if col == brows:
            iguales = True
    
    if iguales == False:
        print("Las filas de A no coinciden con las columnas de b.")
        return A
    else:
        # Ya tenemos todo para resolver el sistema.
        # Definimos los 3 vectores de las 3 diagonales.
        a = np.zeros((row,1),float)
        c = np.zeros((row-1, 1), float)
        d = np.zeros((row-1, 1), float)

        # Les damos los valores
        for i in range(row):
            for j in range(col):
                if i==j:
                    a[i,0] = A[i,j] # Diagonal principal
                elif i-j==1:
                    c[i-1,0] = A[i,j] # Diagonal superior
                elif i-j==-1:
                    d[i,0] = A[i,j] # Diagonal inferior
        
        # Definimos las matrices L y U
        L = np.zeros((row,col), float)
        U = np.zeros((row,col), float)

        # Les asignamos sus valores
        U[0,0] = a[0,0]
        L[0,0] = 1
        for i in range(row):
            for j in range(col):
                if i==j and i!=0:
                    L[i,j] = 1
                    U[i,j] = a[i,0] - L[i,i-1]*d[i-1,0]
                elif i-j == -1:
                    U[i,j] = d[i,0]
                elif i-j == 1:
                    L[i,j] = c[i-1,0]/U[i-1,i-1]
        
        # Calculamos la matriz z (Lz = b)
        bcols = np.shape(b)[1]
        z = np.zeros((brows, bcols), float)
        z[0,0] = b[0,0]
        for i in range(brows):
            z[i,0] = b[i,0] - L[i,i-1]*z[i-1,0]
        
        # Calculamos la matriz x (Ux = z)
        x = np.zeros((brows, bcols), float)
        print(A)
        print(b)
        x[brows-1,0] = z[brows-1,0]/U[brows-1,brows-1]
        for i in range(brows-2,-1,-1):
            x[i,0] = (z[i,0] - d[i,0]*x[i+1,0]) / U[i,i]
        
        # Retornamos el valor de la matriz solución 
        return x

def EDO_diferencias_finitas(n: int, xmin: float, xmax: float, u0: float, un: float) -> np.array:
    '''Crea el sistema lineal tridiagonal a partir de una ecuación 
    diferencial, llama a una función que lo resuelve y retorna el 
    resultado de la ecuación diferencial en cada punto.'''

    # Calculamos h en función del número de intervalos y de los extremos.
    h = (xmax - xmin)/n
    x = xmin

    # Creamos las matrices con los valores de p(x), q(x) y r(x) para los distintos valores de x.
    p = np.zeros((n,1), float)
    q = np.zeros((n,1), float)
    r = np.zeros((n,1), float)
    for i in range(n):
        p[i,0] = pol_p(x)
        q[i,0] = pol_q(x)
        r[i,0] = pol_r(x)
        x = x + h
    
    # Creamos las matrices A y b del sistema Au = b
    A = np.zeros((n-1,n-1), float)
    b = np.zeros((n-1,1), float)
    for i in range(n-1):
        for j in range(n-1):
            if i==j:
                A[i,j] = 2 + (h*h*q[i+1,0])
            elif i-j==1:
                A[i,j] = -(h/2 * p[i+1,0] + 1)
            elif i-j==-1:
                A[i,j] = (h/2 * p[i+1,0]) - 1
            else:
                A[i,j] = 0

    for i in range(n-1):
        if i == 0:
            b[i,0] = -(h*h*r[i+1,0]) + (h/2 * p[i+1,0] + 1)*u0
        elif i==n-2:
            b[i,0] = -(h*h*r[i+1,0]) - (h/2 * p[i+1,0] - 1)*un
        else:
            b[i,0] = -(h*h*r[i+1,0])
    
    # Matriz solución:
    X = np.zeros((n,1), float)
    X = sol_tridiagonales(A, b)
    return X

def main():
    n = 5
    xmin = 1
    xmax = 3
    u0 = 1.17520
    un = 10.0178
    # Te falta cambiar cuando las condiciones están en función de u'
    Solucion = EDO_diferencias_finitas(n, xmin, xmax, u0, un)
    print(Solucion)

if __name__ == "__main__":
    main()
            



                