# Integración numérica

# Solución analítica = 0.1606028

#------------------------------------
# IMPORTACIONES
#------------------------------------

from math import exp, fabs

#------------------------------------
# FUNCIONES
#------------------------------------

# Cálculo del error absoluto
def error(exacto: float, obtenido: float):
    Ea = fabs(exacto - obtenido)
    return Ea

# Devuelve el valor de la función que vamos a integrar
def funcion(x: float) -> float:
    f = (x*x)*exp(-x)
    return f

# Función que calcula la integral por la regla trapezoidal.
def trapecio(n:int, a:float, b:float) -> float:
    # Calculamos h
    h = (b - a)/n

    # Calculamos el sumatorio de los f(a + hi) que tenemos que calcular para éste método.
    sumatorio, x = 0, a
    for i in range(1,n):
        x += h
        sumatorio += funcion(x)
    
    # Integral
    I = (h/2)*(funcion(a) + 2*sumatorio + funcion(b))
    return I

# Función que calcula la integral por la regla de Simpson 1/3 (n es par).
def simpson1_3(n:int, a:float, b:float) -> float:
    # Control de errores en la entrada de n
    if n%2 != 0:
        print(f"El valor n introducido es impar: n = {n}")
        print("No se puede seguir el método de Simpson 1/3")
        return
    
    # Calculamos h
    h = (b - a)/n

    # Calculamos f(x0) + 4f(x1) + 2f(x2) + ... + 4f(xn-1) + f(xn).
    sumatorio, x = 0, a
    for i in range(n+1):
        if i == 0:
            sumatorio += funcion(x)
        elif i == n:
            sumatorio += funcion(x)
        elif i%2 == 0:
            sumatorio += 2*funcion(x)
        else:
            sumatorio += 4*funcion(x)
        x += h
    
    # Integral
    I = (h/3) * sumatorio
    return I

# Función que calcula la integral por la regla de Simpson 1/3 (n múltiplo de 3).
def simpson3_8(n:int, a:float, b:float) -> float:
    # Control de errores en la entrada de n
    if n%3 != 0:
        print(f"El valor n introducido no es múltiplo de 3: n = {n}")
        print("No se puede seguir el método de Simpson 3/8")
        return
    
    # Calculamos h
    h = (b - a)/n

    # Calculamos f(x0) + 3f(x1) + 3f(x2) + 2f(x3) + 3f(x4) + 3f(x5) + 2f(x6) + ... + f(xn).
    sumatorio, x = 0, a
    for i in range(n+1):
        if i == 0:
            sumatorio += funcion(x)
        elif i == n:
            sumatorio += funcion(x)
        elif i%3 == 0:
            sumatorio += 2*funcion(x)
        else:
            sumatorio += 3*funcion(x)
        x += h
    
    # Integral
    I = (3*h/8) * sumatorio
    return I

# Función principal del programa
def main():
    a, b = 0, 1
    Sol = 0.160602794
    # Utilizo el encoding para poder leer acentos y ñ
    with open("Sol_Trapecio.txt", "w", encoding="utf-8") as f:
        f.write("# MÉTODO TRAPECIO\n")
        f.write("n\t Integral\t    Error absoluto\n")
        for i in range(1,301):
            f.write(f"{i}    {trapecio(i, a, b):.8f}    {error(Sol,trapecio(i, a, b)):.8f}\n")

    with open("Sol_Simpson1_3.txt", "w", encoding="utf-8") as f:
        f.write("# MÉTODO SIMPSON 1/3\n")
        f.write("n\t Integral\t    Error absoluto\n")
        for i in range(2, 31, 2):
            f.write(f"{i}    {simpson1_3(i, a, b):.8f}    {error(Sol,simpson1_3(i, a, b)):.8f}\n")
    
    with open("Sol_Simpson3_8.txt", "w", encoding="utf-8") as f:
        f.write("# MÉTODO SIMPSON 3/8\n")
        f.write("n\t Integral\t    Error absoluto\n")
        for i in range(3, 31, 3):
            f.write(f"{i}    {simpson3_8(i, a, b):.8f}    {error(Sol,simpson3_8(i, a, b)):.8f}\n")
    
#------------------------------------
# EJECUTAMOS 
#------------------------------------

if __name__ == "__main__":
    main()