from __future__ import annotations

import os
import random
import shutil
from pathlib import Path
from textwrap import dedent


REPO_ROOT = Path(__file__).resolve().parent / "repo"


def _ensure_dir(p: Path) -> None:
    p.mkdir(parents=True, exist_ok=True)


def _write(path: Path, content: str) -> None:
    _ensure_dir(path.parent)
    path.write_text(content.lstrip("\n"), encoding="utf-8")


def _py_header(module_doc: str) -> str:
    return dedent(
        f"""
        from __future__ import annotations

        \"\"\"{module_doc}\"\"\"
        """
    )


def generate_repo(n_noise_modules: int = 1000, seed: int = 1337) -> None:
    """
    Generate a large, realistic-ish repo in ./repo for benchmarking.

    Key properties:
    - Layered architecture: cli/ -> services/ -> domain/ (+ infra/, adapters/)
    - Two entrypoints (multi-command): run_server.py and run_client.py
    - Deterministic workload: 50 requests
    - Two real tasks:
      1) correctness bug (wrong responses)
      2) efficiency bug (parses config once per request instead of once overall)
    - Large import graph: many "noise" modules + a registry that imports a subset.
    """
    random.seed(seed)

    if REPO_ROOT.exists():
        shutil.rmtree(REPO_ROOT)
    _ensure_dir(REPO_ROOT)

    _write(
        REPO_ROOT / "README.md",
        dedent(
            """
            # Generated Service+Client Benchmark Repo

            Entrypoints:
            - `python run_server.py` (bootstrap / warmup)
            - `python run_client.py` (runs deterministic workload)

            Metrics are intentionally *not* printed; they are expected to be emitted to `artifacts/metrics.json`
            via Remoroo instrumentation.
            """
        ),
    )

    # ---------------------------------------------------------------------
    # Packages / init
    # ---------------------------------------------------------------------
    for pkg in [
        "cli",
        "services",
        "domain",
        "domain/handlers",
        "infra",
        "adapters",
        "pkg",
        "pkg/a_noise",
    ]:
        _write(REPO_ROOT / pkg / "__init__.py", _py_header(f"Package: {pkg}") + "\n")

    # ---------------------------------------------------------------------
    # Infra: logging, timing, and config parsing (efficiency bug lives here)
    # ---------------------------------------------------------------------
    _write(
        REPO_ROOT / "infra" / "logging.py",
        _py_header("Lightweight logging primitives (silent by default).")
        + dedent(
            """
            import time
            from dataclasses import dataclass
            from typing import Any, Dict

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
                    return LogEvent(ts=time.time(), level=level, name=self.name, message=message, fields=dict(fields))

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

    _write(
        REPO_ROOT / "infra" / "timing.py",
        _py_header("Deterministic timing helpers used for 'latency units' style metrics.")
        + dedent(
            """
            from dataclasses import dataclass
            from typing import List

            @dataclass
            class LatencyTracker:
                samples: List[int]

                def __init__(self):
                    self.samples = []

                def add(self, units: int) -> None:
                    self.samples.append(int(units))

                def p95(self) -> int:
                    if not self.samples:
                        return 0
                    xs = sorted(self.samples)
                    # nearest-rank p95
                    idx = int((0.95 * (len(xs) - 1)))
                    return xs[idx]
            """
        ),
    )

    # Efficiency bug: parse_config increments parse_calls every time it is invoked.
    # The "fix" is to cache the parsed config (e.g., memoize load_config()) so parse_calls becomes 1 for the full workload.
    _write(
        REPO_ROOT / "infra" / "config_loader.py",
        _py_header("Config parsing and loading utilities (intentionally inefficient baseline).")
        + dedent(
            """
            from dataclasses import dataclass
            from typing import Dict, Any

            _PARSE_CALLS = 0

            @dataclass(frozen=True)
            class Config:
                mode: str
                flags: Dict[str, Any]

            def parse_calls() -> int:
                return _PARSE_CALLS

            def parse_config(text: str) -> Config:
                \"\"\"Parse config text.

                BUG (intentional inefficiency): this parser is called once per request in baseline.
                \"\"\"
                global _PARSE_CALLS
                _PARSE_CALLS += 1
                # Simulate 'parsing work' deterministically.
                parts = [p.strip() for p in text.split(",") if p.strip()]
                mode = parts[0] if parts else "default"
                flags = {f"f{i}": (len(p) % 2 == 0) for i, p in enumerate(parts[1:])}
                return Config(mode=mode, flags=flags)

            def load_config() -> Config:
                \"\"\"Load configuration.

                Baseline: returns parse_config(...) every call (inefficient).
                Fix: cache/memoize the Config so parse_calls() == 1 across the workload.
                \"\"\"
                text = "prod,alpha,beta,gamma,delta"
                return parse_config(text)
            """
        ),
    )

    # ---------------------------------------------------------------------
    # Domain: request/response + handlers (correctness bug lives here)
    # ---------------------------------------------------------------------
    _write(
        REPO_ROOT / "domain" / "protocol.py",
        _py_header("Core request/response protocol types.")
        + dedent(
            """
            from dataclasses import dataclass
            from typing import Dict, Any

            @dataclass(frozen=True)
            class Request:
                op: str
                payload: Dict[str, Any]

            @dataclass(frozen=True)
            class Response:
                ok: bool
                result: Any
                error: str = ""
            """
        ),
    )

    _write(
        REPO_ROOT / "domain" / "handlers" / "math_handler.py",
        _py_header("Math handler (intentionally buggy correctness).")
        + dedent(
            """
            from typing import List

            def sum_numbers(xs: List[int]) -> int:
                return sum(xs)

            def mean_numbers(xs: List[int]) -> float:
                # BUG (intentional correctness): uses (n - 1) in denominator.
                if not xs:
                    return 0.0
                return sum(xs) / (len(xs) - 1)
            """
        ),
    )

    _write(
        REPO_ROOT / "domain" / "handlers" / "router.py",
        _py_header("Domain request router that maps ops to handler functions.")
        + dedent(
            """
            from __future__ import annotations

            from typing import Any, Dict, List
            from domain.protocol import Request, Response
            from domain.handlers.math_handler import sum_numbers, mean_numbers

            def handle(req: Request) -> Response:
                op = req.op
                payload = req.payload or {}
                if op == "sum":
                    xs = list(payload.get("xs") or [])
                    return Response(ok=True, result=sum_numbers(xs))
                if op == "mean":
                    xs = list(payload.get("xs") or [])
                    return Response(ok=True, result=mean_numbers(xs))
                return Response(ok=False, result=None, error=f"unknown_op:{op}")
            """
        ),
    )

    # ---------------------------------------------------------------------
    # Services: dispatcher (uses config; does per-request load_config in baseline)
    # ---------------------------------------------------------------------
    _write(
        REPO_ROOT / "services" / "dispatcher.py",
        _py_header("Service layer dispatcher (baseline does extra work per request).")
        + dedent(
            """
            from __future__ import annotations

            from dataclasses import dataclass
            from typing import Iterable, List

            from domain.protocol import Request, Response
            from domain.handlers.router import handle
            from infra.config_loader import load_config, parse_calls
            from infra.timing import LatencyTracker
            from infra.logging import get_logger

            @dataclass(frozen=True)
            class DispatchReport:
                responses: List[Response]
                correct_responses: int
                parse_calls: int
                p95_latency_units: int

            def dispatch_requests(requests: Iterable[Request]) -> DispatchReport:
                log = get_logger("dispatcher")
                tracker = LatencyTracker()
                responses: List[Response] = []
                correct = 0

                for req in requests:
                    # BUG (intentional inefficiency): reload/parse config per request.
                    cfg = load_config()
                    # Deterministic "latency units" proxy.
                    latency_units = 5 + (1 if cfg.mode == "prod" else 3) + len(cfg.flags)

                    resp = handle(req)
                    responses.append(resp)

                    # Deterministic correctness criterion:
                    # - "sum" always ok
                    # - "mean" should equal 2.5 for xs=[1,2,3,4]
                    if req.op == "sum" and resp.ok and resp.result == 10:
                        correct += 1
                    elif req.op == "mean" and resp.ok and abs(float(resp.result) - 2.5) < 1e-9:
                        correct += 1

                    tracker.add(latency_units)
                    log.info("handled", op=req.op, ok=resp.ok)

                return DispatchReport(
                    responses=responses,
                    correct_responses=correct,
                    parse_calls=parse_calls(),
                    p95_latency_units=tracker.p95(),
                )
            """
        ),
    )

    # ---------------------------------------------------------------------
    # CLI: server bootstrap + client workload
    # ---------------------------------------------------------------------
    _write(
        REPO_ROOT / "cli" / "server.py",
        _py_header("Server bootstrap (short-lived).")
        + dedent(
            """
            from __future__ import annotations

            from dataclasses import dataclass
            from infra.logging import get_logger

            @dataclass(frozen=True)
            class ServerBootResult:
                server_boot_ok: int
                build_id: str

            def main() -> ServerBootResult:
                log = get_logger("server")
                # short-lived bootstrap; used to force multi-command planning
                log.info("boot")
                return ServerBootResult(server_boot_ok=1, build_id="bench-1")
            """
        ),
    )

    _write(
        REPO_ROOT / "cli" / "client.py",
        _py_header("Client workload runner (deterministic).")
        + dedent(
            """
            from __future__ import annotations

            from dataclasses import dataclass
            from typing import List

            from domain.protocol import Request
            from services.dispatcher import dispatch_requests, DispatchReport

            @dataclass(frozen=True)
            class ClientResult:
                correct_responses: int
                parse_calls: int
                p95_latency_units: int

            def build_requests(n: int = 50) -> List[Request]:
                # Deterministic: alternate sum/mean over the same payload.
                reqs: List[Request] = []
                for i in range(n):
                    op = "sum" if (i % 2 == 0) else "mean"
                    reqs.append(Request(op=op, payload={"xs": [1, 2, 3, 4]}))
                return reqs

            def main() -> ClientResult:
                report: DispatchReport = dispatch_requests(build_requests(50))
                return ClientResult(
                    correct_responses=report.correct_responses,
                    parse_calls=report.parse_calls,
                    p95_latency_units=report.p95_latency_units,
                )
            """
        ),
    )

    # Root entrypoints (thin wrappers; do not print metric keys/values)
    _write(
        REPO_ROOT / "run_server.py",
        dedent(
            """
            from cli.server import main

            if __name__ == "__main__":
                _ = main()
                print("server complete")
            """
        ),
    )
    _write(
        REPO_ROOT / "run_client.py",
        dedent(
            """
            from cli.client import main

            if __name__ == "__main__":
                _ = main()
                print("client complete")
            """
        ),
    )

    # ---------------------------------------------------------------------
    # Noise modules: larger, real-ish, and cross-import infra.logging.
    # Also generate a registry that imports a subset for a denser import graph.
    # ---------------------------------------------------------------------
    noise_root = REPO_ROOT / "pkg" / "a_noise"
    imported_indices = sorted(random.sample(range(n_noise_modules), k=min(60, n_noise_modules)))

    # Registry imports a subset (static imports) so the indexer sees a graph.
    reg_lines = [
        _py_header("Noise registry to create a real-ish import graph.").rstrip(),
        "from dataclasses import dataclass",
        "from typing import Dict, Callable",
        "",
        "from infra.logging import get_logger",
        "",
        "@dataclass(frozen=True)",
        "class Plugin:",
        "    name: str",
        "    f: Callable[[int], int]",
        "",
        "REGISTRY: Dict[str, Plugin] = {}",
        "",
        "def register(name: str, f: Callable[[int], int]) -> None:",
        "    REGISTRY[name] = Plugin(name=name, f=f)",
        "",
    ]

    for i in imported_indices:
        reg_lines.append(f"from pkg.a_noise.mod_{i:04d} import transform as transform_{i:04d}")
        reg_lines.append(f"register('p{i:04d}', transform_{i:04d})")
    reg_lines.append("")
    reg_lines.append("def count() -> int:")
    reg_lines.append("    return len(REGISTRY)")
    reg_lines.append("")
    _write(noise_root / "registry.py", "\n".join(reg_lines) + "\n")

    for i in range(n_noise_modules):
        _write(
            noise_root / f"mod_{i:04d}.py",
            _py_header(f"Noise module {i:04d} (used for indexing/navigation stress).")
            + dedent(
                f"""
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
                    \"\"\"Deterministic transform.\"\"\"
                    return x + VALUE

                def batch_transform(xs: List[int]) -> NoiseResult:
                    log = get_logger(f"noise.mod_{i:04d}")
                    ys = [transform(v) for v in xs]
                    log.info("batch_transform", n=len(xs), module_id=VALUE)
                    return NoiseResult(module_id=VALUE, inputs=list(xs), outputs=ys)

                def summarize(res: NoiseResult) -> Dict[str, int]:
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
    seed = int(os.environ.get("REMOROO_SEED", "1337"))
    generate_repo(n_noise_modules=n, seed=seed)
    print(f"generated_repo={REPO_ROOT}")
    print(f"noise_modules={n}")


if __name__ == "__main__":
    main()

