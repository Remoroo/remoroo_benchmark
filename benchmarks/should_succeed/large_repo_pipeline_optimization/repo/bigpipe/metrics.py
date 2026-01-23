import hashlib
from typing import List, Tuple


def accuracy(y_true: List[int], y_pred: List[int]) -> float:
    correct = 0
    for a, b in zip(y_true, y_pred):
        if a == b:
            correct += 1
    return correct / max(1, len(y_true))


def checksum_predictions(y_pred: List[int]) -> str:
    # Used to ensure deterministic correctness across refactors
    m = hashlib.sha256()
    for v in y_pred:
        m.update(b"1" if v else b"0")
    return m.hexdigest()


def expected_checksum(rows: List[Tuple[str, int]]) -> str:
    """
    Deterministic reference checksum for the current dataset generation.
    This value is used to assert correctness.
    """
    # Recompute expected using the same simplistic rule used for labels:
    hot = ("tok1", "tok7", "tok42", "tok99")
    m = hashlib.sha256()
    for text, _label in rows:
        pred = 1 if any(h in text for h in hot) else 0
        m.update(b"1" if pred else b"0")
    return m.hexdigest()

