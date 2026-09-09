from pathlib import Path
import ast
import hashlib
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


class ProjectSelfContainmentTests(unittest.TestCase):
    def test_normative_source_is_local_and_verified(self):
        source = PROJECT_ROOT / "15kr0005.doc"
        self.assertTrue(source.is_file())
        self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(), "bca94f5db76962bf46f6f5569d2d18872dc6e5355b01bd77d79edb985263043e")

    def test_project_text_has_no_parent_or_absolute_legacy_paths(self):
        forbidden_paths = (".." + "/15kr0005.doc", "/Users/tema/Desktop/" + "xml_creator")
        paths = [PROJECT_ROOT / "AGENTS.md", PROJECT_ROOT / "README.md", PROJECT_ROOT / "pyproject.toml"]
        paths += list((PROJECT_ROOT / "src").rglob("*.py"))
        paths += list((PROJECT_ROOT / "tests").rglob("*.py"))
        paths += list((PROJECT_ROOT / "tools").rglob("*.py"))
        paths += list((PROJECT_ROOT / "project_memory").rglob("*.md"))
        for path in paths:
            text = path.read_text(encoding="utf-8")
            for value in forbidden_paths:
                with self.subTest(path=path, value=value): self.assertNotIn(value, text)
            if path.suffix == ".py":
                self.assertNotIn("sys" + ".path", text)

    def test_python_imports_do_not_reference_legacy_modules(self):
        forbidden_roots = {"app", "processes", "main"}
        for path in (*list((PROJECT_ROOT / "src").rglob("*.py")), *list((PROJECT_ROOT / "tests").rglob("*.py")), *list((PROJECT_ROOT / "tools").rglob("*.py"))):
            tree = ast.parse(path.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                names = [item.name for item in node.names] if isinstance(node, ast.Import) else ([node.module] if isinstance(node, ast.ImportFrom) and node.module else [])
                for name in names:
                    with self.subTest(path=path, name=name): self.assertNotIn(name.split(".")[0], forbidden_roots)

    def test_project_contains_no_symbolic_links(self):
        self.assertEqual([path for path in PROJECT_ROOT.rglob("*") if path.is_symlink()], [])


if __name__ == "__main__": unittest.main()
