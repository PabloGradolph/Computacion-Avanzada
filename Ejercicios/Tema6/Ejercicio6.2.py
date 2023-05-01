import numpy as np
import matplotlib.pyplot as plt

def temperaturas_placa_Crank_Nicolson(x_min: float, x_max: float, r: float) -> np.array:
    global pasos, puntos, delta_t

    # Constantes
    k = 0.13
    c = 0.11
    ro = 7.8
    delta_x = 0.25
    delta_t = r*c*ro*(delta_x**2)/k
    pasos = int(3/delta_t)
    puntos = int((x_max-x_min)/delta_x)

    # Matriz de temperatura con condiciones iniciales.
    u = np.zeros((puntos+1, 1), float)
    for i in range(len(u)):
        if i*delta_x <= 1:
            u[i] = 100*i*delta_x
        else:
            u[i] = 200 - 100*i*delta_x
    u0 = u

    # Define matrix A (tridiagonal)
    A = np.zeros((puntos+1, puntos+1), float)
    for i in range(1, puntos):
        A[i, i-1] = -0.5*r
        A[i, i] = 1 + r
        A[i, i+1] = -0.5*r
    A[0, 0] = 1
    A[puntos, puntos] = 1

    # Inicializamos el tiempo.
    t = 0
    temperaturas = [(t, u0)]
    
    while t < pasos:
        b = np.zeros((puntos+1, 1), float)
        for i in range(1, puntos):
            b[i] = u[i] + 0.5*r*(u[i+1] - 2*u[i] + u[i-1])
        
        u = np.linalg.solve(A, b)
        t+=1
        temperaturas.append((t, u))

    return temperaturas

def main():
    # Constantes.
    x_min = 0
    x_max = 2
    erres = [0.4, 0.5, 0.6]

    for r in erres:
        # Calculamos las temperaturas.
        temperaturas = temperaturas_placa_Crank_Nicolson(x_min, x_max, r)

        # Separamos los pasos de tiempo y las temperaturas.
        t = []
        u = np.zeros((pasos+1, puntos+1), float)
        i = 0
        for temp in temperaturas:
            valores_u = temp[1]
            valores_u = np.transpose(valores_u)
            t.append(temp[0])
            u[i,:] = valores_u[0,:]
            i += 1

        # Convertimos en arrays de numpy.
        t = np.array(t)
        u = np.array(u)
        # np.savetxt("matriz.txt", u, fmt="%5.2f")

        # Primera representación: Para un cierto valor x (posición en la barra), vemos la evolución en el tiempo.
        # Se pueden elegir más puntos para representar.
        fig1 = plt.figure("Temperaturas")
        ax = fig1.add_subplot(1,1,1)
        ax.plot(t, u[:, 2], "o", linestyle="solid", markersize=3, color="blue")
        ax.plot(t, u[:, 4], "o", linestyle="solid", markersize=3, color="k")
        ax.set_ylabel("Temperatura, ºC")
        ax.set_xlabel("Pasos de tiempo")
        ax.set_title(f"Temperaturas en el tiempo para r={r}")
        ax.legend(("x=0.5","x=1"), shadow=True)
        plt.show()

        # Segunda representación: Para un cierto valor t (tiempo), vemos la temperatura en los distintos puntos de la barra.
        # Se pueden elegir más puntos para representar.
        x = np.linspace(0, x_max, puntos+1)
        fig2 = plt.figure("Temperaturas")
        ax = fig2.add_subplot(1,1,1)
        ax.plot(x, u[2, :], "o", linestyle="solid", markersize=3, color="blue")
        ax.plot(x, u[4, :], "o", linestyle="solid", markersize=3, color="k")
        ax.plot(x, u[8, :], "o", linestyle="solid", markersize=3, color="green")
        ax.plot(x, u[12, :], "o", linestyle="solid", markersize=3, color="m")
        ax.plot(x, u[0, :], color = 'red')
        ax.set_ylabel("Temperatura, ºC")
        ax.set_xlabel("Espesor x (cm)")
        ax.set_title(f"Temperaturas en para tiempos dados con r={r}")
        ax.legend((f"t={delta_t*2}",f"t={delta_t*4}",f"t={delta_t*8}",f"t={delta_t*13}", "t=0"), shadow=True)
        plt.show()

if __name__ == "__main__":
    main()