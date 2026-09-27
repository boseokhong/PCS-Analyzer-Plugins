# PCS Analyzer Plugin Catalog Schema v1

The official plugin catalog is a JSON document consumed by the PCS Analyzer Module Manager.

## Root object

```json
{
  "schema_version": 1,
  "plugins": []
}
```

Requirements:

- `schema_version` must be the integer `1`.
- `plugins` must be a JSON array.
- Plugin IDs must be unique within the catalog.
- Unknown fields are ignored by the current schema-v1 reader.
- The catalog response must remain below the PCS Analyzer catalog-size limit (currently 5 MiB).

## Plugin entry

Example:

```json
{
  "id": "pcs_test_plugin",
  "name": "PCS Test Plugin",
  "latest_version": "1.0.0",
  "author": "Boseok Hong",
  "description": "Minimal plugin for Module Manager integration testing.",
  "homepage_url": "https://github.com/boseokhong/PCS-Test-Plugin",
  "source_url": "https://github.com/boseokhong/PCS-Test-Plugin",
  "download_url": "https://github.com/boseokhong/PCS-Test-Plugin/releases/download/v1.0.0/pcs_test_plugin-1.0.0.zip",
  "sha256": "0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
  "min_app_version": "1.3.4",
  "max_app_version": null,
  "status": "active",
  "category": "Testing",
  "tags": ["test", "integration"],
  "license": "BSD-3-Clause"
}
```

## Required fields

Every entry requires the following non-empty strings:

- `id`
- `name`
- `latest_version`
- `author`
- `description`
- `status`

At least one of the following must also be supplied:

- `homepage_url`
- `source_url`

## Plugin ID

`id` must match:

```text
^[a-z][a-z0-9_]*$
```

Plugin IDs should be treated as permanent identifiers and should not be reused for unrelated plugins.

## Versioning

`latest_version`, `min_app_version`, and `max_app_version` use PEP 440 version semantics.

Examples:

```text
1.0
1.0.0
1.2.0rc1
2.0.dev1
```

Under PEP 440, `1.0` and `1.0.0` compare as equal.

If both compatibility bounds are present, `min_app_version` must not exceed `max_app_version`.

Compatibility bounds are inclusive.

## URLs

URLs are validated intentionally simply:

- absolute URL;
- `http` or `https` scheme;
- non-empty host.

Official catalog entries should use HTTPS.

## Download metadata

For `active` plugins:

- `download_url` is required;
- `sha256` is required.

For `deprecated`, `unavailable`, and `blocked` entries, package metadata may be omitted when the plugin is no longer distributable.

If either `download_url` or `sha256` is supplied, both must be supplied.

`sha256` must contain exactly 64 hexadecimal characters. Uppercase input is accepted by the PCS Analyzer parser and normalized to lowercase.

## Lifecycle status

Allowed values:

```text
active
deprecated
unavailable
blocked
```

Meaning:

- `active`: available for installation and update when compatible.
- `deprecated`: retained but no longer recommended; it may still remain distributable.
- `unavailable`: historical catalog entry; package may no longer be available.
- `blocked`: distribution should not be offered by PCS Analyzer.

## Optional metadata

Optional fields include:

- `min_app_version`
- `max_app_version`
- `category`
- `tags`
- `license`

`category` and `license`, when present, must be non-empty strings.

`tags` must be an array of unique, non-empty strings. Tag uniqueness is case-insensitive.

## SHA-256

Example commands for producing a digest:

### PowerShell

```powershell
Get-FileHash .\pcs_test_plugin-1.0.0.zip -Algorithm SHA256
```

### Python

```python
from hashlib import sha256
from pathlib import Path

path = Path("pcs_test_plugin-1.0.0.zip")
print(sha256(path.read_bytes()).hexdigest())
```

For very large files, streaming is preferable to reading the whole file into memory.

## Distribution model

The plugin's own repository remains authoritative for source code, documentation, issues, and releases.

This catalog is authoritative only for the version and package that PCS Analyzer distributes through its Module Manager.

A new developer release does not automatically become the catalog version. Catalog updates should be reviewed separately.

## Security note

Catalog SHA-256 verification protects package integrity relative to the catalog metadata. It is not a security sandbox, code-signing system, or scientific validation mechanism.
