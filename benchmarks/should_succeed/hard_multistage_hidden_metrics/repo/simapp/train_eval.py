from __future__ import annotations

import json
import os
from dataclasses import asdict, dataclass
from typing import Any, Dict

import numpy as np

from .data import make_dataset
from .features import build_features
from .model import SoftmaxModel, fit_softmax, predict


@dataclass(frozen=True)
class EvalResult:
    correct: int
    total: int

    def accuracy(self) -> float:
        if self.total <= 0:
            return 0.0
        return float(self.correct) / float(self.total)


def _model_path(workdir: str) -> str:
    return os.path.join(workdir, "model.json")


def _save_model(path: str, model: SoftmaxModel) -> None:
    obj = {
        "w": model.w.tolist(),
        "b": model.b.tolist(),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f)


def _load_model(path: str) -> SoftmaxModel:
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)
    w = np.asarray(obj["w"], dtype=np.float32)
    b = np.asarray(obj["b"], dtype=np.float32)
    return SoftmaxModel(w=w, b=b)


def run_train(*, workdir: str, seed: int) -> None:
    ds = make_dataset(seed=seed)
    feats = build_features(ds.x_train)

    model = fit_softmax(
        feats.x,
        ds.y_train,
        k=3,
        steps=12,
        lr=0.06,
        reg=0.001,
        seed=seed,
    )
    _save_model(_model_path(workdir), model)


def run_evaluate(*, workdir: str, seed: int) -> EvalResult:
    ds = make_dataset(seed=seed)
    model = _load_model(_model_path(workdir))

    feats = build_features(ds.x_val)
    pred = predict(model, feats.x)

    correct = int(np.sum(pred == ds.y_val))
    total = int(ds.y_val.shape[0])
    return EvalResult(correct=correct, total=total)

