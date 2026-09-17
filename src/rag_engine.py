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


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


# These variables will store the current PDF data
chunks = []
index = None


def load_pdf(pdf_path):
    """
    Loads the uploaded PDF and prepares it for questions.
    """

    global chunks, index

    print("Loading uploaded PDF...")

    text = extract_text_from_pdf(pdf_path)

    print("PDF loaded successfully!")

    print("Splitting text into chunks...")

    chunks = split_text_into_chunks(text)

    print("Total chunks:", len(chunks))

    print("Generating embeddings...")

    embeddings = model.encode(chunks)

    print("Embeddings generated successfully!")

    print("Creating FAISS vector index...")

    index = create_vector_index(embeddings)

    print("Vector index created successfully!")

    return True


def get_answer(question):
    """
    Answers a question using the uploaded PDF.
    """

    global chunks, index

    question = question.strip()

    if not question:
        return "Please enter a question."

    if index is None or not chunks:
        return "Please upload a PDF first."

    # Convert question into embedding
    query_embedding = model.encode([question])

    # Search three relevant chunks
    distances, indices = search_vector_index(
        index,
        query_embedding,
        k=3
    )

    # Collect relevant chunks
    retrieved_chunks = [
        chunks[i] for i in indices[0]
    ]

    context = "\n\n".join(retrieved_chunks)

    prompt = f"""
You are a university notes chatbot.

Answer the user's question using only the provided context.

If the answer is not available in the context, say:
"I could not find this information in the uploaded PDF."

Give one clear and proper answer.
Explain in simple language.
Do not mention chunks, embeddings, FAISS, or retrieval.

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    return response.text