
## 자연수 
# - 소수
# - 소인수 분해 
# - 최대 공약수 
# - 최소 공배수 
# - 십진법, 이진법


#소수(Prime number)

def is_prime(a):
     b = range(2, a)
     #print(b)
     c = 0 
     for i in b:
          if a % i == 0:
               c += 1
               print(c)
          if c > 0 :
               print('{}는 소수가 아니다'.format(a))
               d = False
          else: 
               print('{}는 소수이다'.format(a))
               d = True
          return d

retVal = is_prime(16)
print(retVal)

# for i in range(2, 17):
#      print(i)
