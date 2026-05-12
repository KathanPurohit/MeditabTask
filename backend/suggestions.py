import logging
import re


logger = logging.getLogger(__name__)


GENERIC_SUGGESTION_PHRASES = (
    "favorite hobby",
    "have a pet",
    "like to travel",
    "favorite color",
    "favorite food",
    "tell me more about yourself",
)

STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "could",
    "do", "does", "for", "from", "how", "i", "in", "is", "it", "me",
    "my", "of", "on", "or", "please", "should", "that", "the", "this",
    "to", "what", "when", "where", "who", "why", "with", "would", "you",
    "your",
}


def _content_words(text: str) -> set[str]:
    return {
        word
        for word in re.findall(r"[a-zA-Z0-9_]+", text.lower())
        if len(word) > 2 and word not in STOPWORDS
    }


def _is_simple_closed_exchange(
    user_input: str,
    response: str
) -> bool:
    user_words = _content_words(user_input)
    response_words = _content_words(response)

    if len(response.split()) <= 3 and len(response) <= 40:
        return True

    if not user_words or not response_words:
        return True

    return False


def _is_relevant_suggestion(
    suggestion: str,
    context_words: set[str]
) -> bool:
    normalized = suggestion.lower()

    if any(
        phrase in normalized
        for phrase in GENERIC_SUGGESTION_PHRASES
    ):
        return False

    suggestion_words = _content_words(suggestion)

    if not suggestion_words:
        return False

    return bool(suggestion_words & context_words)


def generate_suggestions(
    user_input: str,
    response: str,
    active_llm
) -> list[str]:

    if _is_simple_closed_exchange(user_input, response):
        return []

    context_words = (
        _content_words(user_input)
        | _content_words(response)
    )

    prompt = f"""
Based on this conversation, generate up to 3 short
follow-up questions that the USER might ask next.

User's last message:
{user_input}

Assistant's response:
{response}

Rules:
- Write questions from USER perspective
- Keep each under 10 words
- Only suggest questions directly related to this exchange
- Do not ask personal small-talk questions
- If there are no useful next questions, return NONE
- Return ONLY bullet points or NONE
- No explanations

Example:
- How does memory work?
- Can you improve this code?
- What are the limitations?
"""

    try:

        result = active_llm.invoke(prompt)

        content = (
            result.content
            if hasattr(result, "content")
            else str(result)
        )

        suggestions = []

        for line in content.split("\n"):

            stripped = line.strip()

            if stripped.upper() == "NONE":
                return []

            if stripped.startswith(("-", "*")):

                cleaned = (
                    stripped
                    .lstrip("-* ")
                    .strip()
                )

                if (
                    cleaned
                    and _is_relevant_suggestion(
                        cleaned,
                        context_words
                    )
                ):
                    suggestions.append(
                        cleaned
                    )

        suggestions = list(
            dict.fromkeys(suggestions)
        )

        return suggestions[:3]

    except Exception as e:

        logger.warning(
            "Suggestion generation failed: %s",
            e
        )

        return []
