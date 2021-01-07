
arr = [5, 3, 6, 9, 8, 7, 1, 10]

def bubble_sort(arr):
    for i in range(len(arr) - 1, 0, -1):
        print(i)
        swapped = False
        for j in range(i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr

result = bubble_sort(arr)
print(result)