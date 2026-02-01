from __future__ import annotations

"""Server bootstrap (short-lived)."""

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
