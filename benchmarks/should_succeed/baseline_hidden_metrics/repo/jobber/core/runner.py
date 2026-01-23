from typing import Dict, List

from ..io.dataset import load_dataset
from ..io.output import write_predictions
from .model import predict_from_counts
from .text import build_vocab, counts, tokenize


def run() -> int:
    """
    Entrypoint for `python -m jobber`.
    Intentionally does NOT emit metrics; it only writes predictions.
    """
    repo_root = "."
    rows = load_dataset(repo_root)
    vocab = build_vocab()

    preds: List[Dict[str, int]] = []
    # Repeat to amplify overhead (still deterministic).
    for _ in range(1):
        preds = []
        for r in rows:
            t = str(r["text"])
            toks = tokenize(t)
            c = counts(toks, vocab)
            pred = predict_from_counts(c)
            preds.append({"id": int(r["id"]), "pred": int(pred)})

    write_predictions(repo_root, preds)
    return 0

