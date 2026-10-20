"""Command-line entry point for import-cycle."""

import argparse
import sys

from graph import build_graph, find_cycles
from scanner import scan


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="import-cycle",
        description="Detect circular imports in a Python package.",
    )
    parser.add_argument("path", nargs="?", default=".", help="root directory to scan")
    args = parser.parse_args(argv)

    _modules, imports = scan(args.path)
    adj = build_graph(imports)
    cycles = find_cycles(adj)

    if not cycles:
        print("No circular imports found.")
        return 0

    print(f"Found {len(cycles)} circular import(s):")
    for cycle in cycles:
        print(" -> ".join(cycle + [cycle[0]]))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
