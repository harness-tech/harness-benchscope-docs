---
title: "Starting the Platform"
description: "Start the BenchScope Web platform with one command, and learn the common options and the first Dashboard overview."
---

# Starting the Platform

Once you have confirmed the [Requirements](/en/docs/quickstart/requirements/) are met and the [installation](/en/docs/quickstart/) is complete, start the entire Web platform with a single command.

## Start Command

```bash
benchscope
```

A few seconds later, your default browser opens `http://127.0.0.1:8080`. If no browser is available (for example, on a headless server), add `--no-browser` to skip auto-opening:

```bash
benchscope --port 8080 --no-browser
```

### Common Options

| Option | Default | Description |
| --- | --- | --- |
| `--host` | `0.0.0.0` | Listen address; listens on all network interfaces by default for LAN access, and can be restricted to localhost with `127.0.0.1` |
| `--port` | `8080` | Listen port |
| `--no-browser` | off | Do not automatically open the browser at startup |
| `--debug` | off | Enable debug logging |

The same options can also be passed through the explicit `serve` subcommand:

```bash
benchscope serve --host 127.0.0.1 --port 8080 --no-browser
```

After startup the console prints the access address and logs, for example:

```console
INFO  BenchScope server started
INFO  Web UI: http://127.0.0.1:8080
INFO  Browsing http://127.0.0.1:8080 ...
```

<div class="warning">

**Warning**:

- The default listen address is `0.0.0.0`, meaning other machines on the LAN can also access the platform. If you only use it locally, add `--host 127.0.0.1`.
- The first startup creates the data root directory under `~/.benchscope`; see [Configuration](/en/docs/install/configuration/) for details.

</div>

## First Start: the Overview Dashboard

Open `http://127.0.0.1:8080` in your browser; the first thing you see is the **Overview Dashboard**:

![BenchScope Dashboard overview](/images/benchscope-dashboard.png)

The Dashboard shows:

- **Overview** — quick counts for Performance / Accuracy / Sessions / built-in skills / Models / Datasets, with a Providers row at the bottom (number of Providers + number of Provider models).
- **Envs info** — hardware (Host / CPU / memory / GPU), operating system (system / version / kernel), network (MAC / IP / subnet / mask per interface), framework versions (Python / PyTorch / vLLM / SGLang / benchscope).
- **Test Records** — the 8 most recent performance stress-test records (Run ID / model / framework / status / time); clicking Detail jumps to Datas → Perfs.

Detailed field descriptions for each panel are in [Dashboard Overview](/en/docs/tools/dashboard/).

Use the top navigation bar to switch between **Dashboard · Performance · Accuracy · Sessions · Datas · Settings**.

## FAQ

**Question: The browser did not open automatically after startup?**
Make sure you did not use `--no-browser`; you can also manually open the address printed in the console in a browser.

**Question: http://127.0.0.1:8080 does not respond?**
Confirm the service process is still running and the port is not occupied (you can switch to another port with `--port`).

**Question: How do I restrict access to the local machine only?**
Add `--host 127.0.0.1` at startup.

## Related Docs

- [Quick Start](/en/docs/quickstart/) — feature overview and installation
- [Requirements](/en/docs/quickstart/requirements/) — prerequisites for running
- [Install](/en/docs/install/) — installation and startup details
- [Configuration](/en/docs/install/configuration/) — data root directory and settings.json
- [Dashboard Overview](/en/docs/tools/dashboard/) — detailed breakdown of each panel on the home page