import pytest
from pathlib import Path
from grove.directory import create_directory

def test_create_directory_creates_new_folder(tmp_path):
    target = tmp_path / "my_folder"
    result = create_directory(target)
    
    assert result.exists()
    assert result.is_dir()
    assert result == target.resolve()

def test_create_directory_raises_if_exists(tmp_path):
    existing = tmp_path / "existing_folder"
    existing.mkdir()
    
    with pytest.raises(FileExistsError):
        create_directory(existing)

def test_create_directory_with_exist_ok(tmp_path):
    existing = tmp_path / "folder"
    existing.mkdir()
    
    # Ne doit pas lever d'exception
    result = create_directory(existing, exist_ok=True)
    
    assert result.exists()
    assert result.is_dir()

def test_create_directory_invalid_name(tmp_path):
    invalid = tmp_path / "in*valid"
    
    with pytest.raises(ValueError):
        create_directory(invalid)

