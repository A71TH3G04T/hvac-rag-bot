with open("hvac_manual.txt", "r", encoding="utf-8") as f:
    text = f.read()

CHUNK_SIZE = 800

# split into paragraphs first - blank line between them
paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]

chunks = []
current = ""

for para in paragraphs:
    # would adding this paragraph push us over the limit?
    if len(current) + len(para) + 2 > CHUNK_SIZE and current:
        chunks.append(current.strip())
        current = para
    else:
        current = current + "\n\n" + para if current else para

# don't forget the last one
if current.strip():
    chunks.append(current.strip())

print(f"{len(text)} characters -> {len(chunks)} chunks\n")

for n, chunk in enumerate(chunks[:3], 1):
    print(f"--- CHUNK {n} ({len(chunk)} chars) ---")
    print(chunk)
    print()