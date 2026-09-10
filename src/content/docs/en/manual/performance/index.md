---
title: "Performance Overview"
description: "BenchScope Performance Testing manual overview: page structure, task list, task state machine, and a navigation index of the five documents in this manual."
---

# Performance Overview

This manual covers the **Performance Testing** module: how to navigate the pages, how to fill in task settings, and how tasks run in the backend. Performance testing stress-tests a deployed inference service (OpenAI-compatible API) and supports two modes — **Concurrency Mode** and **Threshold Mode** — providing real-time monitoring, statistics charts, and Excel export.

<div class="info">

**Info:**

Navigation location: left nav "Performance Testing (performance)", route `/performance`; when no task exists the intro page is shown, and clicking "Concurrency Mode / Threshold Mode" enters the creation wizard (`/performance/create?mode=concurrency|threshold`).

</div>

## 1. Page Structure

The performance page (`PerformanceView.vue`) switches between two layouts depending on whether a task exists:

- **No task — intro page**: top `a-result` (title + subtitle "One-click performance benchmarking for vLLM / SGLang services") + two mode buttons + 3 feature cards (⚡ Concurrency Testing / 🎯 Threshold Search / 📈 Real-time Performance Charts).
- **Task exists — four-row layout**:
  - **Row 1, three equal-width panels**: Perf panel (task info + Start Test/Stop Test/Close) | Cases panel (condition groups and request-count tags) | Logs panel (terminal-style logs + download).
  - **Row 2, live monitoring**: Profile Progress (left 1/3) + Real-Time Metrics (right 2/3), rendered from the "current request" snapshot.
  - **Row 3, Realtime Data**: results table grouped by condition group (local panel threshold + column settings + Excel export).
  - **Row 4, Statistics**: 12 stat charts (4 metric groups × Mean/Median/P99), with tooltip linkage.

```
┌───────────────────────────────────────────────────────────┐
│ Row 1: Perf panel | Cases panel | Logs panel (each 1/3)   │
│ Row 2: Profile Progress (1/3) | Real-Time Metrics (2/3)   │
│ Row 3: Realtime Data grouped results | Row 4: Statistics  │
└───────────────────────────────────────────────────────────┘
```

## 2. Task List

The performance page uses **single-task semantics**: it always shows the most recently created task, while the backend `TaskManager` maintains the full task list (`GET /api/tasks` ordered by `created_at` descending, excluding `rows`), persisted at `~/.benchscope/perfs/tasks/<task_id>.json`. i18n keeps keys such as `newTask` / `taskList` (from the older multi-task list version), but the current UI no longer renders a standalone task list; history can be viewed under **Datas → Perfs**.

| Field | Description |
| --- | --- |
| `task_id` | Format `task-MMDD-HHMMSS` |
| `model` / `framework` | Model and framework under test (Bench CLI / vLLM / SGLang) |
| `mode` | `concurrency` (Concurrency Mode) / `threshold` (Threshold Mode) |
| `cases` | Condition group list (with `case_id`, input/output length, per-group thresholds) |
| `status` | Task status, see the state machine below |
| `rows` | Completed result rows (one row per request count; excluded from the list endpoint, requires `GET /api/tasks/{task_id}` to fetch separately) |
| `run_dir` / `log_path` | Run directory `~/.benchscope/perfs/<run_id>/` and terminal log path |

## 3. Task State Machine

The backend `TaskManager` (`benchscope/task_manager.py`) maintains the task state machine:

| State | Value | Trigger Condition |
| --- | --- | --- |
| Pending | `pending` | After task creation (`POST /api/tasks`), the initial state before starting |
| Running | `running` | `POST /api/tasks/{task_id}/start` starts the execution thread |
| Done | `done` | All points executed; in Threshold Mode, when forced to end by exceeding `max_requests`, the page displays `Finish` |
| Stopped | `stopped` | Click "Stop Test", or a `running` task is interrupted on service restart |
| Error | `error` | An exception is thrown during execution (service unreachable, engine error, etc.) |

Transitions: `pending` → (start) → `running` → (end) → `done` / `stopped` / `error`; when `pending` / `error`, you can click "Start Test" again to retry; when not running, you can "Close" (delete the task).

<div class="warning">

**Warning:**

When a task ends in the `stopped` state, the frontend automatically removes it from the local list and calls `DELETE /api/tasks/{task_id}` (the page returns to the intro page); the run directory is retained and can still be viewed under Datas → Perfs.

</div>

## 4. Manual Navigation

| Doc | Document | Content |
| --- | --- | --- |
| 2.1 | [Performance Overview](/en/docs/manual/performance/) | Page structure, task list, task state machine |
| 2.2 | [Create a Benchmark Task](/en/docs/manual/performance/create-task/) | Three-step wizard: performance conditions → performance parameters → launch test |
| 2.3 | [Concurrency & Threshold Modes](/en/docs/manual/performance/modes/) | Parameters, constraints and scan logic for both modes |
| 2.4 | [Live Monitoring & Curves](/en/docs/manual/performance/live-metrics/) | Profile Progress, Real-Time Metrics, 12 live curves |
| 2.5 | [View & Export Results](/en/docs/manual/performance/results/) | Stat charts, results table, Excel/log export |

## 5. Related Docs

- [Performance Reference](/en/docs/performance/) — concepts and metric definitions
- [Data Manual](/en/docs/manual/datas/) — view and back up/import historical runs