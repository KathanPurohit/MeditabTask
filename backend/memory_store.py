from langchain.memory import (
    ConversationBufferWindowMemory
)

memory = ConversationBufferWindowMemory(
    k=5,
    human_prefix="Human",
    ai_prefix="Assistant",
    memory_key="history",
    return_messages=True
)