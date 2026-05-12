_DEFAULT_SYSTEM_PROMPT = """You are a helpful, autonomous assistant capable of reasoning and using tools.

STRICT RULES:
- Answer ONLY what the user just asked.
- Keep responses concise and to the point.
- If the user asks a simple question like their name, answer it simply and stop.
- Make use of tools when necessary (e.g. for calculations, current time).
"""

REACT_AGENT_PROMPT = """{system_prompt}

TOOLS:
------
You have access to the following tools:

{tools}

To use a tool, please use the following format:

```
Thought: Do I need to use a tool? Yes
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
```

When you have a response to say to the Human, or if you do not need to use a tool, you MUST use the format:

```
Thought: Do I need to use a tool? No
Final Answer: [your response here]
```

Begin!

Previous conversation history:
{history}

New input: {input}
{agent_scratchpad}"""

try:
    SYSTEM_PROMPT: str = _DEFAULT_SYSTEM_PROMPT
    assert isinstance(SYSTEM_PROMPT, str) and SYSTEM_PROMPT.strip(), \
        "SYSTEM_PROMPT must be a non-empty string"
except Exception as e:
    import warnings
    warnings.warn(
        f"Could not load custom SYSTEM_PROMPT ({e}). Falling back to default.",
        stacklevel=1,
    )
    SYSTEM_PROMPT = _DEFAULT_SYSTEM_PROMPT