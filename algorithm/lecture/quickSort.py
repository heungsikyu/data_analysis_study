import sys
# 40을 기준으로 오름차순으로 정렬하라 
numbers = [53, 35, 27, 50, 75, 74, 89, 22, 58 ]


def quickSort(array):
    if len(array) < 2:
        return array
    else:
        pivot = array[0]
        less = [number for number in array[1:] if number <= pivot]
        greater = [number for number in array[1:] if number > pivot]

        return quickSort(less) + [pivot] + quickSort(greater)



#특정 위치 기준없이 퀵정렬
def quickSort2(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr)-1]
    less_arr, equal_arr, greater_arr = [], [], []
    for num in arr:
        if num < pivot:
            less_arr.append(num)
        elif num > pivot:
            greater_arr.append(num)
        else:
            equal_arr.append(num)

    return quickSort2(less_arr) + equal_arr + quickSort2(greater_arr)



# 최적화 
def quick_Sort(arr):
    def sort(low, high):
        print(arr[low], arr[high])
        if high <= low:
            return 

        mid = partition(low, high)
        print(arr[mid])
        sort(low, mid - 1)
        sort(mid, high)

    def partition(low, high):
        pivot = arr[(low + high)//2]
        while low <= high:
            while arr[low] < pivot:
                low += 1
            while arr[high] > pivot:
                high -= 1
            if low <= high:
                arr[low], arr[high] = arr[high], arr[low]
                low, high = low + 1, high - 1
        return low

    return sort(0, len(arr) - 1)
    

if __name__ == '__main__':
    result = quickSort(numbers)
    print(result)

    result2 = quickSort2(numbers)
    print(result2)

    # sys.setrecursionlimit(10**7)
    print(quick_Sort(numbers))
    
