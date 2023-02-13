#------------------------------------
# Clase del 13 de febrero de 2023
# Autor: Pablo Gradolph Oliva
# Contenido: Representación gráfica en 2D
# (uso de matplotlib)
#------------------------------------

#In[0]

import matplotlib.pyplot as plt
y = [1.0, 2.4, 1.7, 0.3, 0.6, 1.8]
plt.plot(y)
plt.show()

# In[2]:


import matplotlib.pyplot as plt
x=[0.5, 1.0, 2.0, 4.0, 7.0, 10.0]
y=[1.0, 2.4, 1.7, 0.3, 0.6, 1.8]
plt.plot(x,y)
plt.show()


# In[3]:


import matplotlib.pyplot as plt
import numpy as np
x=np.linspace(0,10,101)
y=np.sin(x)
plt.plot(x,y)
plt.show()
plt.plot(x,np.cos(x))
plt.show()

# In[4]:


import matplotlib.pyplot as plt
import numpy as np
x=np.linspace(0,10,101)
y=np.sin(x)
plt.plot(x,y,'o')
plt.show()


# In[5]:


import numpy as np
import matplotlib.pyplot as plt
x = np.arange(4)
plt.plot(x, x**2, label='x**2') 
plt.plot(x, x**3, label='x**3') 
plt.plot(x, 2*x, label='2*x') 
plt.plot(x, 2**x, label='2**x') 
plt.legend()
#plt.legend(loc='upper center')
plt.grid(True)
plt.xlabel('x') 
plt.xlim([0, 3])
plt.ylabel('y = f(x)') 
plt.ylim([0, 30]) 
plt.title('Simple Plot Demo') 
plt.show()


# In[6]:


import numpy as np
import matplotlib.pyplot as plt

x = np.arange(10)
y=x**2
plt.plot(x, y, 'mo--')
plt.xticks(range(len(x)), ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j'])
plt.yticks(range(0, 100, 10))
plt.show()


# In[7]:


import matplotlib.pyplot as plt
import numpy as np

x1, x2 = np.linspace(0.0, 2.0, 20), np.linspace(0.0, 2.0, 200)
y1, y2, y3 = np.exp(-x1), np.exp(-x2), np.sin(2 * np.pi * x2)
y4 = y2 * y3
l1 = plt.plot(x1, y1, "bD--", markersize=5)
l3 = plt.plot(x2, y3, "go-", markersize=5)
l4 = plt.plot(x2, y4, "rs-", markersize=5) 
plt.ylim(-1.1, 1.1)
plt.xlabel("Segundos")
plt.ylabel("Voltios")
plt.legend( (l3[0], l4[0]), ("Oscilatorio", "Amortiguado"), shadow = True ) 
plt.title("Movimiento Oscilatorio Amortiguado")
plt.show()


# In[8]:


import matplotlib.pyplot as plt
import numpy as np
		
x = np.linspace(0, 2, 100)
plt.plot(x, x, label='linear')  # Plot some data on the (implicit) axes.
plt.plot(x, x**2, label='quadratic')  # etc.
plt.plot(x, x**3, label='cubic')
plt.xlabel('x label')
plt.ylabel('y label')
plt.title("Simple Plot")
plt.legend()
plt.show()


# In[9]:


import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2, 100)
fig, ax = plt.subplots()  # Create a figure and an axes.
ax.plot(x, x, label='linear')  # Plot some data on the axes.
ax.plot(x, x**2, label='quadratic')  # Plot more data on the axes...
ax.plot(x, x**3, label='cubic')  # ... and some more.
ax.set_xlabel('x label')  # Add an x-label to the axes.
ax.set_ylabel('y label')  # Add a y-label to the axes.
ax.set_title("Simple Plot")  # Add a title to the axes.
ax.legend()  # Add a legend.
plt.show()