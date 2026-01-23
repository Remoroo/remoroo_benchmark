from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass
class SoftmaxModel:
    w: np.ndarray  # (d, k)
    b: np.ndarray  # (k,)


def _softmax(logits: np.ndarray) -> np.ndarray:
    m = logits.max(axis=1, keepdims=True)
    z = logits - m
    exp = np.exp(z)
    return exp / exp.sum(axis=1, keepdims=True)


def fit_softmax(
    x: np.ndarray,
    y: np.ndarray,
    *,
    k: int,
    steps: int,
    lr: float,
    reg: float,
    seed: int,
) -> SoftmaxModel:
    rng = np.random.RandomState(seed)
    x = np.asarray(x, dtype=np.float32)
    y = np.asarray(y, dtype=np.int64)
    n, d = x.shape

    w = (0.01 * rng.normal(size=(d, k))).astype(np.float32)
    b = np.zeros((k,), dtype=np.float32)

    # Slow but correct gradient descent (hotspot).
    for _ in range(int(steps)):
        dw = np.zeros_like(w)
        db = np.zeros_like(b)
        loss = 0.0

        for i in range(n):
            logits = x[i].dot(w) + b
            logits = logits - float(np.max(logits))
            exps = np.exp(logits).astype(np.float32)
            probs = exps / float(np.sum(exps))
            yi = int(y[i])
            loss += -float(np.log(max(float(probs[yi]), 1e-12)))

            for c in range(k):
                grad = float(probs[c]) - (1.0 if c == yi else 0.0)
                db[c] += grad
                for j in range(d):
                    dw[j, c] += grad * float(x[i, j])

        inv_n = 1.0 / float(n)
        dw = (dw * inv_n) + (reg * w)
        db = (db * inv_n)
        w -= (lr * dw).astype(np.float32)
        b -= (lr * db).astype(np.float32)

        _ = loss * inv_n + 0.5 * reg * float(np.sum(w * w))

    return SoftmaxModel(w=w, b=b)


def predict(model: SoftmaxModel, x: np.ndarray) -> np.ndarray:
    x = np.asarray(x, dtype=np.float32)
    logits = x.dot(model.w) + model.b
    probs = _softmax(logits)
    return probs.argmax(axis=1).astype(np.int64)

