from __future__ import annotations

from adapters.store import InMemoryStore
from services.alpha_service import run_alpha
import os

def main() -> None:
    store = InMemoryStore(data={})
    _res = run_alpha(store)
    print("alpha complete")