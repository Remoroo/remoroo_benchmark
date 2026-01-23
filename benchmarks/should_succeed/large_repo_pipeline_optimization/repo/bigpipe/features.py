from typing import Dict, List


def featurize(tokens: List[str], vocab_list: List[str]) -> Dict[str, int]:
    """
    Intentionally inefficient feature builder:
    - O(n^2) membership checks via list containment
    - builds a dict of token counts only for tokens in vocab
    """
    counts: Dict[str, int] = {}
    for tok in tokens:
        if tok in vocab_list:  # O(vocab_size) membership
            counts[tok] = counts.get(tok, 0) + 1
    return counts

