# FIX #6: Wrap the import in a try/except so a missing or malformed prompts
# module surfaces a clear, actionable error at startup instead of a cryptic
# AttributeError or ImportError later during the first request.

_DEFAULT_SYSTEM_PROMPT = """You are a helpful assistant.

STRICT RULES:
- Answer ONLY what the user just asked.
- Do NOT summarize or repeat previous conversation unless explicitly asked.
- Do NOT assume or invent things the user said or asked.
- Do NOT add follow-up questions about previous topics unless directly relevant.
- Keep responses concise and to the point.
- If the user asks a simple question like their name, answer it simply and stop.
"""

try:
    # If you have a custom system prompt defined elsewhere, import it here.
    # from my_custom_prompts import SYSTEM_PROMPT  # noqa: F401
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