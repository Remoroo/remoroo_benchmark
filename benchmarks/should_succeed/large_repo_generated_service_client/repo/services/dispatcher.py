from __future__ import annotations

"""Service layer dispatcher (baseline does extra work per request)."""

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
