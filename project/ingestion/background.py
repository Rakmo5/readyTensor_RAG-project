import os
from project.app.rag import chunk_documents, embed_and_store_chunks

def process_document_ingestion(file_path: str, user_id: str):
    """
    Worker function to process uploaded files into the vector store.
    """
    try:
        # 1. Read the file
        content = ""
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 2. Prepare as a 'document' object for your existing rag.py logic
        documents = [{
            "content": content,
            "source": os.path.basename(file_path)
        }]

        # 3. Use your existing logic (already tested and certified!)
        chunks = chunk_documents(documents)
        embed_and_store_chunks(user_id, chunks)
        
        print(f"✅ Background Ingestion Success: {file_path}")
        
    except Exception as e:
        print(f"❌ Background Ingestion Failed: {str(e)}")