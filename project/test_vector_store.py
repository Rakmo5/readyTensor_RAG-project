from app.rag import load_user_documents, chunk_documents, embed_and_store_chunks
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

docs = load_user_documents("rak")
chunks = chunk_documents(docs)

embed_and_store_chunks("rak", chunks)

print(f"Stored {len(chunks)} chunks in vector DB.")
