from sentence_transformers import SentenceTransformer


# Step 1: Load the pretrained embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")


# Step 2: Create a function to convert text into embeddings
def create_embedding(text):

    embedding = model.encode(text)

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