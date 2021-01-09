# 몬테카를로 시뮬레이션을 통한 삼성전자 주가 예측

import pandas_datareader as pdr
import pandas as pd 
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib import style

style.use('ggplot')


# 한국거래소(KRX) 종목타입
stockType = {'kospi': 'stockMkt', 'kosdaq':'kosdaqMkt'}

# 주식종목타입가져오기
def getStockCode(df, name):
    code = df.query("name=='{}'".format(name))['code'].to_string(index=False)
    code = code.strip()
    return code

# 주식종목타입별 데이터 다운로드
def getDownloadStockData(marketTypeParam=None):
    marketType = stockType[marketTypeParam]
    downloadLink = 'http://kind.krx.co.kr/corpgeneral/corpList.do?method=download'
    downloadLink = downloadLink + '&marketType=' + marketType  

    df = pd.read_html(downloadLink, header=0)[0]
    return df

#코스피 데이터가져오기 
def getDownloadKospi():
    df = getDownloadStockData('kospi')
    df.종목코드 = df.종목코드.map('{:06d}.KS'.format)
    return df

#코스닥 데이터가져오기 
def getDownloadKosdaq():
    df = getDownloadStockData('kosdaq')
    df.종목코드 = df.종목코드.map('{:06d}.KQ'.format)
    return df


# 주식 종목 가져오기 
kospidf = getDownloadKospi()
kosdaqdf = getDownloadKosdaq()

codedf = pd.concat([kospidf,kosdaqdf])
codedf = codedf[['회사명','종목코드']]

codedf = codedf.rename(columns={'회사명':'name', '종목코드':'code'})
print(codedf)


# 삼성전자 주가 가져오기
# code = getStockCode(codedf, '삼성전자')
# code = getStockCode(codedf, 'LG전자')
# code = getStockCode(codedf, 'NAVER')
code = getStockCode(codedf, '카카오')
df = pdr.get_data_yahoo(code, adjust_price=True)
# print(df)
# df['Close'].plot(figsize=(10,15))
# plt.show()


# 몬테카를로 시뮬레이션 주가 예측 
start = dt.datetime(2016, 1, 1)
end = dt.datetime(2021, 1, 8)

closePrice_df = pdr.get_data_yahoo(code, start, end)['Close']
#삼성전자 수익률 계산 
returns = closePrice_df.pct_change() 

# print(returns)
# print(returns.std())
# returns.plot()
# plt.show()

# 마지막 장마감 금액 
last_price = closePrice_df[-1]
# print(last_price)

#시뮬레이션 횟수 
num_simmulations = 1000 
num_days = 300

# print((start-end).days)
simmulations_df = pd.DataFrame()

for x in range(num_simmulations):
    count = 0 
    daily_vol = returns.std()
    price_series = []

    price = last_price * (1 + np.random.normal(0, daily_vol))
    price_series.append(price)

    for y in range(num_days):
        if count == 299:
            break
        price = price_series[count] * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)
        count += 1

    simmulations_df[x] = price_series


# print(simmulations_df)
fig = plt.figure()
fig.suptitle('Monte Carlo Simmulation: '+ code )
plt.plot(simmulations_df)
plt.axhline(y = last_price, color='r', linestyle='-')
plt.xlabel('Day')
plt.ylabel('Price')
plt.show()