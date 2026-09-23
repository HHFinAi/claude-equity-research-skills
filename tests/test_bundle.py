import importlib.util
from pathlib import Path
import tempfile
import unittest
import zipfile
spec = importlib.util.spec_from_file_location('builder', Path(__file__).resolve().parents[1] / 'tools/build_bundle.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)


class BundleTests(unittest.TestCase):
    def test_missing_submodule_fails(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            with self.assertRaises(ValueError):
                builder.build_skill(root, 'earnings-analysis', root / 'out', root / 'LICENSE')

    def test_structure_license_and_hidden_files(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            source = root / 'skill'
            source.mkdir()
            (source / 'SKILL.md').write_text('test')
            (source / '.env').write_text('excluded')
            (root / 'LICENSE').write_text('license')
            path = builder.build_skill(source, 'test-skill', root / 'out', root / 'LICENSE')
            with zipfile.ZipFile(path) as z:
                self.assertEqual(set(z.namelist()), {'test-skill/SKILL.md', 'test-skill/LICENSE'})
            first = path.read_bytes()
            builder.build_skill(source, 'test-skill', root / 'out', root / 'LICENSE')
            self.assertEqual(first, path.read_bytes())

    def test_symlinks_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)
            (root / 'SKILL.md').write_text('test')
            (root / 'outside').symlink_to('/etc/passwd')
            with self.assertRaises(ValueError):
                builder.build_skill(root, 'test-skill', root / 'out', root / 'LICENSE')

    def test_name_traversal_rejected(self):
        with self.assertRaises(ValueError):
            builder.build_skill(Path('.'), '../bad', Path('out'), Path('LICENSE'))


if __name__ == '__main__':
    unittest.main()
