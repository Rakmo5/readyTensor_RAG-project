# 📝 Mandatory Explanations — RAG-Based Question Answering System

This document explains key design decisions and observations made during the development of the RAG-based API system, as required by the evaluation criteria.

---

## 1. Chunking Strategy & Size Selection

### 🔹 Method Used
Recursive Character Text Splitter

### 🔹 Chunk Size
**500 characters**

### 🔹 Overlap
**100 characters**

---

### ✅ Why 500 Characters?

A chunk size of 500 characters was selected to balance:

1. **Relevance Precision**  
   Smaller chunks improve similarity matching by focusing embeddings on specific ideas.

2. **Context Sufficiency**  
   Each chunk typically contains 3–5 complete sentences, giving the LLM enough context to generate meaningful answers.

3. **Efficient Context Window Usage**  
   Smaller chunks allow multiple relevant segments to be included in the prompt without exceeding token limits.

Very small chunks (100–200 chars) were found to fragment ideas, while very large chunks (1000+ chars) diluted topic focus and reduced retrieval precision.

---

### ✅ Why 100 Characters of Overlap?

Overlap ensures that:

- Important information near chunk boundaries is preserved
- Sentences split between chunks still appear fully in at least one chunk

This prevents **context clipping**, where semantically related information becomes separated and harder to retrieve together.

---

## 2. Retrieval Failure Case Observed

### ❌ Failure Case: Ambiguous Pronoun Queries

During testing, queries such as:

> "What is his deadline?"

sometimes failed to retrieve the correct document chunk or retrieved unrelated information.

---

### 🔍 Root Cause

The embedding model (**all-MiniLM-L6-v2**) prioritizes semantic keywords.  
Pronouns like *"his"* carry very low semantic weight compared to named entities like *"Alex"* or *"project supervisor"*.

Without conversational context, the retriever cannot associate "his" with the correct entity.

---

### ✅ Solution Implemented: Conversational Memory

To mitigate this:

- Last **6 chat messages** are stored in SQLite
- Recent conversation context is included during LLM generation

This allows the LLM to resolve references such as:

> "his" → "Alex (supervisor)"

Even if retrieval does not directly return the correct chunk, conversational grounding enables the model to answer correctly using combined memory and retrieved context.

This effectively creates a **hybrid retrieval + memory system**.

---

## 3. Metric Tracked — End-to-End Latency

### 📊 Metric: API Request Latency (milliseconds)

Latency is measured from:

> API request received → retrieval completed → LLM response generated → API response returned

---

### 📈 Observed Results

Average latency observed:

- **1.2 to 2.5 seconds per request**

---

### 🔍 Bottleneck Analysis

Component timing breakdown:
```bash
| Component | Approx Time |
|--------|------------|
| Embedding & Vector Search | < 100 ms |
| LLM Generation (Groq API) | 1–2+ seconds |

```
The LLM call is the dominant latency contributor.

---

### ✅ Design Actions Taken

To prevent performance degradation and API abuse:

- Implemented **rate limiting (5 requests/minute per IP)**
- Prevents hitting Groq API quotas
- Maintains consistent response times for concurrent users

Latency tracking also enables future optimization such as:

- Caching frequent queries
- Using faster embedding models
- Reducing number of retrieved chunks

---

## 🏗️ Architecture Diagram Description

The following flow was used to create the system architecture diagram:

```bash
Client (Swagger UI / Postman)
│
▼
FastAPI Server
│
├── Rate Limiter (In-Memory)
│
├── Upload Endpoint
│ │
│ ▼
│ Background Ingestion Task
│ │
│ ▼
│ Sentence-Transformers Embeddings
│ │
│ ▼
│ ChromaDB (Vector Store)
│
└── Ask Endpoint
│
├── Fetch Chat History (SQLite)
├── Similarity Search (ChromaDB)
│
▼
LLM via Groq API (Llama 3.1)
│
▼
Response (Answer + Sources + Latency)
```

---

---

## 🎯 Design Philosophy

This system is intentionally designed to:

- Demonstrate complete RAG lifecycle
- Focus on backend API engineering
- Remain explainable and reproducible
- Avoid heavy orchestration frameworks

The implementation emphasizes:

- Clear separation of concerns
- Persistent memory
- Production-style validation and monitoring

---

## ✅ Evaluation Criteria Mapping
```bash

| Evaluation Area | How It Is Addressed |
|--------|----------------|
| Chunking Strategy | Recursive splitter, 500 size, 100 overlap |
| Retrieval Quality | Hybrid retrieval + memory |
| API Design | FastAPI, validated requests, async endpoints |
| Metrics Awareness | End-to-end latency tracking |
| System Clarity | Modular architecture and documentation |
```
---

