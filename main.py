from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

from functions.openai_requests import get_chat_response
from functions.database import store_messages, reset_messages

openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the FastAPI application"}

@app.get("/health")
async def check_health():
    return {"response": "healthy"}

@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"response": "conversation reset"}

@app.post("/post-text/")
async def post_text(text: str = Form(...)):
    chat_response = get_chat_response(text)

    store_messages(text, chat_response)
    print(chat_response)
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")

    return {"response": chat_response}
