"""Build an import graph and find circular imports."""

from typing import Dict, List, Set


def build_graph(imports: Dict[str, Set[str]]) -> Dict[str, List[str]]:
    return {name: sorted(targets) for name, targets in imports.items()}


def find_cycles(adj: Dict[str, List[str]]) -> List[List[str]]:
    """Return a list of simple cycles, each as an ordered list of module names."""
    nodes = sorted(adj.keys())
    index = {name: i for i, name in enumerate(nodes)}
    found: Set[tuple] = set()
    cycles: List[List[str]] = []

    def dfs(start: str, node: str, path: List[str]) -> None:
        for nb in adj.get(node, []):
            if nb not in index:
                continue
            if index[nb] < index[start]:
                continue
            if nb == start:
                if len(path) >= 2:
                    key = tuple(path)
                    if key not in found:
                        found.add(key)
                        cycles.append(list(path))
            elif nb not in path:
                dfs(start, nb, path + [nb])

    for start in nodes:
        dfs(start, start, [start])
    return cycles
