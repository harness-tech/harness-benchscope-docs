---
title: "Create a Benchmark Task"
description: "BenchScope performance benchmark task creation three-step wizard: performance conditions (engine/Provider/condition groups), performance parameters (per-engine grouped parameters), and launch test (preview command and Token estimate)."
---

# Create a Benchmark Task

This document explains the three-step wizard for creating a benchmark task: **Performance Conditions → Performance Parameters → Launch Test**. The entry point is the "Concurrency Mode / Threshold Mode" button on the performance intro page, route `/performance/create?mode=concurrency|threshold` (the mode is decided by the entry point and cannot be switched inside the wizard).

## 1. Feature Overview

| Item | Description |
| --- | --- |
| Entry point | "Concurrency Mode" / "Threshold Mode" button on the performance intro page |
| Test engine | Bench CLI (in-house, no environment dependency) / vLLM native / SGLang native; native engines require the local environment check to pass |
| Service under test | Selected from a Provider (OpenAI-compatible API) configured in Settings, with the model list probed in real time |
| Output | Creating and starting the task returns you to the performance page in the execution monitoring view (see [Live Monitoring & Curves](/en/docs/manual/performance/live-metrics/)) |

## 2. Page Structure

```
┌──────────────────────────────────────────────────────────┐
│ Header: [←] Create Perf Test                [Concurrency]│
├──────────────────────────────────────────────────────────┤
│ Step bar: ① Conditions  ② Parameters  ③ Launch           │
├──────────────────────────────────────────────────────────┤
│ Step 1: Test engine (dropdown + env-check tag/details)   │
│        Provider panel (Provider/Base URL/Model/Status)   │
│        Max Requests (threshold mode only)                │
│        Condition panel (groups ×N: in/out/dataset/       │
│        request-count/threshold)                          │
│ Step 2: Selected engine id + grouped parameter list      │
│        (inline edit)                                     │
│ Step 3: Preview Conditions + Preview Command (copyable)  │
├──────────────────────────────────────────────────────────┤
│ Footer: [Cancel] [Previous] [Next / Launch]              │
└──────────────────────────────────────────────────────────┘
```

## 3. Input Parameters

### 3.1 Step 1 · Performance Conditions

| Field | Type | Constraint | Default | Description |
| --- | --- | --- | --- | --- |
| Test engine | Enum dropdown | `benchscope` / `vllm-*` / `sglang-*`; native engines require `env-check` to pass | `benchscope` | Determines the Step 2 parameter list and command shape |
| Provider | Enum dropdown | Providers configured in Settings | First | Determines Base URL and API Key |
| Model | Enum dropdown | Filled from probe results (`POST /api/config/test-connection`); **required** | First after probing | Model under test |
| Max Requests | Integer | ≥ 1 (shown in threshold mode only) | 4096 | Request-count cap for the next run; exceeding it forces an end |
| Input | Integer | Up to 6 digits; resets to 1024 on blur if ≤ 0 | 1024 | Per-group input token length |
| Output | Integer | Same as above | 1024 | Per-group output token length |
| Dataset | Enum | Currently only `Random` | `Random` | The backend also supports `sharegpt` (auto-downloaded from ModelScope) / `custom` |
| Request-count condition | Set of positive integers | Auto-deduplicated, ascending; group 1 is required in Concurrency Mode | `1,2,4,8,16,32,40,64,128` | Per-group concurrency (request-count) level |
| TTFT threshold | Statistic + integer | Statistic `mean/median/p99`; integer ≥ 0 (threshold mode) | `mean` + 0 | `0` = this condition does not participate in the decision |
| TPOT threshold | Statistic + integer | Same as above | `mean` + 100 | `0` = this condition does not participate in the decision |
| Output throughput threshold | Integer | ≥ 0 (threshold mode), unit tok/s | 0 | `0` = this condition does not participate in the decision |

### 3.2 Step 2 · Performance Parameters

Parameters **follow the engine selected in Step 1** (each engine has its own parameter list, edited in memory only, not written back to files), and the list is grouped automatically:

| Group | Parameters (keys) | Interaction |
| --- | --- | --- |
| Service config | `backend` (openai-chat / openai), `endpoint` | Dropdown (with option descriptions) |
| Sampling | `temperature`, `top-p`, `top-k`, `min-p`, `frequency-penalty`, `presence-penalty` | Click a value to edit inline / dropdown |
| Model & resources | `max-model-len`, `gpu-memory-utilization`, `mem-fraction-static`, `sharegpt-output-len` | Click a value to edit inline |
| Eval config | `trust-remote-code`, `ignore-eos`, `burstiness`, `seed`, `num-warmups`, `metric-percentiles` | Inline edit / toggle |
| Other | `request-rate` (inf / value), `num-prompts` (0 = follow concurrency), `timeout`, etc. | Dropdown / inline edit |

In-house engine (Bench CLI) defaults: `request-rate=inf`, `num-prompts=0`, `num-warmups=0`, `timeout=600`, `temperature=0.0`, `seed=0`; `chars-per-token` is fixed at 4 and hidden (the backend uses the default).

### 3.3 Step 3 · Launch Test

| Field | Source | Description |
| --- | --- | --- |
| Preview Conditions | Assembled on the frontend | Engine/framework/model/Base URL/dataset/request rate (Concurrency Mode appends the request-count list; Threshold Mode appends Max Requests and the three thresholds), copyable |
| Preview Command | `POST /api/tasks/preview` | In-house engine: one equivalent command per case × request count; native engines: `vllm bench serve` / `sglang.bench_serving`; Threshold Mode previews only the first command at concurrency 1 |
| Token usage estimate | Frontend estimate | Pops up after clicking "Launch": per-group "request count × input/output token" table, group totals, and total input/output (in millions) |

## 4. Field Constraints (Validation Rules)

| Validation | Rule | Trigger |
| --- | --- | --- |
| Model | Required, otherwise "Please select a model" | Next / Launch |
| Condition groups | Keep at least one group | Next / Launch |
| Request-count condition | Group 1 non-empty in Concurrency Mode; positive integers, auto-deduplicated ascending | Next / Launch |
| Thresholds (Threshold Mode) | Per group: all three must be integers ≥ 0, and **cannot all be 0** | Next / Launch |
| Max Requests | Integer ≥ 1 | On blur |
| Input / Output | Resets to 1024 on blur if ≤ 0 | On blur |
| Native engine environment | `env-check` failure blocks "Next" (allowed if that engine's Mock toggle is on, running in FAKE mode with simulated data) | Next |

## 5. Operation Steps

1. Enter the **Performance** page and click the **Concurrency Mode** or **Threshold Mode** button on the intro page.
2. Step 1: select the **Test engine** and wait for the environment check tag (native engines show a green "environment satisfied").
3. Select the **Provider** and **Model** (switching Provider re-probes automatically; online/offline status is shown below).
4. Fill in the condition groups: **Input/Output** length; in Concurrency Mode also fill the **Request-count condition**; in Threshold Mode fill **Max Requests** and the three per-group thresholds.
5. Click "+" to **Add a condition group** for multiple length combinations (the new group copies the previous group's values); click the delete icon to **remove a group**.
6. Click **Next**: validation passes and the current engine's parameter list loads, moving to Step 2.
7. Step 2: adjust parameters as needed (click a value to edit inline, save on blur/Enter, cancel with Esc; toggles switch directly), then click **Next**.
8. Step 3: review **Preview Conditions** and **Preview Command** (earlier changes refresh automatically, 250 ms debounce); click the copy icon when needed.
9. Click **Launch**: after validation passes, the **Token usage estimate** dialog pops up.
10. In the dialog, confirm the cost and click **Confirm**: the task is created, auto-started, and you are returned to the performance page.

The wizard advances through three steps, each gated by validation:

1. **Step 1 · Performance Conditions**: pick the engine, Provider, model, and fill the condition groups (and Max Requests + thresholds in Threshold Mode).
2. **Step 2 · Performance Parameters**: review and tune the engine's grouped parameters.
3. **Step 3 · Launch Test**: confirm the preview conditions and command, then launch after confirming the token estimate.

Each "Next" runs the validation rules in section 4; "Launch" additionally pops the token estimate for final confirmation.

## 6. Backend Execution Logic

| Phase | Frontend call | Backend behavior |
| --- | --- | --- |
| Page load | `GET /api/benchs` | Returns the engine list and default engine |
| Switch engine | `GET /api/benchs/{id}/env-check`, `GET /api/benchs/{id}/params`, `GET /api/benchs/{id}/params-yaml` | Validates the local framework version (required vs installed); returns parameter definitions and the parameter list |
| Switch Provider | `GET /api/config/providers`, `POST /api/config/test-connection` | Returns the Provider list; probes the model list and online status |
| Enter Step 3 | `POST /api/tasks/preview` | `build_command_lines()` generates commands (in-house/native/threshold first), without writing to disk |
| Confirm launch | `POST /api/tasks` | `TaskManager.create_task()`: generates `task_id` (`task-MMDD-HHMMSS`), creates `perfs/<run_id>/`, parses `cases` (including per-group thresholds), persists `tasks/<task_id>.json`, `status=pending` |
| Auto start | `POST /api/tasks/{id}/start` | `start_task()`: `status=running`, clears old `rows`, starts the execution thread (see [Concurrency & Threshold Modes](/en/docs/manual/performance/modes/)) |

Key payload fields: `framework`, `engine_id`, `model`, `dataset.length_pairs` (each item `[input, output, label, case_id, {three thresholds}]`), `concurrency_list` (Concurrency Mode = request-count condition; Threshold Mode = `[1]`), `mode`, `max_requests`, `engine_params_yaml`, `api` (inlined Provider config).

<div class="tip">

**Tip:**

The token estimate is a pure frontend calculation: Concurrency Mode computes each request count independently (when `num-prompts=0`, request count = the concurrency level value); Threshold Mode accumulates along the `1,2,4,…≤max_requests` ladder. It is only a cost reminder and does not affect execution.

</div>

## 7. FAQ

**Question: Why can't I move to the next step with the vLLM/SGLang native engines?**
Step 1 validates the local environment (required version vs installed version). When it fails, "Next" is blocked and the details list the missing dependencies and installation hints. You can install the matching version, or enable that engine's Mock toggle in Settings (to run with simulated data).

**Question: Can I switch modes partway through the wizard?**
No. The mode is determined by the URL query parameter (`?mode=`) and carries through the whole wizard; switching modes requires returning to the performance page and entering again.

**Question: Does clicking "Cancel" create a task?**
No. Cancel only discards the current draft and returns to the performance page (`/performance`); no task is created in the backend.

## 8. Related Docs

- [Performance Overview](/en/docs/manual/performance/) — page structure and task state machine
- [Concurrency & Threshold Modes](/en/docs/manual/performance/modes/) — parameter semantics and execution/scan logic
- [Settings Manual](/en/docs/manual/settings/) — Provider and Bench engine configuration
- [Performance Reference](/en/docs/performance/) — concepts and metric definitions