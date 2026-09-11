import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA

def main():
    df = pd.read_csv('Project/PCA_Project/Train.csv')
    df_small = df.sample(n=200, random_state=42)
    k = 2
    embedded_sentence = transform_sentence(df_small)
    data_centered = center_data(embedded_sentence)
    matrix = calculate_covariance(data_centered)
    eigenvalues, eigenvectors = calculate_eigen(matrix)
    eigenvalues_sorted, eigenvectors_sorted = sort_eigen(
        eigenvalues, eigenvectors
    )
    reduced_data = reduce(data_centered, eigenvectors_sorted, k)
    validate_pca(
        data_centered,
        reduced_data,
        eigenvalues_sorted,
        eigenvectors_sorted,
        k
    )

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


def calculate_eigen(matrix):
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    return eigenvalues, eigenvectors


def sort_eigen(eigenvalues, eigenvectors):
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues_sorted = eigenvalues[sorted_indices]
    eigenvectors_sorted = eigenvectors[:,sorted_indices]
    return eigenvalues_sorted, eigenvectors_sorted


def reduce(data_centered, eigenvectors_sorted, k):
    reduced_vectors = eigenvectors_sorted[:, :k]
    reduced_data = np.matmul(data_centered, reduced_vectors)
    return reduced_data


def validate_pca(
    data_centered,
    reduced_data,
    eigenvalues_sorted,
    eigenvectors_sorted,
    k
    ):
    pca = PCA(n_components=k, svd_solver="full")
    sklearn_reduced = pca.fit_transform(np.array(data_centered))

    for i in range(k):
        normal_diff = np.max(
            np.abs(reduced_data[:, i] - sklearn_reduced[:, i])
        )

        flipped_diff = np.max(
            np.abs(reduced_data[:, i] + sklearn_reduced[:, i])
        )

        print(
        f"PC{i + 1} normal diff: {normal_diff}, "
        f"flipped diff: {flipped_diff}"
    )

    top_eigenvectors = eigenvectors_sorted[:, :k]

    print(
        np.abs(
            top_eigenvectors.T @ pca.components_.T
        )
    )

    print("Mine:", eigenvalues_sorted[:k])
    print("sklearn:", pca.explained_variance_)

if __name__ == "__main__":
    main()
