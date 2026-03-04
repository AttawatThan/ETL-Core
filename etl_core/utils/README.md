# Utils Module

Utility helpers for file system operations. The `FileSystem` class wraps `pathlib` and `shutil` with guardrails to make ETL tasks safe and predictable.

## Quick Start
```python
from etl_core.utils.file_system import FileSystem

# Ensure a directory exists
logs_dir = FileSystem.create_directory("data/logs/current")

# Move a file (creates destination parents automatically)
FileSystem.move("data/logs/app.log", "data/archive/app.log")

# Find files
csv_paths = FileSystem.find("data", "*.csv")

# Remove files or non-empty directories
FileSystem.remove("data/temp_cache")
```

## API
- `exists(target)`: Return True if the path exists.
- `is_file(target)`: True only when the path is an existing file.
- `is_directory(target)`: True only when the path is an existing directory.
- `create_directory(path)`: Create the directory and parents; returns `Path`.
- `move(src, dest)`: Move or rename; creates destination parents; raises `FileNotFoundError` if `src` is missing.
- `find(root, pattern="*")`: Return matched `Path` objects or an empty list if `root` is absent.
- `remove(target)`: Delete files or directories (even non-empty); returns False if target is missing.

## Notes
- Accepts both `str` and `pathlib.Path` inputs.
- All paths are normalized to absolute paths before operations.

---

# Number Utilities

Rounding helpers in `number_util.py` that provide deterministic rounding behaviour, avoiding Python's built-in `round()` which uses banker's rounding (round half to even).

## Quick Start
```python
from etl_core.utils.number_util import round_half_up, round_half_down

# Round half up (away from zero on .5)
round_half_up(2.5)        # 3
round_half_up(2.55, 1)    # 2.6
round_half_up(-2.5)       # -3

# Round half down (towards zero on .5)
round_half_down(2.5)      # 2
round_half_down(2.55, 1)  # 2.5
round_half_down(-2.5)     # -2

# Pass as string to avoid float imprecision
round_half_up("2.555", 2)   # 2.56
round_half_down("2.555", 2) # 2.55
```

## API
- `round_half_up(number, decimal_places=0)`: Round to nearest value; on exactly 0.5, round away from zero.
- `round_half_down(number, decimal_places=0)`: Round to nearest value; on exactly 0.5, round towards zero.

Both functions share the same signature:

| Parameter | Type | Description |
|---|---|---|
| `number` | `float \| int \| str` | Value to round. Pass as `str` for highest precision. |
| `decimal_places` | `int` | Number of decimal places. Defaults to `0`. |

**Returns:** `int` when `decimal_places=0`, `float` otherwise.

**Raises:** `ValueError` if `decimal_places` is negative. `decimal.InvalidOperation` if `number` is a non-numeric string.

## Notes
- Uses `localcontext()` internally to avoid mutating the global `Decimal` context.
- Behaviour for negative numbers follows the "away from zero" / "towards zero" rule consistently with positive numbers.
