#!/usr/bin/env python3
"""Linting tool for 2048-game-204-2499 source architecture.

Enforces:
- Every file under src/ belongs to exactly one layer directory.
- Imports respect the forward dependency direction in src/README.md.
- No file exceeds 300 lines.

Exit 0 on clean codebase, exit 1 with violation list on failure.
"""

import ast
import os
import sys
from pathlib import Path

# Layer ordering for dependency checking
LAYERS = ["types", "config", "repo", "service", "runtime", "ui", "providers", "utils"]
LAYER_INDEX = {layer: idx for idx, layer in enumerate(LAYERS)}

# Permitted imports per layer (index into LAYERS)
PERMITTED = {
    "types": [0],
    "config": [0, 1],
    "repo": [0, 1, 2],
    "service": [0, 1, 2, 3, 5],  # service can import from providers (index 5 is providers, 3 is service)
    "runtime": [0, 1, 2, 3, 4, 5],  # runtime, providers
    "ui": [0, 1, 3, 4, 5, 6],  # types, config, service, runtime, providers, ui
    "providers": [0, 1, 6, 7],  # types, config, providers, utils
    "utils": [7],
}

# Convert to layer name sets
PERMITTED_LAYERS = {
    "types": {"types"},
    "config": {"types", "config"},
    "repo": {"types", "config", "repo"},
    "service": {"types", "config", "repo", "service", "providers"},
    "runtime": {"types", "config", "repo", "service", "runtime", "providers"},
    "ui": {"types", "config", "service", "runtime", "providers", "ui"},
    "providers": {"types", "config", "utils", "providers"},
    "utils": {"utils"},
}


def get_layer(file_path: Path) -> str | None:
    """Determine which layer a file belongs to."""
    src_root = Path("src")
    try:
        rel_path = file_path.relative_to(src_root)
        parts = rel_path.parts
        if len(parts) > 0:
            layer = parts[0]
            if layer in LAYERS:
                return layer
    except ValueError:
        pass
    return None


def get_imported_modules(tree: ast.Module) -> list[str]:
    """Extract all module names from import statements."""
    modules = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                modules.append(alias.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                modules.append(node.module.split(".")[0])
    return modules


def lint_file(file_path: Path) -> list[str]:
    """Lint a single Python file. Returns list of violations."""
    violations = []

    # Check line count
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            if len(lines) > 300:
                violations.append(f"{file_path}: exceeds 300 lines ({len(lines)} lines)")
    except Exception as e:
        violations.append(f"{file_path}: could not read file: {e}")
        return violations

    # Check imports
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        tree = ast.parse(content)
    except SyntaxError as e:
        violations.append(f"{file_path}: syntax error at line {e.lineno}: {e.msg}")
        return violations

    layer = get_layer(file_path)
    if layer is None:
        violations.append(f"{file_path}: file does not belong to any layer directory")
        return violations

    imported_modules = get_imported_modules(tree)

    # Check each import against layer's permitted imports
    for module in imported_modules:
        # Determine the layer of the imported module
        imported_layer = None
        for candidate in LAYERS:
            if module == candidate:
                imported_layer = candidate
                break

        if imported_layer is None:
            # External module or local package; allow
            continue

        permitted = PERMITTED_LAYERS[layer]
        if imported_layer not in permitted:
            violations.append(
                f"{file_path}: imports '{imported_layer}' which is not in allowed layers {permitted}"
            )

    return violations


def main() -> int:
    """Run linter on all .py files under src/. Returns exit code."""
    violations = []

    src_dir = Path("src")
    if not src_dir.exists():
        print("Error: src/ directory not found", file=sys.stderr)
        return 1

    for root, _, files in os.walk(src_dir):
        for filename in files:
            if filename.endswith(".py"):
                file_path = Path(root) / filename
                file_violations = lint_file(file_path)
                violations.extend(file_violations)

    if violations:
        print("Linting violations found:", file=sys.stderr)
        for v in violations:
            print(f"  {v}", file=sys.stderr)
        return 1

    print("Linting passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
