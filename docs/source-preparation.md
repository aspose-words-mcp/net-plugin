# Source preparation

`plugin.json` is authoritative for repository URLs, branches, prefixes, and layout metadata. Source paths are relative to the engine ingestion workspace; use this checkout as that workspace with the default manifest.

Run from this repository root:

```sh
mkdir -p sources
git clone --filter=blob:none --sparse --branch master https://github.com/sabir-aspose/words-docs-com.git sources/documentation-current
git -C sources/documentation-current sparse-checkout set en/net
git clone --filter=blob:none --sparse --branch main https://github.com/aspose-words/Aspose.Words-API-References.git sources/api-reference
git -C sources/api-reference sparse-checkout set english/net
```

These are the source repositories configured by the existing plugin, including the documentation fork. They are distinct from the unpublished context-engine and MCP repositories. If a replacement documentation repository is chosen for publication, update its URL, branch, and prefix together in `plugin.json` and this guide, and validate the new layout before ingestion.

Expected layout:

```text
sources/
  documentation-current/en/net/
  api-reference/english/net/
  gist-examples.json
```

## Prepare Gist examples

After creating the virtual environment described in the README:

```sh
PYTHONPATH=src .venv/bin/python -m adcs_words_net.gist_examples --source-root sources/documentation-current/en/net --cache sources/gist-examples.json
```

This explicit network step fetches referenced public Gist files and records pinned revisions and checksums. Existing valid entries are reused; `--refresh` updates them. Extraction itself uses the cache offline. Missing or corrupt referenced examples fail extraction rather than silently dropping code. Do not prepare the same cache concurrently.

Keep the default cache path when using the source worker: `--cache` changes the preparation destination, not the worker's lookup location.

## Reproducibility

Record `git rev-parse HEAD` and verify `git status --short` is clean in each source checkout before ingestion. Preserve the Gist cache with the ingestion records because documentation revisions alone do not pin external examples. Source corpora, caches, and generated output are excluded from this repository.

## Optional full-source audit

```sh
.venv/bin/python scripts/check_constructor_invariants.py --repo-root sources/api-reference --output /tmp/words-constructor-invariants.json
```

This checks constructor identity, parent types, and classification against the local API corpus. It does not publish data or check the live MCP index.
