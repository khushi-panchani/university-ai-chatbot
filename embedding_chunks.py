from src.pdf_loader import extract_text_from_pdf
from src.text_chunker import split_text_into_chunks
from sentence_transformers import SentenceTransformer


# Step 1: Extract text from PDF
text = extract_text_from_pdf("data/DBMS.pdf")

print("PDF text extracted successfully!")
print("Total characters:", len(text))


# Step 2: Split extracted text into chunks
chunks = split_text_into_chunks(
    text,
    chunk_size=500,
    chunk_overlap=50
)

print("Total chunks:", len(chunks))


# Step 3: Load the embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

print("Embedding model loaded successfully!")


# Step 4: Convert all chunks into embeddings
embeddings = model.encode(
    chunks,
    show_progress_bar=True
)

print("All chunks converted into embeddings!")


# Step 5: Display embedding information
print("Embedding type:", type(embeddings))
print("Embedding shape:", embeddings.shape)


# Step 6: Display first chunk and its embedding
print("First chunk:", chunks[0][:100])

print("First embedding:", embeddings[0][:10])