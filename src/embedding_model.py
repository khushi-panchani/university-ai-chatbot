import os
import numpy as np
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_TOKEN")

if not HF_TOKEN:
    raise ValueError("HF_TOKEN not found in .env file")


# Connect to Hugging Face Inference API
client = InferenceClient(
    provider="hf-inference",
    api_key=HF_TOKEN
)

MODEL_NAME = "BAAI/bge-small-en-v1.5"


class HFEmbeddingModel:

    def encode(self, texts):

        # Convert single text into a list
        if isinstance(texts, str):
            texts = [texts]

        embeddings = client.feature_extraction(
            texts,
            model=MODEL_NAME
        )

        # Convert result into NumPy array
        return np.asarray(embeddings, dtype="float32")


# Create embedding model
model = HFEmbeddingModel()


def get_embedding_model():
    return model


def create_embedding(text):
    embedding_model = get_embedding_model()
    return embedding_model.encode(text)