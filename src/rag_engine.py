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


# Load API key
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


# These variables store the current PDF data
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
    Takes a question and returns a detailed answer
    from the uploaded university PDF.
    """

    global chunks, index

    question = question.strip()

    if not question:
        return "Please enter a question."

    if index is None or not chunks:
        return "Please upload a PDF first."

    # Convert the question into an embedding
    query_embedding = model.encode([question])

    # Search the three most relevant chunks
    distances, indices = search_vector_index(
        index,
        query_embedding,
        k=3
    )

    # Collect the retrieved chunks
    retrieved_chunks = [
        chunks[i] for i in indices[0]
    ]

    # Combine the chunks into one context
    context = "\n\n".join(retrieved_chunks)

    # Detailed answer prompt
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

    print("Sending question to Gemini...")

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=prompt
    )

    print("Answer generated successfully!")

    return response.text