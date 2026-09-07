'''
This is a simple exercise to understanding covariance, one of the parts of the pca pipeline. Covariance measures how two embeddings vary together across review. 
If one moves up will the other move down>
'''
data = [
    [ 2,  4],
    [-1, -2],
    [ 1,  2],
    [-2, -4]
]
products = [x * y for x,y in data] 
sum_products = sum(products)
print(sum_products)

denominator = len(products) - 1

cov = sum_products / denominator
print(cov)