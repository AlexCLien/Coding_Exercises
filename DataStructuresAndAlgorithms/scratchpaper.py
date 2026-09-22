'''
Merge Sort
'''
'''
data_first = [1,5,18,3,7,12]
data_second = [2,6,13,26,30,31]
def merge(data_1,data_2):
    length = len(data_1) + len(data_2)
    first_array = data_1
    second_array = data_2
    merged_array = [None] * length
    i = 0
    j = 0
    k = 0
    while i < len(first_array) and j < len(second_array):
        if first_array[i] < second_array[j]:
            merged_array[k] = first_array[i]
            i += 1

        else:
            merged_array[k] = second_array[j]
            j += 1
        k += 1
    while i < len(first_array):
        merged_array[k] = first_array[i]
        i += 1
        k += 1
    while j < len(second_array):
        merged_array[k] = second_array[j]
        j += 1
        k += 1
    
    return merged_array

print(merge(data_first,data_second))
'''
def summation(num):
    array = []
    i = 0
    count = 0
    for i in range(num):
        i = i + count
        count += 1
        array += [count]
        
        
    return sum(array)

print(summation(8))
