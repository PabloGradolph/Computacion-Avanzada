# Búsqueda de ceros de una función por el método de Newton y de la bisección

#------------------------------------
# IMPORTACIONES
#------------------------------------

from math import exp, fabs

#------------------------------------
# FUNCIONES
#------------------------------------

# Devuelve la función altura
def funcion(t: float) -> float:
    # Datos iniciales
    g, s0, m, k = 9.8, 91.44, 113.4, 45.36
    # Retornamos el valor de la función
    return s0 - (m*g/k)*t + (m*m*g)/(k*k)*(1-exp(-k*t/m))

# Devuelve la derivada de la función anterior
def derivada(t: float) -> float:
    # Datos iniciales
    g, m, k = 9.8, 113.4, 45.36
    # Retornamos el valor de la derivada
    return - (m*g/k) - ((m*m*g)/(k*k)*exp(-k*t/m)*(-k/m))

# Cálculo de ceros de la función por el método de la bisección
def biseccion(t1: float, t2: float, tol: float) -> float:
    # Definimos el nuevo punto
    t3 = (t1+t2)/2 

    # Número de iteraciones
    n = 1
    while fabs(funcion(t3)) > tol:
        if funcion(t3)*funcion(t1) < 0:
            t2 = t3
        else:
            t1 = t3
        t3 = (t1 + t2)/2
        n += 1

    # Retornamos valor del tiempo y el número de iteraciones.
    return t3, n

# Cálculo de ceros de la función por el método de Newton.
def newton(t1: float, tol: float) -> float:
    t = t1 - funcion(t1)/derivada(t1)
    f = funcion(t)

    # Número de iteraciones
    n = 1
    while fabs(f) > tol:
        t = t - funcion(t)/derivada(t)
        f = funcion(t)
        n += 1
    
    # Retornamos valor del tiempo y el número de iteraciones.
    return t, n

def main():
    # Tiempo e iteraciones por bisección
    t_b, nb = biseccion(0, 10 , 0.001)
    print("MÉTODO BISECCIÓN:")
    print(f"Tiempo en llegar al suelo: {t_b}.")
    print(f"Número de iteraciones: {nb}")
    print()

    # Tiempo e iteraciones por newton
    t_n, nn = newton(1, 0.001)
    print("MÉTODO NEWTON:")
    print(f"Tiempo en llegar al suelo: {t_n}.")
    print(f"Número de iteraciones: {nn}")


#------------------------------------
# EJECUTAMOS
#------------------------------------

if __name__ == "__main__":
    main()