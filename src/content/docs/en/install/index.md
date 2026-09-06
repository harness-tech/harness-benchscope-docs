---
title: "Install"
---

# Install

This page covers installing BenchScope, starting the platform, and basic configuration. For full data-directory and configuration details see [Configuration](/en/docs/install/configuration/); for upgrades and uninstall see [Update & Uninstall](/en/docs/install/update-uninstall/).

## Requirements

- **Python** 3.9+ (3.10+ recommended; 3.9 / 3.11 / 3.12 are also supported).
- **pip** — keep it recent (`pip install --upgrade pip`).
- **Network** — access to PyPI during install, and to your target inference service when testing.
- **Browser** — a modern browser (Chrome recommended).

## Installation

Install BenchScope from PyPI:

```bash
pip install benchscope
```

Verify the version and available commands:

```console
$ benchscope --version
benchscope 1.1.0
$ benchscope --help
usage: benchscope [-h] [--version] {serve,perf,eval} ...
```

> To use **Native accuracy evaluation** (offline evaluation with local transformers weights), install the optional extra: `pip install benchscope[accuracy-native]`.

The web frontend is fully embedded in the Python package, so no separate Node.js / frontend setup is required.

## Starting the platform

Start the whole web platform with a single command:

```bash
benchscope
```

Common options:

```bash
benchscope --port 8080 --no-browser
```

| Option | Default | Description |
| --- | --- | --- |
| `--host` | `0.0.0.0` | Listening address; defaults to all interfaces for LAN access |
| `--port` | `8080` | Listening port |
| `--no-browser` | off | Do not auto-open the browser |
| `--debug` | off | Enable debug logging |

The console prints the access address; visit `http://127.0.0.1:8080` in a browser to enter the platform:

```console
INFO  BenchScope server started
INFO  Web UI: http://127.0.0.1:8080
```

> **Note**: the default `0.0.0.0` binding exposes the platform to your LAN. For local-only use, add `--host 127.0.0.1`. On first start, BenchScope creates a data root under `~/.benchscope` (see [Configuration](/en/docs/install/configuration/)).

## Next steps

Once started:

1. Configure your inference service (Base URL & API key) in **Settings → Providers**.
2. Run concurrency or threshold performance tests on the **Performance** page.
3. Run quantitative accuracy evaluation on the **Accuracy** page.
4. Chat interactively with a model in the **Sessions** page.

## Related

- [Quick Start](/en/docs/quickstart/) — feature overview and getting started
- [Configuration](/en/docs/install/configuration/) — data root, settings.json, and built-in config lists
- [Update & Uninstall](/en/docs/install/update-uninstall/) — upgrade, uninstall, and data cleanup
- [CLI](/en/docs/cli/) — command line and options
