#------------------------------------
# Clase del 23 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Método de Euler: Ecuaciones diferenciales con condiciones iniciales.
#------------------------------------

# Función para generar nombres de ficheros.
def file_name(xmin: float, xmax: float, h: float, metodo: str) -> str:
    fname = f"{metodo}_tmin"
    fname += f"{xmin:.2f}_tau"
    fname += f"{xmax:.1f}_h"
    fname += f"{h:.2f}_"
    fname += ".txt"
    return fname

def y_prima(x: float, y: float) -> float:
    pass

def sol_exacta(x: float, y: float) -> float:
    pass

# Función para la resolución de una ecuación diferencial por el método de Euler.
def euler(h: float, xmin: float, y0: float, tau: float):
    # Inicializamos x e y
    x, y = xmin, y0

    fname = file_name(xmin,tau,h,"Euler")
    with open(fname, "w", encoding="utf-8") as f:
        f.write(f"#Datos para h = {h}\n")
        f.write("x\t\t\ty\t\t\tSolución Exacta\n")
        f.write(f"{x:.3f}\t{y:.5f}\t{sol_exacta(x):.5f}\n")
        for _ in range(100):
            x = x + h
            y = y + (h*y_prima(y, tau))
            f.write(f"{x:.3f}\t{y:.5f}\t{sol_exacta(x):.5f}\n")
    print(f"Fichero de salida: {fname}")