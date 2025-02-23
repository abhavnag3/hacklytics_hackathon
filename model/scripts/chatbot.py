from langchain_community.vectorstores import Chroma
from openai import OpenAI
from dotenv import load_dotenv
import embeddings  
import os

load_dotenv()

# Initialize embedding function
embedding_function = embeddings.HuggingFaceEmbeddings(embeddings.api_url, embeddings.headers)

# Ensure collections exist before accessing them
if "consumer_finance_embeddings" not in embeddings.client.list_collections():
    consumer_collection = embeddings.client.create_collection(name="consumer_finance_embeddings")
else:
    consumer_collection = embeddings.client.get_collection(name="consumer_finance_embeddings")

if "business_finance_embeddings" not in embeddings.client.list_collections():
    business_collection = embeddings.client.create_collection(name="business_finance_embeddings")
else:
    business_collection = embeddings.client.get_collection(name="business_finance_embeddings")

print(f"✅ Consumer Embeddings: {consumer_collection.count()} | Business Embeddings: {business_collection.count()}")

def query_consumer_chatbot(query_text, top_k=5):
    consumer_chroma = Chroma(
        collection_name="consumer_finance_embeddings",
        embedding_function=embedding_function
    )
    results = consumer_chroma.similarity_search(query_text, k=top_k)
    
    context = "\n".join([f"- {doc.page_content}" for doc in results]) if results else "No relevant financial matches found."

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4",
        temperature=0.2,
        messages=[
            {"role": "system", 
             "content": "You are a financial advisor helping everyday consumers. You provide clear, precise, and trustworthy financial advice on credit cards, personal loans, and financial literacy terms. DO NOT INCLUDE LINKS. Format output cleanly, removing any asterisks."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query_text}"}
        ]
    )
    
    return completion.choices[0].message.content

def query_business_chatbot(query_text, top_k=5):
    business_chroma = Chroma(
        collection_name="business_finance_embeddings",
        embedding_function=embedding_function
    )
    results = business_chroma.similarity_search(query_text, k=top_k)

    context = "\n".join([f"- {doc.page_content}" for doc in results]) if results else "No relevant business financial matches found."

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4",
        temperature=0.2,
        messages=[
            {"role": "system", 
             "content": "You are a financial advisor helping business owners. You provide clear, precise, and trustworthy advice on business credit cards, business loans, and finance terms relevant to small businesses and startups. DO NOT INCLUDE LINKS. Format output cleanly, removing all asterisks."},
            {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query_text}"}
        ]
    )
    
    return completion.choices[0].message.content

if __name__ == "__main__":
    '''test_query1 = "What is a good credit card for travel with no annual fee?"
    test_query2 = "I'm a small business owner. What are my best financing options?"

    consumer_response = query_consumer_chatbot(test_query1)
    business_response = query_business_chatbot(test_query2)

    print("\n💳 Consumer Chatbot Response:\n", consumer_response)
    print("\n🏢 Business Chatbot Response:\n", business_response)'''
