from pathlib import Path
from jinja2 import Environment, FileSystemLoader, meta
import json

def find_template(template_name: str, template_root: Path, vendor: str = None) -> Path:
    """
    Recherche un template dans l'ordre :
      - vendor/ (si spécifié)
      - override/
      - default/
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
    """
    template_path = find_template(template_name, template_root, vendor)
    source = template_path.read_text(encoding="utf-8")
    env = Environment(loader=FileSystemLoader(template_path.parent))

    # Analyse statique des variables Jinja utilisées (pour le mode strict)
    if strict:
        try:
            # On tente de parser le JSON brut pour extraire _var
            parsed_json = json.loads(source)
            root_key = next(iter(parsed_json))
            raw_var_block = parsed_json[root_key].get("_var", {})
        except Exception:
            raw_var_block = {}

        if raw_var_block:
            parsed_ast = env.parse(source)
            used_vars = meta.find_undeclared_variables(parsed_ast)
            unused_vars = set(raw_var_block.keys()) - used_vars
            if unused_vars:
                var = list(unused_vars)[0]
                raise ValueError(f"La variable '{var}' est définie dans _var mais jamais utilisée.")

    # Premier rendu (pour déterminer la clé racine)
    template = env.get_template(template_path.name)
    rendered = template.render(context)
    parsed = json.loads(rendered)
    if len(parsed) != 1:
        raise ValueError("Le template doit contenir une seule clé racine.")
    root_key = next(iter(parsed))
    node = parsed[root_key]

    # Fusion du contexte global avec _var (priorité à _var)
    local_vars = node.get("_var", {})
    full_context = {**context, **local_vars}

    # Second rendu si _var existe, sinon garde le rendu initial
    if local_vars:
        rendered = template.render(full_context)
        parsed = json.loads(rendered)
        root_key = next(iter(parsed))
        node = parsed[root_key]

    # Nettoyage : suppression de _var dans le bloc racine
    if isinstance(node, dict) and "_var" in node:
        node.pop("_var")

    return parsed

