import pandas as pd
import numpy as np 
import seaborn as sns 

sns.set_style('whitegrid')

# https://pbpython.com/monte-carlo.html
# 이전과거 데이를 살펴보면 과거비율은 평균 100 %와 표준 편차 10 %를 가지고 있습니다. 
# 이변수로 평균(avg)와 표준편차(std_dev), 영업 담당자(num_reps) 및 시뮬레이션 수(num_simulations)를 정의 해 보겠습니다.

avg  = 1
std_dev = .1
num_reps = 500
num_simulations = 1000

# pct_to_target = np.random.normal(avg, std_dev, num_reps).round(2)#소수점 2자리 이하 반올림 

# print(pct_to_target)


#판매 목표량 
sales_target_values = [75_000, 100_000, 200_000, 300_000, 400_000, 500_000]
sales_target_prob = [.3, .3, .2, .1, .05, .05]

# sales_target = np.random.choice(sales_target_values, num_reps, p=sales_target_prob)

# df = pd.DataFrame(index=range(num_reps), data = { 'Pct_To_Target': pct_to_target, 'Sales_Target': sales_target})

# df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']

# Pct_To_Target을 커미션 비율에 매핑 함슈 
def calc_commission_rate(x):
    """ Return the comminssion rate based on table:
        0-90% = 2%
        91-99% = 3%
        >=100 = 4%
    """
    if x <= .90:
        return .02
    elif x <= .99:
        return .03
    else:
        return .04


# df['Commission_Rate'] = df['Pct_To_Target'].apply(calc_commission_rate)
# df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']



all_stats = []

for i in range(num_simulations):

    sales_target = np.random.choice(sales_target_values, num_reps, p=sales_target_prob)
    pct_to_target = np.random.normal(avg, std_dev, num_reps).round(2)

    df = pd.DataFrame(index=range(num_reps), data = { 'Pct_To_Target': pct_to_target, 'Sales_Target': sales_target})

    df['Sales'] = df['Pct_To_Target'] * df['Sales_Target']

    df['Commission_Rate'] = df['Pct_To_Target'].apply(calc_commission_rate)
    df['Commission_Amount'] = df['Commission_Rate'] * df['Sales']
    
    # We want to track sales,commission amounts and sales targets over all the simulations
    all_stats.append([df['Sales'].sum().round(0),
                      df['Commission_Amount'].sum().round(0),
                      df['Sales_Target'].sum().round(0)])


results_df = pd.DataFrame.from_records(all_stats, columns=['Sales','Commission_Amount','Sales_Target'])
results_df.describe().round(0).style.format('{:,}')
# print(results_df.describe().style.format('{:,}'))

results_df['Commission_Amount'].plot(kind='hist', title="Total Commission Amount")
                                