import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

#model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
#sentences = ["The weather is lovely today", "It's so sunny outside"]
#embeddings = model.encode(sentences)
#similarities = model.similarity(embeddings, embeddings)
#print(similarities)

df = pd.read_csv('Project/PCA_Project/Train.csv')
df_small = df.sample(n=200, random_state=42)
print(df.head(1))

def transform_sentence(data):
    '''
    This function takes a csv file and adds the first column into a list. 
    Then we use Bert Sentence Transformer to vectorize the sentence from the data
    it returns a list of the embedding
    '''
    my_list = data.iloc[:,0].tolist()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    embeddings = model.encode(my_list)
    return embeddings
embedded_sentence = transform_sentence(df_small)
print(embedded_sentence[0])
print(embedded_sentence.shape)
print(embedded_sentence.shape[1])
'''
def reduce_eigen_dimension(sentence_embedding, num_of_components):

    We will first initialize a dictionary called eigen. This is where we want to store our eigenvector/eigenvalue pairs
    Then we will calculate the covariance .

    eigen = {}
    total = 0
    for dim[0] in sentence_embedding:
'''
def center_data(sentence_embedding):
    '''
    This function takes the sentence embeddings we get from the transform_sentence function
    and centers it to focus on the variance of the vectors. we do this by 
    finding the mean of the nth column and subtracting that over each element in that nth column. 
    We do this through 2 main forloops. The first forloops' purpose is to calculate the means of each column. The second forloop is to subtract the mean and "center" the data.
    '''
    means = []
    for dimension in range(sentence_embedding.shape[1]):
        total = 0
        for row in sentence_embedding:
            total = row[dimension] + total
        mean = total / len(sentence_embedding)
        means.append(mean)

    centered_data = []
    for row in sentence_embedding:
        centered_review = []
        for dimension in range(sentence_embedding.shape[1]):
            centering = row[dimension] - means[dimension]
            centered_review.append(centering)
        centered_data.append(centered_review)
    return centered_data
data_centered = center_data(embedded_sentence)

print(data_centered[:5])
print(len(data_centered))
print(len(data_centered[0]))

def calculate_covariance(centered_data):
    covariance_matrix = []
    for first_dimension in range(len(centered_data[0])):
        covariance_row = []
        for second_dimension in range(len(centered_data[0])):
            products = []
            for array in centered_data: #this for look iterates through every array in the data and calculates the product of the elements. it then adds it to the products list
                products += [array[first_dimension] * array[second_dimension]]
            sum_products = sum(products) #adds all the products todether
            denominator = len(products) - 1 #takes the length and subtracts by 1
            cov = sum_products / denominator #calculates the covariance
            covariance_row.append(cov)
        
        covariance_matrix.append(covariance_row)
    return covariance_matrix

matrix = calculate_covariance(data_centered)

print(len(matrix))
print(len(matrix[0]))
print(matrix[0][1])
print(matrix[1][0])

print(matrix[10][25])
print(matrix[25][10])

matrix_np = np.array(matrix)
cov_np = np.cov(data_centered, rowvar=False)
print(np.allclose(cov_np, matrix))

