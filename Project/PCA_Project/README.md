This is a project that I started for my Linear Algebra class. It uses Principal Component Analysis to transform high-dimensional vectors into lower-dimensional representation. An important mathmatical concept for this transformation is Eigenstuff. What PCA does is find the eigenvectors of the covariance matrix, then rank them by their eigenvalues. Then we can reduce the components by their rank of eigenvalue.
---
The current pipeline for this project is:
# 1. Create sentences
# 2. Convert sentences into numerical embeddings
# 3. Put embeddings into a matrix
# 4. Reduce the dimensions with PCA
# 5. Plot the resulting points
# 6. Examine whether similar sentence groups cluster
---