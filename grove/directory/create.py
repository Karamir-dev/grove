from pathlib import Path

def create_directory(directory_path: Path, exist_ok: bool = False) -> Path:
    """Crée un dossier à l'emplacement donné.

    Args:
        directory_path (Path): Le chemin complet du dossier à créer.
        exist_ok (bool): Si True, ne lève pas d'erreur si le dossier existe déjà.

    Returns:
        Path: Le chemin absolu du dossier créé.

    Raises:
        ValueError: Si le nom du dossier est invalide.
        FileExistsError: Si le dossier existe déjà et exist_ok est False.
    """
    if not directory_path.name.isidentifier():
        raise ValueError(f"Nom de dossier invalide : '{directory_path.name}'")

    if directory_path.exists() and not exist_ok:
        raise FileExistsError(f"Le dossier '{directory_path}' existe déjà.")

    directory_path.mkdir(parents=True, exist_ok=exist_ok)
    print(f"✅ Dossier créé : {directory_path.resolve()}")

    return directory_path

