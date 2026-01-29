from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

# Update: Absolute import changed to match new project structure
# from project.app.auth import get_user_dir 

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"} # Added .pdf for Phase 2 goals

def get_user_dir(user_id: str) -> Path:
    # 1. Start from this file: project/app/auth.py
    # 2. Go up two levels to reach the 'project' folder
    # 3. Then go into 'data/users'
    base_path = Path(__file__).resolve().parent.parent / "data" / "users"
    
    user_path = base_path / user_id
    
    # Ensure the directory exists on the physical disk
    user_path.mkdir(parents=True, exist_ok=True)
    
    return user_path
def load_user_documents(user_id: str):
    user_dir = get_user_dir(user_id)
    # Note: In Phase 2, files come from project/data/uploads/
    docs_dir = user_dir / "documents"

    if not docs_dir.exists():
        return []

    documents = []
    for file_path in docs_dir.iterdir():
        if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
            # Simple text read (PDFs will be handled by Loader in background.py)
            try:
                text = file_path.read_text(encoding="utf-8")
                documents.append({
                    "content": text,
                    "source": file_path.name,
                })
            except Exception:
                continue
    return documents

def chunk_documents(documents, chunk_size=500, overlap=100):
    chunks = []
    for doc in documents:
        text = doc["content"]
        source = doc["source"]
        start = 0
        chunk_id = 0
        while start < len(text):
            end = start + chunk_size
            chunk_text = text[start:end]
            chunks.append({
                "content": chunk_text,
                "source": source,
                "chunk_id": chunk_id,
            })
            chunk_id += 1
            start += chunk_size - overlap
    return chunks

def get_vector_store(user_id: str):
    user_dir = get_user_dir(user_id)
    # Data is now stored in project/data/users/{user_id}/vector_db
    vector_dir = user_dir / "vector_db"
    vector_dir.mkdir(parents=True, exist_ok=True)

    # Use PersistentClient for newer versions of ChromaDB
    client = chromadb.PersistentClient(path=str(vector_dir))
    return client.get_or_create_collection(name="documents")

def embed_and_store_chunks(user_id: str, chunks):
    if not chunks:
        return
    model = SentenceTransformer("all-MiniLM-L6-v2")
    collection = get_vector_store(user_id)

    texts = [c["content"] for c in chunks]
    metadatas = [{"source": c["source"], "chunk_id": c["chunk_id"]} for c in chunks]
    ids = [f"{c['source']}_{c['chunk_id']}" for c in chunks]

    embeddings = model.encode(texts).tolist()
    collection.add(
        documents=texts,
        metadatas=metadatas,
        ids=ids,
        embeddings=embeddings,
    )

def retrieve_relevant_chunks(user_id: str, query: str, top_k: int = 3):
    model = SentenceTransformer("all-MiniLM-L6-v2")
    collection = get_vector_store(user_id)
    
    count = collection.count()
    if count == 0:
        return []

    query_embedding = model.encode([query]).tolist()
    n_results = min(top_k, count)

    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results,
    )

    retrieved_chunks = []
    for i in range(len(results["documents"][0])):
        retrieved_chunks.append({
            "content": results["documents"][0][i],
            "metadata": results["metadatas"][0][i],
        })
    return retrieved_chunks