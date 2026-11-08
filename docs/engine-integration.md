# Context engine integration

[aspose-core-mcp/context-engine](https://github.com/aspose-core-mcp/context-engine)
**TODO: WORDS_NET_MCP_PUBLIC_REPOSITORY_URL**

Install and configure the context engine using its [public deployment guide](https://github.com/aspose-core-mcp/context-engine/blob/main/DEPLOYMENT.md). The extractor itself has no runtime engine dependency, but ingestion orchestration and serving require a compatible engine implementing `adcs.extraction.v1` and the retrieval profile schema.

## Register the source checkout

Add the absolute path to this checkout's `plugin.json` to the engine catalog's `plugins` array. Preserve other catalog entries. A minimal catalog shape is:

```json
{
  "plugins": ["/absolute/path/to/net-plugin/plugin.json"]
}
```

The existing integration uses an engine-owned `config/product-platform-plugins.json`. Supply the following values to the engine ingestion CLI; use `adcs-platform-ingest` as documented in the [engine plugin guide](https://github.com/aspose-core-mcp/context-engine/blob/main/docs/engine-only.md):

| Parameter | Value |
| --- | --- |
| Plugin ID | `aspose.words.net` |
| `--catalog` | Absolute path to the engine catalog |
| `--workspace` | Absolute path to this checkout, when using the default manifest source paths |
| `--python` | Absolute path to this checkout's `.venv/bin/python` |

Registration does not clone sources or publish data. Prepare sources first. Validation can write engine operation metadata in the workspace; publishing requires a separate explicit `--publish` invocation and configured runtime stores. Follow the engine's deployment documentation for its storage and publication requirements.

## Retrieval serving

The manifest references `retrieval-profile.json`. Configure the engine's serving process to load the catalog; the existing integration supports `ADCS_RETRIEVAL_PLUGIN_CATALOG` with an absolute catalog path. The engine must support this profile's fields before enabling it. Reload or restart serving processes after profile updates to clear cached policies.

Extractor changes require re-extraction and publication of affected data. A service restart alone does not update stored symbols or excerpts. Retrieval-profile-only changes generally require a serving reload rather than reingestion.

## MCP and clients

The MCP server exposes the engine's retrieval capabilities. This repository does not launch that server, provision its stores, or configure authentication. Use the MCP repository's deployment guide and then configure the Copilot client with its published endpoint.
