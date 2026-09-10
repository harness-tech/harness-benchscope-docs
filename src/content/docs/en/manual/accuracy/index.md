---
title: "Accuracy Manual Overview"
description: "BenchScope Accuracy testing manual overview: page structure, task list, evaluation state machine, and a navigation index of the four documents in this manual."
---

# Accuracy Manual Overview

This manual covers the **Accuracy testing** module and explains "what to click, what to fill in, and how the backend runs". Accuracy testing performs quantitative evaluation of model output, supports both the **Serving link** and **Native** modes, ships with **9 evaluation datasets** and dedicated scorers, and provides token estimation plus open-source baseline benchmarking.

<div class="info">

**Info:**

**Navigation location**: left navigation "Accuracy testing (accuracy)". When no tasks exist, the intro page is shown; click "Create Accuracy Task (accCreateTask)" to enter the three-step wizard.

</div>

## 1. Page Structure

The accuracy page (`AccuracyView.vue`) switches between two layouts depending on whether tasks exist:

- **No tasks — intro page**: top `a-result` (title + "Create Accuracy Task" button), below it 3 feature cards (🎯 Model Serving Accuracy Evaluation / ⚖️ Offline Model Accuracy Evaluation / 🚨 Model Accuracy Benchmark Comparison).
- **Tasks exist — two-column layout**:
  - **Left column: task list card** (`accTasks`): "Refresh / Create" buttons in the top-right + task table (ID / Model / Mode / Dataset / Status / Accuracy / Actions).
  - **Right column: detail panel** (vertically stacked cards): ① task header (model/dataset/seed/temperature/progress bar) → ② core metrics `accMetrics` → ③ token statistics (Serving only) → ④ open-source baseline benchmark `accBenchmark` → ⑤ per-subject accuracy `accSubjects` → ⑥ evaluation log `accConsole` → ⑦ single-sample traceability `accSamples`.

```
┌────────────────────┐  ┌────────────────────────────────────────────┐
│ Task list card     │  │ Detail panel (vertically stacked cards)    │
│ [Refresh][Create]  │  │ ① Task header ② Core metrics ③ Token stats │
│ Task table         │  │ ④ Baseline benchmark ⑤ Per-subject ⑥ Log   │
│ ID/Model/Mode/     │  │ ⑦ Sample traceability                      │
│ Dataset/Status/    │  └────────────────────────────────────────────┘
│ Accuracy           │
└────────────────────┘
```

## 2. Task List

The task list (`accTasks`) columns are as follows; clicking a row selects the task and loads its details:

| Column | Field | Description |
| --- | --- | --- |
| Task ID | `task_id` | Format `eval-MMDD-HHMMSS` (a `-N` suffix is appended on collision) |
| Model | `model` | Name of the model under test; a `LoRA` tag is appended when LoRA is configured |
| Mode | `mode` | `Native` (green) / `Serving` (blue) |
| Dataset | `dataset_name` | Dataset name or local path |
| Status | `status` | See the state machine below |
| Accuracy | `accuracy` | Shows `xx%` after completion; shows a progress bar while running |
| Actions | — | "Stop" is shown while `running`; "Delete" is always shown |

## 3. Evaluation State Machine

The backend `EvalTaskManager` maintains an independent state machine; tasks are persisted under `evals/<task_id>/`:

| Status | Value | Trigger condition |
| --- | --- | --- |
| Pending | `pending` | Initial state after task creation, before start |
| Running | `running` | `start_task()` starts the execution thread |
| Done | `done` | All samples have been inferred and scored successfully |
| Stopped | `stopped` | "Stop" clicked manually, or a `running` task was interrupted by a service restart |
| Error | `error` | An exception was thrown during execution (e.g. dataset load failure, missing dependency) |

Transitions: `pending` → (`start_task()`) → `running` → (finish) → `done` / `stopped` / `error`.

<div class="warning">

**Warning:**

**Service restart**: if the service restarts while a task is running, all `running` tasks are set to `stopped`, and the `error` field records "service restarted, task interrupted".

</div>

## 4. Manual Navigation

| Ch. | Document | Content |
| --- | --- | --- |
| 3.1 | [Accuracy Manual Overview](/en/docs/manual/accuracy/) | Page structure, task list, evaluation state machine |
| 3.2 | [Create an Evaluation Task](/en/docs/manual/accuracy/create-task/) | Three-step wizard: dataset selection → mode & model → preview & start |
| 3.3 | [Datasets & Modes](/en/docs/manual/accuracy/datasets-modes/) | 9 built-in datasets, Serving/Native dual mode, scorers |
| 3.4 | [Viewing Results & Traceability](/en/docs/manual/accuracy/results/) | Core metrics, baseline benchmark, per-subject accuracy, single-sample traceability |

## 5. Related Documentation

- [Accuracy testing reference](/en/docs/accuracy/) — concepts and metric definitions
- [Performance testing manual](/en/docs/manual/performance/) — stress testing operation guide
- [CLI reference](/en/docs/cli/) — `benchscope eval` command line parameters
- [API reference](/en/docs/api/) — complete `/api/accuracy` routes