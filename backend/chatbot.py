import logging
import time
from datetime import datetime

import os
from langchain_community.chat_models import ChatOllama
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate
from langchain.tools import tool

from prompts import SYSTEM_PROMPT, REACT_AGENT_PROMPT
from memory_store import memory
from tools import tools
from suggestions import generate_suggestions


logger = logging.getLogger(__name__)

llm_ollama = ChatOllama(
    model="qwen2.5-coder:7b",
    temperature=0.7,
    num_predict=512,
)


prompt_template = PromptTemplate.from_template(
    template=REACT_AGENT_PROMPT.replace("{system_prompt}", SYSTEM_PROMPT)
)

agent_ollama = create_react_agent(llm_ollama, tools, prompt_template)
executor_ollama = AgentExecutor(agent=agent_ollama, tools=tools, memory=memory, verbose=True, handle_parsing_errors=True)


def chat_with_bot(
    user_message: str,
    provider: str = "ollama"
) -> dict:

    start_time = time.time()

    user_message = user_message.strip()

    logger.info("User message: %s", user_message)

    try:

        response_obj = executor_ollama.invoke({
            "input": user_message
        })

        logger.info(
            "Raw response: %s",
            response_obj
        )

        response_text = (
            response_obj.get("output", "").strip()
        )

        if not response_text:
            response_text = (
                "I couldn't generate a response."
            )

    except Exception as e:

        logger.error(
            "Agent execution failed: %s",
            e
        )

        return {
            "response": (
                "Something went wrong while "
                "processing your request."
            ),
            "suggestions": []
        }

    suggestions = generate_suggestions(
        user_message,
        response_text,
        llm_ollama
    )

    execution_time = time.time() - start_time

    logger.info(
        "Execution completed in %.2f seconds",
        execution_time
    )

    return {
        "response": response_text,
        "suggestions": suggestions,
    }