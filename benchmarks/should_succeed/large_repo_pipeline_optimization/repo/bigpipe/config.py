from dataclasses import dataclass


@dataclass(frozen=True)
class Config:
    seed: int = 1337
    n_rows: int = 12000
    vocab_size: int = 5000
    # Pipeline repeats work to simulate a larger workload; optimizations should reduce overhead.
    repeats: int = 3


CFG = Config()

