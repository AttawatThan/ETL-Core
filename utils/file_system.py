import shutil
from pathlib import Path
from typing import List, Union

class FileSystem:
    """A utility class for performing common file system operations.

    This class provides a unified interface for creating directories, moving files,
    finding resources, and performing cleanups. It abstracts the underlying
    pathlib and shutil operations to provide safe defaults (e.g., auto-creating
    parent directories).
    """
    
    @staticmethod
    def _normalize(path: Union[str, Path]) -> Path:
        """Converts a string or Path object into a resolved absolute Path.

        Args:
            path: The file system path to normalize.

        Returns:
            A resolved pathlib.Path object.
        """
        return Path(path).resolve()
    
    @staticmethod
    def exists(target: Union[str, Path]) -> bool:
        """Checks if the target path exists.

        Args:
            target: The path to check.

        Returns:
            True if the target exists, False otherwise.
        """
        return FileSystem._normalize(target).exists()

    @staticmethod
    def is_file(target: Union[str, Path]) -> bool:
        """Checks if the target exists and is explicitly a file.

        Args:
            target: The path to check.

        Returns:
            True if the target is an existing file, False otherwise.
        """
        return FileSystem._normalize(target).is_file()

    @staticmethod
    def is_directory(target: Union[str, Path]) -> bool:
        """Checks if the target exists and is explicitly a directory.

        Args:
            target: The path to check.

        Returns:
            True if the target is an existing directory, False otherwise.
        """
        return FileSystem._normalize(target).is_dir()

    @staticmethod
    def create_directory(directory_path: Union[str, Path]) -> Path:
        """Creates a directory, including any missing parent directories.

        Args:
            directory_path: The path of the directory to create.

        Returns:
            The Path object of the created (or existing) directory.
        """
        path = FileSystem._normalize(directory_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return path
    
    @staticmethod
    def move(source: Union[str, Path], destination: Union[str, Path]) -> Path:
        """Moves or renames a source file/directory to a destination.

        If the destination's parent directory does not exist, it will be created.

        Args:
            source: The path of the item to move.
            destination: The target path where the item should be moved.

        Returns:
            The Path object of the moved item at its new location.

        Raises:
            FileNotFoundError: If the source path does not exist.
        """
        src_path = FileSystem._normalize(source)
        dest_path = FileSystem._normalize(destination)
        
        if not src_path.exists():
            raise FileNotFoundError(
                f"Cannot move: Source not found at '{src_path}'"
            )

        # Ensure the container folder for the destination exists
        if not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)

        return src_path.rename(dest_path)
    
    @staticmethod
    def find(root_directory: Union[str, Path], file_pattern: str = "*") -> List[Path]:
        """Searches for files or directories matching a pattern.

        Args:
            root_directory: The directory to start the search in.
            file_pattern: A glob pattern to match files (e.g., "*.csv").
                            Defaults to "*" (match all).

        Returns:
            A list of Path objects matching the pattern. Returns an empty list
            if the root directory does not exist.
        """
        root = FileSystem._normalize(root_directory)
        if root.exists() and root.is_dir():
            return list(root.glob(file_pattern))
        return []

    @staticmethod
    def remove(target: Union[str, Path]) -> bool:
        """Permanently removes a file or directory.

        This method handles both files and directories (even if non-empty).

        Args:
            target: The path of the item to remove.

        Returns:
            True if the item was successfully removed (or didn't exist).
            Raises OSError if permission errors occur.
        """
        path = FileSystem._normalize(target)

        if not path.exists():
            return False

        if path.is_file():
            path.unlink()
        elif path.is_dir():
            try:
                path.rmdir()
            except OSError:
                shutil.rmtree(path)
        return True
