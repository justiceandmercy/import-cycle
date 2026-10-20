# import-cycle

Detect circular imports in Python packages and report the dependency cycle.

## Description

`import-cycle` walks a directory of Python source, builds a module-level import graph, and
reports every circular import it finds. Circular imports are a common source of
`ImportError`, partially-initialized modules, and confusing startup failures. This tool gives
you a clear, ordered list of the cycle so you can break it.

## Features

- Pure standard library — no dependencies to install.
- Resolves both absolute and relative imports.
- Understands packages (`__init__.py`) and nested modules.
- Reports each cycle once, in import order.
- Exit code `1` when cycles are found, `0` otherwise (CI-friendly).
- Skips files with syntax errors instead of crashing.

## Install

```sh
git clone https://github.com/yourname/import-cycle.git
cd import-cycle
```

No third-party packages are required. Python 3.9+ is sufficient.

Optional editable install:

```sh
pip install -e .
```

## Usage

Scan the current directory:

```sh
python cli.py
```

Scan a specific package:

```sh
python cli.py src/mypackage
```

Example output:

```
Found 1 circular import(s):
mypackage.a -> mypackage.b -> mypackage.c -> mypackage.a
```

Use as a library:

```python
from scanner import collect_modules, parse_imports
from graph import find_cycles

root_path, modules = collect_modules("src")
imports = {name: parse_imports(path, name, modules) for name, path in modules.items()}
cycles = find_cycles(imports)
print(cycles)
```

## How it works

1. `scanner.collect_modules` walks the tree and maps dotted module names to files.
2. `scanner.parse_imports` uses `ast` to extract imports and resolve them to module names.
3. `graph.find_cycles` runs a depth-first search that enumerates simple cycles once.

## License

MIT
