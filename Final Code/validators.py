"""Input parsing helpers for ProfitPilot.

The GUI passes raw text into these helpers. They either return a clean numeric
value or raise ``ValueError`` with a message that can be shown to the user.
"""


def safe_parse_float(value: str, missing_message: str, invalid_message: str) -> float:
    """Parse a float and raise a friendly error message if it is invalid."""
    text = value.strip()
    if not text:
        raise ValueError(missing_message)
    try:
        return float(text)
    except ValueError:
        raise ValueError(invalid_message)


def safe_parse_int(value: str, missing_message: str, invalid_message: str) -> int:
    """Parse an integer and raise a friendly error message if it is invalid."""
    text = value.strip()
    if not text:
        raise ValueError(missing_message)
    try:
        return int(text)
    except ValueError:
        raise ValueError(invalid_message)
