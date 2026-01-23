from __future__ import annotations

import argparse
import os
import sys

from .train_eval import run_evaluate, run_train


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="simapp")
    g = p.add_mutually_exclusive_group(required=True)
    g.add_argument("--train", action="store_true")
    g.add_argument("--evaluate", action="store_true")
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--workdir", type=str, default="workdir")
    return p


def main(argv: list[str] | None = None) -> None:
    argv = list(sys.argv[1:] if argv is None else argv)
    args = _build_parser().parse_args(argv)

    workdir = args.workdir
    os.makedirs(workdir, exist_ok=True)

    if args.train:
        run_train(workdir=workdir, seed=int(args.seed))
        sys.stdout.write("ok\n")
        return

    if args.evaluate:
        run_evaluate(workdir=workdir, seed=int(args.seed))
        sys.stdout.write("ok\n")
        return

    raise SystemExit(2)

