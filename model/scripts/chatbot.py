# fourth script in pipeline

from langchain_chroma import Chroma
from openai import OpenAI
from dotenv import load_dotenv
import embeddings # Ensure this matches your embeddings file name
import os

load_dotenv()

def query_with_langchain(query_text, top_k=5):
    """Searches ChromaDB for the best credit cards based on user input and generates a response."""
    
    # Retrieve top-matching credit card features from ChromaDB
    chroma_store = Chroma(
        collection_name="credit_card_embeddings",
        embedding_function=embeddings.HuggingFaceEmbeddings(embeddings.api_url, embeddings.headers),
        client=embeddings.client
    )
    results = chroma_store.similarity_search(query_text, k=top_k)
    
    # Format results into a readable context
    if not results:
        context = "No relevant credit card matches found."
    else:
        context = "\n".join([f"- {doc.page_content}" for doc in results])
    
    # Generate response using OpenAI
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", 
 "content": "You are a helpful financial advisor specializing in credit cards. DO NOT INCLUDE LINKS. Your goal is to recommend 3-5 cards that **EXACTLY** match the user's needs.  Prioritize accuracy over quantity. Formatting Guide: - Start with '💳 **Top Credit Card Matches for You**:' - List each card with emojis for readability - Keep it **short and to the point** (no unnecessary details) - Only include cards that match ALL requested criteria If no perfect match exists, suggest alternatives **briefly** without forcing irrelevant cards."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query_text}"}
        ]
    )
    
    return completion.choices[0].message.content

# Test to see if embeddings exist
collection = embeddings.client.get_collection(name="credit_card_embeddings")
print(f"✅ Number of stored embeddings: {collection.count()}")

if __name__ == "__main__":
    test_query = "I want a credit card with no annual fee and good travel rewards."
    response = query_with_langchain(test_query)
    print("\n💳 Chatbot Response:\n", response)
