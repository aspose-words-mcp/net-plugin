"""Re-extract all API pages and independently audit constructor contract invariants."""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'src'))
from adcs_words_net.worker import handle


def audit(symbols):
    types = {s['member_fqn'] for s in symbols if s['kind'] in {'class', 'struct', 'interface'}}
    by_fold = {}
    for name in types:
        by_fold.setdefault(name.casefold(), set()).add(name)
    mismatches, classification, absent, members = [], [], [], []
    constructors = 0
    for s in symbols:
        signature = s.get('signature') or ''
        # Independent signature oracle: constructors have access/modifiers and
        # a callable name, but no return type. Do not depend on emitted kind.
        declared = bool(re.match(
            r'^(?:(?:public|private|protected|internal|static|extern)\s+)+'
            r'[A-Za-z_]\w*\s*\(', signature))
        tagged = s['kind'] == 'constructor'
        if declared != tagged:
            classification.append({k: s.get(k) for k in ('member_fqn', 'kind', 'signature')})
        if not (declared or tagged):
            continue
        constructors += 1
        parent = s.get('parent_fqn') or ''
        if s['member_fqn'] != parent + '.' + parent.rsplit('.', 1)[-1]:
            members.append(s['member_fqn'])
        candidates = by_fold.get(parent.casefold(), set())
        if candidates and parent not in types:
            mismatches.append({'member_fqn': s['member_fqn'], 'parent_fqn': parent,
                               'canonical_types': sorted(candidates)})
        elif not candidates:
            absent.append(s['member_fqn'])
    return dict(symbols=len(symbols), constructors=constructors,
                parent_mismatches=mismatches, classification_errors=classification,
                member_identity_errors=members,
                declaring_type_absent=absent)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    root = args.repo_root.resolve()
    symbols = []
    pages = 0
    for source in sorted((root / 'english/net').rglob('*.md')):
        relative = source.relative_to(root).as_posix()
        result = handle(dict(
            contract='adcs.extraction.v1', plugin_id='aspose.words.net',
            operation='extract', source_kind='apiref', repo_id='aspose.words.net.apiref',
            product_id='aspose.words', language='net', product_family='aspose.words',
            source_path=str(source), relative_repo_path=relative, repo_root=str(root),
            source_prefix='english/net', raw_markdown=source.read_text(encoding='utf-8-sig'),
            source_revision='constructor-invariant-audit',
            canonical_base_url='https://reference.aspose.com/words/net',
            layout_detection={'layout_type': 'doc_locale/programming_language/namespace'},
        ))
        symbols.extend(result['symbols'])
        pages += 1
    report = dict(pages=pages, **audit(symbols))
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
    return bool(report['parent_mismatches'] or report['classification_errors']
                or report['member_identity_errors'])


if __name__ == '__main__':
    raise SystemExit(main())
