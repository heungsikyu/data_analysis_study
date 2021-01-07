

#배열의 특정 연속된 구간을 처리 하는 경우 
 # 아래와 같이 자연수로 구성된 수열이 있다.
 #합이 5인 부분 연속 수열의 개수를 구하시오
 #1, 2, 3, 2, 5

n = 5
m = 5
data = [1, 2, 3, 2, 5]

result = 0 
summary = 0
end = 0

for start in range(n):
    while summary < m and end <  n:
        summary += data[end]
        end += 1
    if summary == m:
        result += 1
        
    summary -= data[start]

print(result, summary)

    