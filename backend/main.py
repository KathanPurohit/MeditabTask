import logging
import os

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from chatbot import chat_with_bot
from models import ChatRequest, ChatResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="AI Chatbot API")

_raw_origins = os.getenv("ALLOWED_ORIGINS", "*")
allowed_origins = (
    ["*"] if _raw_origins == "*" else [o.strip() for o in _raw_origins.split(",")]
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "AI Chatbot API Running"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    try:
        result = chat_with_bot(request.message, request.provider)
        return ChatResponse(
            response=result["response"],
            suggestions=result["suggestions"],
        )
    except Exception as e:
        logger.error("Chat error: %s", e, exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error. Please try again.")