import logging


logger = logging.getLogger(__name__)


def generate_suggestions(
    user_input: str,
    response: str,
    active_llm
) -> list[str]:

    prompt = f"""
Based on this conversation, generate 3 short
follow-up questions that the USER might ask next.

User's last message:
{user_input}

Assistant's response:
{response}

Rules:
- Write questions from USER perspective
- Keep each under 10 words
- Avoid generic questions
- Return ONLY bullet points
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

            if stripped.startswith(
                ("-", "*", "•")
            ):

                cleaned = (
                    stripped
                    .lstrip("-*• ")
                    .strip()
                )

                if cleaned:
                    suggestions.append(
                        cleaned
                    )

        # Remove duplicates
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