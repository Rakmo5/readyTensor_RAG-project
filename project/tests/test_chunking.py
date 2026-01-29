from app.rag import load_user_documents, chunk_documents
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

docs = load_user_documents("rak")
chunks = chunk_documents(docs)

for c in chunks:
    print(f"{c['source']} | chunk {c['chunk_id']}")
    print(c["content"])
    print("-" * 40)
