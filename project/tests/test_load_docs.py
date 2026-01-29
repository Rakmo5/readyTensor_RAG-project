from app.rag import load_user_documents
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

docs = load_user_documents("rak")

for d in docs:
    print("SOURCE:", d["source"])
    print("CONTENT:")
    print(d["content"])
    print("-" * 40)
