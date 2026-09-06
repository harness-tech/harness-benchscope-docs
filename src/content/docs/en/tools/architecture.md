---
title: "Architecture"
---

# Architecture

BenchScope is a **monolithic web platform** that combines a **Python (FastAPI) backend** with a **Vue frontend**, and both are started together by the single `benchscope` command.

## Overall Architecture

```
┌────────────────────────────────────────────────────────────┐
│                    Web Frontend (Vue3 + antd)               │
│   Dashboard · Performance · Accuracy · Sessions · Datas ·   │
│   Settings                                                  │
└───────────────────────────────┬────────────────────────────┘
                                │ HTTP / SSE / WS
┌───────────────────────────────┴────────────────────────────┐
│              backend (FastAPI — benchscope/server)          │
│   api_benchs · api_accuracy · api_dashboard ·               │
│   api_config · api_logs · api_sessions · api_tasks ·        │
│   api_skills · api_plugins                                  │
└────────┬─────────────────────────┬──────────────────────────┘
         │ task execution          │ config persistence
┌────────┴──────────┐     ┌────────┴─────────────┐
│  benches/         │     │  config.py           │
│  runner ·         │     │  ~/.benchscope/      │
│  builtin_bench    │     │  settings.json       │
│  vllm · sglang    │     └──────────────────────┘
├───────────────────┤
│  accuracy/        │  executor · metrics · baselines ·
│  native_runner    │  scorers · datasets · estimator
└────────┬──────────┘
         ▼
 Inference service (vLLM / SGLang / any OpenAI-compatible API)
```

The browser talks to the FastAPI backend over **HTTP / SSE / WebSocket**. The backend dispatches task execution to the bench / accuracy engines and persists configuration under the data root.

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

The backend exposes a set of API groups that the frontend consumes:

- `api_benchs` — performance test task management
- `api_accuracy` — accuracy evaluation tasks
- `api_dashboard` — overview / environment info
- `api_config` — configuration read / write
- `api_logs` — log streaming and retrieval
- `api_sessions` — session chat (SSE)
- `api_tasks` — task scheduling
- `api_skills` / `api_plugins` — skill and plugin management

### Performance module (`benches`)

- `runner` — the task runner: launches tasks, collects and aggregates metrics;
- `builtin_bench` — the self-developed engine (streaming timeline collection, metric definitions aligned with vLLM);
- `vllm` / `sglang` — thin wrappers over the upstream official bench engines, version-pinned.

### Accuracy module (`accuracy`)

- `executor` — the evaluation executor;
- `metrics` — metric computation (accuracy / pass_rate / special metrics);
- `baselines` — open-source baseline library and tier ratings;
- `scorers` — graders (choice / math / code / judge);
- `datasets` — built-in dataset definitions and loading;
- `estimator` — token estimation.

### Config & scheduling

- Configuration is persisted by `config.py` to `settings.json` under the **data root** (default `~/.benchscope/settings.json`). The data root can be overridden via the `BENCHSCOPE_DATA_DIR` environment variable — see [Configuration](/en/docs/install/configuration/) for the full layout.
- Task scheduling is handled by `task_manager`; session management by `session_manager`.

<div class="info">

**info**：

The architecture deliberately keeps the **performance and accuracy modules decoupled** — independent tasks, results, and scheduling that do not depend on each other, so each can be extended and maintained on its own.

</div>

## Bench Engine Abstraction

The engine abstraction supports:

- the **self-developed `benchscope` engine**,
- upstream **vLLM / SGLang engines** (version-pinned, e.g. `vllm-0.23`, `sglang-0.5.10`),
- **custom engines** registered through skills / plugins.

It includes **environment validation** and **parameter descriptions** (surfaced as dropdowns with descriptions in the UI), with **explicit metric availability** for third-party engines. See [Bench Engine](/en/docs/tools/bench-engine/) for details.

## Technology Stack

| Layer | Technology |
| --- | --- |
| Frontend | Vue 3 + antd |
| Backend | Python + FastAPI |
| Real-time | HTTP / SSE / WebSocket |
| Config | settings.json (with YAML built-in manifests) |
| Inference | vLLM / SGLang / any OpenAI-compatible API |

## See Also

- [Bench Engine](/en/docs/tools/bench-engine/) — where engines fit in the abstraction
- [Configuration](/en/docs/install/configuration/) — data root and persistence
- [Contributing](/en/docs/help/contributing/) — how to develop against this architecture
