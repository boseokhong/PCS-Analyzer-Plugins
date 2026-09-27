# PCS Analyzer Plugins

Official plugin catalog for [PCS Analyzer](https://github.com/boseokhong/PCS-analyzer).

This repository does **not** contain plugin source code. It contains the catalog metadata used by the PCS Analyzer Module Manager to discover approved plugin releases.

## Repository structure

```text
PCS-Analyzer-Plugins/
├─ catalog.json
├─ README.md
└─ docs/
   └─ catalog-schema.md
```

## How plugin distribution works

1. A plugin is developed and released in its own repository.
2. The developer publishes a versioned ZIP as an explicit GitHub Release asset.
3. The ZIP contains the plugin package expected by PCS Analyzer.
4. The release asset SHA-256 is calculated.
5. The approved release metadata is added to `catalog.json`.
6. PCS Analyzer fetches this catalog and classifies plugins as Available, Installed, Updates, Incompatible, or other lifecycle states.
7. PCS Analyzer downloads the ZIP, verifies SHA-256, and passes the verified package to its transactional installer.

A developer release is therefore not automatically distributed by PCS Analyzer. The catalog defines which version is approved for distribution.

## Catalog endpoint

PCS Analyzer uses the raw `catalog.json` file from the `main` branch as its official catalog endpoint.

```text
https://raw.githubusercontent.com/boseokhong/PCS-Analyzer-Plugins/main/catalog.json
```

---
## Available Plugins

The table below is generated automatically from `catalog.json`.

<!-- PLUGIN_TABLE_START -->

<!-- PLUGIN_TABLE_END -->

---

## Plugin release conventions

Recommended conventions:

- Plugin ID: stable lowercase identifier matching `^[a-z][a-z0-9_]*$`
- Manifest version: `1.2.0`
- Git tag / release: `v1.2.0`
- ZIP asset: `<plugin_id>-1.2.0.zip`
- Versions follow PEP 440 semantics.

Example:

```text
pcs_motion_explorer-1.2.0.zip
```

The release ZIP should contain the plugin package directly, for example:

```text
manifest.json
plugin.py
resources/
```

A single top-level wrapper directory is also supported by the current PCS Analyzer installer, but direct package-root layout is preferred for official releases.

## Lifecycle states

Supported catalog states:

- `active` — available for normal installation/update.
- `deprecated` — retained in the catalog but no longer recommended for new use.
- `unavailable` — retained as historical metadata but no longer distributable.
- `blocked` — installation should not be offered by PCS Analyzer.

## Integrity and security

Every distributable catalog entry must provide a SHA-256 digest. PCS Analyzer verifies the downloaded package before installation.

SHA-256 confirms that the downloaded package matches the catalog metadata. It does **not** prove that a plugin is safe, trustworthy, scientifically correct, or free of malicious code. PCS Analyzer plugins are Python code and can execute arbitrary code with the user's permissions.

## Adding or updating a plugin

A typical contribution should:

1. Publish the plugin release in the plugin's own repository.
2. Upload the versioned ZIP release asset.
3. Calculate the SHA-256 digest.
4. Update the corresponding entry in `catalog.json`.
5. Submit the catalog change for review.

The catalog entry must pass the schema described in [`docs/catalog-schema.md`](docs/catalog-schema.md).

## Current status

The catalog may remain empty while the Module Manager end-to-end smoke tests are being prepared. A minimal test plugin can be added first before production plugins are registered.
