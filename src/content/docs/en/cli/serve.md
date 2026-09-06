---
title: "serve"
---

# serve

Starts the Web service, opening the full platform at `http://127.0.0.1:8080` by default.

```bash
benchscope serve [--host HOST] [--port PORT] [--no-browser] [--debug]
```

| Argument | Default | Description |
| --- | --- | --- |
| `--host` | `0.0.0.0` | Listening address |
| `--port` | `8080` | Listening port |
| `--no-browser` | off | Do not automatically open the browser |
| `--debug` | off | Enable debug logging (more detailed logs for troubleshooting) |

<div class="tip">

**tip**：

`--debug` is very useful when troubleshooting task startup or API calls, as it outputs detailed debug-level logs.

</div>

<div class="info">

**info**：

**Backward-compatible behaviour**：When you pass **no arguments**, or the *first* argument is an option (for example `--port 8080`), the CLI falls back to the "start service" behaviour — equivalent to running `benchscope serve`.

</div>

Example:

```bash
benchscope serve --host 127.0.0.1 --port 9090 --no-browser
```

## Related

- [CLI Overview](/en/docs/cli/) — sub-command overview and quick start
- [perf](/en/docs/cli/perf/) — performance testing
- [eval](/en/docs/cli/eval/) — accuracy evaluation
- [Quick Start](/en/docs/quickstart/) — installing and launching
