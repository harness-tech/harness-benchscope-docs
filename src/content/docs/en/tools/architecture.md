---
title: "Architecture"
description: "The overall architecture of the BenchScope monolithic web platform: core modules, API surface, the decoupled performance and accuracy modules, and data flow."
---

# Architecture

BenchScope is a **monolithic web platform** with a "Python (FastAPI) backend + Vue frontend"; the frontend and backend are started together by the same `benchscope` command.

## Overall Architecture

```text
┌────────────────────────────────────────────────────────────┐
│                    Web Frontend (Vue3 + antd)              │
│   Dashboard · Performance · Accuracy · Sessions · Datas ·  │
│   Settings                                                 │
└───────────────────────────────┬────────────────────────────┘
                                │ HTTP / SSE / WS
┌───────────────────────────────┴────────────────────────────┐
│                 backend (FastAPI — benchscope/server)       │
│   api_benchs · api_accuracy · api_dashboard ·               │
│   api_config · api_logs · api_sessions · api_tasks ·        │
│   api_skills · api_test (legacy) · /api/version · /ws       │
└───────┬────────────────────────┬───────────────────────────┘
        │ task execution         │ config persistence
┌───────┴────────┐     ┌──────────┴───────┐
│  benches/      │     │  config.py       │
│  runner ·      │     │  ~/.benchscope/  │
│  builtin_bench │     │  settings.json   │
│  vllm · sglang │     └──────────────────┘
├────────────────┤
│  accuracy/     │  executor · metrics · baselines ·
│  native_runner │  scorers · datasets · estimator
└───────┬────────┘
        ▼
 Inference service (vLLM / SGLang / any OpenAI-compatible API)
```

The frontend interacts with the backend via **HTTP / SSE / WebSocket**; the backend executes performance stress tests and accuracy evaluations, and persists configurations and artifacts under the data root directory.

## Core Modules

| Module | Responsibility |
| --- | --- |
| `benchscope/server` | FastAPI application and the various REST / SSE APIs |
| `benchscope/benches` | Performance testing engines: the self-developed engine, vLLM, SGLang, and the runner |
| `benchscope/accuracy` | Accuracy evaluation: executor / metrics / baselines / scorers / estimator / datasets |
| `benchscope/config.py` | Configuration persistence (`settings.json`) and the runtime singleton |
| `benchscope/task_manager.py` / `session_manager.py` | Task scheduling and session management |
| `benchscope/cli.py` | Command-line entry point (`serve` / `perf` / `eval`) |

### API surface

The backend exposes a set of API groups for the frontend to consume (for the full list, see [API Overview](/en/docs/api/)):

- `api_config` — configuration read / write (including Providers / Models / Datasets / directories / restart)
- `api_tasks` — performance test task management (create / start / stop / logs / export)
- `api_logs` — logs and historical runs (list / detail / realtime / backup / import / summary)
- `api_dashboard` — overview statistics / environment info
- `api_sessions` — session conversation (SSE streaming)
- `api_accuracy` — accuracy evaluation tasks (tasks / samples / benchmarking / engines / datasets / estimation / baselines)
- `api_benchs` — built-in engines (list / detail / environment validation / upload / import / parameters)
- `api_skills` — built-in skills (list / download)
- `api_test` — legacy accuracy-test endpoint (start / preview / stop / status)
- `/api/version` · `/ws` — version query and WebSocket real-time push

### Performance module (`benches`)

- `runner`: the task runner, responsible for launching stress tests, collecting and aggregating metrics;
- `builtin_bench`: the self-developed engine implementation (streaming timeline collection, metric definitions aligned with vLLM);
- `vllm` / `sglang`: encapsulation and versioning of the upstream official bench engines.

### Accuracy module (`accuracy`)

- `executor`: the evaluation executor;
- `metrics`: metric statistics (accuracy / pass_rate / specialized metrics);
- `baselines`: open-source baseline library and tier rating;
- `scorers`: graders (choice / math / code / judge);
- `datasets`: built-in dataset definitions and loading;
- `estimator`: Token pre-estimation.

### Config & scheduling

- Configuration is persisted uniformly to `settings.json` under the data root directory (default `~/.benchscope/settings.json`); the data root directory can be overridden via the environment variable `BENCHSCOPE_DATA_DIR`, see [Configuration](/en/docs/install/configuration/);
- Task scheduling is handled by `task_manager`, and session management by `session_manager`.

<div class="info">

**Info**:

The architecture decouples the performance and accuracy modules: each has independent tasks, results, and scheduling, with no dependencies between them, making each easier to extend and maintain.

</div>

## Bench Engine Abstraction

The engine abstraction supports the self-developed `benchscope` engine, vLLM / SGLang upstream engines, and custom engines, with **environment validation** and **parameter descriptions**, and makes **metric availability** explicit for third-party engines. See [Bench Engine](/en/docs/tools/bench-engine/) for details.

## Technology Stack

| Layer | Technology |
| --- | --- |
| Frontend | Vue 3 + antd |
| Backend | Python + FastAPI |
| Real-time communication | HTTP / SSE / WebSocket |
| Configuration | settings.json (YAML built-in manifest) |
| Inference service | vLLM / SGLang / any OpenAI-compatible API |

## Related docs

- [Bench Engine](/en/docs/tools/bench-engine/) — engine abstraction and customization
- [Configuration](/en/docs/install/configuration/) — data directories and persistence
- [Contributing](/en/docs/help/contributing/) — local development and the contribution workflow