import numpy as np
import matplotlib.pyplot as plt 
from math import factorial


def bin_disk(k, n, p):
    nck = factorial(n) / (factorial(k) * factorial(n - k))
    pd = nck * p**k * (1-p)**(n-k)
    return pd 

x = np.arange(10)
pd1 = np.array([bin_disk(k,  10, 1/6) for k in range(10)])
print(pd1)
#plt.ylim(0, 0,3)
plt.text(12.5, 0.28, 'n, p=7, 0.5')
plt.plot(x, pd1, color='lightcoral')
plt.show()