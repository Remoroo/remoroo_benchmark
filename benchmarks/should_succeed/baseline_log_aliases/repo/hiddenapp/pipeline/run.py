from typing import List

from .data import make_dataset
from .features import build_vocab_list, featurize
from .model import predict
from .tokenize import tokenize


def accuracy(y_true: List[int], y_pred: List[int]) -> float:
    correct = 0
    for a, b in zip(y_true, y_pred):
        if a == b:
            correct += 1
    return correct / max(1, len(y_true))


def run_job() -> float:
    """
    Correct but slow implementation; intended to be optimized by the engine.
    """
    rows = make_dataset()
    vocab_list = build_vocab_list()

    y_true: List[int] = []
    y_pred: List[int] = []

    # Repeat to amplify inefficiencies (still deterministic)
    for _ in range(2):
        y_true = []
        y_pred = []
        for text, label in rows:
            toks = tokenize(text)
            feats = featurize(toks, vocab_list)
            y_true.append(label)
            y_pred.append(predict(feats))

    return float(accuracy(y_true, y_pred))

