import time
import json

from fastapi import FastAPI, Request
from api.helpers.openai import revalidate, related, search, chat_query

app = FastAPI()

# Revalidate the Chroma instance
@app.get("/api/revalidate")
def handle_revalidate():
    revalidate()

    return {
        "status": "Revalidated",
    }

# Chat bot
@app.post("/api/chat-query")
async def handle_query(request: Request):
    data = await request.json()
    search = data["query"]
    result = chat_query(search)

    return result
    
    
# Get related products from a product
@app.post('/api/related')
async def post_related(question: Request):
	data = await question.json()
	res = related(json.dumps(data))
	return res

# Search
@app.post('/api/search')
async def post_search(search_term: Request):
  res = search(search_term.value)
  return res