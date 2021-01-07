import matplotlib.pyplot as plot
import numpy as np
import datetime 
from datetime import timedelta

np.random.seed(1)

init_time = datetime.datetime(2021, 1, 1, 9, 0, 0)
time_series = np.array([init_time])

for i  in range(120):
    new_time = time_series[-1] + timedelta(minutes=1)
    time_series = np.append(time_series, new_time)

print(time_series[0])
print(time_series[1])