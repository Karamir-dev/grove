# tests/project/test_resolve_template.py

import pytest
from grove.project import resolve_template


@pytest.fixture
def template_dir(tmp_path):
    """
    Crée un dossier templates avec uniquement 'default/'.
    C’est le comportement attendu par défaut à l’installation de Grove.
    """
    root = tmp_path / "templates"
    (root / "default").mkdir(parents=True)
    return root


@pytest.fixture
def write_template(template_dir):
    """
    Permet d’écrire dynamiquement un template dans un sous-dossier (default, override, etc.).
    """
    def _write(subdir: str, name: str, content: str):
        path = template_dir / subdir / f"{name}.j2"
        path.write_text(content.strip())
        return path
    return _write


class Test_lorsque_je_veux_appliquer_un_template_jinja_et_que_seul_default_existe:

    def test_alors_je_peux_generer_une_structure_minimale_depuis_un_template_default(self, write_template, template_dir):
        write_template("default", "simple", '''
        {
          "{{ folder_name }}": {
            "contains": ["README.md", "main.tf"]
          }
        }
        ''')
        result = resolve_template("simple", context={"folder_name": "project"}, template_root=template_dir)
        assert list(result.keys()) == ["project"]
        assert result["project"]["contains"] == ["README.md", "main.tf"]

    def test_alors_je_veux_pouvoir_configurer_le_nom_du_dossier_depuis__var(self, write_template, template_dir):
        write_template("default", "with_var", '''
        {
          "{{ prefix }}_network": {
            "_var": { "prefix": "01" },
            "contains": ["main.tf"]
          }
        }
        ''')
        result = resolve_template("with_var", context={}, template_root=template_dir)
        assert "01_network" in result
        assert "_var" not in result["01_network"]

    def test_alors_je_veux_conserver_les_meta_dans_la_structure(self, write_template, template_dir):
        write_template("default", "meta", '''
        {
          "{{ folder_name }}": {
            "_meta": { "type": "terraform_module" },
            "contains": ["main.tf"]
          }
        }
        ''')
        result = resolve_template("meta", context={"folder_name": "infrastructure"}, template_root=template_dir)
        assert "infrastructure" in result
        node = result["infrastructure"]
        assert "_meta" in node
        assert node["_meta"]["type"] == "terraform_module"

    def test_alors_je_verifie_que_le_template_a_une_clef_racine_contenant__meta_et_contains(self, write_template, template_dir):
        write_template("default", "structured", '''
        {
          "{{ folder_name }}": {
            "_meta": {
              "type": "terraform_module"
            },
            "contains": [
              "main.tf",
              "outputs.tf"
            ]
          }
        }
        ''')
        result = resolve_template("structured", context={"folder_name": "01_network"}, template_root=template_dir)
        assert list(result.keys()) == ["01_network"]
        node = result["01_network"]
        assert "contains" in node
        assert isinstance(node["contains"], list)
        assert "main.tf" in node["contains"]
        assert "_meta" in node
        assert node["_meta"]["type"] == "terraform_module"

    def test_alors_je_veux_detecter_si_une_variable__var_n_est_pas_utilisee_dans_le_template(self, write_template, template_dir):
        write_template("default", "unused_var", '''
        {
          "network": {
            "_var": {
              "prefix": "01"
            },
            "contains": ["main.tf"]
          }
        }
        ''')
        with pytest.raises(ValueError, match="La variable 'prefix' est définie dans _var mais jamais utilisée."):
            resolve_template("unused_var", context={}, template_root=template_dir, strict=True)

