"""Constructor source identity and independent dataset audit regressions."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

from adcs_words_net.worker import handle

PLUGIN = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    'constructor_audit', PLUGIN / 'scripts/check_constructor_invariants.py')
audit_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit_module)


class ConstructorIdentityTest(unittest.TestCase):
    def extract(self, root, raw):
        relative = ('english/net/aspose.words.digitalsignatures/'
                    'timestampsettings/timestampsettings/_index.md')
        return handle(dict(
            contract='adcs.extraction.v1', plugin_id='aspose.words.net',
            operation='extract', source_kind='apiref', repo_id='fixture',
            product_id='aspose.words', language='net', product_family='aspose.words',
            source_path=relative, relative_repo_path=relative, repo_root=str(root),
            source_prefix='english/net', raw_markdown=raw, source_revision='fixture',
            canonical_base_url='https://reference.aspose.com/words/net',
            layout_detection={'layout_type': 'doc_locale/programming_language/namespace'}))

    def test_parent_source_identity_and_overloads(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            parent = root / 'english/net/aspose.words.digitalsignatures/timestampsettings'
            parent.mkdir(parents=True)
            # Explicit canonical identity differs from the path AND child label:
            # this proves that the declaring page is the authority.
            (parent / '_index.md').write_text('''---
title: TimestampSettings
symbol_fqn: Aspose.Words.DigitalSignatures.TimeStampSettings
---
## TimeStampSettings class
```csharp
public class TimeStampSettings
```
''')
            result = self.extract(root, '''---
title: TimestampSettings
---
## TimestampSettings() {#constructor}
```csharp
public TimestampSettings()
```
## TimestampSettings(string) {#constructor_1}
```csharp
public TimestampSettings(string url)
```
''')
            canonical = 'Aspose.Words.DigitalSignatures.TimeStampSettings'
            self.assertEqual(len(result['symbols']), 2)
            for symbol in result['symbols']:
                self.assertEqual(symbol['kind'], 'constructor')
                self.assertEqual(symbol['parent_fqn'], canonical)
                self.assertEqual(symbol['member_fqn'], canonical + '.TimeStampSettings')
            document = result['normalized_document']['document']
            self.assertEqual(document['symbol_kind'], 'constructor')
            self.assertEqual(document['symbol_fqn'], canonical + '.TimeStampSettings')

    def test_examples_and_return_type_do_not_classify_constructor(self):
        with tempfile.TemporaryDirectory() as root:
            for declaration in ['public void TimestampSettings()',
                                'public static TimestampSettings Create()']:
                result = self.extract(root, f'''---
title: TimestampSettings
---
## TimestampSettings method
```csharp
{declaration}
```
### Examples
```csharp
public TimestampSettings()
```
''')
                self.assertEqual(result['normalized_document']['document']['symbol_kind'], 'method')

    def test_audit_classification_is_independent_of_parent_casing(self):
        rows = [dict(member_fqn='N.TypeName', kind='class')]
        for parent, kind in [('N.Typename', 'constructor'), ('N.TypeName', 'symbol')]:
            rows.append(dict(member_fqn=parent + '.TypeName', parent_fqn=parent,
                             kind=kind, signature='public TypeName()'))
        report = audit_module.audit(rows)
        self.assertEqual(len(report['parent_mismatches']), 1)
        self.assertEqual(len(report['classification_errors']), 1)
        self.assertEqual(report['constructors'], 2)
        rows[1]['parent_fqn'] = 'N.TypeName'
        rows[2]['kind'] = 'constructor'
        report = audit_module.audit(rows)
        self.assertEqual(report['parent_mismatches'], [])
        self.assertEqual(report['classification_errors'], [])
