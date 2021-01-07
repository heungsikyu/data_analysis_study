import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

pd.set_option('max_columns', 50)
mpl.rcParams['lines.linewidth'] = 2


df = pd.read_excel('/Users/heungsikyu/Library/Mobile Documents/com~apple~CloudDocs/data_analysis/cohort/data_sample/Online-Retail.xlsx',
 dtype={'CustomerID': str, 
        'InvoiceID': str},
parse_dates=['InvoiceDate'])

df.head()

#df['OrderPeriod'] = df.OrderDate.apply(lambda  x: x.strftime('%Y-%m'))