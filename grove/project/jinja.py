from pathlib import Path
from jinja2 import Environment, FileSystemLoader, meta
import json

def find_template(template_name: str, template_root: Path, vendor: str = None) -> Path:
    """
    Recherche un template dans l'ordre :
      - vendor/ (si spécifié)
      - override/
      - default/

    Parameters
    ----------
    template_name : str
        Nom du template (sans .j2).
    template_root : Path
        Chemin racine des templates.
    vendor : str, optional
        Nom du vendor à privilégier (par défaut None).

    Returns
    -------
    Path
        Chemin complet du template trouvé.

    Raises
    ------
    FileNotFoundError
        Si aucun template n'est trouvé dans l'ordre attendu.
    """
    paths = []
    if vendor:
        paths.append(template_root / vendor / f"{template_name}.j2")
    paths.append(template_root / "override" / f"{template_name}.j2")
    paths.append(template_root / "default" / f"{template_name}.j2")

    for path in paths:
        if path.exists():
            return path
    raise FileNotFoundError(f"Template '{template_name}.j2' introuvable dans {paths}")


def _template_extract_var(source: str) -> dict:
    """
    Extrait le bloc _var (s'il existe) de la source JSON brute du template.

    Parameters
    ----------
    source : str
        Source brute du template Jinja.

    Returns
    -------
    dict
        Bloc _var s'il existe, sinon un dict vide.
    """
    try:
        parsed_json = json.loads(source)
        root_key = next(iter(parsed_json))
        return parsed_json[root_key].get("_var", {})
    except Exception:
        return {}


def _check_unused_var_in_template(source: str, env: Environment, raw_var_block: dict):
    """
    Vérifie que chaque variable _var est utilisée dans le template Jinja.

    Parameters
    ----------
    source : str
        Source brute du template Jinja.
    env : Environment
        Instance Jinja2 pour le parsing.
    raw_var_block : dict
        Dictionnaire des variables _var extraites.

    Raises
    ------
    ValueError
        Si au moins une variable _var n'est pas utilisée dans le template.
    """
    if not raw_var_block:
        return

    parsed_ast = env.parse(source)
    used_vars = meta.find_undeclared_variables(parsed_ast)
    unused_vars = set(raw_var_block.keys()) - used_vars
    if unused_vars:
        var = list(unused_vars)[0]
        raise ValueError(f"La variable '{var}' est définie dans _var mais jamais utilisée.")


def _render_template_with_context(template_path: Path, env: Environment, context: dict) -> tuple[dict, str, dict]:
    """
    Rend le template avec le contexte fourni et retourne le JSON parsé,
    la clé racine et le bloc racine.

    Parameters
    ----------
    template_path : Path
        Chemin du template à rendre.
    env : Environment
        Instance Jinja2 pour le rendu.
    context : dict
        Contexte passé à Jinja.

    Returns
    -------
    parsed : dict
        Dictionnaire résultant du rendu.
    root_key : str
        Clé racine du template rendu.
    node : dict
        Bloc racine (sous-dictionnaire correspondant à root_key).

    Raises
    ------
    ValueError
        Si le template rendu ne contient pas exactement une seule clé racine.
    """
    template = env.get_template(template_path.name)
    rendered = template.render(context)
    parsed = json.loads(rendered)
    if len(parsed) != 1:
        raise ValueError("Le template doit contenir une seule clé racine.")
    root_key = next(iter(parsed))
    node = parsed[root_key]
    return parsed, root_key, node


def _clean_var_in_root(node: dict):
    """
    Supprime la clé _var du bloc racine si présente.

    Parameters
    ----------
    node : dict
        Bloc racine du template rendu (modifiable en place).
    """
    if isinstance(node, dict) and "_var" in node:
        node.pop("_var")


def resolve_template(
    template_name: str,
    context: dict,
    *,
    template_root: Path,
    vendor: str = None,
    strict: bool = False
) -> dict:
    """
    Résout un template de projet basé sur Jinja2.
    - Recherche dans default/, override/, vendor/ (dans cet ordre)
    - Fusionne les variables `_var` du bloc racine au contexte pour le rendu
    - Supprime `_var` du bloc racine après rendu
    - Conserve `_meta` dans le bloc racine
    - En mode strict, lève une ValueError si une variable _var n’est pas utilisée dans le template.

    Parameters
    ----------
    template_name : str
        Nom du template (sans .j2).
    context : dict
        Contexte de rendu Jinja (valeurs pour les variables).
    template_root : Path
        Chemin racine où chercher les templates.
    vendor : str, optional
        Vendor prioritaire à chercher (par défaut None).
    strict : bool, optional
        Si True, lève une erreur si une variable _var est inutilisée (par défaut False).

    Returns
    -------
    dict
        Dictionnaire issu du rendu et parsing du template.

    Raises
    ------
    FileNotFoundError
        Si aucun template n'est trouvé dans l'ordre attendu.
    ValueError
        Si le template ne contient pas une seule clé racine,
        ou si (en mode strict) une variable _var n'est pas utilisée.
    """
    template_path = find_template(template_name, template_root, vendor)
    source = template_path.read_text(encoding="utf-8")
    env = Environment(loader=FileSystemLoader(template_path.parent))

    if strict:
        _check_unused_var_in_template(source, env, _template_extract_var(source))

    parsed, root_key, node = _render_template_with_context(template_path, env, context)
    local_vars = node.get("_var", {})
    full_context = {**context, **local_vars}

    if local_vars:
        parsed, root_key, node = _render_template_with_context(template_path, env, full_context)

    _clean_var_in_root(node)

    return parsed

