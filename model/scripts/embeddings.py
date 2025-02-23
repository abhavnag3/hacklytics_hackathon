# third script in pipeline

import os
import json
import requests
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings
from langchain.embeddings.base import Embeddings

# Load environment variables
load_dotenv()
hf_token = os.environ.get("HF_TOKEN")

# Hugging Face API settings
model_id = "sentence-transformers/all-MiniLM-L6-v2"
api_url = f"https://api-inference.huggingface.co/pipeline/feature-extraction/{model_id}"
headers = {"Authorization": f"Bearer {hf_token}"}

# File paths
base_dir = os.path.dirname(os.path.abspath(__file__))
input_path = os.path.join(base_dir, "..", "data", "chunked_credit_cards.json")

# Load chunked credit card data
with open(input_path, "r", encoding="utf-8") as f:
    chunked_data = json.load(f)

# Extract texts and metadata
texts = [chunk["text"] for chunk in chunked_data]
metadata_list = [chunk["metadata"] for chunk in chunked_data]

# Hugging Face Embeddings Wrapper
class HuggingFaceEmbeddings(Embeddings):
    def __init__(self, api_url, headers):
        self.api_url = api_url
        self.headers = headers
    
    def embed_documents(self, texts):
        try:
            return query(texts)
        except Exception as e:
            print(f"Error embedding documents: {e}")
            return None

    def embed_query(self, text):
        try:
            return query([text])[0]
        except Exception as e:
            print(f"Error embedding query: {e}")
            return None

# Function to query Hugging Face API for embeddings
def query(texts):
    response = requests.post(api_url, headers=headers, json={"inputs": texts, "options": {"wait_for_model": True}})
    response.raise_for_status()
    return response.json()

try:
    # Generate embeddings for the chunked data
    output = query(texts)
    
    # Initialize ChromaDB client
    client = chromadb.PersistentClient(path="chromadb_store")  # Ensures embeddings are saved

    
    collection = client.get_or_create_collection(name="credit_card_embeddings")

    # Only run embedding if there are no stored documents
    if collection.count() == 0:
        print("🔄 No embeddings found. Generating embeddings now...")
        output = query(texts)  # Generate embeddings

        for idx, (text, metadata) in enumerate(zip(texts, metadata_list)):
            collection.add(
                documents=[text],
                embeddings=[output[idx]],
                ids=[f"doc_{idx}"],
                metadatas=[metadata]
            )
        print(f"✅ Stored {len(texts)} embeddings in ChromaDB.")
    else:
        print(f"✅ {collection.count()} embeddings already exist. Skipping re-embedding.")


except Exception as e:
    print(f"Error: {e}")
