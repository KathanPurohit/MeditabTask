from dotenv import load_dotenv
import logging
from datetime import datetime

from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import tool

from prompts import SYSTEM_PROMPT, REACT_AGENT_PROMPT
from memory_store import memory

load_dotenv()

logger = logging.getLogger(__name__)

llm = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0.7,
)

@tool
def get_current_time(query: str) -> str:
    """Returns the current date and time."""
    return f"The current date and time is {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

@tool
def calculator(expression: str) -> str:
    """Evaluates a mathematical expression and returns the result."""
    try:
        # Use eval safely by restricting globals and locals
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except Exception as e:
        return f"Error evaluating expression: {e}"

tools = [get_current_time, calculator]

prompt_template = PromptTemplate.from_template(
    template=REACT_AGENT_PROMPT.replace("{system_prompt}", SYSTEM_PROMPT)
)

agent = create_react_agent(llm, tools, prompt_template)
agent_executor = AgentExecutor(agent=agent, tools=tools, memory=memory, verbose=True, handle_parsing_errors=True)


def generate_suggestions(user_input: str, response: str) -> list[str]:
    """Generate 3 follow-up question suggestions based on the conversation turn."""

    prompt = f"""Based on this conversation, generate 3 short follow-up questions that the USER might want to ask next.

The questions should be from the USER's perspective, not the assistant's.

User's last message: {user_input}
Assistant's response: {response}

Rules:
- Write questions as if the user is asking them
- Keep them short and relevant
- Return ONLY 3 bullet points starting with "- ", nothing else, no preamble

Example format:
- How do I implement that?
- What are the pros and cons?
- Can you give me an example?
"""

    result = llm.invoke(prompt)

    suggestions = []
    content = result.content if hasattr(result, 'content') else str(result)
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("-", "*", "•")):
            cleaned = stripped.lstrip("-*• ").strip()
            if cleaned:
                suggestions.append(cleaned)

    return suggestions[:3]


def chat_with_bot(user_message: str) -> dict:
    """Run a conversation turn and return the response plus suggestions."""

    response_obj = agent_executor.invoke({"input": user_message})
    response_text = response_obj.get("output", "")

    try:
        suggestions = generate_suggestions(user_message, response_text)
    except Exception as e:
        logger.warning("Suggestion generation failed: %s", e)
        suggestions = []

    return {
        "response": response_text,
        "suggestions": suggestions,
    }