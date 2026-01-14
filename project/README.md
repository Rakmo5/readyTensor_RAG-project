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


---

## 🚀 How to Run

### 1️⃣ Setup environment

```bash
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```
### 2️⃣ Environment variables

Create a .env file:

```bash
GROQ_API_KEY=your_api_key_here

```

### 3️⃣ Add documents

Place .txt or .md files inside:

```bash
data/users/<your_username>/documents/

```

### 4️⃣ Ingest documents

```bash
python test_vector_store.py
```

### 5️⃣ Ask questions

``` bash
python test_chat.py
```

---

### 🧠 Knowledge vs Conversation Memory

* Conversation memory

    * Stored automatically in SQLite

    * Used for conversational continuity

* Knowledge base

    * Updated explicitly via user action

    * Prevents accidental or noisy ingestion

This separation ensures accuracy and explainability.

--- 

### ⚠️ Limitations

* Manual document ingestion step

* Limited document formats (text/markdown)

* Minimal interface (CLI-based)

### 🔮 Future Improvements

* Web-based chat interface

* Document upload via UI

* Memory summarization

* Knowledge editing and deletion

* Advanced retrieval strategies

---

✅ Why This Project Matters
This project demonstrates:

* Practical understanding of RAG

* Persistent memory handling

* User-scoped data isolation

* Clean system design

* Real-world AI assistant architecture

It goes beyond a basic chatbot into a foundational personal AI system.

