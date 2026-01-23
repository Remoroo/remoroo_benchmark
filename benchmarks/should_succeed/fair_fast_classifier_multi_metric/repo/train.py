from __future__ import annotations

import json
import os
import time
from typing import Dict

import numpy as np

import config
from data import make_synthetic, train_test_split
from metrics import compute_all
from model import init_model, step_sgd


def train_one_run() -> Dict[str, float]:
    ds = make_synthetic(seed=config.SEED, n_samples=config.N_SAMPLES, n_features=config.N_FEATURES)
    train, test = train_test_split(ds, train_fraction=config.TRAIN_FRACTION, seed=config.SEED)

    # Standardize features using TRAIN stats only
    mu = train.X.mean(axis=0)
    sigma = train.X.std(axis=0) + 1e-8
    X_train = (train.X - mu) / sigma
    X_test = (test.X - mu) / sigma

    model = init_model(n_features=X_train.shape[1], seed=config.SEED)

    t0 = time.time()

    # Intentionally slow / unstable training loop (benchmark starts "hard")
    n = X_train.shape[0]
    for epoch in range(config.EPOCHS):
        # crude "fairness" term: not actually correct; kept as a trap
        fairness_grad = 0.0
        if config.FAIRNESS_WEIGHT != 0.0:
            fairness_grad = config.FAIRNESS_WEIGHT * 0.01

        for i in range(n):
            step_sgd(
                model=model,
                x=X_train[i],
                y=int(train.y[i]),
                lr=config.LEARNING_RATE,
                l2_reg=config.L2_REG,
                fairness_grad=fairness_grad,
            )

        # Early stop heuristic (bad: uses test labels indirectly by peeking at test predictions distribution)
        if epoch % 50 == 0:
            probs = model.predict_proba(X_test)
            if float(np.mean(probs)) < 0.05 or float(np.mean(probs)) > 0.95:
                # Degenerate; keep going anyway (wastes time)
                pass

    training_time = time.time() - t0

    y_prob = model.predict_proba(X_test)
    y_pred = (y_prob >= 0.5).astype(np.int64)
    metrics = compute_all(y_true=test.y, y_prob=y_prob, y_pred=y_pred, g=test.g)
    metrics["training_time"] = float(training_time)
    return metrics


def main() -> None:
    metrics: Dict[str, float]
    try:
        metrics = train_one_run()
    except Exception as e:
        metrics = {"error": str(e)}  # type: ignore[assignment]

    os.makedirs("artifacts", exist_ok=True)
    with open(os.path.join("artifacts", "metrics.json"), "w") as f:
        json.dump(metrics, f, indent=2)

    # Also print a minimal summary for stdout_regex extraction
    for k in ["accuracy", "loss", "fairness_gap", "training_time"]:
        if k in metrics:
            print(f"{k}: {metrics[k]}")


if __name__ == "__main__":
    main()


