# Source preparation

`plugin.json` is authoritative for repository URLs, branches, prefixes, and layout metadata. Source paths are relative to the engine ingestion workspace; use this checkout as that workspace with the default manifest.

Run from this repository root:

```sh
mkdir -p sources
git clone --filter=blob:none --sparse --branch master https://github.com/aspose-words-mcp/docs.git sources/documentation-current
git -C sources/documentation-current sparse-checkout set en/net
git clone --filter=blob:none --sparse --branch main https://github.com/aspose-words-mcp/reference.git sources/api-reference
git -C sources/api-reference sparse-checkout set english/net
```

These public repositories provide the documentation and API reference source content for this plugin. Documentation uses the `master` branch and `en/net` prefix; API reference uses `main` and `english/net`. Citations continue to point to the published pages on `docs.aspose.com` and `reference.aspose.com`.

For existing source checkouts, update their remotes before the next source synchronization:

```sh
git -C sources/documentation-current remote set-url origin https://github.com/aspose-words-mcp/docs.git
git -C sources/api-reference remote set-url origin https://github.com/aspose-words-mcp/reference.git
```

Changing the plugin configuration or a Git remote does not refresh an already published index. Synchronize the sources, prepare the Gist cache, and run the normal ingestion and publication workflow to update indexed content. Preserve any local source changes before synchronization.

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
