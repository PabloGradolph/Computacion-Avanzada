import numpy as np
import matplotlib.pyplot as plt

def temperaturas_placa(x_min: float, x_max: float, r: float) -> np.array:
    global delta_t

    # Constantes
    k = 0.13
    c = 0.11
    ro = 7.8
    delta_x = 0.25
    delta_t = r*c*ro*(delta_x**2)/k
    pasos = int(3/delta_t)
    puntos = int((x_max-x_min)/delta_x)

    # Matriz de temperatura.
    u = np.zeros((pasos+1, puntos+1), float)

    # Inicializamos la x y el tiempo.
    x = 0
    t = 0
    
    # Condiciones iniciales.
    for i in range(len(u[0, :])): 
        if x<=1:
            u[t, i] = 100*x
        else:
            u[t, i] = 200 - 100*x
        x+=delta_x

    # Recorremos todos los puntos calculando los valores.
    while t<pasos:
        for i in range(len(u[0, :])-1):
            if i == 0:
                u[t+1, i] = 0
            elif  i == 8:
                u[t+1, i] = 0
            else:
                u[t+1,i] = r * (u[t,i+1] + u[t,i-1]) + (1-2*r)*u[t,i]
        t+=1

    return u, pasos, puntos

def main():
    # Constantes.
    x_min = 0
    x_max = 2
    erres = [0.4, 0.5, 0.6]

    for r in erres: # Para los distintos valores de r.
        # Cálculo de las temperaturas.
        u, pasos, puntos = temperaturas_placa(x_min, x_max, r)
        
        # Primera representación: Para un cierto valor x (posición en la barra), vemos la evolución en el tiempo.
        # Se pueden elegir más puntos para representar.
        t = np.linspace(0, pasos, pasos+1)
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