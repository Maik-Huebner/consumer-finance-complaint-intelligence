# Dependency lock

`lock-py311.txt` and `lock-py313.txt` pin the complete runtime, test, quality,
and build environments. Separate locks are required because the newest NumPy
line available to Python 3.13 does not provide a Python 3.11 wheel.

The package itself is installed separately and without dependency resolution:

```bash
python -m pip install -r requirements/lock-py313.txt  # or lock-py311.txt
python -m pip install --no-deps --no-build-isolation .
```

Builds use the already locked build tools:

```bash
python -m build --no-isolation
```

`requirements.in` records the direct resolution inputs. When dependencies
change, resolve both complete environments again, verify Linux-wheel
availability, and update both locks as one reviewable change. Open minimum
versions remain in `pyproject.toml` for package metadata; CI and release
validation always use the matching exact lock.
