from src.pdf_loader import extract_text_from_pdf
from src.text_chunker import split_text_into_chunks


text = extract_text_from_pdf("data/DBMS.pdf")


chunks = split_text_into_chunks(
    text,
    chunk_size=500,
    chunk_overlap=50
)


print("Total chunks:", len(chunks))

print("\nFirst chunk:\n")
print(chunks[0])