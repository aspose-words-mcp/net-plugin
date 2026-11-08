# Aspose.Words for .NET Extraction Plugin

Prepare Aspose.Words for .NET documentation and API references for retrieval through the Aspose context engine and MCP server.

This Python package discovers Markdown sources, extracts documentation and C# examples, produces semantic chunks and structured API symbols, and supplies a declarative retrieval profile. Its runtime uses only the Python standard library; it does not import the context engine or other plugins.

## Project family

Publication organization: [aspose-words-mcp](https://github.com/aspose-words-mcp).

| Project | Role | Public repository |
| --- | --- | --- |
| net-plugin | Extraction and retrieval configuration (this repository) | [aspose-words-mcp/net-plugin](https://github.com/aspose-words-mcp/net-plugin) |
| aspose-context-engine-core | Ingestion, indexing, storage, and retrieval integration | [aspose-core-mcp/context-engine](https://github.com/aspose-core-mcp/context-engine) |
| Aspose.Words for .NET MCP server | Exposes retrieval and API tools to clients | **TODO: WORDS_NET_MCP_PUBLIC_REPOSITORY_URL** |
| net-copilot-client-agent | GitHub Copilot client configuration and custom agent | **TODO: COPILOT_CLIENT_PUBLIC_REPOSITORY_URL** |

The plugin is a one-request extraction worker, not an HTTP service or an MCP client. Engine integration and serving are configured separately.

## Quick start

Requirements: Python 3.12 or newer. Git is needed when preparing external source repositories and Gist examples.

From the repository root:

```sh
python3.12 -m venv .venv
PYTHONPATH=src .venv/bin/python -m unittest discover -s tests -v
.venv/bin/python -I worker.py < examples/extract-request.json
```

The example uses inline Markdown and needs no source download, engine, network connection, or credentials. It prints one JSON response with a normalized document, chunks, and API symbols. See the [worker contract](docs/worker-contract.md).

## Prepare real sources and integrate

1. Follow [source preparation](docs/source-preparation.md) to clone the sources declared in `plugin.json` and prepare referenced Gist examples.
2. Follow [engine integration](docs/engine-integration.md) to register the manifest with your context engine deployment.
3. Validate extraction before publishing indexed data through the engine.
4. Deploy the MCP server separately and connect your preferred client.

See the [engine integration guide](https://github.com/aspose-core-mcp/context-engine/blob/main/docs/engine-only.md) for engine setup and ingestion commands. Standalone tests and the example above work without it.

## Repository layout

| Path | Purpose |
| --- | --- |
| `plugin.json` | Plugin identity, source locations, worker command, and retrieval-profile path |
| `worker.py` | Isolated source-checkout launcher |
| `src/adcs_words_net/` | Extraction, normalization, chunking, symbol, and Gist-cache implementation |
| `retrieval-profile.json` | Product-specific retrieval preferences and namespace exclusions |
| `examples/` | Self-contained extraction request |
| `tests/` | Unit and fixture-based regression tests |
| `scripts/check_constructor_invariants.py` | Full API-source constructor identity audit |
| `docs/` | Setup, integration, worker contract, and extraction behavior |

## Package installation

```sh
.venv/bin/python -m pip install .
.venv/bin/adcs-words-net-extract < examples/extract-request.json
```

When using the virtual environment, invoke the installed entry point as `.venv/bin/adcs-words-net-extract`. The distribution is named `adcs-words-net-extractor`; the import namespace is `adcs_words_net` and the plugin identity is `aspose.words.net`. These stable integration names are independent of the public repository name.

Use a source checkout for engine integration. The wheel does not bundle `plugin.json`, `retrieval-profile.json`, source corpora, or the prepared Gist cache. Building a wheel also requires the setuptools build dependency declared in `pyproject.toml`.

## Development and license

See [CONTRIBUTING.md](CONTRIBUTING.md) for checks and change guidance. GitHub Actions runs the regression suite on Python 3.12 and 3.13.

Licensed under [MIT](LICENSE), preserving Aspose Pty Ltd attribution. The parser/converter implementation originated from the MIT-licensed ADCS pilot and is maintained independently here. Downloaded documentation and examples retain their own upstream terms and attribution.
