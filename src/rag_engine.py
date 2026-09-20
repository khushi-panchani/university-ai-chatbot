import os
import time

from dotenv import load_dotenv
from google import genai

from src.pdf_loader import extract_text_from_pdf
from src.text_chunker import split_text_into_chunks
from src.embedding_model import get_embedding_model
from src.vector_store import (
    create_vector_index,
    search_vector_index
)

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found")

client = genai.Client(api_key=api_key)

chunks = []
index = None


# --------------------------------------------------
# Load PDF and create FAISS index
# --------------------------------------------------

def load_pdf(pdf_path):
    global chunks, index

    print("Loading uploaded PDF...")

    text = extract_text_from_pdf(pdf_path)

    print("PDF loaded successfully!")

    print("Splitting text into chunks...")

    chunks = split_text_into_chunks(text)

    print("Total chunks:", len(chunks))

    print("Generating embeddings...")

    embedding_model = get_embedding_model()

    embeddings = embedding_model.encode(chunks)

    print("Embeddings generated successfully!")

    print("Creating FAISS vector index...")

    index = create_vector_index(embeddings)

    print("Vector index created successfully!")

    return True


# --------------------------------------------------
# Ask Gemini with automatic retry
# --------------------------------------------------

def generate_gemini_answer(prompt):

    max_attempts = 3

    for attempt in range(1, max_attempts + 1):

        try:
            print(f"Sending question to Gemini... Attempt {attempt}/{max_attempts}")

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=prompt
            )

            print("Answer generated successfully!")

            return response.text

        except Exception as error:

            error_message = str(error)

            # Retry only temporary errors
            temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
                or "429" in error_message
                or "RESOURCE_EXHAUSTED" in error_message
                or "high demand" in error_message.lower()
            )

            if temporary_error and attempt < max_attempts:

                wait_time = 2 ** attempt

                print(
                    f"Gemini temporarily unavailable. "
                    f"Retrying in {wait_time} seconds..."
                )

                time.sleep(wait_time)

            else:

                print("Gemini request failed.")

                return (
                    "The AI service is temporarily busy. "
                    "Please try again in a moment."
                )


# --------------------------------------------------
# Get answer from uploaded PDF
# --------------------------------------------------

def get_answer(question):

    global chunks, index

    question = question.strip()

    if not question:
        return "Please enter a question."

    if index is None or not chunks:
        return "Please upload a PDF first."

    # Create embedding for user's question
    embedding_model = get_embedding_model()

    query_embedding = embedding_model.encode([question])

    # Search FAISS
    distances, indices = search_vector_index(
        index,
        query_embedding,
        k=3
    )

    # Get retrieved chunks
    retrieved_chunks = [
        chunks[i]
        for i in indices[0]
    ]

    context = "\n\n".join(retrieved_chunks)

    # --------------------------------------------------
    # Prompt for Gemini
    # --------------------------------------------------

    prompt = f"""
You are a helpful university notes chatbot.

Answer the user's question using only the provided context
from the uploaded PDF.

Follow this answer format:

### Definition:
Start with a simple and clear definition of the topic.

### Explanation:
Explain the topic in 2 or 3 easy-to-understand lines.

### Example from the PDF:
Give an example related to the topic using the provided notes.
If the PDF contains a suitable example, use that example.
Do not create an example that is not supported by the context.

### Important Points:
Give 2 or 3 important points about the topic.

Rules:

- Use simple university-level language.
- Give a slightly detailed answer.
- Use headings and bullet points where helpful.
- Answer only from the provided context.
- Do not mention chunks, embeddings, FAISS, retrieval, or the AI system.
- Do not give information that is not present in the uploaded PDF.
- If the answer is not available in the context, say:

"I could not find this information in the uploaded PDF."

Context from the uploaded PDF:

{context}

User Question:

{question}
"""

    # Send prompt to Gemini with retry
    answer = generate_gemini_answer(prompt)

    return answer