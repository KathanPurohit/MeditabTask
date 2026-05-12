import logging
from datetime import datetime

from langchain.tools import tool


logger = logging.getLogger(__name__)


@tool
def get_current_time(query: str) -> str:
    """
    Useful for getting the current date and time.
    """

    return datetime.now().strftime(
        "%Y-%m-%d %H:%M:%S"
    )


@tool
def calculator(expression: str) -> str:
    """
    Useful for solving mathematical expressions.

    Example:
    - 5 + 10
    - 100 / 5
    - 2 * (5 + 3)
    """

    allowed_chars = (
        "0123456789+-*/(). "
    )

    if not all(
        char in allowed_chars
        for char in expression
    ):
        return "Invalid mathematical expression."

    try:

        result = eval(
            expression,
            {"__builtins__": None},
            {}
        )

        return str(result)

    except Exception as e:

        logger.warning(
            "Calculator error: %s",
            e
        )

        return "Error evaluating expression."


tools = [
    get_current_time,
    calculator
]