---
title: "Overview"
---

# Overview

BenchScope's web backend is built on FastAPI and exposes three kinds of HTTP interfaces: an **OpenAI-compatible inference API**, the **platform REST API**, and a **WebSocket**. The default server Base URL is:

```text
http://127.0.0.1:8080
```

<div class="info">

**info**：

The address depends on the `--host` / `--port` used at startup (default `0.0.0.0:8080`) — see [Install](/en/docs/install/). Most endpoints return JSON and use standard HTTP status codes for errors.

</div>

## Session-style inference (OpenAI-compatible)

BenchScope's Sessions and inference pipeline follow the OpenAI-compatible protocol, so you can plug in any OpenAI client / tool:

| Endpoint | Method | Description |
| --- | --- | --- |
| `/v1/models` | GET | List the currently available inference models |
| `/v1/chat/completions` | POST | Chat completions, with streaming (SSE) support |

```bash
curl http://127.0.0.1:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{"model":"Qwen2.5-7B","messages":[{"role":"user","content":"Hello"}],"stream":true}'
```

<div class="tip">

**tip**：

Set `"stream":false` to disable streaming and receive the full response in one shot. Any standard OpenAI client (the `openai` SDK, curl, etc.) can connect directly.

</div>

## Health & version

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/version` | GET | Server version |
| `/api/dashboard/stats` | GET | Dashboard overview counts (Performance / Accuracy / Sessions / Models / Datasets / Providers) |
| `/api/dashboard/env` | GET | Environment info (MAC / IP / subnet, framework & OS versions) |
| `/api/config/status` | GET | Config and Provider availability status |

```bash
curl http://127.0.0.1:8080/api/version
```

## Tasks & evaluation

Performance and accuracy tasks can be created and managed over REST (fully compatible with tasks created in the Web UI):

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/tasks` | GET / POST | List / create performance tasks; `POST /api/tasks/preview` previews the command |
| `/api/tasks/{task_id}` | GET / DELETE | Fetch / delete a task |
| `/api/tasks/{task_id}/start` · `/stop` | POST | Start / stop a task |
| `/api/tasks/{task_id}/logs` | GET | Live task logs |
| `/api/tasks/{task_id}/export` | GET | Export task artifacts (zip) |
| `/api/accuracy/tasks` | GET / POST | List / create accuracy tasks |
| `/api/accuracy/tasks/{task_id}/samples` | GET | Per-sample trace (samples.jsonl) |
| `/api/accuracy/tasks/{task_id}/benchmark` | GET | Baseline comparison result |
| `/api/accuracy/estimate` | GET | Token consumption estimate |

<div class="tip">

**tip**：

Tasks can also be created through the [CLI](/en/docs/cli/): `benchscope perf` and `benchscope eval` produce artifacts fully equivalent to Web tasks, so pick whichever fits your workflow.

</div>

## Config & sessions

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/config` | GET / POST | Read / update global configuration (settings.json) |
| `/api/config/providers` | GET / POST / PUT / DELETE | Provider (Base URL / API Key) management |
| `/api/config/models` · `/datasets` | GET | Built-in model / dataset lists |
| `/api/sessions` | GET / POST / DELETE | List sessions / create / clear |
| `/api/sessions/{session_id}/chat` | POST | Send a message to a session (SSE streaming) |
| `/api/logs/runs` | GET | Historical task records (Perfs) |
| `/ws` | WebSocket | Real-time push (task progress / live metrics) |

## Authentication

There is **no authentication by default** locally. If the target service requires an API Key, configure it in [Settings → Providers](/en/docs/tools/settings/); the platform's own HTTP API does not require an extra token by default.

## FAQ

**Q: How can I confirm the service is running?**
Visit `http://127.0.0.1:8080/api/version` (or your reachable root address) — a returned version number means the service is ready.

**Q: Can I call the chat endpoint directly with curl?**
Yes. The `/v1/chat/completions` example above is a runnable curl command with an OpenAI-compatible request body and SSE streaming.

**Q: How do I let third-party services use my API key?**
Configure the Base URL and API Key for the relevant Provider in [Settings → Providers](/en/docs/tools/settings/). Authentication of the service under test is separate from BenchScope's own API authentication.

**Q: How do I create and preview a performance task over HTTP?**
Post task conditions to `POST /api/tasks/preview` to preview the command that will run; then create the task with `POST /api/tasks` and start it with `POST /api/tasks/{task_id}/start`.

<div class="info">

**info**：

These endpoints are fully compatible with tasks created in the Web UI, and their artifacts can be viewed or imported under **Datas → Perfs**.

## Related

- [CLI](/en/docs/cli/) — the `serve` / `perf` / `eval` commands
- [Settings](/en/docs/tools/settings/) — Providers and global configuration
- [Sessions](/en/docs/tools/sessions/) — session-style inference interaction
- [Architecture](/en/docs/tools/architecture/) — backend modules and route layout
