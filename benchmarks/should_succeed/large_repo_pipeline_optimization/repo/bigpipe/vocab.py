from typing import List

from .config import CFG


def build_vocab_list() -> List[str]:
    """
    Returns a vocab *list* (intentionally inefficient for membership checks).
    """
    return [f"tok{i}" for i in range(CFG.vocab_size)]

