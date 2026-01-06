import pytest
from pathlib import Path
from utils.file_system import FileSystem

class TestFileSystem:
    """TestSuite for the FileSystem utility class.

    Follows OOP style using pytest. Each test method receives the 'tmp_path'
    fixture, which provides a unique temporary directory for isolation.
    """

    def test_create_directory_success(self, tmp_path: Path):
        """Tests that a directory (and parents) are created correctly."""
        print(f"Debug tmp_path: {tmp_path}")
        target_dir = tmp_path / "level_1" / "level_2"

        result = FileSystem.create_directory(target_dir)

        assert result.exists()
        assert result.is_dir()
    
    def test_move_file_creates_destination_parents(self, tmp_path: Path):
        """Tests moving a file to a folder that does not exist yet."""
        source_file = tmp_path / "source.txt"
        source_file.write_text("content", encoding="utf-8")
        
        dest_file = tmp_path / "archive" / "moved.txt"

        FileSystem.move(source_file, dest_file)

        assert not source_file.exists()
        assert dest_file.exists()
        assert dest_file.read_text(encoding="utf-8") == "content"
    
    def test_move_raises_error_if_source_missing(self, tmp_path: Path):
        """Tests that moving a non-existent file raises FileNotFoundError."""
        missing_source = tmp_path / "ghost.txt"
        dest_file = tmp_path / "wont_exist.txt"

        with pytest.raises(FileNotFoundError):
            FileSystem.move(missing_source, dest_file)
    
    def test_find_returns_matching_files(self, tmp_path: Path):
        """Tests finding files with a specific pattern."""
        (tmp_path / "data_1.csv").touch()
        (tmp_path / "data_2.csv").touch()
        (tmp_path / "ignore.txt").touch()

        found_files = FileSystem.find(tmp_path, "*.csv")

        assert len(found_files) == 2
        file_names = [f.name for f in found_files]
        assert "data_1.csv" in file_names
        assert "data_2.csv" in file_names
    
    def test_remove_handles_non_empty_directory(self, tmp_path: Path):
        """Tests removing a directory that contains files."""
        folder_to_delete = tmp_path / "trash_folder"
        FileSystem.create_directory(folder_to_delete)
        (folder_to_delete / "junk.txt").write_text("trash")

        result = FileSystem.remove(folder_to_delete)

        assert result is True
        assert not folder_to_delete.exists()

    def test_existence_checks(self, tmp_path: Path):
        """Tests the is_file and is_directory logic."""
        file_path = tmp_path / "file.txt"
        dir_path = tmp_path / "folder"
        
        file_path.touch()
        FileSystem.create_directory(dir_path)

        assert FileSystem.is_file(file_path) is True
        assert FileSystem.is_directory(file_path) is False

        assert FileSystem.is_directory(dir_path) is True
        assert FileSystem.is_file(dir_path) is False