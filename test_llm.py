import os

from dotenv import load_dotenv
from google import genai

# Step 1: Load .env file
load_dotenv()
# Step 2: Get API key
api_key = os.getenv("GEMINI_API_KEY")


# Step 3: Create Gemini client
client = genai.Client(api_key=api_key)

# Step 4: Ask Gemini a question
response = client.models.generate_content(
    model = "gemini-3.5-flash-lite",
    contents="What is an Entity in DBMS? Explain simply."
)

# Step 5: Print the answer
print("Gemini Response:")
print(response.text)