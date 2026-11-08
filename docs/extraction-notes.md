# Extraction behavior

## Scope and canonical citations

The manifest selects .NET documentation and API-reference prefixes explicitly. Layout mismatches fail rather than silently ingesting another SDK. Canonical citation bases are `https://docs.aspose.com/words/net` and `https://reference.aspose.com/words/net`; local checkout paths are not appended to them.

Front-matter URL overrides are normalized against the platform base or site origin. Unsupported URL schemes and protocol-relative URLs are rejected. Explicit first-heading IDs provide citation anchors; otherwise citations use the page top. Presentation HTML is removed outside code fences while meaningful text and explicit citation anchors are retained.

## API symbols and code examples

Source paths establish symbol identity. Titles, headings, declarations, and namespace index pages restore source-backed .NET casing. Supply `repo_root` for namespace and declaring-type recovery. Legacy requests without source indexes may fall back to path-derived casing.

Signatures come from access-modified declarations outside Examples sections. Examples are extracted separately with language metadata. Constructor identity resolves the declaring type and distinguishes constructors from similarly named members. Regression tests and the full-source constructor audit cover these behaviors.

## Gist examples

Documentation Gist references use a separately prepared, revision-pinned cache. Extraction remains offline and fails on missing or corrupt referenced examples. See [source preparation](source-preparation.md).

## Retrieval profile

The current profile version is 1.4.1. `retrieval-profile.json` is authoritative for its rules, conditions, preferred symbols, and namespace exclusions. Ranking preferences do not fabricate missing symbols. The configured `Aspose.Words.Lowcode` exclusion is a serving policy, not a statement that the SDK lacks those APIs.

The compatible engine enforces profile eligibility and ranking; the extraction worker does not implement serving. Confirm engine schema support before registration. See [engine integration](engine-integration.md).

## Updating published results

Re-extract and publish affected sources after changing normalization, symbols, or stored excerpts. Restarting serving processes alone cannot update existing indexed content. Profile-only changes require the engine to reload its policy. Validate both local extraction and the resulting served evidence when deploying changes.
