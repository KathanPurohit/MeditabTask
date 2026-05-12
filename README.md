# MeditabTask Project

## Overview
MeditabTask is a Python-based project that implements an AI chatbot capable of reasoning and acting using tools. The chatbot is designed to handle user queries, perform calculations, and provide context-aware suggestions. It uses the LangChain framework for building agents and tools.

## Features
- **AI Chatbot**: Powered by the `ChatOllama` model for generating responses.
- **Tool Integration**: Includes tools for:
  - Getting the current time.
  - Performing mathematical calculations.
- **ReAct Prompting**: Implements reasoning and acting for dynamic and iterative problem-solving.
- **Customizable Prompts**: Uses `SYSTEM_PROMPT` and `REACT_AGENT_PROMPT` for defining AI behavior.
- **Follow-up Suggestions**: Generates follow-up questions based on user input and responses.

## Project Structure
```
MeditabTask/
├── backend/
│   ├── chatbot.py          # Main chatbot implementation
│   ├── memory_store.py     # Memory management for the chatbot
│   ├── models.py           # Model-related configurations
│   ├── prompts.py          # Prompt templates for the chatbot
│   ├── requirements.txt    # Backend dependencies
├── backend_venv/           # Virtual environment for backend
├── frontend/
│   ├── app.py              # Frontend implementation using Streamlit
│   ├── requirements.txt    # Frontend dependencies
├── frontend_venv/          # Virtual environment for frontend
└── README.md               # Project documentation
```

## Installation

### Prerequisites
- Python 3.11 or higher
- Virtual environment tools (e.g., `venv` or `virtualenv`)

### Backend Setup
1. Navigate to the `backend` directory:
   ```bash
   cd backend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv ../backend_venv
   source ../backend_venv/bin/activate  # On Windows: ../backend_venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Frontend Setup
1. Navigate to the `frontend` directory:
   ```bash
   cd frontend
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv ../frontend_venv
   source ../frontend_venv/bin/activate  # On Windows: ../frontend_venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Backend
1. Activate the backend virtual environment:
   ```bash
   source ../backend_venv/bin/activate  # On Windows: ../backend_venv\Scripts\activate
   ```
2. Run the backend server:
   ```bash
   python chatbot.py
   ```

### Running the Frontend
1. Activate the frontend virtual environment:
   ```bash
   source ../frontend_venv/bin/activate  # On Windows: ../frontend_venv\Scripts\activate
   ```
2. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Prompts
- **SYSTEM_PROMPT**: Defines the assistant's behavior and rules.
- **REACT_AGENT_PROMPT**: Enables reasoning and acting for dynamic problem-solving.

## Tools
- **`get_current_time`**: Returns the current date and time.
- **`calculator`**: Evaluates mathematical expressions.

## Contributing
1. Fork the repository.
2. Create a new branch for your feature or bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add new feature"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contact
For questions or support, please contact the project maintainer.