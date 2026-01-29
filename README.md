# 🚀 Multi-User Conversational RAG API

A production-style **Retrieval-Augmented Generation (RAG) backend API** built with **FastAPI, LangChain, ChromaDB, and Groq LLM**.  
The system allows multiple users to upload documents, maintain private knowledge bases, and receive **context-aware answers with persistent memory**.

This project demonstrates how to convert an ML-based RAG pipeline into a **scalable API service** with proper backend engineering practices.

---

## ✨ Key Features

- 🧠 **Conversational RAG**  
  Uses **Llama-3.1-8B-Instant via Groq API** for fast and accurate responses.

- 📂 **Multi-User Data Isolation**  
  Each user has a private directory for:
  - Uploaded documents
  - Vector database
  - Chat history (SQLite)

- ⚡ **Background Document Ingestion**  
  File uploads trigger background embedding and indexing using FastAPI BackgroundTasks.

- 🔎 **Hybrid Retrieval**  
  Combines:
  - Vector similarity search from documents
  - Recent conversational memory from SQLite

- 🛡️ **API Hardening**
  - In-memory rate limiting (5 requests/minute)
  - Structured request validation using Pydantic
  - Graceful error handling for LLM and DB failures

- 📊 **Simple Metrics**
  - Retrieval count
  - Response latency per request

---
## 🏗️ System Architecture

![RAG API Architecture](assets/Architecture.jpeg)

This diagram shows the end-to-end flow from client request to document ingestion, vector retrieval, and LLM-based answer generation.


## 🏗️ Tech Stack
```bash
| Component        | Technology |
|--------|------------|
| Backend Framework | FastAPI |
| LLM Provider | Groq Cloud API |
| Model | Llama-3.1-8B-Instant |
| Orchestration | LangChain |
| Vector DB | ChromaDB (persistent local storage) |
| Embeddings | Sentence-Transformers (all-MiniLM-L6-v2) |
| Memory Store | SQLite |
| Validation | Pydantic |
| Python Version | 3.10+ |
```
---

## 📁 Project Structure

```bash
project/
├── api/
│ ├── main.py # FastAPI app entry point
│ ├── routes.py # /upload and /ask endpoints
│ ├── schemas.py # Pydantic request/response models
│ └── rate_limit.py # In-memory rate limiting
│
├── app/ # Core RAG logic (reused from certified project)
│ ├── rag.py
│ ├── memory.py
│ ├── knowledge.py
│ └── auth.py
│
├── ingestion/
│ ├── loader.py # PDF/TXT loaders and chunking
│ └── background.py # Background ingestion jobs
│
├── data/
│ ├── uploads/ # Uploaded documents
│ └── users/ # Per-user vector DB and SQLite memory
│
├── tests/
├── archive/ # Legacy UI (not used)
├── README.md
└── requirements.txt
```

---


## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Rakmo5/readyTensor_RAG-project.git
cd readyTensor_RAG-project
git checkout internship-rag-api
```
### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate      # Linux/Mac
venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```
Pinned versions are used for Chroma compatibility.

### 4. Environment Variables

Create a .env file in the project folder:

```bash
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here
```
### 5. Run the Server
```bash
uvicorn project.api.main:app --reload
```

Open in browser:

- ✅ Health check: http://127.0.0.1:8000/health
- 📘 API Docs: http://127.0.0.1:8000/docs

---

## 🧪 API Usage

### ✅ Upload Documents

Endpoint: POST /upload
Form-Data:
- file: PDF or TXT
- user_id: string
Starts background ingestion and embedding.

Response:
```bash 
{"message": "Ingestion started"}
```

### ✅ Ask Questions (RAG)
Endpoint: Post /ask
```bash
{
  "question": "What is mentioned about deadlines?",
  "user_id": "intern_01",
  "top_k": 3
}

```

Response:
```bash
{
  "question": "What is mentioned about deadlines?",
  "user_id": "intern_01",
  "top_k": 3
}
```

### ✅ Add Knowledge via Chat
Users can dynamically add knowledge:
```bash
{
  "question": "/add The supervisor is Alex.",
  "user_id": "intern_01"
}
```
The system stores this in the user's knowledge base and memory.

---

## 🛡️ Security & Reliability

- Rate Limiting
   - 5 requests per minute per IP (in-memory)
- Failure Handling
   - LLM API failures → HTTP 503
   - Vector DB issues → HTTP 500
   - Rate limit exceeded → HTTP 429
- Request Validation
   - Enforced using Pydantic schemas

---

## 🎯 Design Goals

This internship version focuses on:
- Clean API design
- Separation of concerns
- Background processing
- Production-style validation and monitoring

The system is intentionally scoped to backend engineering and explainable AI pipelines.

---

## 🧠 Learning Outcomes

This project demonstrates:
- Converting ML pipelines into API services
- RAG system design with persistent memory
- Vector database integration
- Async and background task handling
- Production-oriented API hardening

---
## 📌 Notes

- The certified ReadyTensor project remains unchanged on main branch.

- Internship implementation is developed on internship-rag-api branch.

- UI is intentionally excluded to focus on backend evaluation.
