from typing import Dict, Any, List

from .config import CFG
from .data_gen import make_dataset
from .features import featurize
from .metrics import checksum_predictions, expected_checksum
from .model import predict
from .tokenize import tokenize
from .vocab import build_vocab_list


def run_pipeline() -> Dict[str, Any]:
    """
    Full pipeline:
    - build dataset
    - build vocab
    - tokenize + featurize each row
    - predict labels
    - compute checksum correctness

    Intentionally repeats work to amplify performance costs.
    Optimizations should reduce overhead across multiple modules.
    """
    rows = make_dataset()
    vocab_list = build_vocab_list()

    y_pred: List[int] = []
    for _ in range(CFG.repeats):
        y_pred = []
        for text, _label in rows:
            toks = tokenize(text)
            counts = featurize(toks, vocab_list)
            y_pred.append(predict(counts))

    checksum = checksum_predictions(y_pred)
    expected = expected_checksum(rows)
    return {
        "num_rows": len(rows),
        "checksum": checksum,
        "correctness": checksum == expected,
    }

