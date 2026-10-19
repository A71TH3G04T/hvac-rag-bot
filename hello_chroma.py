import chromadb

# PersistentClient saves everything to a folder on your disk.
# No cloud, no API key, no signup. The folder is created automatically.
client = chromadb.PersistentClient(path="./chroma_db")

# A "collection" is like a table. get_or_create means:
# make it if it's new, open it if it already exists.
collection = client.get_or_create_collection(name="hvac_notes")

# The text we want to store and later search through.
documents = [
    "Superheat is the temperature of the refrigerant vapour above its boiling point. Target 8 to 12 degrees Fahrenheit on a fixed orifice system.",
    "Subcooling is the temperature of the liquid refrigerant below its condensing temperature. Target 10 to 15 degrees Fahrenheit on a TXV system.",
    "R-410A replaced R-22 in residential systems. It runs at higher pressure and must be charged as a liquid.",
    "Standard design airflow is 400 CFM per ton of cooling. In humid climates this drops to 350 CFM per ton.",
    "SEER2 replaced SEER in 2023. SEER2 numbers are about 4.5 percent lower than the old SEER number for the same equipment.",
]

# Every document needs a unique id so you can update or delete it later.
ids = ["doc1", "doc2", "doc3", "doc4", "doc5"]

# upsert = add if new, overwrite if the id already exists.
# Chroma embeds the text for you here, using its own built-in model.
collection.upsert(documents=documents, ids=ids)

print("INGESTED:")
for i, d in zip(ids, documents):
    print(f"  {i}: {d[:60]}...")
print()

# The question we want answered.
question = "how cold should the refrigerant vapour be?"
print("QUERY:", question)
print()

# Chroma embeds the question, compares it to every stored document,
# and returns the closest n_results.
results = collection.query(query_texts=[question], n_results=2)

# The results come back nested one level deep, because you can
# send several queries at once. [0] = the first (only) query.
print("RESULTS:")
for doc, doc_id, distance in zip(
    results["documents"][0],
    results["ids"][0],
    results["distances"][0],
):
    print(f"  {doc_id}  (distance {distance:.4f})")
    print(f"     {doc}")
    print()

print("Lower distance = closer meaning = better match.")
print(f"\nCollection now holds {collection.count()} documents.")