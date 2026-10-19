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
MODEL = "gemini-3.6-flash"
DEBUG = True

chroma = chromadb.PersistentClient(path="./chroma_db")
collection = chroma.get_or_create_collection(name="hvac_manual")


def retrieve(question, n_results=3):
    """Find the chunks whose meaning is closest to the question."""
    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=question,
        config=types.EmbedContentConfig(task_type="RETRIEVAL_QUERY"),
    )
    query_vector = result.embeddings[0].values
    results = collection.query(query_embeddings=[query_vector], n_results=n_results)
    return results["documents"][0]

def answer(question):
    """Find chunks, hand them to Gemini, return Gemini's written answer."""
    chunks = retrieve(question)
    if DEBUG:
        print("\n[chunks used]")
        for c in chunks:
            print("  -", c[:70].replace("\n", " "))
        print()
    context = "\n\n---\n\n".join(chunks)

    system_instruction = f"""You are an HVAC assistant.

Below are excerpts from an HVAC manual.

Rules:
- If the excerpts help answer the question, base your answer on them.
- If the question is simple general knowledge and the excerpts don't cover it, you may answer from your own knowledge.
- Write the answer in your own words. Keep it clear and short. Do not copy the excerpts word for word.

EXCERPTS:
{context}
"""

    response = client.models.generate_content(
        model=MODEL,
        contents=question,
        config=types.GenerateContentConfig(system_instruction=system_instruction),
    )
    return response.text

if __name__ == "__main__":
    print("HVAC bot ready. Type 'exit' to quit.\n")

    while True:
        question = input("You: ").strip()

        if question.lower() == "exit":
            print("Bye Ali.")
            break

        if not question:
            continue

        try:
            print("AI:", answer(question), "\n")
        except Exception as error:
            print("Failed:", type(error).__name__, "-", error, "\n")