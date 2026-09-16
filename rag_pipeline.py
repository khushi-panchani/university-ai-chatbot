import os

from dotenv import load_dotenv
from google import genai

from src.pdf_loader import extract_text_from_pdf
from src.text_chunker import split_text_into_chunks
from src.embedding_model import model
from src.vector_store import (
    create_vector_index,
    search_vector_index
)


# Step 1: Load Gemini API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


# Step 2: Load PDF
print("Loading PDF...")

text = extract_text_from_pdf("data/DBMS.pdf")

print("PDF loaded successfully!")


# Step 3: Split PDF text into chunks
print("Splitting text into chunks...")

chunks = split_text_into_chunks(text)

print("Text split successfully!")
print("Total chunks:", len(chunks))


# Step 4: Generate embeddings
print("Generating embeddings...")

embeddings = model.encode(chunks)

print("Embeddings generated successfully!")
print("Embedding shape:", embeddings.shape)


# Step 5: Create FAISS vector index
print("Creating FAISS vector index...")

index = create_vector_index(embeddings)

print("Vector index created successfully!")


# Step 6: Start chatbot loop
print("\nUniversity Notes Chatbot is ready!")
print("Type 'exit' to close the chatbot.")


while True:

    # Ask the user a question
    question = input("\nYou: ").strip()

    # Stop chatbot
    if question.lower() == "exit":
        print("Chatbot closed. Goodbye!")
        break

    # Avoid empty questions
    if not question:
        print("Please enter a question.")
        continue

    # Step 7: Convert question into an embedding
    query_embedding = model.encode([question])

    # Step 8: Search only the best matching chunk
    distances, indices = search_vector_index(
        index,
        query_embedding,
        k=1
    )

    # Step 9: Get the best chunk
    best_chunk = chunks[indices[0][0]]

    # Step 10: Create context
    context = best_chunk

    # Step 11: Create prompt for Gemini
    prompt = f"""
You are a university notes chatbot.

Answer the user's question using only the provided context.

If the answer is not available in the context, say:
"I could not find this information in the provided notes."

Give one clear and proper answer.
Do not mention chunks, embeddings, FAISS, or the retrieval process.
Explain in simple language.

Context:
{context}

Question:
{question}
"""

    # Step 12: Generate answer
    print("\nThinking...")

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    # Step 13: Display only the final answer
    print("\nBot:", response.text)