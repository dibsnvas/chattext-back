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
    "https://chatbotfront-neon.vercel.app/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    print(f"Received text: {text}")
    
    chat_response = get_chat_response(text)
    print(f"Chat response: {chat_response}")

    if chat_response is None:
        print("Chat response is None")
        raise HTTPException(status_code=400, detail="Failed chat response")

    store_messages(text, chat_response)

    return {"response": chat_response}