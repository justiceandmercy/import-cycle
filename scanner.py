"""Scan a Python package and extract its import graph."""

import ast
from pathlib import Path


def collect_modules(root):
    """Return (root_path, {dotted_module_name: Path})."""
    root_path = Path(root).resolve()
    modules = {}
    for path in root_path.rglob("*.py"):
        try:
            rel = path.relative_to(root_path)
        except ValueError:
            continue
        parts = list(rel.with_suffix("").parts)
        if parts and parts[-1] == "__init__":
            parts = parts[:-1]
        name = ".".join(parts)
        if name:
            modules[name] = path
    return root_path, modules


def _package_of(module_name, path):
    if path.name == "__init__.py":
        return module_name
    if "." in module_name:
        return module_name.rsplit(".", 1)[0]
    return ""


def _resolve_relative(base_parts, level, mod):
    if level > 1:
        if level - 1 > len(base_parts):
            return None
        base_parts = base_parts[: len(base_parts) - (level - 1)]
    if mod:
        return ".".join(base_parts + mod.split("."))
    return None


def parse_imports(path, module_name, modules):
    """Return set of module names (subset of modules) imported by path."""
    result = set()
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    except (SyntaxError, OSError, UnicodeDecodeError):
        return result

    package = _package_of(module_name, path)
    base_parts = package.split(".") if package else []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if name in modules:
                    result.add(name)
        elif isinstance(node, ast.ImportFrom):
            level = node.level or 0
            mod = node.module
            if level == 0:
                if mod and mod in modules:
                    result.add(mod)
                continue
            if level - 1 > len(base_parts):
                continue
            cur_base = base_parts[: len(base_parts) - (level - 1)] if level > 1 else list(base_parts)
            if mod:
                target = ".".join(cur_base + mod.split("."))
                if target in modules:
                    result.add(target)
            else:
                for alias in node.names:
                    if alias.name == "*":
                        continue
                    target = ".".join(cur_base + [alias.name])
                    if target in modules:
                        result.add(target)
    return result


def scan(root):
    """Convenience: collect modules and their resolved imports."""
    _root, modules = collect_modules(root)
    imports = {name: parse_imports(path, name, modules) for name, path in modules.items()}
    return modules, imports
