<h2>Ejercicio 5.1</h2>

Resolver la siguiente ecuación:

$$
u'' = u; u'(1) = 1.17520; u'(3) = 10.0178
$$

Comparar con la solución exacta sabiendo que u(x)=cosh(x) y que los valores en la frontera corresponden a senh(1) y senh(3), respectivamente. 
El código debe crear una gráfica con la solución exacta y las soluciones numéricas para 5 intervalos, 10 intervalos y 20 intervalos. 
Entregar el código y un pdf con la gráfica.

<h2>Ejercicio 5.2</h2>

Estudiar la distribución de temperaturas en equilibrio de una placa rectangular como la placa vista en clase (10x20 cm, uno de los lados a 100º C y el resto a 0º C). 
Encontrar la distribución de temperaturas resolviendo el sistema de ecuaciones de manera directa y por métodos iterativos.
Aumentar el número de intervalos duplicándolos cada vez hasta llegar a 128x256 intervalos (si es posible), comenzando por 4x8. 
Estudiar el tiempo de ejecución de cada uno de los métodos para cada valor de h. Comparar entre Python y C++ (opcional). 
Representar la distribución de temperaturas mediante el comando imshow.

Se debe entregar junto con el código utilizado un documento pdf con el resumen de los resultados. Dicho documento debe contener un gráfico del mapa de las 
temperaturas obtenido para cada tamaño de intervalo probado, y junto a cada gráfico los datos de tiempo de ejecución y, eventualmente, del número de 
iteraciones para los distintos métodos utilizados. Se debe incluir también el valor numérico de la temperatura obtenido en el punto central de la placa. 
No se valorará la adición de ningún otro texto añadido.

Utilizar para la convergencia en los métodos iterativos el criterio de que la norma de la diferencia sea menor que 10-2.

<h2>Ejercicio 5.3</h2>

Resolver el potencial y el campo eléctricos en dos dimensiones para una distribución de cargas como la vista en clase (ver figura).
