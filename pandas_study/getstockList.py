import pandas as pd 

df = pd.read_html('http://kind.krx.co.kr/corpgeneral/corpList.do?method=download', header=0)[0]

# print(df.head())

# # 상장일 기준 소팅 
# df = df.sort_values(['상장일'], ascending=[True])
# print(df.head())

df = df[['회사명','종목코드']]
print(df)

# 컬럼명 변경
df = df.rename(columns={'회사명':'companyname', '종목코드': 'stockcode'})
print(df)