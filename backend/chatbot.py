from dotenv import load_dotenv
import boto3

from langchain.chains import ConversationChain
from langchain.prompts import PromptTemplate
from langchain_aws import BedrockLLM

from prompts import SYSTEM_PROMPT
from memory_store import memory

load_dotenv()

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
        "max_gen_len": 512
    }
)

# Prompt Template
prompt_template = PromptTemplate(
    input_variables=["history", "input"],
    template="""<|begin_of_text|><|start_header_id|>system<|end_header_id|>
{system_prompt}
<|eot_id|>
{{history}}<|start_header_id|>user<|end_header_id|>
{{input}}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
""".format(system_prompt=SYSTEM_PROMPT)
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
Based on this conversation, generate 3 short follow-up questions that the USER might want to ask next.

The questions should be from the USER's perspective, not the assistant's.

User's last message: {user_input}
Assistant's response: {response}

Rules:
- Write questions as if the user is asking them
- Keep them short and relevant
- Return only 3 bullet points, nothing else

Example format:
- How do I implement that?
- What are the pros and cons?
- Can you give me an example?
"""

    result = llm.invoke(prompt)
    lines = result.split("\n")
    suggestions = []

    for line in lines:
        cleaned = line.replace("-", "").replace("*", "").strip()
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