<h1>Práctica 2: Alcance de un Proyectil</h1>

Estudiar el movimiento de un proyectil, su alcance y la trayectoria que describe en varios supuestos: 1) sin rozamiento, 2) con rozamiento suponiendo constante la densidad del aire, y 3) con rozamiento teniendo en cuenta la variación de la densidad con la altura en las aproximaciones isoterma y adiabática. Tomar g=9.8 m/s2.

Determinar la trayectoria y el alcance para varios ángulos, tratando de encontrar aquel que maximiza el alcance en cada uno de los casos. Incluir gráficos tanto de la trayectoria como del alcance.

El lenguaje para realizar la práctica puede ser Python o C++. En este último caso se necesitará un programa externo para realizar los gráficos. Si se desea y como tarea adicional, se puede programar en ambos lenguajes y comparar los resultados.

Datos:

v0 = 700 m/s

FR = –B2⋅v⋅v ;  B2/m = 4⋅10-5 m-1 (para y=0)

Aproximación isoterma: ρ = ρ0 exp(-y/y0) ;  y0 ≈ 104 m

Aproximación adiabática: ρ = ρ0 (1 – a⋅y/T0)α ;  a ≈ 6.5⋅10-3 K/m, α ≈ 2.5, T0 = 300 K
