import numpy as np

x = np.array([0.00001, 1, 2, 4, 10, 100])

#exponential function 지수 함수 
expoF = np.exp(x)

print(expoF)

# 로그 함수 
#natural logarithm 
naturallog = np.log(x)

print(naturallog)

np.log10(x)