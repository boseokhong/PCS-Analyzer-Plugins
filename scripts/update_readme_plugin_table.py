\
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
CATALOG_PATH = ROOT / "catalog.json"
README_PATH = ROOT / "README.md"

START_MARKER = "<!-- PLUGIN_TABLE_START -->"
END_MARKER = "<!-- PLUGIN_TABLE_END -->"

SUPPORTED_STATUSES = {"active", "deprecated", "unavailable", "blocked"}


def _escape_cell(value: object) -> str:
    if value is None:
        return "—"
    text = str(value).strip()
    if not text:
        return "—"
    return text.replace("|", r"\|").replace("\n", " ")


def _source_cell(url: object) -> str:
    if not isinstance(url, str) or not url.strip():
        return "—"

    value = url.strip()
    parsed = urlparse(value)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        return "—"

    return f"[Repository]({value})"


def _status_label(status: str) -> str:
    labels = {
        "active": "Active",
        "deprecated": "Deprecated",
        "unavailable": "Unavailable",
        "blocked": "Blocked",
    }
    return labels.get(status, status)


def _load_plugins() -> list[dict]:
    with CATALOG_PATH.open("r", encoding="utf-8") as handle:
        catalog = json.load(handle)

    if not isinstance(catalog, dict):
        raise ValueError("catalog.json root must be an object.")

    if catalog.get("schema_version") != 1:
        raise ValueError("Only catalog schema_version 1 is supported.")

    plugins = catalog.get("plugins")
    if not isinstance(plugins, list):
        raise ValueError("'plugins' must be a list.")

    seen_ids: set[str] = set()
    normalized: list[dict] = []

    for index, plugin in enumerate(plugins):
        if not isinstance(plugin, dict):
            raise ValueError(f"plugins[{index}] must be an object.")

        plugin_id = plugin.get("id")
        if not isinstance(plugin_id, str) or not plugin_id.strip():
            raise ValueError(f"plugins[{index}].id must be a non-empty string.")

        plugin_id = plugin_id.strip()
        if plugin_id in seen_ids:
            raise ValueError(f"Duplicate plugin id: {plugin_id}")
        seen_ids.add(plugin_id)

        status = plugin.get("status", "")
        if status not in SUPPORTED_STATUSES:
            raise ValueError(
                f"Plugin {plugin_id!r} has unsupported status {status!r}."
            )

        normalized.append(plugin)

    return sorted(
        normalized,
        key=lambda item: (
            0 if item.get("status") == "active" else 1,
            str(item.get("name") or item.get("id") or "").casefold(),
            str(item.get("id") or "").casefold(),
        ),
    )


def _build_table(plugins: list[dict]) -> str:
    lines = [
        START_MARKER,
        "",
        "| Plugin | ID | Version | Status | Min. PCS Analyzer | Category | License | Source |",
        "| --- | --- | ---: | --- | ---: | --- | --- | --- |",
    ]

    if not plugins:
        lines.append(
            "| _No plugins are currently registered._ | — | — | — | — | — | — | — |"
        )
    else:
        for plugin in plugins:
            lines.append(
                "| {name} | `{plugin_id}` | {version} | {status} | {minimum} | "
                "{category} | {license_name} | {source} |".format(
                    name=_escape_cell(plugin.get("name")),
                    plugin_id=_escape_cell(plugin.get("id")),
                    version=_escape_cell(plugin.get("latest_version")),
                    status=_escape_cell(_status_label(str(plugin.get("status", "")))),
                    minimum=_escape_cell(plugin.get("min_app_version")),
                    category=_escape_cell(plugin.get("category")),
                    license_name=_escape_cell(plugin.get("license")),
                    source=_source_cell(plugin.get("source_url")),
                )
            )

    lines.extend(["", END_MARKER])
    return "\n".join(lines)


def main() -> None:
    if not CATALOG_PATH.is_file():
        raise FileNotFoundError(f"Catalog not found: {CATALOG_PATH}")
    if not README_PATH.is_file():
        raise FileNotFoundError(f"README not found: {README_PATH}")

    readme = README_PATH.read_text(encoding="utf-8")

    if START_MARKER not in readme or END_MARKER not in readme:
        raise RuntimeError(
            "README.md must contain both plugin table markers:\n"
            f"{START_MARKER}\n{END_MARKER}"
        )

    before, remainder = readme.split(START_MARKER, 1)
    _, after = remainder.split(END_MARKER, 1)

    table = _build_table(_load_plugins())
    updated = before.rstrip() + "\n\n" + table + "\n\n" + after.lstrip()

    if updated != readme:
        README_PATH.write_text(updated, encoding="utf-8", newline="\n")
        print("README plugin table updated.")
    else:
        print("README plugin table already up to date.")


if __name__ == "__main__":
    main()
