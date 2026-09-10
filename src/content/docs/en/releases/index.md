---
title: "Overview"
description: "Release notes for BenchScope versions, with release information, upgrade notes, and related documentation."
---

# Overview

BenchScope release notes. The current version is **1.1.1**, versioned with `x.y.z` semantic versioning. Each entry covers feature highlights, behavioral changes, and upgrade notes.

| Version | Title | Release date |
| --- | --- | --- |
| [v1.1.1](/en/docs/releases/v1-1-1/) | Installer integrity / Provider id backfill / skills moved into the package | 2026-09-05 |
| [v1.1.0](/en/docs/releases/v1-1-0/) | Session experience / Performance real-time panel / Dashboard overview | 2026-09-05 |
| [v1.0.8](/en/docs/releases/v1-0-8/) | Standalone accuracy testing module | 2026-09-01 |
| [v1.0.7](/en/docs/releases/v1-0-7/) | Engine rework | 2026-08-30 |
| [v1.0.6](/en/docs/releases/v1-0-6/) | Feature updates | 2026-08-28 |
| [v1.0.5](/en/docs/releases/v1-0-5/) | Early release | — |

## Upgrade Notes

- We recommend restarting the service after upgrading;
- The legacy `~/.benchscope/config.json` is automatically migrated to `settings.json` — no manual handling needed;
- We recommend backing up the data root directory before upgrading (see [Install → Update & Uninstall](/en/docs/install/update-uninstall/)).

## Related Docs

- [CLI](/en/docs/cli/) — command-line tool
- [API](/en/docs/api/) — HTTP interface
- [Help](/en/docs/help/) — troubleshooting and contributing
