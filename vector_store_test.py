import numpy as np

from src.vector_store import create_vector_index


# Create sample embeddings
embeddings = np.array([
    [1.0, 2.0, 3.0],
    [2.0, 3.0, 4.0],
    [10.0, 10.0, 10.0]
])


# Create FAISS index
index = create_vector_index(embeddings)


print("FAISS index created successfully!")

print("Number of vectors:", index.ntotal)

print("Vector dimension:", index.d)