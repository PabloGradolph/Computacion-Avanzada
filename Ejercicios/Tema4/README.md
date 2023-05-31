<h2>Ejercicio 4.1</h2>

a) Escribir un programa en Python que calcule la velocidad de un ciclista en función del tiempo mediante los métodos de Euler y Runge-Kutta según la ecuación

$$
\frac{dv}{dt} = \frac{P}{mv}
$$

donde P es la potencia que genera el ciclista y m su masa. Tomar P=400 W y m=70 kg. Tomar como velocidad inicial v0=4 m/s. 
Comparar los resultados con la solución exacta. Estudiar la precisión de cada método para distintos valores de dt. 
Usar un intervalo temporal de unos 200 segundos. Representar los resultados gráficamente.

b)Añadir la resistencia del aire resolviendo la ecuación:

$$
\frac{dv}{dt} = \frac{P}{mv} - \frac{C \rho Av^2}{2m}
$$

Tomar el coeficiente de rozamiento C=0.5, la densidad del aire, ρ=1.225 kg/m3, y la sección eficaz efectiva del ciclista, A=0.33 m2. 
Comprobar que la velocidad terminal obtenida se corresponde con la teórica y discutir si el resultado es o no realista. 
Representar los resultados gráficamente.

<h2>Ejercicio 4.2</h2>

Escribir un programa en Python que calcule el alcance de un proyectil en dos dimensiones sin rozamiento por los métodos de Euler y de Runge Kutta. 
Suponer una velocidad inicial de 700 m/s y un ángulo respecto a la horizontal de 30º. Probar distintos intervalos temporales, dt, entre 0.0001 s y 2 s. 
Comparar los resultados con el resultado exacto y determinar para qué valor de dt se consigue un error relativo menor que 10–6 para cada uno de los dos métodos. 
Tomar como valor de g = 9.8 m/s2. Entregar, además del código, un fichero en pdf o word que contenga

- una tabla con los valores de dt que se hayan probado donde quede claro el valor de dt para la precisión mencionada (no tiene por qué ser un valor de dt exacto, simplemente el valor que se haya probado que asegure que el error relativo sea menor que 10–6)
- los valores del alcance calculado y teórico.
- una gráfica de la trayectoria, con las distancias en unidades de km.

<h2>Ejercicio 4.3</h2>

Escribir un programa en Python para determinar el alcance de un proyectil con y sin rozamiento en función del ángulo, entre 30º y 55º en intervalos de 1º, mediante el método de Runge-Kutta de orden 4 con un intervalo temporal dt=0.1 s. 
Determinar el ángulo de alcance máximo en ambos casos. Usar g=9.8 m/s2.

Datos:
v0 = 700 m/s
FR = –B2⋅v⋅v ;  B2/m = 4⋅10-5 m-1

Además del código se debe entregar un documento pdf o word que contenga:
- Un gráfico con las trayectorias del proyectil sin rozamiento para ángulos entre 30º y 55º en intervalos de 5º
- Otro gráfico similar para el caso con rozamiento.
- Sendos gráficos del alcance del proyectil en función del ángulo para todos los ángulos entre 30º y 55º (en intervalos de 1º), para el caso con rozamiento y sin rozamiento, respectivamente. En dichos gráficos deberá incluirse una leyenda con los datos del alcance máximo y el ángulo correspondiente.

<h2>Ejercicio 4.4</h2>

a) Escribir un programa en Python que calcule la trayectoria de una pelota de béisbol en dos dimensiones. Para ello considerar la dependencia del coeficiente de rozamiento con la velocidad de la forma:

$$
\frac{B_2}{m} = 0.0039 + \frac{0.0058}{1+e^{\frac{(v^*-v_d)}{\Delta}}}
$$

con vd = 35 m/s y Δ = 5 m/s, siendo v* la velocidad de la pelota respecto al aire. Considerar como condiciones iniciales x0=0, y0=1 m, y v0=49 m/s y probar 
varios ángulos de lanzamiento entre 30º y 50º. Encontrar el ángulo aproximado de máximo alcance.

b)   Para un ángulo inicial de 35º, incluir el efecto del viento tanto a favor como en contra. Suponer una velocidad de viento de 9 km/h.
Realizar sendos gráficos para mostrar los resultados de ambos apartados.

<h2>Ejercicio 4.5</h2>

Un jugador de fútbol lanza una falta desde un punto situado a 26 metros de la portería, en posición centrada respecto a ésta (ver figura). 
La barrera, formada por jugadores de 1,80 metros, se sitúa a 9 metros del punto de lanzamiento. La idea del lanzador es superar la barrera por encima 
y colocar el balón en la escuadra. Para ello dispara con una velocidad inicial perpendicular a la línea de gol, pero dando un efecto al balón 
para que se desvíe hacia la izquierda. Suponiendo que la velocidad inicial es de 24 m/s, estimar el ángulo de elevación y la rotación en número de 
vueltas por segundo que debe transmitir al balón para que supere la barrera y entre lo más cerca posible de la escuadra. La altura de la portería es de 
2.5 metros. Considerar la fuerza de arrastre sólo en la dirección de máxima velocidad (dirección x), despreciándola en las otras dos direcciones. 
La fuerza de Magnus es perpendicular al eje de rotación del balón y a la dirección del movimiento (~ eje X) y toma el valor: FM=S0⋅ω⋅vx

Datos: 

  Coeficiente de arrastre del aire: B2/m=0.01083

  Coeficiente para la Fuerza de Magnus: S0/m=0.003

  Diámetro del balón de fútbol: 22 cm
  
<h2>Ejercicio 4.6</h2>

Realizar un estudio de la estabilidad de la órbita de un planeta alrededor del sol, sin influencia del resto de los planetas, para exponentes de r distintos de 𝛽=2.
Tomar como parámetros x0 = 1 UA, y0 = 0, vx0 = 0, vy0 = 5 UA/año. Realizar animaciones mediante vpython, así como gráficos mediante matplotlib.

<h2>Ejercicio 4.7</h2>

Escribir un programa en Python para estudiar el efecto de Júpiter en la órbita de la Tierra. Considerar el Sol en reposo en el origen de coordenadas. Si el efecto no es apreciable en la simulación, aumentar la masa de Júpiter hasta que se observen efectos.

Datos: condiciones iniciales para la Tierra: x=1, y=0, vx=0, vy=6.18, para Júpiter x=5.2, y=0, vx=0, vy=2.62



