import openai
from typing import List, Dict

def get_embedding(text: str, openai_api_key: str) -> List[float]:
    openai.api_key = openai_api_key
    response = openai.Embedding.create(
        engine="text-embedding-ada-002",
        input=text
    )
    return response["data"][0]["embedding"]

def embed_and_store_documents(collection, documents: List[Dict]):
    # documents is a list of {"id": str, "text": str, "metadata": dict}
    # Assume API key is managed outside, or we store embeddings offline
    # If you need an OpenAI key here, you might pass it as a parameter
    # and call get_embedding for each text.
    
    # For a production environment, batch embedding queries or handle them carefully.
    for doc in documents:
        # Here, you may need to supply an OpenAI API key or have it globally set
        embedding = get_embedding(doc["text"], openai.api_key)
        collection.add(documents=[doc["id"]], embeddings=[embedding], metadatas=[doc["metadata"]], texts=[doc["text"]])
