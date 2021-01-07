# 오름 차순 정렬
# 첫번째와 두번째를 비교해서 두번째것이 작으면 자리를 바꾼다
# 

numbers = [5, 3, 6, 9, 8, 7, 1, 10]

def bubbleSort(array):
    for front_index in range(0, len(array)-1):
        for index in range(front_index+1,len(array)):
            if array[front_index] > array[index]:
                #자리를 바꾼다. 
                temp = array[front_index]
                array[front_index] = array[index]
                array[index] = temp
            # print(array)
    return array


result = bubbleSort(numbers)
print(result)
