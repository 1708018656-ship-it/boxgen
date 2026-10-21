# Contributing

1. Fork, then `python -m venv .venv && . .venv/bin/activate && pip install -e ".[dev,preview]"`.
2. Make your change; every new shape must produce a mesh that passes `Mesh.check()` (watertight, consistent winding, outward normals). Add a test in `tests/`.
3. Run `pytest` and open a pull request with a short description.

Keep the core dependency-free (pure Python standard library).
