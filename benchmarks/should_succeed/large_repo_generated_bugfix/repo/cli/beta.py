from __future__ import annotations

from adapters.store import InMemoryStore
from services.beta_service import run_beta

def main() -> None:
    store = InMemoryStore(data={})
    _res = run_beta(store)
    print("beta complete")