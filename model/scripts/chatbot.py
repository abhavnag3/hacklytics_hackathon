from langchain_community.vectorstores import Chroma
from openai import OpenAI
from dotenv import load_dotenv
import embeddings  
import os
import json

load_dotenv()

# Initialize embedding function
embedding_function = embeddings.HuggingFaceEmbeddings(embeddings.api_url, embeddings.headers)

# Ensure collections exist before accessing them
if "consumer_finance_embeddings" not in embeddings.client.list_collections():
    embeddings.client.create_collection(name="consumer_finance_embeddings")

if "business_finance_embeddings" not in embeddings.client.list_collections():
    embeddings.client.create_collection(name="business_finance_embeddings")

if "business_chat_history" not in embeddings.client.list_collections():
    embeddings.client.create_collection(name="business_chat_history")

# Store chat history
chat_history = {}

def query_consumer_chatbot(query_text, user_id, top_k=5):
    consumer_chroma = Chroma(
        collection_name="consumer_finance_embeddings",
        embedding_function=embedding_function
    )
    results = consumer_chroma.similarity_search(query_text, k=top_k)

    context = "\n".join([f"- {doc.page_content}" for doc in results]) if results else "No relevant financial matches found."

    history = chat_history.get(user_id, [])

    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history])

    new_user_msg = {"role": "user", "content": query_text}
    history.append(new_user_msg)

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4",
        temperature=0.2,
        messages=[
            {"role": "system", 
             "content": "You are a financial advisor helping everyday consumers. You provide clear, precise, and trustworthy financial advice on credit cards, personal loans, and financial literacy terms. DO NOT INCLUDE LINKS. Format output cleanly, removing any asterisks."},
            {"role": "user", "content": f"Past conversation:\n{history_text}\n\nContext:\n{context}\n\nQuestion: {query_text}"}
        ]
    )

    bot_response = completion.choices[0].message.content
    history.append({"role": "assistant", "content": bot_response})

    chat_history[user_id] = history[-5:]  

    return bot_response


def query_business_chatbot(query_text, user_id, top_k=5):
    business_chroma = Chroma(
        collection_name="business_finance_embeddings",
        embedding_function=embedding_function
    )
    results = business_chroma.similarity_search(query_text, k=top_k)

    context = "\n".join([f"- {doc.page_content}" for doc in results]) if results else "No relevant business financial matches found."

    existing_chat = embeddings.client.get_collection(name="business_chat_history")
    
    past_data = existing_chat.get(ids=[user_id])
    past_messages = json.loads(past_data["documents"][0]) if past_data and past_data["documents"] else []

    history_text = "\n".join([f"{msg['role']}: {msg['content']}" for msg in past_messages])

    past_messages.append({"role": "user", "content": query_text})

    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    completion = client.chat.completions.create(
        model="gpt-4",
        temperature=0.2,
        messages=[
            {"role": "system", 
             "content": "You are a financial advisor helping business owners. You provide clear, precise, and trustworthy advice on business credit cards, business loans, and finance terms relevant to small businesses and startups. DO NOT INCLUDE LINKS. Format output cleanly, removing all asterisks."},
            {"role": "user", "content": f"Past conversation:\n{history_text}\n\nContext:\n{context}\n\nQuestion: {query_text}"}
        ]
    )

    bot_response = completion.choices[0].message.content
    past_messages.append({"role": "assistant", "content": bot_response})

    existing_chat.add(
        documents=[json.dumps(past_messages)],
        ids=[user_id]
    )

    return bot_response