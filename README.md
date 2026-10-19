# HVAC RAG Bot

A small chatbot that answers HVAC questions by reading a manual first and then writing its answer with Gemini.

I built this while learning RAG (retrieval augmented generation). The idea is simple. Instead of pasting a whole document into the prompt every time, the bot searches the document, picks the few pieces that match the question, and gives only those to Gemini.

## How it works

You type a question in the terminal. Behind the scenes:

1. The manual is cut into chunks, paragraph by paragraph, about 800 characters each.
2. Each chunk is turned into a list of numbers (an embedding) using Gemini and saved in a local ChromaDB folder.
3. Your question is turned into numbers the same way, and ChromaDB finds the 3 chunks with the closest meaning.
4. Those 3 chunks go into Gemini's instructions, and it writes the answer.

Steps 1 and 2 run once. Steps 3 and 4 run on every question.

## Example

```
You: why is my ac not cooling?

[chunks used]
  - One ton of cooling capacity equals twelve thousand British thermal uni
  - A frozen evaporator coil is almost always caused by low airflow or low
  - Water leaking from the indoor unit is usually a blocked condensate dra

AI: Your AC may not be cooling because of a few common problems:
* Airflow restrictions and a frozen coil ...
* Low refrigerant ...
(shortened)
```

The `[chunks used]` lines are a debug switch (`DEBUG = True` in `rag_bot.py`). I left it on because it shows exactly what Gemini was given.

## Run it yourself

I used Python 3.14, but any recent Python 3 should work.

```
pip install google-genai python-dotenv chromadb
```

Get an API key from Google AI Studio and put it in a file called `.env` next to the scripts:

```
GEMINI_API_KEY=your_key_here
```

Then:

```
python ingest.py     # reads hvac_manual.txt and builds the database, run once
python rag_bot.py    # ask your questions, type exit to quit
```

## What's in the folder

- `hvac_manual.txt` is a short sample manual (about 11,000 characters) that I used for testing
- `chunker.py` cuts the manual into chunks and prints the first three
- `ingest.py` chunks the manual, embeds every chunk and stores it in ChromaDB
- `searcher.py` takes a question and shows the 3 closest chunks with their distances
- `rag_bot.py` is the full bot
- `hello_chroma.py` is my first ChromaDB experiment
- `check_env.py` checks that the API key loads

## Things I noticed while testing

- Search works on meaning, not exact words. "how do I know if my ac gas is low" found the paragraph about low refrigerant charge even though neither word appears in the question.
- Distance tells you how good a match is (lower is closer). With this manual, a good match was around 0.4 and a weak one was 0.65 or more. Those numbers only describe this manual, not RAG in general.
- It only fetches 3 chunks. The manual has a paragraph about capacitors, but it did not make the top 3 for "why is my ac not cooling", so Gemini filled that part in from its own knowledge.
- The bot is allowed to answer simple general questions even when the manual doesn't cover them, and it doesn't say which parts came from the manual. I chose that on purpose, but it means you can't tell the two apart.
- It has no memory between questions. "How do I fix it?" after a first question won't work.

## What I want to add next

- Chat history, so follow-up questions work
- Labels on answers: "from the manual" or "general knowledge"
- Try more than 3 chunks, and overlap between chunks
- Read PDFs, not just .txt files

Built with Python, the Gemini API (`gemini-embedding-001` for embeddings, `gemini-3.6-flash` for answers) and ChromaDB.
