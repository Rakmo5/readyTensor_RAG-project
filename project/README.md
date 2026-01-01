# 🧠 Personal Knowledge Brain (PKB)

A user-scoped Retrieval-Augmented Generation (RAG) assistant that answers questions grounded in a user’s own documents, with persistent memory and clean modular design.

---

## 📌 Project Overview

Personal Knowledge Brain (PKB) is an AI assistant that allows users to:

- Add their own documents
- Ask questions grounded strictly in those documents
- Maintain conversational memory across sessions
- Keep each user’s data fully isolated

Unlike generic chatbots, PKB is designed as a **personal knowledge system**, not a stateless Q&A tool.

---

## ✨ Key Features

- 🔍 Retrieval-Augmented Generation (RAG)
- 📚 Document ingestion and chunking
- 🧠 Semantic search using embeddings
- 💾 Persistent vector database (ChromaDB)
- 🗂️ Persistent conversation memory (SQLite)
- 👤 User-scoped isolation (multi-tenant ready)
- ⚙️ Modular and extensible architecture

---

## 🧱 Architecture Overview
```bash
User
└── Query
├── Conversation Memory (SQLite)
├── Knowledge Retrieval (ChromaDB)
└── LLM (Groq)
```

Each user has an isolated data directory:

```bash
data/users/<user_id>/
├── chat.db # conversation memory
├── documents/ # user-provided documents
└── vector_db/ # vector embeddings (ChromaDB)   
```


---

## 🔁 RAG Pipeline

1. **Document Loading**
   - User places `.txt` or `.md` files in their documents folder

2. **Chunking**
   - Documents are split into overlapping chunks

3. **Embedding**
   - Sentence Transformers (`all-MiniLM-L6-v2`)

4. **Vector Storage**
   - Persistent ChromaDB collection (per user)

5. **Retrieval**
   - Semantic similarity search (top-k chunks)

6. **Answer Generation**
   - Retrieved context + user query → LLM (Groq)

---

## 🛠️ Tech Stack

- Python 3
- ChromaDB
- Sentence Transformers
- Groq LLM API
- SQLite

---

## 📂 Project Structure

``` bash

project/
├── app/
│ ├── auth.py # user isolation
│ ├── memory.py # SQLite conversation memory
│ ├── rag.py # ingestion and retrieval
│ ├── chat.py # conversational RAG logic
│ └── knowledge.py # explicit knowledge updates
├── data/
│ └── users/
├── test_chat.py
├── test_vector_store.py
├── requirements.txt
└── README.md

```

