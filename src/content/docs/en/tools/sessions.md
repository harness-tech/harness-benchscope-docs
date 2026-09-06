---
title: "Sessions"
---

# Sessions

**Sessions** provides a **session-based, interactive way of working** with your models — a chat-like workspace where you can tune sampling parameters, stream responses in real time, and read reasonings, all with rendering support.

![Sessions page](/images/benchscope_sessions.png)

<div class="tip">

**tip**：

Sessions is for **interactive conversation**, not benchmarking. Use it to sanity-check an answer quality quickly, then run a full performance or accuracy test when you are ready.

</div>

## Main Capabilities

- **Sampling parameters** — configure generation parameters (such as `temperature` / `top_p`) before starting a session request.
- **Markdown rendering** — session output supports Markdown rendering and **code syntax highlighting** (highlight.js with a dark theme).
- **SSE streaming** — streaming output is presented in real time, including **reasoning-process parsing**.
- **Session management** — session items in the sidebar, **renaming**, per-session log storage, and a centered confirmation dialog for clearing.
- **Performance bar** — shows performance information for the current session request.

## Usage Workflow

1. Create a **new session** on the Sessions page.
2. Configure the **sampling parameters** (temperature / top_p, etc.) before sending.
3. Send a message and watch the **streaming output** in real time, including the model’s reasoning process.
4. Sessions are **cached automatically**; you can rename them or export the logs per session.

### Choosing sampling parameters

| Parameter | Purpose |
| --- | --- |
| `temperature` | Controls randomness; lower = more deterministic |
| `top_p` | Nucleus sampling; keeps only the most-likely tokens whose cumulative probability reaches `top_p` |
| `max_tokens` | Caps the length of generated output |

<div class="info">

**info**：

These sampling parameters match those used by `perf` / `eval` in the [CLI](/en/docs/cli/), so the same sampling setup stays consistent across sessions, load tests, and evaluations.

</div>

## Session Management

The sidebar lists all your sessions. From there you can:

- **Switch** between sessions to continue previous conversations.
- **Rename** a session to keep your workspace organized.
- **Clear** a session with a centered confirmation dialog (avoids accidental deletion).
- **Export** the per-session logs for archival or sharing.

## Performance Bar

Each session request shows a **performance bar** with information about the request — useful for quick latency / throughput checks while you interact, without running a full benchmark.

## Where Sessions Are Stored

Sessions are cached under the `sessions` subdirectory of your **data root** (default `~/.benchscope/sessions/`). See [Configuration](/en/docs/install/configuration/) (`sessions_dir`) for the exact location and how to override the data root.

## FAQ

**Q: The output is not scrolling live?**

Make sure the session is using SSE streaming. If there is a proxy on the network path, the SSE long-lived connection can be dropped — check the server logs in that case.

**Q: How do I export a session?**

Select the session in the sidebar and use the export / persist action. The log file is written under the `sessions` subdirectory of your data root.

## Related

- [Configuration](/en/docs/install/configuration/) — session storage directory (`sessions_dir`)
- [Settings](/en/docs/tools/settings/) — the providers that drive session requests
- [Performance Testing](/en/docs/performance/) — structured, repeatable load testing
- [Accuracy Testing](/en/docs/accuracy/) — quantitative evaluation of a model
