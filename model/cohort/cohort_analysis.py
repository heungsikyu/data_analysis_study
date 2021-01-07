import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

pd.set_option('max_columns', 50)
mpl.rcParams['lines.linewidth'] = 2


df = pd.read_excel('/Users/heungsikyu/Library/Mobile Documents/com~apple~CloudDocs/data_analysis/cohort/data_sample/12-relay-foods.xlsx')

df['OrderPeriod'] = df.OrderDate.apply(lambda  x: x.strftime('%Y-%m'))



df.set_index('UserId', inplace=True)
df['CohortGroup'] = df.groupby(level=0)['OrderDate'].min().apply(lambda x: x.strftime('%Y-%m'))
df.reset_index(inplace=True)
df.head()

grouped = df.groupby(['CohortGroup', 'OrderPeriod'])

# count the unique users, orders, and total revenue per Group + Period
cohorts = grouped.agg({'UserId': pd.Series.nunique,
                       'OrderId': pd.Series.nunique,
                       'TotalCharges': np.sum})

# make the column names more meaningful
cohorts.rename(columns={'UserId': 'TotalUsers',
                        'OrderId': 'TotalOrders'}, inplace=True)

def cohort_period(df):
    """
    Creates a `CohortPeriod` column, which is the Nth period based on the user's first purchase.
    
    Example
    -------
    Say you want to get the 3rd month for every user:
        df.sort(['UserId', 'OrderTime', inplace=True)
        df = df.groupby('UserId').apply(cohort_period)
        df[df.CohortPeriod == 3]
    """
    df['CohortPeriod'] = np.arange(len(df)) + 1
    return df

cohorts = cohorts.groupby(level=0).apply(cohort_period)


# reindex the DataFrame
cohorts.reset_index(inplace=True)
cohorts.set_index(['CohortGroup', 'CohortPeriod'], inplace=True)

# create a Series holding the total size of each CohortGroup
cohort_group_size = cohorts['TotalUsers'].groupby(level=0).first()
cohort_group_size.head()


cohorts['TotalUsers'].head()
cohorts['TotalUsers'].unstack(0).head()


user_retention = cohorts['TotalUsers'].unstack(0).divide(cohort_group_size, axis=1)
user_retention.head(10)
#print(user_retention)


plt.rcParams['font.family'] = 'AppleGothic'
user_retention[['2009-01','2009-02','2009-03','2009-04', '2009-05', '2009-06', '2009-07', '2009-08']].plot(figsize=(10,5))
plt.plot(user_retention, marker="o")
plt.title('Cohorts: 사용자 재구매 리텐션')
plt.xticks(np.arange(1, 12.1, 1))
plt.xlim(1, 15)
plt.ylabel('% of Cohort 구매')
plt.show()



import seaborn as sns
sns.set(style='dark')
plt.rcParams['font.family'] = 'AppleGothic'
plt.figure(figsize=(12, 8))
plt.title('Cohorts: 사용자 재구매 리텐션')
sns.heatmap(user_retention.T,cmap="Blues", mask=user_retention.T.isnull(), annot=True, fmt='.0%');
plt.show()