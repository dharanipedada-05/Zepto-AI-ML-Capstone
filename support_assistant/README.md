# Zepto Support Assistant

This module is a small support assistant that answers questions related to Zepto policies.

It uses LangGraph to control the flow, ChromaDB to store and search policy documents, Sentence Transformers to create embeddings, Pydantic to validate the response, and FastAPI to provide the API.

## Project Structure

```text
support_assistant/
├── docs/
├── chroma_db/
├── ingest.py
├── graph.py
├── models.py
├── prompts.py
├── main.py
├── requirements.txt
├── Dockerfile
└── README.md
```

## How It Works

The policy documents are stored as text files in the docs folder.

The ingest.py script reads these files and creates embeddings using the all-MiniLM-L6-v2 Sentence Transformer model. The embeddings and document text are stored in ChromaDB.

When a user sends a question, LangGraph first checks the type of question.

Policy questions are sent to the retrieval step.
The top 3 matching documents are retrieved from ChromaDB.
General questions are handled without document retrieval.
The final response contains the answer, source document IDs, and a confidence value.
## Setup

Install the required packages:

python -m pip install -r requirements.txt

If the ChromaDB database has not been created yet, run:

python ingest.py
## Run the Application

Start the FastAPI application:

uvicorn main:app --reload

Open Swagger in the browser:

http://127.0.0.1:8000/docs

The /ask endpoint can be used to send questions to the assistant.

## API Test 1 - Policy Question
Request
{
  "query": "How much is the delivery fee?"
}
## Response
{
  "answer": "Based on the retrieved context: Delivery Policy: \"Zepto delivers grocery and household essentials to serviceable pin codes within 10 to 30 minutes of order confirmation, depending on the customer's delivery zone and current order vo",
  "sources": [
    "doc_01",
    "doc_05",
    "doc_02"
  ],
  "confidence": 1
}

This question is treated as a policy question. The system searches the policy documents and returns the relevant document IDs as sources.

## API Test 2 - General Question
Request
{
  "query": "What is the capital of India?"
}
## Response
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1
}

This question is not related to a Zepto policy, so the system does not search the policy documents.

## Docker

A Dockerfile is included to run the application in a container.

Build the Docker image:

docker build -t zepto-support .

Run the container:

docker run -p 8000:8000 zepto-support .

Then open:

http://127.0.0.1:8000/docs

The Swagger page can be used to test the /ask endpoint.

## Summary

The support assistant uses local policy documents as its knowledge source. LangGraph handles the question routing, ChromaDB handles document retrieval, Pydantic keeps the response format consistent and FastAPI provides the API. The application can also be built and run using Docker.