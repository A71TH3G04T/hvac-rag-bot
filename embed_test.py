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

# ---------- 1. CHUNK (same as chunker.py) ----------
with open("hvac_manual.txt", "r", encoding="utf-8") as f:
    text = f.read()

CHUNK_SIZE = 800
paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
chunks = []
current = ""
for para in paragraphs:
    if len(current) + len(para) + 2 > CHUNK_SIZE and current:
        chunks.append(current.strip())
        current = para
    else:
        current = current + "\n\n" + para if current else para
if current.strip():
    chunks.append(current.strip())

print("chunks made:", len(chunks))

# ---------- 2. EMBED ALL CHUNKS IN ONE CALL ----------
result = client.models.embed_content(
    model="gemini-embedding-001",
    contents=chunks,
    config=types.EmbedContentConfig(task_type="RETRIEVAL_DOCUMENT"),
)

vectors = [e.values for e in result.embeddings]

print("vectors made:", len(vectors))
print("numbers in each vector:", len(vectors[0]))

# ---------- 3. STORE IN CHROMA ----------
chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection(name="hvac_manual")

ids = [f"chunk{i}" for i in range(len(chunks))]

collection.upsert(
    ids=ids,
    documents=chunks,
    embeddings=vectors,
)

print("stored in Chroma:", collection.count())