# Contributing

Use Python 3.12 or newer and run from the repository root:

```sh
PYTHONPATH=src python3.12 -m unittest discover -s tests -v
python3.12 -I worker.py < examples/extract-request.json
```

Keep changes scoped to this product/platform. Add a regression fixture when changing parsing, canonical URLs, namespace casing, symbol identity, or example extraction. Preserve the worker contract and stable plugin/package identities unless coordinating a versioned integration change.

Keep the MIT attribution in LICENSE. Do not commit source corpora, Gist caches, credentials, virtual environments, or ingestion output. Preserve provenance for copied fixtures.

For a bug report, include Python version, plugin revision, operation, and a minimal sanitized request. Distinguish extraction failures from engine indexing and MCP serving issues. Changes to the retrieval profile should be validated against the compatible engine as well as local tests.
