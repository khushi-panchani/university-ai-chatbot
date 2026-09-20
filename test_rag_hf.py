from src.rag_engine import load_pdf, get_answer


pdf_path = "data/DBMS.pdf"

print("====================================")
print("Testing RAG with Hugging Face")
print("====================================")

# Load PDF and create embeddings + FAISS index
load_pdf(pdf_path)

print("\nPDF processing completed!")

# Ask a question
question = "What is an Entity in DBMS?"

print("\nQuestion:", question)
print("\nGenerating answer...\n")

answer = get_answer(question)

print("====================================")
print("ANSWER")
print("====================================")
print(answer)
print("====================================")