import numpy as np
import matplotlib.pyplot as plt

def func(x, a):
    return -100*np.exp(-a*x)+100

x = np.arange(0, 300, 3)
plt.plot(x,func(x,.1),'r',label='Influence')
plt.plot(x,func(x,.01),'go',label='Desperation')
plt.plot(x,func(x,.01),'b--',label='Hope')

plt.legend()
plt.show()
