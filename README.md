# MeditabTask

MeditabTask is a local AI chatbot application with a Streamlit frontend and a FastAPI backend. The backend runs a LangChain ReAct agent on a local Ollama model, gives the agent access to tools, keeps short conversational memory, and returns suggested follow-up questions with each response.

## Current Architecture

```text
Streamlit UI
frontend/app.py
    |
    | POST /chat
    v
FastAPI API
backend/main.py
    |
    | validates request/response with Pydantic
    v
Chat Orchestration
backend/chatbot.py
    |
    | LangChain ReAct agent + memory + tools
    v
Local Ollama Model
qwen2.5-coder:7b
```

## Components

- `frontend/app.py` provides the chat UI, stores the visible chat history in Streamlit session state, sends user messages to the backend, and renders returned follow-up suggestions as buttons.
- `backend/main.py` exposes the FastAPI app, configures CORS, defines the health route, and serves the `/chat` endpoint.
- `backend/models.py` defines the `ChatRequest` and `ChatResponse` Pydantic schemas. Blank messages are rejected at validation time.
- `backend/chatbot.py` creates the Ollama-backed LangChain agent, invokes it for each user message, and asks the model to generate follow-up suggestions.
- `backend/tools.py` registers the ReAct tools available to the agent: current time lookup and safe arithmetic calculation.
- `backend/memory_store.py` configures a `ConversationBufferWindowMemory` with the last 5 turns.
- `backend/prompts.py` contains the system prompt and ReAct agent prompt template.
- `backend/suggestions.py` generates up to 3 short follow-up questions from the latest user message and assistant response.

## Project Structure

```text
MeditabTask/
+-- backend/
|   +-- chatbot.py
|   +-- main.py
|   +-- memory_store.py
|   +-- models.py
|   +-- prompts.py
|   +-- requirements.txt
|   +-- suggestions.py
|   +-- tools.py
+-- frontend/
|   +-- app.py
|   +-- requirements.txt
+-- backend_venv/
+-- frontend_venv/
+-- .gitignore
+-- README.md
```

## Prerequisites

- Python 3.11 or newer
- Ollama installed and running locally
- The local model used by the backend:

```powershell
ollama pull qwen2.5-coder:7b
```

## Backend Setup

From the project root:

```powershell
python -m venv backend_venv
.\backend_venv\Scripts\Activate.ps1
pip install -r backend\requirements.txt
```

Run the API:

```powershell
cd backend
uvicorn main:app --reload
```

The backend runs at `http://127.0.0.1:8000` by default.

Available routes:

- `GET /` returns a simple API health message.
- `POST /chat` accepts `{"message": "...", "provider": "ollama"}` and returns `{"response": "...", "suggestions": [...]}`.

## Frontend Setup

In a second terminal, from the project root:

```powershell
python -m venv frontend_venv
.\frontend_venv\Scripts\Activate.ps1
pip install -r frontend\requirements.txt
streamlit run frontend\app.py
```

The frontend posts to `http://127.0.0.1:8000/chat`, so start the backend before using the UI.

## Configuration

The backend allows all CORS origins by default. To restrict origins, set `ALLOWED_ORIGINS` before starting FastAPI:

```powershell
$env:ALLOWED_ORIGINS = "http://localhost:8501,http://127.0.0.1:8501"
uvicorn main:app --reload
```

The active model is currently configured in `backend/chatbot.py`:

```python
model="qwen2.5-coder:7b"
```

## Request Flow

1. The user enters a message in the Streamlit chat UI.
2. The frontend sends the message and selected provider to `POST /chat`.
3. FastAPI validates the request with `ChatRequest`.
4. `chat_with_bot()` invokes the LangChain ReAct executor.
5. The agent may call tools from `backend/tools.py`.
6. The backend generates short suggested follow-up questions.
7. FastAPI returns the assistant response and suggestions to Streamlit.

## Notes

- The `provider` field exists in the API and UI, but the current implementation only supports `ollama`.
- Conversation memory is process-local and in-memory. Restarting the backend clears it.
- The frontend stores displayed chat messages in Streamlit session state.
