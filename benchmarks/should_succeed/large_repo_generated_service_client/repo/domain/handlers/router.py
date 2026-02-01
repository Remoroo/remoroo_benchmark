from __future__ import annotations

"""Domain request router that maps ops to handler functions."""

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
