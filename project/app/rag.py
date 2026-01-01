from pathlib import Path

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from app.auth import get_user_dir


SUPPORTED_EXTENSIONS = {".txt", ".md"}


def load_user_documents(user_id: str):
    """
    Loads raw text documents for a given user.
    Returns a list of dicts: {content, source}
    """
    user_dir = get_user_dir(user_id)
    docs_dir = user_dir / "documents"

    if not docs_dir.exists():
        return []

    documents = []

    for file_path in docs_dir.iterdir():
        if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            text = file_path.read_text(encoding="utf-8")
            documents.append(
                {
                    "content": text,
                    "source": file_path.name,
                }
            )

    return documents


def chunk_documents(documents, chunk_size=500, overlap=100):
    """
    Splits documents into overlapping chunks.
    Returns a list of chunk dicts.
    """
    chunks = []

    for doc in documents:
        text = doc["content"]
        source = doc["source"]

        start = 0
        chunk_id = 0

        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]

            chunks.append(
                {
                    "content": chunk_text,
                    "source": source,
                    "chunk_id": chunk_id,
                }
            )

            chunk_id += 1
            start += chunk_size - overlap

    return chunks


def get_vector_store(user_id: str):
    """
    Returns a persistent ChromaDB collection for the user.
    """
    user_dir = get_user_dir(user_id)
    vector_dir = user_dir / "vector_db"
    vector_dir.mkdir(exist_ok=True)

    client = chromadb.Client(
        Settings(
            persist_directory=str(vector_dir),
            is_persistent=True,
            anonymized_telemetry=False,
        )
    )

    return client.get_or_create_collection(name="documents")



def embed_and_store_chunks(user_id: str, chunks):
    """
    Embeds chunks and stores them in the user's vector DB.
    """
    model = SentenceTransformer("all-MiniLM-L6-v2")
    collection = get_vector_store(user_id)

    texts = [c["content"] for c in chunks]
    metadatas = [
        {
            "source": c["source"],
            "chunk_id": c["chunk_id"],
        }
        for c in chunks
    ]
    ids = [f"{c['source']}_{c['chunk_id']}" for c in chunks]

    embeddings = model.encode(texts).tolist()

    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings,
    )

def retrieve_relevant_chunks(user_id:str,query:str,top_k:int=3):
    """
    Retrive top-k relavant chunks for a query from the user's vector DB.
    """
    model = SentenceTransformer("all-MiniLm-L6-v2")
    collection = get_vector_store(user_id)

    query_embedding = model.encode([query]).tolist()

    count = collection.count()
    n_results = min(top_k,count)

    if n_results == 0:
        return []
    
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )

    retrieved_chunks = []

    for i in range(len(results["documents"][0])):
        retrieved_chunks.append(
            {
                "content":results["documents"][0][i],
                "metadata":results["metadatas"][0][i],
            }
        )

    return retrieved_chunks