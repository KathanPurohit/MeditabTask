from dotenv import load_dotenv
import boto3

from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_community.llms import Bedrock

from prompts import SYSTEM_PROMPT
from memory_store import memory

load_dotenv()

# Initialize Bedrock Client
bedrock_client = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1"
)

# Initialize Bedrock Llama Model
llm = Bedrock(
    model_id="us.meta.llama3-3-70b-instruct-v1:0",
    client=bedrock_client,
    provider="meta",          
    model_kwargs={
        "temperature": 0.7,
        "max_gen_len": 512
    }
)

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template=f"""
{SYSTEM_PROMPT}

Conversation History:
{{history}}

User:
{{input}}

A:
"""
)

# Conversation Chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt_template,
    verbose=False
)

# Generate Suggestions
def generate_suggestions(user_input, response):

    prompt = f"""
Generate 3 short follow-up questions.

User Question:
{user_input}

Assistant Response:
{response}

Return only bullet points.
"""

    result = llm.invoke(prompt)

    lines = result.split("\n")  # Note: Bedrock LLM returns string, not object

    suggestions = []

    for line in lines:
        cleaned = line.replace("-", "").strip()
        if cleaned:
            suggestions.append(cleaned)

    return suggestions[:3]


# Main Chat Function
def chat_with_bot(user_message):

    response = conversation.predict(
        input=user_message
    )

    suggestions = generate_suggestions(
        user_message,
        response
    )

    return {
        "response": response,
        "suggestions": suggestions
    }