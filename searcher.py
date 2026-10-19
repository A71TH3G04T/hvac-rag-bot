import os
import chromadb
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("No API key found. Is GEMINI_API_KEY in your .env?")
    exit()

client = genai.Client(api_key=api_key)

chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection(name="hvac_manual")

question = input("Ask a question: ")

# turn the QUESTION into numbers (note: RETRIEVAL_QUERY this time)
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=question,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
)
query_vector = result.embeddings[0].values

# find the 3 chunks with the closest numbers
results = collection.query(query_embeddings=[query_vector], n_results=3)

for doc, dist in zip(results["documents"][0], results["distances"][0]):
    print(f"distance {dist:.4f}")
    print(doc[:200])
    print()