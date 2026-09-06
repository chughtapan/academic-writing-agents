"""Check plugin installation paths and generated specialist freshness."""

import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


_ROOT = pathlib.Path(__file__).resolve().parents[1]


class CodexPluginTest(unittest.TestCase):
    """Exercise a relocated package without relying on the author's checkout."""

    def setUp(self):
        # unittest.addCleanup releases the directory even if setUp fails.
        # pylint: disable-next=consider-using-with
        self.temporary = tempfile.TemporaryDirectory(prefix='academic plugin ')
        self.addCleanup(self.temporary.cleanup)
        self.root = pathlib.Path(self.temporary.name) / 'installed plugin'
        shutil.copytree(
            _ROOT, self.root,
            ignore=shutil.ignore_patterns('.git', '__pycache__'),
        )

    def run_sync(self, *args):
        """Run the real synchronization CLI outside the plugin directory."""
        return subprocess.run(
            [sys.executable, str(self.root / 'scripts/sync_codex_references.py'),
             *args],
            cwd=self.temporary.name, capture_output=True, text=True, check=False,
        )

    def test_marketplace_installs_complete_specialist_roster(self):
        """The marketplace source and manifest expose every specialist."""
        marketplace = json.loads(
            (self.root / '.agents/plugins/marketplace.json').read_text(
                encoding='utf-8'
            )
        )
        entry, = marketplace['plugins']
        source = (self.root / entry['source']['path']).resolve()
        manifest = json.loads(
            (source / '.codex-plugin/plugin.json').read_text(encoding='utf-8')
        )
        self.assertEqual(entry['name'], manifest['name'])
        skills = (source / manifest['skills']).resolve()
        self.assertTrue(skills.is_relative_to(source))
        discovered = {path.parent.name for path in skills.glob('*/SKILL.md')}
        roles = {path.stem for path in (source / 'agents').glob('*.md')}
        self.assertEqual(discovered, roles | {'academic'})
        for field in ('composerIcon', 'logo'):
            self.assertTrue((source / manifest['interface'][field]).is_file())

    def test_references_resolve_inside_relocated_plugin(self):
        """Skills and roles keep working in a plugin cache with a different CWD."""
        documents = list((self.root / 'codex-skills').rglob('*.md'))
        documents.extend((self.root / 'codex-references').rglob('*.md'))
        for document in documents:
            targets = re.findall(
                r'\]\(([^)]+\.md)\)', document.read_text(encoding='utf-8')
            )
            for target in targets:
                if '://' in target:
                    continue
                with self.subTest(document=document.name, target=target):
                    resolved = (document.parent / target).resolve()
                    self.assertTrue(resolved.is_relative_to(self.root))
                    self.assertTrue(resolved.is_file())

    def test_fresh_bundle_passes(self):
        """The committed generated files match their maintained sources."""
        result = self.run_sync('--check')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_check_is_read_only_and_regeneration_repairs_stale_skill(self):
        """A stale directly invokable specialist is detected and repairable."""
        target = self.root / 'codex-skills/writing-reviewer/SKILL.md'
        original = target.read_bytes()
        target.write_text('stale\n', encoding='utf-8')
        self.assertEqual(self.run_sync('--check').returncode, 1)
        self.assertEqual(target.read_text(encoding='utf-8'), 'stale\n')
        self.assertEqual(self.run_sync().returncode, 0)
        self.assertEqual(target.read_bytes(), original)

    def test_check_detects_missing_and_obsolete_roles(self):
        """Removed references and leftover specialist skills cannot pass."""
        target = self.root / 'codex-references/agents/logic-reviewer.md'
        target.unlink()
        self.assertEqual(self.run_sync('--check').returncode, 1)
        self.assertEqual(self.run_sync().returncode, 0)
        obsolete = self.root / 'codex-skills/obsolete/SKILL.md'
        obsolete.parent.mkdir()
        obsolete.write_text('obsolete role\n', encoding='utf-8')
        self.assertEqual(self.run_sync('--check').returncode, 1)


if __name__ == '__main__':
    unittest.main()
