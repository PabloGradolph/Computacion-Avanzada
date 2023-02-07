#In[0]

###
# Prueba de matplotlib y numpy
###

import matplotlib.pyplot as plt
import numpy as np # Importamos numpy como el alias np
a = np.linspace(0,20,50)
b = np.sin(a)
plt.plot(a, b, 'k--', linewidth = 2) 
plt.show()

#In[1]

###
# Prueba pequeña de vpython
###

from vpython import * ## importa libreria vpython con clases de objetos graficos y funciones matematicas
scene2=canvas(background=color.white) ## lienzo, escena
micaja=box(axis=vec(0,2,0))
micaja.color=color.red
t=0
dt=0.01
while True:
    rate(100) # el lazose ejecuta a esterate por segundo, en un segundo se pasa de t=0 a t=1(vuelta en 2pi segundos)
    micaja.axis=vec(2*sin(t),2*cos(t),0)
    micaja.color=vec(sin(2*t)*sin(t),sin(2*t)*cos(t),cos(2*t))
    t=t+dt

#In[2]

###
# Prueba grande de vpython
###

from vpython import * # Cargamos las Librerias de VPython que incluyen Clases de Objetos Graficos, y funciones Matemáticas
canvas() # Creamos una escena (se crea una por default en glowscript)
#GlowScript 3.0 VPython ( para uso en glowscript en lugar de la importación de arriba)
# Constantes fisicas del sistema:
m1=1. ## no depende de este valor
s0=1. ## Cociente de masas s0=m2/m1
s=0.1 ## (s=3., 0.1) ## Define la velocidad tangencial v0=sqrt(s*g*rho), s=1,phi2=0 :circular
m2=s0*m1
L=2. # Longitud de la cuerda
g=9.8 # aceleracion de la gravedad
# Condiciones iniciales
rho=1.
rho_dot=0.
phi=0.
v0=sqrt(s*g*rho) # valor auxiliar
phi_dot=v0/rho
phi2=0.5 # (phi2= 0.5)
phi2_dot=0.
#lz=m1*rho0*v0
# Creamos el sistema en la escena
box(color=color.green,pos=vector(0,-0.1,0),height=0.1,width=4,length=4,opacity=0.4) ### mesa, instancia de la clase box
bola1=sphere(color=color.red,pos=vector(rho*cos(phi),0,rho*sin(phi)),radius=0.1,make_trail=True) ### masa m1, instancia de la clase sphebola2=sphere(color=color.magenta,pos=vector((L-rho)*sin(phi2),-(L-rho)*cos(phi2),0),radius=0.1,make_trail=True) ## masa m2
cuerda=curve(pos=[bola1.pos,vector(0,0,0)],color=color.blue) ### crea una curva llamada cuerda, con dos puntos
bola2=sphere(color=color.magenta,pos=vector((L-rho)*sin(phi2),-(L-rho)*cos(phi2),0),radius=0.1,make_trail=True) ## masa m2
cuerda.append(bola2.pos) ### agrega un punto a la curva llamada cuerda
# graph(scroll=True, fast=False, xmin=0, xmax=5,ymin=0,ymax=1.1)
# fig = gcurve()
t=0 ### Asigna a la variable t el valor 0.
dt=0.001 ### Asigna a la variable dt el valor 0.01
while True: # Lazo de iteración sin salida ( Mientras Verdadero haga:), notar los : y el indentado)
 rate(500) # Controla la taza de muestreo, normalmente hacer que dt*rate sea del orden de la unidad

 rho_dotdot=(1/(1.+s0))*(rho*phi_dot*phi_dot-s0*(L-rho)*(phi2_dot*phi2_dot)-s0*g*cos(phi2))
 phi_dotdot=-(2/rho)*phi_dot*rho_dot # Pendientes en t_i
 phi2_dotdot=(1/((L-rho)*(L-rho)))*(-g*(L-rho)*sin(phi2)+2*(L-rho)*phi2_dot*rho_dot)
 rho=rho+rho_dot*dt
 phi=phi+phi_dot*dt # Euler forward variables en t_i+1
 phi2=phi2+phi2_dot*dt

 rho_dot=rho_dot+rho_dotdot*dt
 phi_dot=phi_dot+phi_dotdot*dt # Euler forward variables en t_i+1
 phi2_dot=phi2_dot+phi2_dotdot*dt

 bola1.pos=rho*vector(cos(phi),0,sin(phi)) ## modifica la posicion de la bola 1
 bola2.pos=(L-rho)*vector(sin(phi2),-cos(phi2),0)
 cuerda.modify(0,bola1.pos) ## modifica la posicion del primer punto de la cuerda
 cuerda.modify(2,bola2.pos) ## modifica la posicion del tercer punto de la cuerda

# fig.plot( t, m1*rho*rho*phi_dot )
 t+=dt ## asignacion del nuevo tiempo t=t+dt





