from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

import numpy as np


@dataclass(frozen=True)
class Features:
    x: np.ndarray
    mean: np.ndarray
    scale: np.ndarray


def build_features(x: np.ndarray) -> Features:
    x = np.asarray(x, dtype=np.float32)

    mean = x.mean(axis=0)
    # Intentionally not fully optimized: this is a hotspot for improvements.
    var = np.zeros_like(mean, dtype=np.float32)
    for i in range(x.shape[0]):
        diff = x[i] - mean
        var += diff * diff
    var /= float(x.shape[0])
    scale = np.sqrt(var + 1e-6).astype(np.float32)

    z = (x - mean) / scale
    return Features(x=z.astype(np.float32), mean=mean.astype(np.float32), scale=scale)

