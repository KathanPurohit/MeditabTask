from langchain.memory import ConversationBufferMemory

# FIX #3: Use plain text prefixes ("Human" / "Assistant") instead of raw Llama 3
# header tokens. The prompt template in chatbot.py already wraps each turn in
# the correct <|start_header_id|>…<|end_header_id|> tokens. Embedding those
# tokens inside the memory prefixes caused them to appear twice in the final
# prompt, producing malformed token sequences that confuse the model.
memory = ConversationBufferMemory(
    human_prefix="Human",
    ai_prefix="Assistant",
    memory_key="history",
)