import os
import json
import chromadb
from chromadb.config import Settings
from embeddings import query  

base_dir = os.path.dirname(os.path.abspath(__file__))
loans_txt_path = os.path.join(base_dir, "..", "data", "loans.txt")
loans_json_path = os.path.join(base_dir, "..", "data", "loans.json")
chunked_loans_path = os.path.join(base_dir, "..", "data", "chunked_loans.json")

with open(loans_txt_path, "r", encoding="utf-8") as file:
    raw_text = file.read().strip()

sections = raw_text.split("#")  
loans = []

for section in sections:
    lines = [line.strip() for line in section.split("\n") if line.strip()]
    
    if len(lines) < 2:
        continue  # Skip empty sections

    loan_name = lines[0]
    loan_description = " ".join(lines[1:])  

    loans.append({
        "name": loan_name,
        "features": [loan_description]
    })

# ✅ Debugging: Check if loans were parsed correctly
print(f"🔍 Total loans parsed: {len(loans)}")
print(f"🔍 First few loans: {loans[:3]}")

with open(loans_json_path, "w", encoding="utf-8") as f:
    json.dump(loans, f, indent=4)

print(f"✅ Converted loans.txt to loans.json at {loans_json_path}")

# ✅ Step 2: Chunk Loans
chunked_loans = []

def chunk_loan(loan):
    chunks = []
    loan_name = loan.get("name", "Unknown Loan")

    for feature in loan.get("features", []):
        chunks.append({
            "text": f"{loan_name}: {feature}",
            "metadata": {"type": "loan", "name": loan_name}
        })

    return chunks

for loan in loans:
    chunked_loans.extend(chunk_loan(loan))

# ✅ Debugging: Check chunked loans
print(f"🔍 Total chunked loans: {len(chunked_loans)}")
print(f"🔍 First few chunks: {chunked_loans[:3]}")

if not chunked_loans:
    print("❌ ERROR: No chunked loans found. Exiting.")
    exit()

# ✅ Save Chunked Loans
with open(chunked_loans_path, "w", encoding="utf-8") as f:
    json.dump(chunked_loans, f, indent=4)

print(f"✅ Chunked loans saved to {chunked_loans_path}")

# ✅ Step 3: Generate Embeddings
client = chromadb.Client(Settings(persist_directory="chromadb_store"))
collection = client.get_or_create_collection(name="loans_data")

stored_ids = set(collection.get()["ids"])
new_data_ids = {f"doc_{i}" for i in range(len(chunked_loans))}

texts = [chunk["text"] for chunk in chunked_loans]

print(f"🔍 First few texts to embed: {texts[:3]}")

output = query(texts)

if not output or len(output) != len(texts):
    print("❌ ERROR: Embedding query failed or returned incorrect number of embeddings.")
    print(f"🔍 Expected: {len(texts)}, Got: {len(output) if output else 'None'}")
    exit()

print(f"🔎 Sample embedding: {output[0]}")

if stored_ids != new_data_ids:
    print("🛑 Removing old loan embeddings...")
    client.delete_collection(name="loans_data")
    collection = client.get_or_create_collection(name="loans_data")

    for idx, chunk in enumerate(chunked_loans):
        collection.add(
            documents=[chunk["text"]],
            embeddings=[output[idx]],
            ids=[f"doc_{idx}"],
            metadatas=[chunk["metadata"]]
        )

    print(f"✅ Successfully stored {collection.count()} loan embeddings in ChromaDB.")
else:
    print(f"✅ No changes detected. Skipping re-embedding. {collection.count()} embeddings already exist.")
