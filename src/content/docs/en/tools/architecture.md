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

The browser talks to the FastAPI backend over **HTTP / SSE / WebSocket**. The backend dispatches task execution to the bench / accuracy engines and persists configuration to `settings.json` under the data root.

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

## Config Persistence

Configuration is persisted by `config.py` to `~/.benchscope/settings.json`. The **data root** can be overridden via `BENCHSCOPE_DATA_DIR`. All task artifacts and cache directories live under the data root — see [Configuration](/en/docs/install/configuration/) for the full layout.

## Bench Engine Abstraction

The engine abstraction supports:

- the **self-developed `benchscope` engine**,
- upstream **vLLM / SGLang engines** (version-pinned, e.g. `vllm-0.23`, `sglang-0.5.10`),
- **custom engines** registered through skills / plugins.

It includes **environment validation** and **parameter descriptions**, with **explicit metric availability** for third-party engines. See [Bench Engine](/en/docs/tools/bench-engine/) for details.

## Performance vs. Accuracy separation

The performance module (`benches/`) and the accuracy module (`accuracy/`) are **fully decoupled** — independent tasks, results, and scheduling. The accuracy module contains no performance metrics, keeping concerns cleanly separated.

## See Also

- Repository docs: `docs/rules/Architecture.md`, `docs/rules/Software.md`
- [Bench Engine](/en/docs/tools/bench-engine/) — the engine abstraction
- [Contributing](/en/docs/help/contributing/) — how to develop against this architecture
