import os
import json
import requests
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from langchain.embeddings.base import Embeddings

# Load API keys
load_dotenv()
hf_token = os.environ.get("HF_TOKEN")

# Hugging Face API
model_id = "sentence-transformers/all-MiniLM-L6-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

# Paths
base_dir = os.path.dirname(os.path.abspath(__file__))
data_paths = {
    "credit_card": os.path.join(base_dir, "..", "data", "chunked_credit_cards.json"),
    "literacy": os.path.join(base_dir, "..", "data", "chunked_literacy.json"),
    "loan": os.path.join(base_dir, "..", "data", "chunked_loans.json"),
}

# Initialize ChromaDB Client
client = chromadb.PersistentClient(path="chromadb_store")
collection = client.get_or_create_collection(name="finance_embeddings")

class HuggingFaceEmbeddings(Embeddings):
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.headers = headers

    def embed_documents(self, texts):
        return query(texts)

    def embed_query(self, text):
        return query([text])[0]

def query(texts):
    """ Queries Hugging Face API for embeddings """
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options": {"wait_for_model": True}})
    response.raise_for_status()
    return response.json()

# Step 1: Load Data
all_data = []
for category, path in data_paths.items():
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            chunked_data = json.load(f)
            for item in chunked_data:
                item["metadata"]["category"] = category  # Add category to metadata
                all_data.append(item)

# Step 2: Check Existing Embeddings
existing_ids = set()
try:
    existing_records = collection.get()  
    existing_ids = set(existing_records["ids"]) if "ids" in existing_records else set()
except Exception as e:
    print(f"⚠️ Warning: Could not fetch existing records - {e}")

new_data = {f"doc_{i}" for i in range(len(all_data))}
texts = [chunk["text"] for chunk in all_data]

# Step 3: Delete Old Embeddings Only if Needed
if existing_ids and existing_ids != new_data:
    print("🛑 Removing outdated embeddings...")
    collection.delete(ids=list(existing_ids))  # ✅ FIX: Pass `ids` explicitly
    print(f"✅ Removed {len(existing_ids)} old embeddings.")

# Step 4: Only Embed New Data
if new_data != existing_ids:
    print("🔄 Generating embeddings...")
    output = query(texts)

    for idx, (text, metadata) in enumerate(zip(texts, [chunk["metadata"] for chunk in all_data])):
        collection.add(
            documents=[text],
            embeddings=[output[idx]],
            ids=[f"doc_{idx}"],
            metadatas=[metadata]
        )

    print(f"✅ Stored {len(texts)} new embeddings in ChromaDB.")
else:
    print(f"✅ No changes detected. {collection.count()} embeddings already exist. Skipping re-embedding.")
