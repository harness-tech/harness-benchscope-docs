---
title: "Starting the Platform"
description: "Launch the BenchScope Web platform with one command, learn common options, and tour the first Dashboard overview."
---

# Starting the Platform

Once you have met the [Requirements](/en/docs/quickstart/requirements/) and finished the [Quick Install](/en/docs/quickstart/), start the entire Web platform with a single command.

## Start Command

```bash
benchscope
```

After a few seconds the platform opens your default browser at `http://127.0.0.1:8080`. If the browser is not available (for example on a headless server), start it without auto-opening:

```bash
benchscope --port 8080 --no-browser
```

### Common Options

| Option | Default | Description |
| --- | --- | --- |
| `--host` | `0.0.0.0` | Listening address (use `127.0.0.1` to restrict to local access) |
| `--port` | `8080` | Listening port |
| `--no-browser` | off | Do not automatically open the browser when starting |
| `--debug` | off | Enable debug logging |

You can also pass the same options through the explicit `serve` subcommand:

```bash
benchscope serve --host 127.0.0.1 --port 8080 --no-browser
```

When the platform starts, the console prints the access address and logs, for example:

```console
INFO  BenchScope server started
INFO  Web UI: http://127.0.0.1:8080
INFO  Browsing http://127.0.0.1:8080 ...
```

<div class="warning">

**warning**：

- The default `--host 0.0.0.0` makes the platform reachable from other machines on your LAN. If you only use it locally, consider adding `--host 127.0.0.1`.
- On first launch, BenchScope creates a data root directory under `~/.benchscope` — see [Configuration](/en/docs/install/configuration/).

</div>

## First Launch: the Dashboard

Open `http://127.0.0.1:8080` in your browser. You first land on the **Dashboard** overview:

![BenchScope Dashboard overview](/images/benchscope-dashboard.png)

From the Dashboard you can see:

- **Count panels** — quick numbers for Performance / Accuracy / Sessions / Skills / Models / Datasets / Providers.
- **Environment info** — network interfaces (MAC / IP / subnet / mask), framework version, hardware, and operating-system details.
- **Recent records** — latest performance and accuracy runs, with quick links into each page.

Use the top navigation bar to jump between **Dashboard · Performance · Accuracy · Sessions · Datas · Settings**.

## FAQ

**Q: The browser does not open automatically after starting.**
Make sure you did not pass `--no-browser`; you can also manually open the address printed in the console.

**Q: Nothing responds at http://127.0.0.1:8080.**
Confirm the server process is still running and the port is not occupied (try a different `--port`).

**Q: How do I restrict access to local only?**
Add `--host 127.0.0.1` when starting.

## Related Docs

- [Quick Start](/en/docs/quickstart/) — feature overview and installation
- [Requirements](/en/docs/quickstart/requirements/) — environment prerequisites
- [Install](/en/docs/install/) — installation and startup details
- [Configuration](/en/docs/install/configuration/) — data root directory and settings.json
