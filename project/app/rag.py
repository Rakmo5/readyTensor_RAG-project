from pathlib import Path
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
import os
from groq import Groq
# Update: Absolute import changed to match new project structure
from project.app.auth import get_user_dir 

SUPPORTED_EXTENSIONS = {".txt", ".md", ".pdf"} 

def load_user_documents(user_id: str):
    user_dir = get_user_dir(user_id)
    docs_dir = user_dir / "documents"

    if not docs_dir.exists():
        return []

    documents = []
    for file_path in docs_dir.iterdir():
        if file_path.suffix.lower() in SUPPORTED_EXTENSIONS:
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
    vector_dir = user_dir / "vector_db"
    vector_dir.mkdir(parents=True, exist_ok=True)
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

def generate_rag_answer(question: str, user_id: str):
    """
    Complete RAG Flow:
    1. Retrieve -> 2. Augment -> 3. Generate
    """
    context_chunks = retrieve_relevant_chunks(user_id, question, top_k=3)
    
    if not context_chunks:
        return {
            "answer": "I couldn't find any relevant information in your documents. Please upload more files.",
            "sources": []
        }

    context_text = "\n\n".join([chunk["content"] for chunk in context_chunks])
    sources = list(set([chunk["metadata"]["source"] for chunk in context_chunks]))

    client = Groq(api_key=os.environ.get("GROQ_API_KEY"))
    
    prompt = f"""
    You are a helpful assistant. Use the provided context to answer the user's question accurately.
    If the answer is not in the context, say you don't know.

    Context:
    {context_text}

    Question: {question}
    """

    # UPDATED MODEL STRING HERE
    chat_completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="llama-3.1-8b-instant",
    )

    return {
        "answer": chat_completion.choices[0].message.content,
        "sources": sources
    }