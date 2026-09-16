import faiss
import numpy as np

def create_vector_index(embeddings):
        # Convert embeddings into float32
    embeddings = np.array(embeddings).astype("float32")
        # Get the number of dimensions
    dimension = embeddings.shape[1]
        # Create FAISS index
    index = faiss.IndexFlatL2(dimension)
        # Add embeddings to the index
    index.add(embeddings)
    return index

def search_vector_index(index, query_embedding, k=3):
       # Convert query embedding into float32
    query_embedding = np.array(query_embedding).astype("float32")
       # Search similar vectors
    distances, indices = index.search(query_embedding, k)

    return distances, indices