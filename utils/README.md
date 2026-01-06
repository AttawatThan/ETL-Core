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
