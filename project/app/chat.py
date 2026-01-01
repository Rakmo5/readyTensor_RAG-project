import os 
from dotenv import load_dotenv

from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage

from app.rag import retrieve_relevant_chunks
from app.memory import save_message, load_recent_messages

from app.knowledge import append_knowledge
from app.rag import (
    load_user_documents,
    chunk_documents,
    embed_and_store_chunks,
)
print("KNOWLEDGE MODULE LOADED FROM:", __file__)
print("KNOWLEDGE DIR CONTENTS:", dir())

load_dotenv()

SYSTEM_PROMPT = """
You are a personal knowledge assistant.
You must answer ONLY using the provided context.
If the answer is not contained in the context, say:
"I don't have enough information to answer that."

Do not use outside knowledge.
Be concise and factual.
"""

def build_context(chunks):
    """
    Combines retrived chunks into a single context string.
    """
    context_parts = []

    for c in chunks:
        context_parts.append(
            f"source:{c['metadata']['source']}\n{c['content']}"
        )
    return "\n\n".join(context_parts)

def answer_question(user_id: str, question: str):
    """
    Conversational RAG:
    - includes recent chat history
    - retrieves relevant knowledge
    - generates grounded response
    """

    # 1. Load recent conversation (memory)
    history = load_recent_messages(user_id, limit=6)

    history_text = ""
    for role, content in history:
        history_text += f"{role.upper()}: {content}\n"

    if question.lower().startswith("/add"):
        new_info = question[4:].strip()

        append_knowledge(user_id, new_info)

        # Re-ingest knowledge immediately
        docs = load_user_documents(user_id)
        chunks = chunk_documents(docs)
        embed_and_store_chunks(user_id, chunks)

        save_message(user_id, "assistant", "I've added this to your knowledge base.")
        return "I've added this to your knowledge base."

    # 2. Retrieve relevant knowledge
    chunks = retrieve_relevant_chunks(user_id, question)
    context = build_context(chunks)

    # 3. Build messages
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=f"""
Conversation so far:
{history_text}

Knowledge context:
{context}

User question:
{question}
"""
        ),
    ]

    # 4. Call LLM
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        temperature=0.3,
        api_key=os.getenv("GROQ_API_KEY"),
    )

    response = llm.invoke(messages)

    # 5. Save memory
    save_message(user_id, "user", question)
    save_message(user_id, "assistant", response.content)

    return response.content
