---
title: "Overview"
description: "Install BenchScope, launch the Web platform, and complete basic setup."
---

# Overview

This page covers how to install BenchScope, start the platform, and complete basic configuration. For full environment and data-directory details see [Configuration](/en/docs/install/configuration/); for upgrading / uninstalling see [Update & Uninstall](/en/docs/install/update-uninstall/).

## Environment Requirements

- **Python**: 3.10 or later recommended (3.9 / 3.11 / 3.12 are also supported).
- **pip**: a recent pip is suggested (`pip install --upgrade pip`).
- **Network**: access to PyPI during installation; access to the inference service under test during stress testing.
- **Browser**: a modern browser such as Chrome / Edge / Firefox (Chrome recommended).

<div class="tip">

**Tip**:

Install BenchScope inside a **virtual environment** (e.g. `python -m venv` / `conda`) to avoid interfering with other system Python packages, and to make version upgrades and uninstallation easier.

</div>

## Installation

Install BenchScope from PyPI:

```bash
pip install benchscope
```

After installation, verify that the command works:

```console
$ benchscope --help
usage: benchscope [-h] [--host HOST] [--port PORT] [--no-browser] [--debug]

LLM inference performance testing tool. Supports vLLM, SGLang, and any
OpenAI-compatible API.

options:
  -h, --help    show this help message and exit
  --host HOST   listen address (default 0.0.0.0)
  --port PORT   listen port (default 8080)
  --no-browser  do not automatically open the browser
  --debug       enable debug logging
```

View the installed version:

```console
$ pip show benchscope
Name: benchscope
Version: 1.1.1
```

> The CLI does not provide a `--version` option; the version can also be viewed via `pip show benchscope`, the Web `/api/version` endpoint, or the Settings page. With no arguments, or when the first argument is an option (e.g. `--port 8080`), it enters the serve-compatible branch, equivalent to `benchscope serve`.

> To use **Native accuracy evaluation** (loading local transformers weights for offline evaluation, with no external inference service), install the additional optional dependency: `pip install benchscope[accuracy-native]`. If you are unsure whether you need it, start with the base install and add it later as needed.

<div class="info">

**Info**:

The BenchScope Web frontend is fully embedded in the Python package; you do **not** need to install Node.js or frontend dependencies separately, or start frontend and backend services independently.

</div>

## Starting the Platform

A single command starts the entire Web platform:

```bash
benchscope
```

Common options:

```bash
benchscope --port 8080 --no-browser
```

| Option | Default | Description |
| --- | --- | --- |
| `--host` | `0.0.0.0` | Listen address; listens on all network interfaces by default, for LAN access |
| `--port` | `8080` | Listen port |
| `--no-browser` | off | Do not automatically open the browser at startup |
| `--debug` | off | Enable debug logging |

After startup the console prints the access address; visit http://127.0.0.1:8080 in a browser to enter the platform:

```console
INFO  BenchScope server started
INFO  Web UI: http://127.0.0.1:8080
```

<div class="warning">

**Warning**:

The default listen address is `0.0.0.0`, meaning **other machines on the LAN can also access** the platform. If you only use it locally, add `--host 127.0.0.1`; the first startup creates the data root directory under `~/.benchscope` (see [Configuration](/en/docs/install/configuration/)).

</div>

## Next Steps

After a successful start:

1. Configure your inference service (Base URL and API Key) in **Settings → Providers**;
2. Go to the **Performance Testing** page to run concurrency stress tests or threshold probing;
3. Go to the **Accuracy Testing** page to run quantitative evaluation;
4. Go to the **Sessions** page to chat interactively with the model.

## FAQ

**Question: What should I do if the port is occupied?**
Use `--port` to specify another port, for example `benchscope --port 9090`, and then visit the corresponding address.

**Question: The browser did not open automatically after startup?**
When explicit parameters such as `--host` / `--port` are passed, the browser is not opened automatically; you can also use `--no-browser` to disable auto-opening and then manually visit the address printed in the console.

**Question: The `benchscope` command cannot be found after installation?**
This is usually because the virtual environment is not activated, or the `Scripts` / `bin` directory is not on the PATH. Check the current environment and retry.

## Related Docs

- [Quick Start](/en/docs/quickstart/) — feature overview and getting started
- [Configuration](/en/docs/install/configuration/) — data root directory, settings.json, and built-in configuration list
- [Update & Uninstall](/en/docs/install/update-uninstall/) — upgrading, uninstalling, and data cleanup
- [CLI](/en/docs/cli/) — `serve` / `perf` / `eval` subcommands and parameters