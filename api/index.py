import json
from fastapi import FastAPI, Request, Cookie, Response
from fastapi.middleware.cors import CORSMiddleware
from api.helpers.openai import revalidate, related, search, chat_query, clear_memory
from api.helpers.chat_history_test import chat_test


app = FastAPI()

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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
    search = data.get('query', None)
    clear_memory_bool = data.get('clear_memory', None)
    if not search and clear_memory_bool:
        print('clearing memory')
        clear_memory()
        return []
    else: 
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
    data = await search_term.json()
    res = search(json.dumps(data))
    return res

# Chat bot
@app.post("/api/chat-test")
async def handle_query(request: Request):
    data = await request.json()
    query = data.get('query', None)
    session_id = data.get('session_id', None)
    print(query, 'search')
    result = chat_test(query, session_id)
    return result
    
# Set cookie 
@app.post("/api/set-cookie") 
async def set_cookie(request: Request): 
    response = Response(content="Cookie set!") 
    data = await request.json()
    session_id = data.get('session_id', None)
    response.set_cookie(key="session_id", value=session_id) 
    return response