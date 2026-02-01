from __future__ import annotations

import os
import shutil
from pathlib import Path
from textwrap import dedent


REPO_ROOT = Path(__file__).resolve().parent / "repo"


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _write_file(path: Path, content: str) -> None:
    _ensure_dir(path.parent)
    path.write_text(content.lstrip("\n"))


def generate_repo(n_noise_modules: int = 1000) -> None:
    """
    Generate a large repo in ./repo (relative to this benchmark folder).
    This intentionally floods the repo with many small modules, and includes
    a small "real" app with two entrypoints and two buggy library functions.
    """
    if REPO_ROOT.exists():
        shutil.rmtree(REPO_ROOT)
    _ensure_dir(REPO_ROOT)

    # -------------------------------------------------------------------------
    # "Real-feeling" app skeleton (cli/services/domain/infra/adapters)
    # -------------------------------------------------------------------------
    _write_file(
        REPO_ROOT / "README.md",
        dedent(
            """
            # Generated Large Repo Benchmark

            This repo is generated for Remoroo benchmarking.

            Entrypoints (multi-command):
            - `python run_alpha.py`
            - `python run_beta.py`

            The application is layered to support system-diagram extraction:
            - `cli/` entrypoints
            - `services/` orchestration
            - `domain/` business logic (intentional bugs live here)
            - `infra/` config/logging/utilities
            - `adapters/` small interfaces + implementations
            """
        ),
    )

    # Package inits
    for pkg in ["cli", "services", "domain", "domain/alpha", "domain/beta", "infra", "adapters", "pkg", "pkg/a_noise"]:
        _write_file(REPO_ROOT / pkg / "__init__.py", f'"""Package: {pkg}"""\n')

    # Infra utilities (used widely to create meaningful imports)
    _write_file(
        REPO_ROOT / "infra" / "logging.py",
        dedent(
            """
            from __future__ import annotations

            import time
            from dataclasses import dataclass
            from typing import Any, Dict, Optional


            @dataclass(frozen=True)
            class LogEvent:
                ts: float
                level: str
                name: str
                message: str
                fields: Dict[str, Any]


            class Logger:
                def __init__(self, name: str):
                    self.name = name

                def _emit(self, level: str, message: str, **fields: Any) -> LogEvent:
                    evt = LogEvent(ts=time.time(), level=level, name=self.name, message=message, fields=dict(fields))
                    # Intentionally quiet to keep benchmark output clean.
                    return evt

                def info(self, message: str, **fields: Any) -> LogEvent:
                    return self._emit("INFO", message, **fields)

                def warn(self, message: str, **fields: Any) -> LogEvent:
                    return self._emit("WARN", message, **fields)

                def error(self, message: str, **fields: Any) -> LogEvent:
                    return self._emit("ERROR", message, **fields)


            def get_logger(name: str) -> Logger:
                return Logger(name=name)
            """
        ),
    )
    _write_file(
        REPO_ROOT / "infra" / "config.py",
        dedent(
            """
            from __future__ import annotations

            from dataclasses import dataclass
            from typing import Optional


            @dataclass(frozen=True)
            class Settings:
                dataset_name: str = "deterministic_numbers"
                strict_mode: bool = True


            def load_settings(dataset_name: Optional[str] = None) -> Settings:
                # Deterministic, no file I/O required.
                if dataset_name:
                    return Settings(dataset_name=dataset_name)
                return Settings()
            """
        ),
    )
    _write_file(
        REPO_ROOT / "infra" / "types.py",
        dedent(
            """
            from __future__ import annotations

            from dataclasses import dataclass
            from typing import List


            @dataclass(frozen=True)
            class Record:
                values: List[int]
            """
        ),
    )

    # Adapters: a tiny interface boundary + one implementation
    _write_file(
        REPO_ROOT / "adapters" / "store.py",
        dedent(
            """
            from __future__ import annotations

            from dataclasses import dataclass
            from typing import Dict, Protocol, Any


            class KeyValueStore(Protocol):
                def put(self, key: str, value: Any) -> None: ...
                def get(self, key: str) -> Any: ...


            @dataclass
            class InMemoryStore:
                data: Dict[str, Any]

                def put(self, key: str, value: Any) -> None:
                    self.data[key] = value

                def get(self, key: str) -> Any:
                    return self.data.get(key)
            """
        ),
    )

    # Data source (deterministic)
    _write_file(
        REPO_ROOT / "domain" / "data_source.py",
        dedent(
            """
            from __future__ import annotations

            from typing import List
            from infra.types import Record


            def load_numbers() -> List[int]:
                # Deterministic dataset.
                return [1, 2, 3, 4]


            def load_record() -> Record:
                return Record(values=load_numbers())
            """
        ),
    )

    # Domain alpha (intentional bug lives here)
    _write_file(
        REPO_ROOT / "domain" / "alpha" / "compute.py",
        dedent(
            """
            from __future__ import annotations

            from typing import Iterable


            def sum_numbers(nums: Iterable[int]) -> int:
                \"\"\"Sum numbers.

                BUG (intentional): drops the last element.
                \"\"\"
                xs = list(nums)
                return sum(xs[:-1])
            """
        ),
    )
    # Domain beta (intentional bug lives here)
    _write_file(
        REPO_ROOT / "domain" / "beta" / "stats.py",
        dedent(
            """
            from __future__ import annotations

            from typing import Iterable


            def mean_numbers(nums: Iterable[int]) -> float:
                \"\"\"Mean numbers.

                BUG (intentional): divides by (n - 1).
                \"\"\"
                xs = list(nums)
                if not xs:
                    return 0.0
                return sum(xs) / (len(xs) - 1)
            """
        ),
    )

    # Services: orchestration layer that uses infra + domain + adapters
    _write_file(
        REPO_ROOT / "services" / "alpha_service.py",
        dedent(
            """
            from __future__ import annotations

            from dataclasses import dataclass
            from typing import List

            from adapters.store import KeyValueStore
            from domain.data_source import load_record
            from domain.alpha.compute import sum_numbers
            from infra.logging import get_logger


            @dataclass(frozen=True)
            class AlphaResult:
                alpha_sum: int


            def run_alpha(store: KeyValueStore) -> AlphaResult:
                log = get_logger("alpha_service")
                rec = load_record()
                log.info("loaded_record", n=len(rec.values))
                val = sum_numbers(rec.values)
                store.put("alpha_sum", val)
                return AlphaResult(alpha_sum=val)
            """
        ),
    )
    _write_file(
        REPO_ROOT / "services" / "beta_service.py",
        dedent(
            """
            from __future__ import annotations

            from dataclasses import dataclass

            from adapters.store import KeyValueStore
            from domain.data_source import load_record
            from domain.beta.stats import mean_numbers
            from infra.logging import get_logger


            @dataclass(frozen=True)
            class BetaResult:
                beta_mean: float


            def run_beta(store: KeyValueStore) -> BetaResult:
                log = get_logger("beta_service")
                rec = load_record()
                log.info("loaded_record", n=len(rec.values))
                val = mean_numbers(rec.values)
                store.put("beta_mean", val)
                return BetaResult(beta_mean=val)
            """
        ),
    )

    # CLI layer: thin entrypoints that call services
    _write_file(
        REPO_ROOT / "cli" / "alpha.py",
        dedent(
            """
            from __future__ import annotations

            from adapters.store import InMemoryStore
            from services.alpha_service import run_alpha


            def main() -> None:
                store = InMemoryStore(data={})
                _res = run_alpha(store)
                print("alpha complete")
            """
        ),
    )
    _write_file(
        REPO_ROOT / "cli" / "beta.py",
        dedent(
            """
            from __future__ import annotations

            from adapters.store import InMemoryStore
            from services.beta_service import run_beta


            def main() -> None:
                store = InMemoryStore(data={})
                _res = run_beta(store)
                print("beta complete")
            """
        ),
    )

    # Root entrypoints (keep stable names, but route through cli)
    _write_file(
        REPO_ROOT / "run_alpha.py",
        dedent(
            """
            from cli.alpha import main

            if __name__ == "__main__":
                main()
            """
        ),
    )
    _write_file(
        REPO_ROOT / "run_beta.py",
        dedent(
            """
            from cli.beta import main

            if __name__ == "__main__":
                main()
            """
        ),
    )

    # Flood the repo with many "real-ish" modules for indexing/navigation stress.
    # Keep them alphabetically early so they dominate truncated summaries.
    noise_root = REPO_ROOT / "pkg" / "a_noise"
    for i in range(n_noise_modules):
        _write_file(
            noise_root / f"mod_{i:04d}.py",
            dedent(
                f"""
                from __future__ import annotations

                from dataclasses import dataclass
                from typing import List, Dict

                from infra.logging import get_logger

                VALUE: int = {i}


                @dataclass(frozen=True)
                class NoiseResult:
                    module_id: int
                    inputs: List[int]
                    outputs: List[int]


                def transform(x: int) -> int:
                    \"\"\"Tiny deterministic transform used by other modules.\"\"\"
                    return x + VALUE


                def batch_transform(xs: List[int]) -> NoiseResult:
                    log = get_logger(f"noise.mod_{i:04d}")
                    ys = [transform(v) for v in xs]
                    log.info("batch_transform", n=len(xs), module_id=VALUE)
                    return NoiseResult(module_id=VALUE, inputs=list(xs), outputs=ys)


                def summarize(res: NoiseResult) -> Dict[str, int]:
                    \"\"\"Return a small summary to create more symbols.\"\"\"
                    return {{
                        "module_id": res.module_id,
                        "count": len(res.outputs),
                        "min": min(res.outputs) if res.outputs else 0,
                        "max": max(res.outputs) if res.outputs else 0,
                    }}
                """
            ),
        )


def main() -> None:
    n = int(os.environ.get("REMOROO_NOISE_MODULES", "1000"))
    generate_repo(n_noise_modules=n)
    print(f"generated_repo={REPO_ROOT}")
    print(f"noise_modules={n}")


if __name__ == "__main__":
    main()

