from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class Dataset:
    x_train: np.ndarray
    y_train: np.ndarray
    x_val: np.ndarray
    y_val: np.ndarray


def make_dataset(*, seed: int, n: int = 6500, d: int = 25, k: int = 3) -> Dataset:
    rng = np.random.RandomState(seed)

    centers = rng.normal(loc=0.0, scale=2.0, size=(k, d)).astype(np.float32)
    labels = rng.randint(0, k, size=(n,), dtype=np.int64)
    noise = rng.normal(loc=0.0, scale=2.0, size=(n, d)).astype(np.float32)
    x = centers[labels] + noise

    # Split deterministically
    idx = np.arange(n, dtype=np.int64)
    rng.shuffle(idx)
    split = int(0.8 * n)
    train_idx = idx[:split]
    val_idx = idx[split:]

    x_train = x[train_idx]
    y_train = labels[train_idx]
    x_val = x[val_idx]
    y_val = labels[val_idx]

    return Dataset(
        x_train=x_train,
        y_train=y_train,
        x_val=x_val,
        y_val=y_val,
    )

