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


#first_elements = [row[0] for row in embedded_sentence]
#mean_test = sum(first_elements) / len(embedded_sentence)
#print(mean_test)



#print(centered_data[:5])
#print(len(centered_data))
#print(len(centered_data[0]))

