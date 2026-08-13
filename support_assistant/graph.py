import os
from typing import TypedDict

from sentence_transformers import SentenceTransformer
import chromadb
from langgraph.graph import StateGraph, END

from prompts import PROMPT_TEMPLATE


# -----------------------------
# Settings
# -----------------------------

MOCK_LLM = os.getenv("MOCK_LLM", "1") != "0"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROMA_DIR = os.path.join(BASE_DIR, "chroma_db")


# -----------------------------
# Embedding model and ChromaDB
# -----------------------------

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path=CHROMA_DIR)

collection = client.get_collection(
    name="zepto_policies"
)


# -----------------------------
# Graph State
# -----------------------------

class GraphState(TypedDict, total=False):
    query: str
    intent: str
    answer: str
    sources: list[str]
    confidence: float


# -----------------------------
# Node 1: Classify Intent
# -----------------------------

def classify_intent(state: GraphState) -> GraphState:

    query = state["query"].lower()

    policy_keywords = [
        "delivery",
        "return",
        "refund",
        "membership",
        "tracking",
        "cancel",
        "gift card",
        "support hours"
    ]

    if any(keyword in query for keyword in policy_keywords):
        intent = "policy_question"
    else:
        intent = "general_question"

    return {
        **state,
        "intent": intent
    }


# -----------------------------
# Node 2: Retrieve and Answer
# -----------------------------

def retrieve_and_answer(state: GraphState) -> GraphState:

    query = state["query"]

    # Create embedding for the question
    query_embedding = embedding_model.encode(query).tolist()

    # Retrieve top 3 similar documents
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=3
    )

    documents = results["documents"][0]
    ids = results["ids"][0]

    # Use the most relevant document
    top_chunk = documents[0]

    if MOCK_LLM:
        answer = (
            f"Based on the retrieved context: "
            f"{top_chunk[:200]}"
        )
    else:
        # Real LLM extension can be added later.
        context = "\n\n".join(documents)

        prompt = PROMPT_TEMPLATE.format(
            context=context,
            question=query
        )

        # Real LLM call would go here.
        answer = prompt

    return {
        **state,
        "answer": answer,
        "sources": ids,
        "confidence": 1.0
    }


# -----------------------------
# Node 3: Direct Answer
# -----------------------------

def direct_answer(state: GraphState) -> GraphState:

    if MOCK_LLM:
        answer = "I can only answer questions about Zepto policies right now."
    else:
        answer = "I can only answer questions about Zepto policies right now."

    return {
        **state,
        "answer": answer,
        "sources": [],
        "confidence": 1.0
    }



# -----------------------------
# Build LangGraph
# -----------------------------

def route_intent(state: GraphState):
    if state["intent"] == "policy_question":
        return "retrieve_and_answer"

    return "direct_answer"


builder = StateGraph(GraphState)

builder.add_node("classify_intent", classify_intent)
builder.add_node("retrieve_and_answer", retrieve_and_answer)
builder.add_node("direct_answer", direct_answer)

builder.set_entry_point("classify_intent")

builder.add_conditional_edges(
    "classify_intent",
    route_intent,
    {
        "retrieve_and_answer": "retrieve_and_answer",
        "direct_answer": "direct_answer"
    }
)

builder.add_edge("retrieve_and_answer", END)
builder.add_edge("direct_answer", END)

graph = builder.compile()
if __name__ == "__main__":

    policy_result = graph.invoke({
        "query": "How much is the delivery fee?"
    })

    print("\nPolicy question:")
    print(policy_result)

    general_result = graph.invoke({
        "query": "What is the capital of India?"
    })

    print("\nGeneral question:")
    print(general_result)