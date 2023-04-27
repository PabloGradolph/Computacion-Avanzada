import numpy as np
import matplotlib.pyplot as plt
from math import *

# 6000 y pico iteraciones.
# ----------------------------------------------------------
# u_ab[:,0] = H/k * (u[:, 1] - ur)
# u[1:-1, in_columnas] = 0.25*(2*u[1:-1, -2] + u[:-2, in_columnas] + u[2:, in_columnas] - (h*h*Q/(k*d) - 2*h*u_arr))
# u[1:-1, 0] = 0.25*(2*u[1:-1, 1] + u[:-2, 0] + u[2:, 0] - (h*h*Q/(k*d) + 2*h*u_ab[1:-1,0]))
# u[0, :] = u_izq
# u[in_filas, :] = u_der
# ----------------------------------------------------------

# Definir las dimensiones de la placa
Lx = 9 # ancho (cm)
Ly = 5 # alto (cm)
d = 0.5 # espesor (cm)

# Definir los intervalos de la malla
nx = 50 # número de intervalos en x
ny = 90 # número de intervalos en y
dx = Lx / (nx - 1)
dy = Ly / (ny - 1)

# Definir los valores de las constantes
k = 0.16 # conductividad térmica (cal / (s cm ºC))
Q = 0.6 # ritmo de pérdida de calor (cal / (s cm^3))
H = 0.073 # coeficiente de transferencia de calor (cal / (s cm^2))
ur = 25 # temperatura ambiente (ºC)

# Inicializar las temperaturas en la placa
T = np.zeros((ny, nx))

# Definir las condiciones de frontera
T[:, 0] = 20 # borde izquierdo
T[:, -1] = 20 # borde derecho
T[0, :] = -15 * dy / d + T[1, :] # borde superior
T[-1, :] = H * k * (T[-2, :] - ur) / (k * dy + H * d) + ur # borde inferior

# Definir el criterio de convergencia
epsilon = 1e-2

# Iterar hasta que el cambio en la norma sea menor que epsilon
norm = 1
old_norm = 2
iter = 0
while fabs(norm - old_norm) > epsilon:
    T_old = T.copy()
    old_norm = np.linalg.norm(T_old)
    
    # Iterar sobre los puntos internos de la placa
    for j in range(1, ny-1):
        for i in range(1, nx-1):
            T[j, i] = 0.25 * (T[j, i-1] + T[j, i+1] + T[j-1, i] + T[j+1, i] + Q * dx**2 / (k * d))
    
    # Aplicar las condiciones de frontera
    T[0, :] = -15 * dy / d + T[1, :]
    T[-1, :] = H * k * (T[-2, :] - ur) / (k * dy + H * d) + ur
    T[:, 0] = 20
    T[:, -1] = 20
    
    norm = np.linalg.norm(T) 
    iter += 1

# Imprimir el número de iteraciones necesarias para alcanzar la convergencia
print(f"Convergencia alcanzada en {iter} iteraciones")

# Imprimir los valores de temperatura en los puntos solicitados
x_cen = nx // 2
y_cen = ny // 2
T_cen = T[y_cen, x_cen]
T_sup_cen = T[0, x_cen]
T_inf_cen = T[-1, x_cen]

fig, ax = plt.subplots(1,1)
im = ax.imshow(T, cmap='gray', origin='lower', extent=[0,9,0,5])
plt.colorbar(im, ax = ax)
ax.set_title("Temperaturas.")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_aspect("equal", "box")
plt.show()


print(f"Temperatura en el centro de la placa: {T_cen:.2f} ºC")
print(f"Temperatura en el centro superior: {T_sup_cen:.2f} ºC")
print(f"Temperatura en el centro inferior: {T_inf_cen:.2f} ºC")
np.savetxt("matriz2.txt", T, fmt="%5.2f")