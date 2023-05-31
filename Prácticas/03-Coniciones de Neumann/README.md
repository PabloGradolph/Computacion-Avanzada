<h1>Práctica 3: Condiciones de Neumann</h1>

Hacer un programa que resuelva la distribución de temperaturas en una placa de 5 cm de alto y 9 cm de ancho, 
con un espesor d=0.5 cm, suponiendo que en toda la superficie de la placa se pierde calor a un ritmo Q=0.6 cal/(s cm3). La ecuación que describe el sistema es:

$$
\triangledown^2u = \frac{Q}{k·d}
$$

donde k es la conductividad térmica, k=0.16 cal/(s cm ºC). Las condiciones de frontera son:

- Los dos bordes laterales se mantienen a 20º.
- En el borde superior se pierde calor a un ritmo constante:

$$
\frac{\partial u}{\partial y} = -15ºC/cm 
$$

- En el borde inferior se pierde o gana calor según

$$
k\frac{\partial u}{\partial y} = H(u-u_r) 
$$

donde H es el coeficiente de transferencia de calor, H=0.073 cal/(s cm2), y ur es la temperatura ambiente, que tomamos como ur = 25ºC. 

Probar varios valores de h. Representar gráficamente los resultados. El informe se debe centrar en la presentación gráfica de resultados y debe ser breve.

Para el caso particular de 50x90 intervalos y un valor de epsilon de 10–2, incluir una tabla con los valores de la temperatura en el centro de la placa, 
en el centro del borde superior y en el centro del borde superior, así como el número de iteraciones que se han utilizado. Usar el criterio de la diferencia de normas.
