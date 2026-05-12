from langchain.memory import ConversationBufferMemory

memory = ConversationBufferMemory(
    human_prefix="Human",
    ai_prefix="Assistant",
    memory_key="history",
)