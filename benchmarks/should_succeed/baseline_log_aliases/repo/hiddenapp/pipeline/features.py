from typing import Dict, List


def featurize(tokens: List[str], vocab_list: List[str]) -> Dict[str, int]:
    """
    Intentionally inefficient:
    - list membership check makes this O(n * vocab)
    """
    out: Dict[str, int] = {}
    for t in tokens:
        if t in vocab_list:
            out[t] = out.get(t, 0) + 1
    return out


def build_vocab_list(size: int = 6000) -> List[str]:
    return [f"tok{i}" for i in range(size)]

