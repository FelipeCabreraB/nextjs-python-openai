import time

from fastapi import FastAPI, Request
from api.helpers.openai import revalidate, query
from api.helpers.openai_chat import chat_query

app = FastAPI()

@app.get("/revalidate")
def handle_revalidate():
    start_time = time.time()

    revalidate()

    end_time = time.time()
    elapsed_time = end_time - start_time

    return {
        "status": "Revalidated",
        "duration": f"{elapsed_time:.4f} seconds"
    }

@app.post("/query")
async def handle_query(request: Request):
    start_time = time.time()

    data = await request.json()
    search = data["query"]

    result = query(search)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return {
        "status": "ok",
        "result": result,
        "duration": f"{elapsed_time:.4f} seconds"
    }

@app.post("/chat-query")
async def handle_query(request: Request):
    start_time = time.time()

    data = await request.json()
    search = data["query"]

    result = chat_query(search)

    end_time = time.time()
    elapsed_time = end_time - start_time

    return {
        "status": "ok",
        "result": result,
        "duration": f"{elapsed_time:.4f} seconds"
    }