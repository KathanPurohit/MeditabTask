from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from chatbot import chat_with_bot
from models import ChatRequest, ChatResponse

app = FastAPI(
    title="AI Chatbot API"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():

    return {
        "message": "AI Chatbot API Running"
    }


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):

    result = chat_with_bot(
        request.message
    )

    return ChatResponse(
        response=result["response"],
        suggestions=result["suggestions"]
    )