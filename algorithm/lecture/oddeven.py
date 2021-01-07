

# 짝수 홀수 구하기
def isOddEven(num):
    print(num )
    if (num % 2 == 0):
        retVal =  'even'
    else:
        retVal =  'odd'
    return retVal


result = isOddEven(121281817134343858590)
print(result)