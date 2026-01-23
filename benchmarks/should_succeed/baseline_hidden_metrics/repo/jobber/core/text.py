import re
from typing import Dict, List


def tokenize(text: str) -> List[str]:
    # Intentionally slow: regex compiled every time.
    pat = re.compile(r"[A-Za-z0-9_]+")
    return pat.findall(text)


def counts(tokens: List[str], vocab: List[str]) -> Dict[str, int]:
    # Intentionally slow: O(n*vocab) list membership.
    out: Dict[str, int] = {}
    for t in tokens:
        if t in vocab:
            out[t] = out.get(t, 0) + 1
    return out


def build_vocab(size: int = 8000) -> List[str]:
    return [f"w{i}" for i in range(size)]

