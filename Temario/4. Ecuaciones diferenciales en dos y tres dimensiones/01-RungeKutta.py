# Recordatorio de métodos de Runge-Kutta

def funcion():
    pass

def RK4(h: float, xmin: float, xmax: float, y0) -> float:
    # Definimos el número de pasos
    npasos = int((xmax - xmin)/h)

    x, y = xmin, y0
    with open("file_name.txt", "w", encoding="utf-8") as f:
        f.write(f"#Datos para h = {h}. Método RK4\n")
        f.write("x\t\t\tv\n")
        f.write(f"{x:.3f}\t{y:.5f}\n")
        for _ in range(npasos):
            x = x + h
            k1 = funcion(y)
            k2 = funcion(y + 0.5*k1*h)
            k3 = funcion(y + 0.5*k2*h)
            k4 = funcion(y + k3*h)
            y = y + (h/6)*(k1 + 2*k2 + 2*k3 + k4)
            f.write(f"{x:.3f}\t{y:.5f}\n")

    print("Fichero de salida: file_name.txt")

def main():
    # Datos iniciales
    xmin, xmax = 0, 200
    y0 = 4
    hs = [0.5, 0.2, 0.05] # Probamos para distintos valores de dt
    for h in hs:
        RK4(h, xmin, xmax, y0)

main()