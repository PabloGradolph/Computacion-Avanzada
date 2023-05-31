<h2>Ejercicio 2.1</h2>

Escribir un programa en Python para calcular la integral

$$
\int ^1 _0 x^2e^{-x}dx
$$

mediante la regla del trapecio y las reglas de Simpson 1/3 y 3/8 para un número de subdivisiones n igual a:

1, 2, …, 300 para la regla del trapecio,

2, 4, …, 30 para la regla de Simpson 1/3 y

3, 6, …, 30 para la regla de Simpson 3/8.

Grabar la aproximación numérica de la integral para cada n en un fichero de salida distinto por cada método utilizado. Comparar con la solución exacta.

<h2>Ejercicio 2.2</h2>

Se ha medido la distancia recorrida por un objeto en función del tiempo obteniéndose los datos que se adjuntan en el fichero “distancia.txt”. Este fichero tiene 500 pares de datos equiespaciados (t y s).

- Realizar un programa en Python que lea los datos del fichero distancia.txt y a partir de ellos calcule la velocidad y aceleración del objeto en función del tiempo (nota: salvo en los puntos extremos usar diferencias centrales)

- Sabiendo que los datos del fichero corresponden a la función $$s(t) = -70+7t+70e^{\frac{-t}{10}}$$ comparar los valores numéricos obtenidos para la velocidad y la aceleración con los valores exactos, es decir, calcular el error cometido.

- Grabar los resultados en un fichero.

- Representar gráficamente los resultados.

<h2>Ejercicio 2.3</h2>

Un objeto que cae verticalmente en el aire está sujeto a una resistencia viscosa y también a la fuerza de gravedad. 
Suponer que se deja caer un objeto de masa m desde una altura s0 y que la altura del objeto después de t segundos es:

$$ 
s(t) = s_0 - \frac{mg}{k}t + \frac{m^2g}{k^2}(1-e^{-\frac{kt}{m}}) 
$$

donde g=9.8 m/s2 y k representa el coeficiente de resistencia del aire en g/s. Suponer s0=91.44 m, m=113.4 g y k=45.36 g/s. 
Calcular el tiempo que tarda este objeto en caer al suelo mediante el método de la bisección en el intervalo [0 s, 10 s] 
y mediante el método de Newton para el punto inicial t=1 s. Comparar el número de iteraciones de cada método.

<h2>Ejercicio 2.4</h2>

Escribir un programa en Python para resolver la ecuación que describe la desintegración radiactiva por el método de Euler:

$$ \frac{dN}{dt} = -\frac{N}{\tau} $$

Generar un fichero de datos y un gráfico para 𝜏=1 con 100 pasos de tiempo de 0.05 s. Tomar N(t=0)=100. Comparar con la solución exacta. 
Explorar cómo cambia la precisión al variar el tamaño del paso de tiempo, por ejemplo para valores de 0.2 s y 0.5 s.Reescalar el tiempo para abordar 
el problema del 235U.



