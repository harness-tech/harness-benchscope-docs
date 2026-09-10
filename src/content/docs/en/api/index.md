---
title: "Overview"
description: "Overview of the BenchScope Web API: the FastAPI-based platform REST and WebSocket interfaces, covering configuration, tasks, logs, sessions, accuracy evaluation, engines, and skills."
---

# Overview

The Web backend of BenchScope is built on FastAPI and provides two kinds of interfaces — the **platform REST API** and **WebSocket** — covering modules such as configuration, tasks, logs, overview, sessions, accuracy evaluation, engines, and skills. The default service address (Base URL) is:

```text
http://127.0.0.1:8080
```

<div class="info">

**Info**:

The service address depends on the `--host` / `--port` at startup (default `0.0.0.0:8080`), see [Install](/en/docs/install/). Most endpoints return JSON, and standard HTTP status codes are used on errors.

</div>

<div class="warning">

**Warning**:

BenchScope **does not provide** OpenAI-compatible `/v1/models`, `/v1/chat/completions` inference endpoints on its own. The Sessions feature **proxies and forwards** requests to the currently active Provider (OpenAI-compatible endpoint); performance / accuracy testing also **calls** external inference services, rather than exposing inference interfaces to the outside.

</div>

## Interface Overview

The backend divides API groups by module, with **9 route groups + version + WebSocket** in total:

| Group | Prefix | Responsibility |
| --- | --- | --- |
| `api_config` | `/api/config` | Global configuration, Provider, models / datasets, directories, restart |
| `api_tasks` | `/api/tasks` | Performance test task management (create / start / stop / logs / export) |
| `api_logs` | `/api/logs` | Logs and historical runs (list / detail / live / backup / import / summary) |
| `api_dashboard` | `/api/dashboard` | Overview statistics / environment info |
| `api_sessions` | `/api/sessions` | Session chat (SSE streaming) |
| `api_test` | `/api/test` | Accuracy testing legacy interface (start / preview / stop / status) |
| `api_accuracy` | `/api/accuracy` | Accuracy evaluation tasks (tasks / samples / benchmark / engines / datasets / estimate / baselines) |
| `api_benchs` | `/api/benchs` | Built-in engines (list / detail / env check / upload / import / params) |
| `api_skills` | `/api/skills` | Built-in skills (list / download) |
| Version | `/api/version` | Service version number |
| WebSocket | `/ws` | Real-time push (task progress / live metrics) |

## Health & Version

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/version` | GET | Service version number |
| `/api/dashboard/stats` | GET | Dashboard overview statistics (Performance / Accuracy / Sessions / Models / Datasets / Providers counts) |
| `/api/dashboard/env` | GET | Environment info (MAC / IP / subnet, framework and operating system versions) |
| `/api/config/status` | GET | Configuration and Provider availability status |

```bash
curl http://127.0.0.1:8080/api/version
```

## Configuration (api_config)

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/config` | GET / POST | Read / update global configuration (settings.json) |
| `/api/config/providers` | GET / POST | Provider list / add |
| `/api/config/providers/{provider_id}` | PUT / DELETE | Update / delete a Provider |
| `/api/config/providers/{provider_id}/activate` | POST | Activate the specified Provider |
| `/api/config/status` | GET | Configuration and Provider availability status |
| `/api/config/models` | GET | Built-in model list |
| `/api/config/test-connection` | POST | Test a Provider connection |
| `/api/config/gpu` | GET | GPU info |
| `/api/config/params/{framework}` | GET | Framework parameters (JSON) |
| `/api/config/params-yaml/{framework}` | GET / PUT | Framework parameters (YAML read/write) |
| `/api/config/datasets` | GET | Built-in dataset list |
| `/api/config/model-catalog` | GET | Model catalog |
| `/api/config/datasets/download` | POST | Download a dataset |
| `/api/config/dirs` | GET / POST | Data directory read/write |
| `/api/config/restart` | POST | Restart the service |

## Performance Tasks (api_tasks)

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/tasks` | GET / POST | List / create performance test tasks |
| `/api/tasks/preview` | POST | Preview the task command |
| `/api/tasks/{task_id}` | GET / DELETE | Query / delete a task |
| `/api/tasks/{task_id}/logs` | GET | Real-time logs of the task |
| `/api/tasks/{task_id}/threshold` | PATCH | Update the task threshold configuration |
| `/api/tasks/{task_id}/start` | POST | Start the task |
| `/api/tasks/{task_id}/stop` | POST | Stop the task |
| `/api/tasks/{task_id}/export` | POST | Export task artifacts (zip) |
| `/api/tasks/{task_id}/preview` | POST | Preview a single task command |

## Logs & Historical Runs (api_logs)

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/logs/runs` | GET | Historical run records (Perfs) |
| `/api/logs/runs/{run_id}` | GET / DELETE | Query / delete a run |
| `/api/logs/runs/{run_id}/live` | GET | Live run logs (SSE) |
| `/api/logs/runs/{run_id}/backup` | GET | Packaged backup (flat zip) |
| `/api/logs/runs/import` | POST | Import a backup zip to restore a task |
| `/api/logs/runs/{run_id}/preview` | GET | Run detail preview |
| `/api/logs/runs/{run_id}/download` | GET | Download run artifacts |
| `/api/logs/runs/{run_id}/summary` | GET | Run summary (metrics) |
| `/api/logs/datasets` | GET | Dataset list |
| `/api/logs/datasets/upload` | POST | Upload a dataset |
| `/api/logs/datasets/{name}` | DELETE | Delete a dataset |
| `/api/logs/datasets/sharegpt` | GET | ShareGPT dataset status |
| `/api/logs/datasets/sharegpt/download` | POST | Download the ShareGPT dataset |

## Sessions (api_sessions)

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/sessions` | GET / POST / DELETE | Session list / create / clear all |
| `/api/sessions/{session_id}` | GET / DELETE | Query / delete a session |
| `/api/sessions/{session_id}/chat` | POST | Send a message to a session (SSE streaming response, proxied to the active Provider) |
| `/api/sessions/{session_id}/perf` | PATCH | Update session performance parameters |
| `/api/sessions/{session_id}/title` | PATCH | Rename a session |

<div class="info">

**Info**:

`/api/sessions/{session_id}/chat` **proxies and forwards** requests to the currently active Provider (OpenAI-compatible endpoint). BenchScope itself does not expose `/v1/*` inference endpoints; see [Sessions](/en/docs/tools/sessions/) for session parameters (`temperature` / `top_p` / `top_k` / `quality` / `enable_thinking`).

</div>

## Accuracy Testing Legacy (api_test)

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/test/start` | POST | Start accuracy testing (legacy) |
| `/api/test/preview` | POST | Preview accuracy testing (legacy) |
| `/api/test/stop` | POST | Stop accuracy testing (legacy) |
| `/api/test/status` | GET | Query accuracy testing status (legacy) |

> `api_test` is the **legacy interface** for accuracy testing; new code should use the `api_accuracy` route group.

## Accuracy Evaluation (api_accuracy)

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/accuracy/tasks` | GET / POST | List / create accuracy evaluation tasks |
| `/api/accuracy/tasks/{task_id}` | GET / DELETE | Query / delete a task |
| `/api/accuracy/tasks/{task_id}/stop` | POST | Stop the task |
| `/api/accuracy/tasks/{task_id}/samples` | GET | Single-sample traceability (samples.jsonl) |
| `/api/accuracy/tasks/{task_id}/export-samples` | GET | Export samples |
| `/api/accuracy/tasks/{task_id}/benchmark` | GET | Baseline benchmarking result |
| `/api/accuracy/engines` | GET | Accuracy engine list |
| `/api/accuracy/engines/{engine_id}/env-check` | GET | Engine environment check |
| `/api/accuracy/datasets` | GET | Accuracy dataset list |
| `/api/accuracy/datasets/import` | POST | Import a custom dataset |
| `/api/accuracy/datasets/{dataset_id}` | DELETE | Delete a dataset |
| `/api/accuracy/datasets/preview` | POST | Preview a dataset |
| `/api/accuracy/datasets/stats` | POST | Dataset statistics |
| `/api/accuracy/estimate` | GET | Token consumption estimate |
| `/api/accuracy/baselines` | GET / PUT | Baseline library read/write |
| `/api/accuracy/compare` | POST | Benchmarking comparison |

## Engines (api_benchs)

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/benchs` | GET | Engine list |
| `/api/benchs/{engine_id}` | GET | Engine detail |
| `/api/benchs/{engine_id}/mock` | POST | Set the engine Mock switch |
| `/api/benchs/authoring` | GET | Engine authoring contract |
| `/api/benchs/upload` | POST | Upload a custom engine |
| `/api/benchs/import` | POST | Import an engine |
| `/api/benchs/config/yaml` | GET / PUT | Engine configuration YAML read/write |
| `/api/benchs/{engine_id}/params` | GET | Engine parameters (JSON) |
| `/api/benchs/{engine_id}/params-yaml` | GET / PUT | Engine parameters YAML read/write |
| `/api/benchs/{engine_id}/params/{param_key}/option-desc` | GET | Parameter option descriptions |
| `/api/benchs/{engine_id}/env-check` | GET | Engine environment check |

## Skills (api_skills)

| Endpoint | Method | Description |
| --- | --- | --- |
| `/api/skills` | GET | Built-in skill list |
| `/api/skills/{skill_id}/download` | GET | Download a skill package (tar.gz) |

## Real-time Push (WebSocket)

| Endpoint | Method | Description |
| --- | --- | --- |
| `/ws` | WebSocket | Real-time push (task progress / live metrics) |

## Authentication

By default there is **no authentication** locally. If the service under test requires an API Key, configure it via [Settings → Providers](/en/docs/tools/settings/); the endpoints themselves do not require an extra token by default.

## FAQ

**Question: How can I confirm the service started properly?**
Visit `http://127.0.0.1:8080/api/version` (or refresh the root URL); a returned version number means the service is ready.

**Question: Does BenchScope provide an OpenAI-compatible `/v1/chat/completions` endpoint?**
**No.** BenchScope itself does not expose `/v1/*` inference endpoints. The Sessions feature **proxies and forwards** to the currently active Provider (OpenAI-compatible endpoint); performance / accuracy testing also **calls** external inference services, rather than exposing inference interfaces to the outside.

**Question: Can I call the session interface directly with curl?**
Yes. `POST /api/sessions/{session_id}/chat` is the session interface, returning SSE streaming data; it proxies the request to the currently active Provider (OpenAI-compatible endpoint).

**Question: How do I let a third-party service use my API Key?**
Configure the Base URL and API Key for the corresponding Provider in [Settings → Providers](/en/docs/tools/settings/). Authentication of the service under test is separate from BenchScope's own API authentication.

**Question: How do I create and preview a performance task over HTTP?**
Submit the task conditions to `POST /api/tasks/preview` to preview the command that will be executed; after confirming, create the task with `POST /api/tasks` and then start it with `POST /api/tasks/{task_id}/start`.

<div class="info">

**Info**:

The endpoints above are fully compatible with tasks created in the Web; the artifacts can be viewed / imported under **Datas → Perfs**.

## Related Docs

- [CLI](/en/docs/cli/) — the `serve` / `perf` / `eval` commands
- [Settings](/en/docs/tools/settings/) — Provider and global configuration
- [Performance Core Metrics](/en/docs/performance/metrics/) — performance task output metric definitions
- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — accuracy task output metric definitions
- [Sessions](/en/docs/tools/sessions/) — session interface and sampling parameters