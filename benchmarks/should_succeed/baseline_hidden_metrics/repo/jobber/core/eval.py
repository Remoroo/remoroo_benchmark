from typing import Dict, List


def accuracy(rows: List[Dict[str, object]], preds: Dict[int, int]) -> float:
    correct = 0
    total = 0
    for r in rows:
        i = int(r["id"])
        y = int(r["label"])
        p = int(preds.get(i, 0))
        total += 1
        if p == y:
            correct += 1
    return correct / max(1, total)

