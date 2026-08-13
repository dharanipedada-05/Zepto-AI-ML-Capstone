from fastapi import FastAPI

from graph import graph
from models import AskRequest, AskResponse


app = FastAPI(title="Zepto Support Assistant")


@app.post("/ask", response_model=AskResponse)
def ask(request: AskRequest):

    result = graph.invoke({
        "query": request.query
    })

    return AskResponse(
        answer=result["answer"],
        sources=result["sources"],
        confidence=result["confidence"]
    )