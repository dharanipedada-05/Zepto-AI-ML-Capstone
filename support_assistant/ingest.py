from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer


# Folder where this script is located
BASE_DIR = Path(__file__).resolve().parent

# Documents and ChromaDB folders
DOCS_DIR = BASE_DIR / "docs"
CHROMA_DIR = BASE_DIR / "chroma_db"

print("Looking for documents in:", DOCS_DIR)
print("Documents found:", list(DOCS_DIR.glob("*.txt")))

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path=str(CHROMA_DIR))

collection = client.get_or_create_collection(
    name="zepto_policies",
    metadata={"hnsw:space": "cosine"}
)

# Add documents
for file_path in sorted(DOCS_DIR.glob("*.txt")):

    text = file_path.read_text(encoding="utf-8").strip()

    if not text:
        continue

    embedding = embedding_model.encode(text).tolist()

    collection.upsert(
        ids=[file_path.stem],
        documents=[text],
        embeddings=[embedding],
        metadatas=[{"source": file_path.name}]
    )

    print(f"Added: {file_path.name}")

print("\nTotal documents in ChromaDB:", collection.count())