import numpy as np
from math import *
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

g = 9.8

# Transforma grados a radianes
def radianes(angulo: float) -> float:
    rad = angulo * pi/180
    return rad

# Obtener el segundo valor de la tupla dada por (angulo, alcance)
def obtener_valor(tupla: tuple):
    return tupla[1]

# Devuelve la matriz Y' de cada iteración.
def sistema_Yprima(t: float, Y: np.array, omega: float) -> np.array:

    # Valores necesarios para las ecuaciones.
    r = 0.11 # Radio en metros
    v = sqrt(Y[3,0]*Y[3,0] + Y[4,0]*Y[4,0] + Y[5,0]*Y[5,0])
    B2_m = 0.01083
    S0_m = 0.003

    # Medimos el tamaño de la matriz de entrada
    row = np.shape(Y)[0]
    col = np.shape(Y)[1]

    # Creamos la matriz que vamos a retornar
    Yprima = np.zeros((row,col),float)
    Yprima[0,0] = Y[3,0] # (dx/dt) = vx 'alcance'
    Yprima[1,0] = Y[4,0] # (dy/dt) = vy 'altura'
    Yprima[2,0] = Y[5,0] # (dz/dt) = vz 'rotación'
    Yprima[3,0] = - B2_m * v * Y[3,0] # (dvx/dt) = ax
    Yprima[4,0] = - g # (dvy/dt) = ay
    Yprima[5,0] = S0_m * omega * Y[3,0] # (dvz/dt) = az

    return Yprima

def RK4_sistemas(dt: float, tmin: float, Y0: np.array, omega: float) -> list:

    t = tmin

    # Inicializamos Y y las matrices K
    Y = Y0
    k1 = sistema_Yprima(t, Y, omega)
    k2 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k1, omega)
    k3 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k2, omega)
    k4 = sistema_Yprima(t + dt, Y + dt*k3, omega)
    
    # Vectores donde iremos guardando los resultados (Además de en los ficheros)
    x = [Y[0,0]]
    y = [Y[1,0]]
    z = [Y[2,0]]

    while True:
        Y = Y + (dt/6 * (k1 + 2*k2 + 2*k3 + k4))
        t = t + dt
        x.append(Y[0,0])
        y.append(Y[1,0])
        z.append(Y[2,0])

        k1 = sistema_Yprima(t, Y, omega)
        k2 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k1, omega)
        k3 = sistema_Yprima(t + 0.5*dt, Y + 0.5*dt*k2, omega)
        k4 = sistema_Yprima(t + dt, Y + dt*k3, omega)

        if Y[1,0] < 0: # Si el balón toca el suelo no seguimos iterando
            break
        if Y[0,0] >= 9 and Y[1,0] <= 1.80:
            break
        if Y[0,0] > 26: # Si pasamos la línea de fondo no seguimos iterando.
            break 

    return x, y, z

def main():
    # Datos iniciales.
    radio = 0.11
    dt = 0.005 # Se recomienda poner este valor en 0.001 para alcanzar una mayor precisión, pero invertiríamos más tiempo para el cálculo.
    tmin = 0.0
    x0, y0, z0 = 0, 0, 0
    v0 = 24
    omega = 1.5 # Valor para hacer las pruebas del ángulo. No influye en la altura.

    angulos = [] # Guardaremos ángulos para los que el balón entra en la portería.

    # Primera comprobación de los ángulos.
    for angulo in range(1, 51):
        # Condición inicial.
        Y0 = np.array([[x0],[y0],[z0], [v0*cos(radianes(angulo))],[v0*sin(radianes(angulo))],[0]], float) 

        # Primero nos quedamos con los ángulos potenciales de llegar a la portería.
        x, y, z = RK4_sistemas(dt, tmin, Y0, omega)
        if y[-1] > 0:
            angulos.append(angulo)

    # A partir del ángulo que no bota en el suelo comprobamos si supera la barrera.
    angulos_2 = []
    for angulo in angulos:
        # Condición inicial.
        Y0 = np.array([[x0],[y0],[z0], [v0*cos(radianes(angulo))],[v0*sin(radianes(angulo))],[0]], float)
        
        x, y, z = RK4_sistemas(dt, tmin, Y0, omega)
        yfinal = (y[-2] + ((x[-1] - 26)/(26 - x[-2]))*y[-1])/(((x[-1] - 26)/(26 - x[-2]))+1) # Interpolación.
        if x[-1] >= 9 and y[-1] > 1.8:
            angulos_2.append(angulo)

    # Con todos los ángulos que superan la barrera, nos quedaremos con los que entran en la portería.
    angulos = []
    for angulo in angulos_2:
        # Condición inicial.
        Y0 = np.array([[x0],[y0],[z0], [v0*cos(radianes(angulo))],[v0*sin(radianes(angulo))],[0]], float)
        
        x, y, z = RK4_sistemas(dt, tmin, Y0, omega)
        yfinal = (y[-2] + ((x[-1] - 26)/(26 - x[-2]))*y[-1])/(((x[-1] - 26)/(26 - x[-2]))+1) # Interpolación.

        #
        # Cómo se haría para el resto:
        # -> zfinal = (z[-2] + ((x[-1] - 26)/(26 - x[-2]))*z[-1])/(((x[-1] - 26)/(26 - x[-2]))+1)
        # -> xfinal = 26
        # -> x[-1], y[-1], z[-1] = xfinal, yfinal, zfinal
        #

        if yfinal <= 2.5: 
            angulos.append(angulo)
    
    # El ángulo se encuentra entre 20 y 21 grados. Vamos a calcular exactamente ahora cuál es.
    angulo = angulos[0]
    while angulo < 21:

        Y0 = np.array([[x0],[y0],[z0], [v0*cos(radianes(angulo))],[v0*sin(radianes(angulo))],[0]], float) # Condición inicial.

        x, y, z = RK4_sistemas(dt, tmin, Y0, omega)
        yfinal = (y[-2] + ((x[-1] - 26)/(26 - x[-2]))*y[-1])/(((x[-1] - 26)/(26 - x[-2]))+1) # Interpolación.
        if yfinal > 2.5 - radio: # Tenemos en cuenta el radio: 2.50 - radio
            angulos = [angulo]
            break
        angulo = angulo + 0.01 # Aproximación con 2 decimales.
    
    # Ya tenemos el ángulo de lanzamiento: angulos[0]
    # Ahora veamos que velocidad angular es necesaria para que el balón entre por la escuadra.
    desviacion = 7.32/2 - radio # La desviación hacia la izquierda que queremos alcanzar es el ancho de la portería entre 2 - el radio del balón.
    omega = 0
    while True:

        omega += 0.1
        Y0 = np.array([[x0],[y0],[z0], [v0*cos(radianes(angulos[0]))],[v0*sin(radianes(angulos[0]))],[0]], float) # Condición inicial.
        x, y, z = RK4_sistemas(dt, tmin, Y0, omega)
        zfinal = (z[-2] + ((x[-1] - 26)/(26 - x[-2]))*z[-1])/(((x[-1] - 26)/(26 - x[-2]))+1)
        if fabs(zfinal) > desviacion:
            break
    
    # Ya tenemos la velocidad angular ahora hacemos el cálculo preciso del lanzamiento:
    Y0 = np.array([[x0],[y0],[z0], [v0*cos(radianes(angulos[0]))],[v0*sin(radianes(angulos[0]))],[0]], float) # Condición inicial.
    x, y, z = RK4_sistemas(dt, tmin, Y0, omega)
    xfinal = 26
    yfinal = (y[-2] + ((x[-1] - 26)/(26 - x[-2]))*y[-1])/(((x[-1] - 26)/(26 - x[-2]))+1)
    zfinal = (z[-2] + ((x[-1] - 26)/(26 - x[-2]))*z[-1])/(((x[-1] - 26)/(26 - x[-2]))+1)
    x[-1], y[-1], z[-1] = xfinal, yfinal, zfinal

    print("LANZAMIENTO BALÓN DE FÚTBOL A UNA PORTERÍA AFECTADO POR LA FUERZA DE MAGNUS:")
    print()
    print(f"Resultados para un radio del balón = {radio} metros.")
    print("El lanzamiento más ajustado a la escuadra viene dado por las condiciones:")
    print()
    print(f"Ángulo = {angulos[0]:.7} grados.")
    print(f"Velocidad angular = {omega:.7} rad/s = {omega/(2*pi):.7} vueltas por segundo.")
    print(f"El lanzamiento entra exactamente a una altura = {yfinal:.7} metros. Y una desviación a la izquierda de {zfinal:.7} metros.")

    # Representación del tiro:
    # Creamos la figura
    fig = plt.figure()

    # Agregamos un plano 3D
    ax1 = fig.add_subplot(111, projection='3d')

    # Datos en array bi-dimensional
    x = np.array([x])
    y = np.array([y])
    z = np.array([z])

    # plot_wireframe nos permite agregar los datos x, y, z. Pero es necesario que 
    # los datos estén contenidos en un array bi-dimensional.
    ax1.plot_wireframe(x, z, y)
    ax1.set_xlabel("Distancia (metros)")
    ax1.set_ylabel("Desviación (metros)")
    ax1.set_zlabel("Altura (metros)")
    ax1.set_title("LANZAMIENTO BALÓN DE FÚTBOL")

    # Creamos los puntos de la portería:
    x = [26 for _ in range(1000)]
    z = [3.66 for _ in range(1000)]
    y = [0.0025*i for i in range(1000)]
    x = np.array([x])
    y = np.array([y])
    z = np.array([z])
    ax1.scatter(x, z, y, c = "k") # Se añade primer palo

    x = [26 for _ in range(1000)]
    z = [-3.66 for _ in range(1000)]
    y = [0.0025*i for i in range(1000)]
    x = np.array([x])
    y = np.array([y])
    z = np.array([z])
    ax1.scatter(x, z, y, c = "k") # Se añade el segundo palo

    x = [26 for _ in range(1000)]
    z = [-3.66 + i*0.00732 for i in range(1000)]
    y = [2.5 for _ in range(1000)]
    x = np.array([x])
    y = np.array([y])
    z = np.array([z])
    ax1.scatter(x, z, y, c = "k") # Se añade el larguero
    plt.show()

if __name__ == "__main__":
    main()


