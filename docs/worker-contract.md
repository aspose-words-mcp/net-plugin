# Worker contract

The worker accepts one JSON request on stdin, prints one JSON response on stdout, and exits. Launch it from a source checkout with `python -I worker.py`.

Required identity fields:

```json
{
  "contract": "adcs.extraction.v1",
  "plugin_id": "aspose.words.net",
  "product_id": "aspose.words",
  "language": "net",
  "source_kind": "apiref",
  "operation": "extract"
}
```

`source_kind` is `docs` or `apiref`. The remaining fields depend on the operation.

## Discovery

For `operation: discover`, supply `repo_root` and `source_prefix`. The prefix must be a relative directory inside the repository. Discovery returns `result.files`, a sorted list of eligible Markdown paths relative to that repository. Missing content or an escaping prefix is an error.

## Extraction

See the runnable [extract request](../examples/extract-request.json) for a complete payload. It supplies source identity, paths, revision, layout detection, canonical URL base, and inline Markdown. For real API sources, also provide `repo_root` so namespace and declaring-type casing can be recovered from the checked-out source indexes.

A successful response contains `contract`, `plugin_id`, `plugin_version`, and `result`. The result contains `page`, `normalized_document`, `chunk_records`, and `symbols` (empty for documentation extraction).

Errors return an `error` object with `type` and `message`, and exit status 1. A successful response exits with status 0. The worker is not a persistent JSON-lines or HTTP server.
