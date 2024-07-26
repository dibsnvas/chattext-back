import os
import json
import random
from fastapi import FastAPI, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai

from functions.openai_requests import get_chat_response
from functions.database import store_messages, reset_messages, get_recent_messages

openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
    "https://chatbotfront-neon.vercel.app",
    "https://chatbotfront-bhss.vercel.app",
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
    try:
        chat_response = get_chat_response(text)

        if not chat_response:
            raise HTTPException(status_code=503, detail="ChatGPT service unavailable")  # More appropriate status code

        store_messages(text, chat_response)
        return {"response": chat_response}
    except openai.error.APIError as e:
        raise HTTPException(status_code=503, detail=f"OpenAI API error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {e}")
