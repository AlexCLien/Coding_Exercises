import pandas as pd
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
sentences = ["The weather is lovely today", "It's so sunny outside"]
embeddings = model.encode(sentences)
similarities = model.similarity(embeddings, embeddings)
print(similarities)

df = pd.read_csv('Project/PCA_Project/Train.csv')
print(df.head(1))