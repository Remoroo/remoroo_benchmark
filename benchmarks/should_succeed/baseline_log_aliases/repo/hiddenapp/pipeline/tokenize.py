import re
from typing import List


def tokenize(text: str) -> List[str]:
    """
    Intentionally slow:
    - compiles regex each call
    - uses a slightly heavier pattern than needed
    """
    pat = re.compile(r"[A-Za-z0-9_]+")
    return pat.findall(text.lower())

