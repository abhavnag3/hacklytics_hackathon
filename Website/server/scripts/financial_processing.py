import os
import json
import chromadb
from chromadb.config import Settings
from embeddings import query  

base_dir = os.path.dirname(os.path.abspath(__file__))
literacy_txt_path = os.path.join(base_dir, "..", "data", "literacy.txt")
literacy_json_path = os.path.join(base_dir, "..", "data", "literacy.json")
chunked_literacy_path = os.path.join(base_dir, "..", "data", "chunked_literacy.json")

with open(literacy_txt_path, "r", encoding="utf-8") as file:
    raw_text = file.readlines()

literacy_terms = []
current_term = {}

for line in raw_text:
    line = line.strip()
    if not line:
        continue  

    if "Term:" in line:
        if current_term:
            literacy_terms.append(current_term)
        current_term = {"name": line.replace("Term:", "").strip(), "definition": ""}

    elif current_term:
        current_term["definition"] += " " + line.strip()

if current_term:
    literacy_terms.append(current_term)

with open(literacy_json_path, "w", encoding="utf-8") as f:
    json.dump(literacy_terms, f, indent=4)

print(f"✅ Converted literacy.txt to literacy.json at {literacy_json_path}")

chunked_literacy = []

def chunk_literacy(term):
    return [{
        "text": f"{term.get('name', 'Unknown Term')}: {term.get('definition', '')}",
        "metadata": {"type": "literacy", "name": term.get("name", "Unknown Term")}
    }]

for term in literacy_terms:
    chunked_literacy.extend(chunk_literacy(term))

with open(chunked_literacy_path, "w", encoding="utf-8") as f:
    json.dump(chunked_literacy, f, indent=4)

print(f"✅ Chunked literacy terms saved to {chunked_literacy_path}")

client = chromadb.Client(Settings(persist_directory="chromadb_store"))
collection = client.get_or_create_collection(name="literacy_data")

if collection.count() == 0:  # 🔥 Forces embedding if none exist
    print("🔄 No embeddings found. Generating embeddings now...")

    texts = [chunk["text"] for chunk in chunked_literacy]
    output = query(texts)  

    if not output or len(output) != len(texts):
        print("❌ ERROR: Embedding output is empty or incorrect!")
        exit()

    for idx, chunk in enumerate(chunked_literacy):
        collection.add(
            documents=[chunk["text"]],
            embeddings=[output[idx]],
            ids=[f"doc_{idx}"],
            metadatas=[chunk["metadata"]]
        )

    print(f"✅ Successfully stored {collection.count()} literacy embeddings in ChromaDB.")
else:
    print(f"✅ {collection.count()} embeddings already exist. Skipping re-embedding.")

disable_reembedding = os.path.join(base_dir, "..", "data", "disable_reembedding.txt")

if not os.path.exists(disable_reembedding):
    with open(disable_reembedding, "w") as f:
        f.write("Embeddings are now stored. No need to regenerate unless dataset changes.")
    print("🚀 Future re-embedding disabled. Delete 'disable_reembedding.txt' to regenerate embeddings.")
