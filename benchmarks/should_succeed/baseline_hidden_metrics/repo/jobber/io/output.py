import json
import os
from typing import Dict, List


def write_predictions(repo_root: str, preds: List[Dict[str, int]]) -> None:
    os.makedirs(os.path.join(repo_root, "artifacts"), exist_ok=True)
    path = os.path.join(repo_root, "artifacts", "preds.jsonl")
    with open(path, "w") as f:
        for p in preds:
            f.write(json.dumps(p) + "\n")


def load_predictions(repo_root: str) -> Dict[int, int]:
    path = os.path.join(repo_root, "artifacts", "preds.jsonl")
    out: Dict[int, int] = {}
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            out[int(obj["id"])] = int(obj["pred"])
    return out

