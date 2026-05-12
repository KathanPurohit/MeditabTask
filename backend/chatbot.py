from dotenv import load_dotenv
import boto3
import logging

from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_aws import BedrockLLM

from prompts import SYSTEM_PROMPT
from memory_store import memory

load_dotenv()

logger = logging.getLogger(__name__)

# Initialize Bedrock Client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Initialize Bedrock Llama Model
llm = BedrockLLM(
    model_id="us.meta.llama3-3-70b-instruct-v1:0",
    client=bedrock_client,
    provider="meta",
    model_kwargs={
        "temperature": 0.7,
        "max_gen_len": 1024
    }
)

# How the two-stage formatting works:
#
# Stage 1 — Python's .format(system_prompt=SYSTEM_PROMPT) runs at import time.
#   - {{history}} and {{input}} are ESCAPED, so .format() leaves them alone
#     and outputs the literal text {history} and {input}.
#   - {system_prompt} is the ONLY placeholder .format() fills right now.
#
# Stage 2 — LangChain fills {history} and {input} at runtime per request,
#   because PromptTemplate sees them as its declared input_variables.
#
# This is why both sets of braces must be treated differently:
#   {system_prompt}   → single braces  → filled by Python's .format() now
#   {{history}}       → double braces  → escaped through .format(), becomes
#   {{input}}                            {history}/{input} for LangChain later

prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template=(
        "<|begin_of_text|><|start_header_id|>system<|end_header_id|>\n"
        "{system_prompt}\n"
        "<|eot_id|>\n"
        "{{history}}<|start_header_id|>user<|end_header_id|>\n"
        "{{input}}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
    ).format(system_prompt=SYSTEM_PROMPT)
)

# Note: ConversationChain is deprecated in newer LangChain versions.
# Consider migrating to RunnableWithMessageHistory + ChatPromptTemplate
# when upgrading LangChain.
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt_template,
    verbose=False
)


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
    for line in result.split("\n"):
        stripped = line.strip()
        if stripped.startswith(("-", "*", "•")):
            cleaned = stripped.lstrip("-*• ").strip()
            if cleaned:
                suggestions.append(cleaned)

    return suggestions[:3]


def chat_with_bot(user_message: str) -> dict:
    """Run a conversation turn and return the response plus suggestions."""

    response = conversation.predict(input=user_message)

    try:
        suggestions = generate_suggestions(user_message, response)
    except Exception as e:
        logger.warning("Suggestion generation failed: %s", e)
        suggestions = []

    return {
        "response": response,
        "suggestions": suggestions,
    }