---
title: "serve"
description: "The benchscope serve command: start the Web service and open the full platform, with host, port, and debugging options."
---

# serve

Starts the Web service, opening the full platform at `http://127.0.0.1:8080` by default.

```bash
benchscope serve [--host HOST] [--port PORT] [--no-browser] [--debug]
```

| Parameter | Default | Description |
| --- | --- | --- |
| `--host` | `0.0.0.0` | Listening address |
| `--port` | `8080` | Listening port |
| `--no-browser` | off | Do not automatically open the browser at startup |
| `--debug` | off | Enable debug logging (outputs more detailed runtime logs to aid troubleshooting) |

<div class="tip">

**Tip:**

`--debug` outputs detailed debug-level logs, which helps troubleshoot issues such as task startup or API calls.

</div>

<div class="info">

**Info:**

**Backward-compatible behaviour**: when `benchscope` is run with no arguments, or the first argument is an option (e.g. `--port 8080`), it falls back to starting the service, equivalent to `benchscope serve`.

</div>

Example:

```bash
benchscope serve --host 127.0.0.1 --port 9090 --no-browser
```

## Related Documentation

- [CLI Overview](/en/docs/cli/) — subcommand overview and quick start
- [perf Command](/en/docs/cli/perf/) — performance stress testing
- [eval Command](/en/docs/cli/eval/) — accuracy evaluation
- [Quick Start](/en/docs/quickstart/) — installation and startup