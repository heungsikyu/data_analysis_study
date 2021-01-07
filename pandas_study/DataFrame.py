import numpy as np
import pandas as pd 
from pandas import DataFrame as df 


df_1 = df(data=np.arange(24).reshape(3,8),
index =['r0', 'r1', 'r2'],
columns=['c0', 'c1', 'c2', 'c3','c4','c5','c6','c7'],
dtype='int',
copy=False)

print(df_1)
print("-----------------------")
print("행과 열을 전치 : \n", df_1.T )
print("-----------------------")
print("행과 열 이름을 리스트로 반환 : ", df_1.axes)
print("-----------------------")
print("df_1의 데이터 형 반환 :\n",df_1.dtypes)
print("-----------------------")
print("df_1 행과 열 개수를 튜플로 변환 : ", df_1.shape)
print("-----------------------")
print("df_1의 원소의 개수 반환 : ", df_1.size)
print("-----------------------")
print("df_1의 원소를 numpy형태로 반환 : n ", df_1.values)


print("========================================================")
print("DataFrame의 행 또는 열 데이터 선택해서 가져오기")
print("========================================================")

df_2 = df({'class_1': ['a','a','b','b','c'],
          'var_1' : np.arange(5),
          'var_2' : np.random.randn(5)}
          ,index=['r0','r1', 'r2', 'r3', 'r4'])

print("df_2: \n", df_2)
print("--------------------------------------------")
print("행 기준으로 선택해서 가져오기 ")
print(df_2.index)
print("--------------------")
print("2번 행부터  가져오기 : \n", df_2.iloc[2:])
print("--------------------")
print("특정 위치 행 가져오기 : \n", df_2.iloc[2])
print("--------------------")
print("특정 레이블 행 가져오기 : \n", df_2.loc['r4'])



