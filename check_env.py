import os
from dotenv import load_dotenv, find_dotenv

print("Using .env at:", find_dotenv())

load_dotenv()
key = os.getenv("GEMINI_API_KEY")
print("Key found    :", key is not None)