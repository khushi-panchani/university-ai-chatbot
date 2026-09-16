from src.pdf_loader import extract_text_from_pdf
from src.text_chunker import split_text_into_chunks
from src.embedding_model import model
from src.vector_store import create_vector_index


# Step 1: Extract text from PDF
text = extract_text_from_pdf("data/DBMS.pdf")

print("PDF text extracted successfully!")


# Step 2: Split text into chunks
chunks = split_text_into_chunks(
    text,
    chunk_size=500,
    chunk_overlap=50
)

print("Total chunks:", len(chunks))


# Step 3: Convert chunks into embeddings
embeddings = model.encode(chunks)

print("Embeddings created successfully!")


# Step 4: Create FAISS vector index
index = create_vector_index(embeddings)

print("FAISS index created successfully!")


# Step 5: Display index information
print("Number of vectors:", index.ntotal)
print("Vector dimension:", index.d)