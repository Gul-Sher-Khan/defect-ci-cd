# tests/conftest.py
import os, sys

# project root: .../defect-ci-cd
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Add BOTH the root and the src folder to sys.path to be extra-safe on Windows
for p in (ROOT, os.path.join(ROOT, "src")):
    if p not in sys.path:
        sys.path.insert(0, p)
