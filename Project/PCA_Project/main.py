import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

def main():


    # Load data
    df = pd.read_csv('Project/PCA_Project/Train.csv')
    df_small = df.sample(n=500, random_state=42)
    labels = df_small["label"].to_numpy()


    k = 2


    # Create embedding
    embedded_sentence = transform_sentence(df_small)
    data_centered = center_data(embedded_sentence)
    matrix = calculate_covariance(data_centered)


    # Proccess matrix through PCA
    eigenvalues, eigenvectors = calculate_eigen(matrix)
    eigenvalues_sorted, eigenvectors_sorted = sort_eigen(
        eigenvalues, eigenvectors
    )


    reduced_data = reduce(data_centered, eigenvectors_sorted, k)


    # Calculate variance
    variance_dict = analyze_variation(eigenvalues_sorted)

    print("variation near 50% ", find_k(variance_dict,.5))
    print("variation near 80% ", find_k(variance_dict,.8))
    print("variation near 90% ", find_k(variance_dict,.9))
    print("variation near 95% ", find_k(variance_dict,.95))



    n_samples = embedded_sentence.shape[0]
    n_features = embedded_sentence.shape[1]
    max_components = min(n_samples - 1, n_features)

    reduced_for_analysis = reduce(
        data_centered,
        eigenvectors_sorted,
        max_components
    )


    # Calculate Cohen's D
    label_cohen_d = analyze_label_cohen_d(reduced_for_analysis, labels)


    # Calculate individual explained variance
    iev_dict = individual_explained_variance(eigenvalues_sorted)


    # Validate the PCA with SKLearns PCA algorithms
    validate_pca(
        data_centered,
        reduced_data,
        eigenvalues_sorted,
        eigenvectors_sorted,
        k
    )


    # Create the graphs
    plot_pca(reduced_data, labels)
    plot_variance(variance_dict)
    plot_cohen_d(label_cohen_d)
    plot_iev_vs_cohen_d(iev_dict, label_cohen_d)


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
    '''
    Takes our centered data and initializesa list called covariance matrix. it then creates an nxn covariance matrix
    
    '''
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
    '''
    Uses Numpy linear algebra function to take a matrix and return its eigenvalues and eigenvectors
    
    '''
    eigenvalues, eigenvectors = np.linalg.eigh(matrix)
    return eigenvalues, eigenvectors


def sort_eigen(eigenvalues, eigenvectors):
    '''
    Takes the eigenvalues and eigenvectors and, through numpy's argsort(), sorts them. It then returns eigenvalues_sorted and eigenvectors_sorted
    '''
    sorted_indices = np.argsort(eigenvalues)[::-1]
    eigenvalues_sorted = eigenvalues[sorted_indices]
    eigenvectors_sorted = eigenvectors[:,sorted_indices]
    return eigenvalues_sorted, eigenvectors_sorted


def reduce(data_centered, eigenvectors_sorted, k):
    '''
    reduces the vectors of eigenvectors_sorted to k, it is then projected onto data_centered through matrix multiplication
    '''
    reduced_vectors = eigenvectors_sorted[:, :k]
    reduced_data = np.matmul(data_centered, reduced_vectors)
    return reduced_data

def p_variation(eigenvalues_sorted, k):
    '''
    finds how much of the total variance is explained by the first k principal components.
    '''
    ratio = sum(eigenvalues_sorted[:k]) / sum(eigenvalues_sorted)
    return ratio

def analyze_variation(eigenvalues_sorted):
    '''
    Calculate cumulative explained variance for differentnumbers of principal components.

    Returns a dictionary mapping k to the proportion of total variance explained by the first k principal components.
    
    '''
    variation_by_k = {}
    for k in range(1, len(eigenvalues_sorted) + 1):
        key = k
        value = p_variation(eigenvalues_sorted, k)
        variation_by_k[key] = value
    return variation_by_k

def find_k(variance_dict, target):
    '''
    Finds a k that is less than or equal to the target.
    '''
    for key, values in variance_dict.items():
        if values >= target:
            return key

    return False

def compare_labels_on_pc(reduced_data, labels, pc_index):

    pc_values = reduced_data[:, pc_index]
    label_0_values = pc_values[labels == 0]
    label_1_values = pc_values[labels == 1]
    length_0 = len(label_0_values)
    length_1 = len(label_1_values)
    mean_0 = np.mean(label_0_values)
    mean_1 = np.mean(label_1_values)
   
    std_0 = np.std(label_0_values, ddof=1)
    std_1 = np.std(label_1_values, ddof=1)
    pstd = np.sqrt(((length_0 - 1) * std_0**2) + ((length_1 - 1) * std_1**2) / (length_0 + length_1 -2) )
    d = (mean_0 - mean_1) / pstd
    return d

def analyze_label_cohen_d(reduced_data, labels):
    differences = {}

    for pc_index in range(reduced_data.shape[1]):
        difference = compare_labels_on_pc(
            reduced_data,
            labels,
            pc_index
        )

        differences[pc_index + 1] = difference

    return differences

def individual_explained_variance(eigenvalues_sorted):
    iev_dict = {} 

    for i in range(len(eigenvalues_sorted)):  # range needs an integer
        key = i + 1
        iev = eigenvalues_sorted[i] / sum(eigenvalues_sorted)
        iev_dict[key] = iev  

    return iev_dict

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


def plot_pca(reduced_data, labels):
    labels = np.array(labels)

    plt.scatter(
        reduced_data[labels == 0, 0],
        reduced_data[labels == 0, 1],
        label="0"
    )

    plt.scatter(
        reduced_data[labels == 1, 0],
        reduced_data[labels == 1, 1],
        label="1"
    )

    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("PCA of Sentence Embeddings")
    plt.legend()
    plt.show()


def plot_variance(variance_dict):
    x_coords = list(variance_dict.keys())
    y_coords = list(variance_dict.values())

    plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b')

    plt.xlabel('K values (X)')
    plt.ylabel('Variance (Y)')
    plt.title('Line Plot of k values vs variance')


    plt.show()

def plot_cohen_d(cohen_dict):
    x_coords = list(cohen_dict.keys())
    y_coords = list(cohen_dict.values())

    plt.plot(x_coords, y_coords, marker='o', linestyle='-', color='b')
    #plt.xticks(np.arange(0, 20, 1))
    plt.xlabel('Principal Component # (X)')
    plt.ylabel('Cohens D')
    plt.title('PC# vs Cohens d')


    plt.show()

def plot_iev_vs_cohen_d(iev_dict, cohen_dict):
    x_coords = [iev_dict[key] for key in cohen_dict]
    y_coords = [abs(value) for value in cohen_dict.values()]

    plt.scatter(x_coords, y_coords)
    plt.xlabel('Individual Explained Variance')
    plt.ylabel('Absolute Cohens D')
    plt.title('Individual Explained Variance vs Cohen D')

    print(len(x_coords), len(y_coords))
    
    plt.show()


if __name__ == "__main__":
    main()
