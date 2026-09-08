
numbers = [8, 3, 12, 5, 7, 20, 4]

'''
1. Find the largest value without using max().
2. Find the smallest value without using min().
3. Calculate the sum without using sum().
4. Count how many values are greater than 6.
5. Find the index of the first occurrence of 7.
'''
#1
def find_largest(numbers):
    largest = 0
    for n in numbers:
        if n > largest:
            largest = n
    return largest
print(find_largest(numbers))
#2
def find_smallest(numbers):
    smallest = 1000
    for n in numbers:
        if n < smallest:
            smallest = n
    return smallest
print(find_smallest(numbers))

#3
sum = 0
for n in numbers:
    sum += n
print(sum)

#4 
values_greater_than_six = []

for n in numbers:
    if n > 6:
        values_greater_than_six += [n]
print(len(values_greater_than_six))

#5 
def find_index(numbers):
    count = 0
    for n in numbers:
        if n != 7:
            count += 1
        if n == 7:
            return count           
print(find_index(numbers))