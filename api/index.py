import json
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.helpers.openai import revalidate, related, search, chat_query

app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Revalidate the Pinecone instance
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
    query = data.get('query', None)
    session_id = data.get('session_id', None)
    print(query, 'search')
    result = chat_query(query, session_id)
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
    data = await search_term.json()
    res = search(json.dumps(data))
    return res