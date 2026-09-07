'''
This is a simple exercise to understanding covariance, one of the parts of the pca pipeline. Covariance measures how two embeddings vary together across review. 
If one moves up will the other move down>
'''
import math

data = [
    [ 2,  4],
    [-1, -2],
    [ 1,  2],
    [-2, -4]
] #dataset
'''
First implementation 

products = [x * y for x,y in data]  #saves the sum of the two elements in the dataset into an array called products
sum_products = sum(products) #adds all the elements in the list
denominator = len(products) - 1 #takes the length and subtracts by 1

cov = sum_products / denominator
print(cov)
'''

products = [] #initialize array to store products
for array in data: #this for look iterates through every array in the data and calculates the product of the elements. it then adds it to the products list
    products += [math.prod(array)]
sum_products = sum(products) #adds all the products todether
denominator = len(products) - 1 #takes the length and subtracts by 1
print(sum_products)
cov = sum_products / denominator #calculates the covariance
print(cov)

