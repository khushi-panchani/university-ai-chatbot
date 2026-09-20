import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env")

client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)

text = "What is an Entity in DBMS?"

embedding = client.feature_extraction(
    text,
    model="BAAI/bge-small-en-v1.5"
)

print("Embedding created successfully!")
print("Type:", type(embedding))
print("Shape:", embedding.shape)