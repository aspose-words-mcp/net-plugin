"""Canonical namespace spelling from actual Hugo namespace index pages."""
import tempfile
import unittest
from pathlib import Path
from adcs_words_net.normalized_document import _canonical_namespace_from_source

class CanonicalNamespaceTest(unittest.TestCase):
    def test_source_frontmatter_preserves_case(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for slug, canonical in [
                ('aspose.words.digitalsignatures', 'Aspose.Words.DigitalSignatures'),
                ('aspose.words.ai', 'Aspose.Words.AI'),
            ]:
                path = root / 'english/net' / slug
                path.mkdir(parents=True)
                (path / '_index.md').write_text(f'---\ntitle: {canonical}\n---\n')
                self.assertEqual(_canonical_namespace_from_source(
                    repo_root=temp, namespace_path=Path('english/net') / slug,
                    slug=slug), canonical)

    def test_rejects_mismatched_namespace(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / 'english/net/aspose.words.ai'
            path.mkdir(parents=True)
            (path / '_index.md').write_text('---\ntitle: Aspose.Words.Other\n---\n')
            self.assertIsNone(_canonical_namespace_from_source(
                repo_root=temp, namespace_path=Path('english/net/aspose.words.ai'),
                slug='aspose.words.ai'))
