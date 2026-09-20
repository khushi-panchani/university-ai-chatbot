
# Model is not imported or loaded when the server starts
model = None


def get_embedding_model():
    global model

    if model is None:
        print("Loading embedding model...")

        # Import only when the model is actually needed
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(
            "all-MiniLM-L6-v2",
            device="cpu"
        )

        print("Embedding model loaded successfully!")

    return model


def create_embedding(text):
    embedding_model = get_embedding_model()

    embedding = embedding_model.encode(text)

    return embedding


# from sentence_transformers import SentenceTransformer


# # Load the pretrained embedding model
# model = SentenceTransformer("all-MiniLM-L6-v2")


# # Our first test sentence
# sentence = "What is an Entity in DBMS?"


# # Convert sentence into an embedding vector
# embedding = model.encode(sentence)


# # Display the result
# print("Embedding created successfully!")

# print("Embedding type:", type(embedding))

# print("Embedding shape:", embedding.shape)

# print("First 10 numbers:", embedding[:10])