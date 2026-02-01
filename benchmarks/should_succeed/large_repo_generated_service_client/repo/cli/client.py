from __future__ import annotations

"""Client workload runner (deterministic)."""

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
