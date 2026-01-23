from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class Dataset:
    X: np.ndarray  # (N, D)
    y: np.ndarray  # (N,)
    g: np.ndarray  # (N,) group membership: 0 or 1


def make_synthetic(seed: int, n_samples: int, n_features: int) -> Dataset:
    """
    Synthetic binary classification with group-dependent shift.
    The task is solvable with a linear model, but naive training can become unstable.
    """
    rng = np.random.RandomState(seed)

    # Group membership
    g = (rng.rand(n_samples) > 0.5).astype(np.int64)

    # Features: base gaussian + group-specific shift on a few dimensions
    X = rng.randn(n_samples, n_features).astype(np.float64)
    shift = np.zeros((n_features,), dtype=np.float64)
    shift[:3] = 0.8  # group shift affects first 3 features
    X = X + (g[:, None] * shift[None, :])

    # True weights
    w_true = rng.randn(n_features).astype(np.float64)
    w_true[:3] += 1.5  # make the shifted dimensions predictive
    b_true = -0.2

    logits = X @ w_true + b_true
    p = 1.0 / (1.0 + np.exp(-logits))

    # Add label noise that differs slightly by group (creates fairness pressure)
    noise = rng.rand(n_samples)
    flip = (noise < (0.04 + 0.03 * g)).astype(np.int64)
    y = (p > 0.5).astype(np.int64)
    y = (y ^ flip).astype(np.int64)

    return Dataset(X=X, y=y, g=g)


def train_test_split(ds: Dataset, train_fraction: float, seed: int) -> Tuple[Dataset, Dataset]:
    rng = np.random.RandomState(seed + 1)
    n = ds.X.shape[0]
    idx = np.arange(n)
    rng.shuffle(idx)
    n_train = int(train_fraction * n)
    train_idx = idx[:n_train]
    test_idx = idx[n_train:]

    train = Dataset(X=ds.X[train_idx], y=ds.y[train_idx], g=ds.g[train_idx])
    test = Dataset(X=ds.X[test_idx], y=ds.y[test_idx], g=ds.g[test_idx])
    return train, test


