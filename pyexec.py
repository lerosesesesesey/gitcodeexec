#!/usr/bin/env python3
"""Run a Python file or a short snippet of Python code."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path
from typing import Sequence


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Execute a Python file, or execute inline code with --code."
    )
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("script", nargs="?", type=Path, help="Python file to execute")
    source.add_argument("-c", "--code", help="Python code to execute")
    parser.add_argument(
        "script_args",
        nargs=argparse.REMAINDER,
        metavar="ARG",
        help="arguments passed to the Python file",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.code is not None:
        command = [sys.executable, "-c", args.code, *args.script_args]
    else:
        script = args.script.expanduser()
        if not script.is_file():
            print(f"pyexec: file not found: {script}", file=sys.stderr)
            return 2
        command = [sys.executable, str(script), *args.script_args]

    try:
        return subprocess.run(command, check=False).returncode
    except KeyboardInterrupt:
        return 130


if __name__ == "__main__":
    raise SystemExit(main())
