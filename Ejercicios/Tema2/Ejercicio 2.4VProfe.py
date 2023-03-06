from numpy import *
from matplotlib.pyplot import *

# Parámetros del problema

tau=1
dt=0.5         # 1% del tiempo representativo del sistema (tau) 
time=5          # Tiempo total
n=int(time/dt)  # Número de intervalos

# Para reescalar al caso del uranio:

tau=1e9
dt=tau/100
time=5*tau
n=int(time/dt)

# Si quisiéramos hacer el programa interactivo:

# tau=double(input("time constant -> "))
# dt=double(input("time step -> "))
# time=double(input("total time -> "))
# n=int(time/dt)

# Creo arrays para contener los resultados

n_uranium=zeros(n+1, float)
n_exacto=zeros(n+1, float)
t=zeros(n+1,float)

# n_uranium[0]=n_exacto[0]=N=100
n_uranium[0]=n_exacto[0]=N=6e23   # Número de Avogadro
# n_uranium[0]=n_exacto[0]=double(input("Initial number of nuclei -> "))
t[0]=0

# Aplico el método de Euler

for i in range(1,n+1):
	n_uranium[i]=n_uranium[i-1]-(n_uranium[i-1]/tau)*dt
	t[i]=t[i-1]+dt
	n_exacto[i]=n_exacto[0]*exp(-t[i]/tau)

# Sería más eficiente calcular la solución exacta usando operaciones con arrays:
# n_exacto=n_exacto[0]*exp(-t/tau)

# Guardo los datos con savetxt

savetxt("salida.txt", transpose([t,n_uranium]))

# Represento los datos numéricos y teóricos:

xlabel("time (años)")
ylabel("Number of Nuclei")
line1=plot(t,n_uranium,"go", markersize=4)
line2=plot(t,n_exacto, "k-")
legend((line1[0],line2[0]), ("Numerical solution", "Exact solution"))

# Curiosidad: insertar texto en un gráfico. La "f" es necesaria cuando se
# van a insertar valores de variables en el texto, entre {}.

#text(1.5,70,f"Time constant = {tau} s", fontsize=16)
#text(1.5,50,f"Time step = {dt} s", fontsize=16)

# En el caso de los valores para el uranio, notar el modo de dar
# formato a los valores numéricos para que salgan en notación científica.
# Para float sería a.bf

text(0.3*time,0.7*N,f"Time constant = {tau:.1E} s", fontsize=16)
text(0.3*time,0.5*N,f"Time step = {dt:.1E} s", fontsize=16)

show()
