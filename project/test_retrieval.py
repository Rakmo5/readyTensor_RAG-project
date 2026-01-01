from app.rag import retrieve_relevant_chunks, get_vector_store
import os
os.environ["ANONYMIZED_TELEMETRY"] = "False"

collection = get_vector_store("rak")

print("Vector DB count:", collection.count())

query = "What is this document about?"

results = retrieve_relevant_chunks("rak", query)

print("Retrieved chunks:", len(results))

for r in results:
    print("SOURCE:", r["metadata"]["source"])
    print("CHUNK ID:", r["metadata"]["chunk_id"])
    print("CONTENT:")
    print(r["content"])
    print("-" * 40)
