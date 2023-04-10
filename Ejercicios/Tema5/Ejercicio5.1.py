# Queremos resolver u'' = u.
# Tenemos los siguiente datos: u'(1) = 1.17520, u'(3) = 10.0178
# La ecuación es del tipo: u'' = p(x)*u' + q(x)*u + r(x) con x en [a,b]
# Vamos a tener en cuenta estos polinomios para resolver la ecuación diferencial
# Por el método de las diferencias finitas llegando a una matriz tridiagonal.

from math import *
import numpy as np
import matplotlib.pyplot as plt

def errores(exacto: float, obtenido: float):
    # Cálculo de los errores absoluto y relativo
    Ea = fabs(exacto - obtenido)
    Er = fabs(Ea/exacto)*100
    errors = (Ea, Er)
    return errors

def uReal(x: float) -> float:
    '''Devuelve el valor real de la función en cada punto
    para comparar con los resultados numéricos al final.'''
    
    if x<1 or x>3:
        print("Valor x fuera de las condiciones de contorno.")
    else:
        return cosh(x)

# Polinomios p(x), q(x) y r(x) de nuestra ecuación diferencial: u'' = p(x)*u' + q(x)*u + r(x) -> p(x) = 0 = r(x), q(x) = 1
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
    brows = np.shape(b)[0]
    bcols = np.shape(b)[1]
    z = np.zeros((brows, bcols), float)
    z[0,0] = b[0,0]
    for i in range(brows):
        z[i,0] = b[i,0] - L[i,i-1]*z[i-1,0]
        
    # Calculamos la matriz x (Ux = z)
    x = np.zeros((brows, bcols), float)
    x[brows-1,0] = z[brows-1,0]/U[brows-1,brows-1]
    for i in range(brows-2,-1,-1):
        x[i,0] = (z[i,0] - d[i,0]*x[i+1,0]) / U[i,i]
        
    # Retornamos el valor de la matriz solución 
    return x

def EDO_diferencias_finitas(n: int, xmin: float, xmax: float, u0: float, un: float) -> np.array:
    '''Crea el sistema lineal tridiagonal a partir de una ecuación 
    diferencial, llama a una función que lo resuelve y retorna el 
    resultado de la ecuación diferencial en cada punto.'''

    # Como las condiciones vienen en función de u' tenemos dos incógnitas más. 
    # El tamaño de la matriz debe salir de n+1 en vez de n-1.
    
    # Calculamos h en función del número de intervalos y de los extremos.
    h = (xmax - xmin)/n
    x = xmin

    # Creamos las matrices con los valores de p(x), q(x) y r(x) para los distintos valores de x.
    p = np.zeros((n+2,1), float)
    q = np.zeros((n+2,1), float)
    r = np.zeros((n+2,1), float)
    for i in range(n+2):
        p[i,0] = pol_p(x)
        q[i,0] = pol_q(x)
        r[i,0] = pol_r(x)
        x = x + h
    
    # Creamos las matrices A y b del sistema Au = b
    A = np.zeros((n+1,n+1), float)
    b = np.zeros((n+1,1), float)

    # Creamos A
    for i in range(n+1):
        for j in range(n+1):
            # Ecuaciones 0 y n. Diferentes por las condiciones de frontera en función de u'
            if i == 0 and j == 0:
                A[i,j] = 2 + (h*h*q[i,0])
            elif i == 0 and j == 1:
                A[i,j] = (h/2 * p[i,0]) - 2
            elif i == n and j == n:
                A[i,j] = 2 + (h*h*q[i+1,0])
            elif i == n and j == n-1:
                A[i,j] = -(h/2 * p[i+1,0] + 2)

            # Ecuaciones intermedias.
            elif i==j:
                A[i,j] = 2 + (h*h*q[i+1,0])
            elif i-j==1:
                A[i,j] = -(h/2 * p[i+1,0] + 1)
            elif i-j==-1:
                A[i,j] = (h/2 * p[i+1,0]) - 1
            else:
                A[i,j] = 0

    # Creamos b
    for i in range(n+1):
        if i == 0:
            b[i,0] = - 2*h*u0 - (h*h*r[i,0])
        elif i==n:
            b[i,0] = 2*h*un - (h*h*r[i,0])
        else:
            b[i,0] = -(h*h*r[i+1,0])
    
    # Matriz solución:
    X = sol_tridiagonales(A, b)
    return X

def main():
    intervalos = [5, 10, 20]
    xmin = 1
    xmax = 3
    u0 = 1.17520
    un = 10.0178
    
    for n in intervalos:
        # Cálculo de la solución numérica.
        Solucion = EDO_diferencias_finitas(n, xmin, xmax, u0, un)

        # Cálculo de la solución analítica.
        X = np.zeros(n+1)
        X[0] = uReal(xmin)
        X[n] = uReal(xmax)
        h = (xmax - xmin)/n
        x = xmin + h
        for i in range(1, n):
            X[i] = uReal(x)
            x = x + h

        # Imprimimos las soluciones por pantalla
        print(f"---------- Solución para {n} intervalos: ----------")
        print("x\tu Numérica\tu Analítica\tError absoluto.")
        x = xmin
        for i in range(n+1):
            print(f"{float(x):.2}\t{Solucion[i][0]:.7}\t{X[i]:.7}\t{errores(X[i], Solucion[i][0])[0]:.7}")
            x = x + h
        print()

        # Gráfica con las soluciones
        x = np.linspace(1,3,n+1)
        plt.plot(x, Solucion[:,0], label='Solución numérica')
        plt.plot(x, X, label='Solución analítica')
        plt.xlabel("Valor de x")
        plt.ylabel("Valor de u")
        plt.xticks(list(x))
        plt.legend(shadow=True)
        plt.grid()
        plt.title(f"Soluciones para n={n}")
        plt.show()

if __name__ == "__main__":
    main()