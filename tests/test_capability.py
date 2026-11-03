"""Portable release and install boundaries; all writes stay in temporary folders."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
from zipfile import ZipFile

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("capability", ROOT / "scripts/capability.py")
capability = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(capability)


class PortableTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="arxivchecker-portable-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = capability.config()

    def test_complete_install_is_idempotent(self):
        first = capability.install(self.config, self.root)
        self.assertFalse(first["unchanged"])
        self.assertTrue(capability.install(self.config, self.root)["unchanged"])
        target = Path(first["installed"])
        self.assertEqual(capability.installed_map(target), capability.file_map(self.config))

    def test_conflict_refusal_preserves_edits(self):
        target = Path(capability.install(self.config, self.root)["installed"])
        (target / "SKILL.md").write_text("local change\n")
        with self.assertRaisesRegex(ValueError, "Existing skill differs"):
            capability.install(self.config, self.root)
        self.assertEqual((target / "SKILL.md").read_text(), "local change\n")

    def test_explicit_replace_retains_backup(self):
        target = Path(capability.install(self.config, self.root)["installed"])
        (target / "SKILL.md").write_text("local change\n")
        result = capability.install(self.config, self.root, replace=True)
        self.assertEqual((Path(result["backup"]) / "SKILL.md").read_text(), "local change\n")
        self.assertEqual(capability.installed_map(target), capability.file_map(self.config))

    def test_symlink_destination_is_rejected(self):
        outside = self.root / "other"
        outside.mkdir()
        (self.root / "arxivchecker").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(ValueError, "symlink"):
            capability.install(self.config, self.root)
        self.assertEqual(list(outside.iterdir()), [])

    def test_export_is_deterministic_complete_and_safe(self):
        first, second = self.root / "a.zip", self.root / "b.zip"
        capability.export(self.config, first)
        capability.export(self.config, second)
        self.assertEqual(first.read_bytes(), second.read_bytes())
        with ZipFile(first) as archive:
            expected = capability.file_map(self.config)
            self.assertEqual(set(archive.namelist()), {"arxivchecker/" + name for name in expected})
            self.assertTrue(all(archive.read("arxivchecker/" + name) == data for name, data in expected.items()))
            self.assertFalse(any("__pycache__" in name or name.endswith(".pyc") for name in archive.namelist()))
        with self.assertRaisesRegex(ValueError, "already exists"):
            capability.export(self.config, first)

    def test_install_source_overlap_is_rejected(self):
        source = capability.skill_root(self.config)
        with self.assertRaisesRegex(ValueError, "overlap"):
            capability.install(self.config, source.parent)


if __name__ == "__main__":
    unittest.main()
