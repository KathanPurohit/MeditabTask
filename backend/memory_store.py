from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    human_prefix="<|start_header_id|>user<|end_header_id|>\n",
    ai_prefix="<|start_header_id|>assistant<|end_header_id|>\n",
    memory_key="history"
)