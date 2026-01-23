import re
from typing import List


def tokenize(text: str) -> List[str]:
    """
    Intentionally slow tokenization:
    - Compiles regex every call
    - Uses findall with a relatively heavy pattern
    """
    pattern = re.compile(r"[A-Za-z0-9_]+")
    return pattern.findall(text.lower())

