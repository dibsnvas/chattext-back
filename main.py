# main.py
from fastapi import FastAPI, HTTPException, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import openai
import logging

from functions.openai_requests import get_chat_response  # Update if needed
from functions.database import store_messages, reset_messages  # Update if needed

# Set up logging
logging.basicConfig(level=logging.INFO)

openai.organization = config("OPEN_AI_ORG")
openai.api_key = config("OPEN_AI_KEY")

app = FastAPI()

origins = [
    "http://localhost:5173",
    "http://localhost:5174",
    "http://localhost:4173",
    "http://localhost:3000",
    "https://chatbotfront-neon.vercel.app",  # Add your deployed frontend URL here
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
async def post_text(request: Request, text: str = Form(...)):
    logging.info(f"Received request: {request.method} {request.url}")
    if request.method != "POST":
        raise HTTPException(status_code=405, detail="Method Not Allowed")

    logging.info(f"Form data: {text}")
    try:
        # Get the chat response using the OpenAI API
        chat_response = get_chat_response(text)

        if not chat_response:
            raise HTTPException(status_code=400, detail="Failed chat response")
        
        # Store the messages
        store_messages(text, chat_response)
        logging.info("Message stored successfully.")
        return {"response": chat_response}
    except Exception as e:
        logging.error(f"Error in post_text: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
