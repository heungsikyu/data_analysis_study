import numpy as np
import pandas as pd 

import matplotlib.pyplot as plt 
import seaborn as sns


plt.rcParams['figure.figsize'] = [10, 5]

tips = sns.load_dataset('tips')
#tips.shape(244, 7)

tips.head()

tips_sum_by_day = tips.groupby('day').tip.sum()

tips_sum_by_day


label = ['Thur', 'Fri', 'Sat', 'Sun']
index = np.arange(len(label))


plt.bar(index, tips_sum_by_day)