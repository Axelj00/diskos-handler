from chromadb.config import Settings
import chromadb

def get_chroma_collection(chroma_db_dir: str, collection_name: str):
    client = chromadb.Client(Settings(
        chroma_db_impl="duckdb+parquet",
        persist_directory=chroma_db_dir
    ))
    return client.get_or_create_collection(name=collection_name)

def query_chroma(collection, query: str, metadata_filter: dict = None, top_k: int = 5):
    results = collection.query(
        query_texts=[query],
        n_results=top_k,
        where=metadata_filter if metadata_filter else {}
    )
    
    # Format the results
    texts = results["documents"][0]
    metadatas = results["metadatas"][0]
    return [{"text": t, "metadata": m} for t, m in zip(texts, metadatas)]
