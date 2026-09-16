from src.pdf_loader import extract_text_from_pdf
from src.text_chunker import split_text_into_chunks
from src.embedding_model import model
from src.vector_store import create_vector_index, search_vector_index
# Step 1: Extract text from PDF
text = extract_text_from_pdf("data/DBMS.pdf")
# Step 2: Split text into chunks
chunks = split_text_into_chunks(
    text,
    chunk_size=500,
    chunk_overlap=50
)
# Step 3: Convert chunks into embeddings
embeddings = model.encode(chunks)
# Step 4: Create FAISS index
index = create_vector_index(embeddings)
# Step 5: Ask a question
question = "What is an Entity in DBMS?"
# Step 6: Convert question into embedding
query_embedding = model.encode([question])
# Step 7: Search similar chunks
distances, indices = search_vector_index(
    index,
    query_embedding,
    k=3
)
# Step 8: Display results
print("\nQuestion:", question)

print("\nMost relevant chunks:\n")

for i, index_value in enumerate(indices[0]):

    print(f"Result {i + 1}")
    print("Distance:", distances[0][i])
    print("Chunk:\n", chunks[index_value])
    print("-" * 50)