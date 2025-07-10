import pytest
import shutil
from pathlib import Path

from grove.directory import create_directory

@pytest.fixture(autouse=True)
def cleanup_tmp_path(tmp_path):
    yield
    # Nettoie tout le contenu du dossier temporaire
    for child in tmp_path.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()

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

def test_create_directory_parents(tmp_path):
    nested = tmp_path / "a" / "b" / "c"
    result = create_directory(nested)
    assert result.exists()
    assert result.is_dir()

@pytest.mark.parametrize("name", ["1abc", "folder-name", " folder"])
def test_create_directory_invalid_identifier(tmp_path, name):
    path = tmp_path / name
    with pytest.raises(ValueError):
        create_directory(path)

@pytest.mark.parametrize("name", ["fôlder"])
def test_create_directory_valid_unicode_identifier(tmp_path, name):
    path = tmp_path / name
    result = create_directory(path)
    assert result.exists()
    assert result.is_dir()

def test_create_directory_file_exists(tmp_path):
    file_path = tmp_path / "file"
    file_path.write_text("test")
    with pytest.raises(FileExistsError):
        create_directory(file_path)

