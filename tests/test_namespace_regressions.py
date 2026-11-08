"""#135689: namespace metadata must preserve API identity, not URL slug casing."""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((PLUGIN / "plugin.json").read_text())


class NamespaceRegressionTests(unittest.TestCase):
    def extract(self, root, header, *, explicit=None):
        relative = "english/net/aspose.words.ai/aimodel/_index.md"
        index = root / "english/net/aspose.words.ai/_index.md"
        index.parent.mkdir(parents=True, exist_ok=True)
        if header is not None:
            index.write_text(header, encoding="utf-8")
        metadata = f"symbol_fqn: {explicit}\n" if explicit else ""
        source = MANIFEST["sources"]["apiref"]
        request = dict(
            contract=MANIFEST["contract"],
            plugin_id=MANIFEST["plugin_id"],
            product_id=MANIFEST["product_id"],
            language="net",
            operation="extract",
            source_kind="apiref",
            repo_id=source["repo_id"],
            product_family="aspose",
            source_path=source["path"] + "/" + relative,
            relative_repo_path=relative,
            source_prefix=source["prefix"],
            layout_detection=source["layout"],
            source_revision="namespace-fixture",
            canonical_base_url=source["canonical_base_url"],
            repo_root=str(root),
            raw_markdown="---\ntitle: AiModel class\n"
            + metadata
            + "---\n## AiModel class\n```csharp\npublic class AiModel\n```\n",
        )
        result = subprocess.run(
            [sys.executable, "-I", str(PLUGIN / "worker.py")],
            input=json.dumps(request),
            text=True,
            capture_output=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)["result"]

    def assert_identity(self, output, expected):
        self.assertEqual(output["normalized_document"]["document"]["symbol_fqn"], expected)
        self.assertTrue(output["chunk_records"])
        self.assertTrue(all(c["symbol_fqn"] == expected for c in output["chunk_records"]))
        self.assertEqual(output["symbols"][0]["member_fqn"], expected)
        self.assertEqual(output["symbols"][0]["parent_fqn"], expected.rsplit(".", 1)[0])
        self.assertEqual(
            output["symbols"][0]["canonical_url"],
            "https://reference.aspose.com/words/net/aspose.words.ai/aimodel/",
        )

    def test_supported_frontmatter_spellings_and_bom(self):
        headers = [
            "---\ntitle: Aspose.Words.AI\n---\n",
            '\ufeff---\ntitle: "Aspose.Words.AI"\n---\n',
            "---\narticleTitle: 'Aspose.Words.AI'\n---\n",
            "---\ntitle: Namespace overview\nlinktitle: Aspose.Words.AI\n---\n",
            '+++\ntitle = "Aspose.Words.AI"\n+++\n',
        ]
        for header in headers:
            with self.subTest(header=header), tempfile.TemporaryDirectory() as temp:
                self.assert_identity(self.extract(Path(temp), header), "Aspose.Words.AI.AiModel")

    def test_absent_mismatched_or_prose_only_metadata_keeps_fallback(self):
        for header in [
            None,
            "---\ntitle: Aspose.Words.Other\n---\n",
            "# Aspose.Words.AI\n",
            "---\ntitle: Overview\n---\nAspose.Words.AI\n",
            "---\ntitle: Aspose.Words.AI\n",
        ]:
            with self.subTest(header=header), tempfile.TemporaryDirectory() as temp:
                self.assert_identity(self.extract(Path(temp), header), "Aspose.Words.Ai.AiModel")

    def test_explicit_fqn_remains_authoritative(self):
        with tempfile.TemporaryDirectory() as temp:
            output = self.extract(
                Path(temp),
                "---\ntitle: Aspose.Words.AI\n---\n",
                explicit="Aspose.Words.Custom.AiModel",
            )
            self.assert_identity(output, "Aspose.Words.Custom.AiModel")

    def test_namespace_index_symlink_cannot_escape_source_root(self):
        with tempfile.TemporaryDirectory() as temp, tempfile.TemporaryDirectory() as outside:
            root = Path(temp)
            index = root / "english/net/aspose.words.ai/_index.md"
            index.parent.mkdir(parents=True)
            target = Path(outside) / "_index.md"
            target.write_text("---\ntitle: Aspose.Words.AI\n---\n")
            index.symlink_to(target)
            self.assert_identity(self.extract(root, None), "Aspose.Words.Ai.AiModel")
