---
title: "Viewing Results & Traceability"
description: "A detailed look at the Accuracy results detail panel: core metrics, token statistics, open-source baseline benchmark, per-subject accuracy and single-sample traceability, wrong-answer set export, including input parameters, button operations, and backend data flow."
---

# Viewing Results & Traceability

After an accuracy task finishes running, click any task in the left-hand task list; the right-hand **detail panel** displays, from top to bottom: task header → core metrics (accMetrics) → token statistics (Serving only) → open-source baseline benchmark (accBenchmark) → per-subject accuracy (accSubjects) → evaluation log (accConsole) → single-sample traceability (accSamples).

<div class="info">

**Info:**

**Loading timing**: while a task is running, only the progress bar and the real-time log are shown; after all samples have been scored, the core metrics / token statistics / baseline benchmark / per-subject / sample traceability panels appear.

</div>

## 1. Page Structure

```
┌──────────────────────────────────────────────────────────┐
│ Detail panel (vertically stacked cards)                  │
│ ① Task header: model/dataset/seed/temperature + progress │
│   bar + [Stop]                                           │
│ ② Core metrics accMetrics: 6 metric cards + dataset-     │
│   specific metrics + conclusion                          │
│ ③ Token stats accTokenReport (Serving): 5 items +        │
│   estimate vs actual                                     │
│ ④ Baseline benchmark accBenchmark: grade/baseline/diff/  │
│   rank/radar chart                                       │
│ ⑤ Per-subject accuracy accSubjects: subject/correct/     │
│   total/accuracy table                                   │
│ ⑥ Evaluation log accConsole: real-time scrolling log     │
│ ⑦ Sample traceability accSamples: filter + table +       │
│   wrong-answer set export                                │
└──────────────────────────────────────────────────────────┘
```

## 2. Input Parameters

The results detail panel is primarily read-only; the interactive input parameters are concentrated in the filter and export of **single-sample traceability**:

| Field | Identifier | Type | Default | Description |
| --- | --- | --- | --- | --- |
| Sample filter | `sampleFilter` | Radio `all`/`wrong`/`invalid` | `all` | All (accSampleAll) / Wrong (accSampleWrong) / Invalid (accSampleInvalid) |
| Export filter | `filter` | Fixed `wrong` | `wrong` | Export wrong-answer set (accExportWrong); the backend also supports `invalid` |
| Sample pagination | — | Pagination | 10 per page | Initial load `limit=200, offset=0`, front-end pagination of 10 |

## 3. Field Constraints

| Field | Required | Constraint / Enum |
| --- | --- | --- |
| `sampleFilter` | Optional (default all) | Enum `all` / `wrong` / `invalid` (the 3 UI options); the backend `filter` also supports `correct` |
| `filter` (export) | Optional | Enum `wrong` / `invalid` (default `wrong`); returns 404 when no matching samples exist |
| Sample pagination | — | `limit` / `offset` are non-negative integers, page size fixed at 10 |

## 4. Core Metrics (accMetrics)

| Metric | Key | Definition / Formula |
| --- | --- | --- |
| Accuracy | `accuracy` | `correct_samples / total_samples` (the core primary metric) |
| Pass rate | `pass_rate` | `(total - invalid) / total` (share of valid parseable samples) |
| Total samples | `total_samples` | Number of samples that actually took part in the evaluation |
| Correct | `correct_samples` | Count of `status = correct` |
| Wrong | `wrong_samples` | Count of `status = wrong` |
| Invalid | `invalid_samples` | Count of `status = invalid` |
| Evaluation conclusion | `conclusion` | See the conclusion rules below |

**Evaluation conclusion (`conclusion`) rules** (the final conclusion enum is **Pass / Accuracy Drop / Abnormal**):

| Conclusion | Trigger condition |
| --- | --- |
| Abnormal | `total_samples = 0` or `invalid / total > 0.2` |
| Accuracy Drop | Baseline primary-metric diff `diff_pp < -5.0` |
| Pass | All other cases |

<div class="warning">

**Warning:**

**Pay attention to the distinction**: `result.conclusion` (evaluation conclusion) is the final enum **Pass / Accuracy Drop / Abnormal**; `benchmark.conclusion` (baseline benchmark conclusion) is comparison wording relative to the open-source baselines (better than / on par with / clearly worse than). The two are independent of each other.

</div>

## 5. Token Consumption Statistics (Serving, accTokenReport)

| Metric | Key | Description |
| --- | --- | --- |
| Input tokens | `prompt_tokens_total` | Sum of input tokens across all samples |
| Output tokens | `completion_tokens_total` | Sum of output tokens across all samples |
| Total consumption | `total_tokens` | Input + output |
| Avg input per sample | `avg_prompt_tokens_per_sample` | Total input / sample count |
| Avg output per sample | `avg_completion_tokens_per_sample` | Total output / sample count |
| Estimate vs actual | `estimate_vs_actual` | `estimate_total → actual_total` (`deviation_pct` deviation percentage) |

<div class="info">

**Info:**

**Native mode has no token statistics**: `result.tokens` is `null`, and the card is automatically hidden (this is a Native capability boundary).

</div>

## 6. Open-Source Baseline Benchmark (accBenchmark)

| Field | Key | Description |
| --- | --- | --- |
| Grade | `grade` | Relative to the best baseline: S (≥0) / A (≥-5pp) / B (≥-15pp) / C |
| Baseline used | `baseline_used` | `name` / `score` of the closest-size baseline |
| Diff | `diff_pp` | Current score − baseline score (percentage points) |
| Same-size rank | `rank_pct` | Share of same-size-segment baselines that the current model surpasses (%) |
| Benchmark conclusion | `conclusion` | Better than the same-size open-source baselines / on par with the baselines / clearly worse than the baselines (risk warning) |
| Capability radar | `radar` | Four dimensions: knowledge / math / code / conversation (for a single dataset, only that dimension has a value) |

## 7. Per-Subject Accuracy (accSubjects)

| Column | Field | Description |
| --- | --- | --- |
| Subject | `subject` | Sample subject label (samples with an empty value do not participate) |
| Correct | `correct` | Number correct in that subject |
| Total | `total` | Number of samples in that subject |
| Accuracy | `accuracy` | `correct / total` for that subject |

## 8. Single-Sample Traceability (accSamples)

Column fields: `#` (index), subject (`subject`), Prompt (`prompt`), model output (`output`), reference answer (`answer`), Token (in/out) (`tokens`), verdict (`status`).

- **Filter**: All (accSampleAll) / Wrong (accSampleWrong) / Invalid (accSampleInvalid); the backend `filter` also supports `correct`.
- **Export wrong-answer set (accExportWrong)**: download the `wrong` samples as `wrong_samples.jsonl` (including prompt/output/answer/verdict), for error analysis and feedback into training.

## 9. Button Operations and Execution Steps

1. In the left-hand task list, **click a task row** → the full details and sample list are loaded.
2. Review from top to bottom: core metrics → token statistics (Serving) → baseline benchmark → per-subject accuracy → evaluation log.
3. In "Sample traceability", switch the filter with "All / Wrong / Invalid" to pinpoint the specific problem samples.
4. Click **Export wrong-answer set** to download `wrong_samples.jsonl`.
5. (`running`) Click **Stop** in the task header or list row to send a stop request.
6. Click **Delete** to remove the task (the persisted directory is deleted at the same time).

## 10. Backend Execution Logic

| Action | API / Data flow |
| --- | --- |
| Task selected | `store.loadTask()` → `GET /api/accuracy/tasks/{task_id}` (the list snapshot does not include result; fetches the full details) |
| Samples loaded | `GET /api/accuracy/tasks/{task_id}/samples?filter=all&limit=200&offset=0` |
| Filter switched | `watch(sampleFilter)` re-requests `samples` (new `filter`) |
| Wrong set exported | `window.open` → `GET /api/accuracy/tasks/{task_id}/export-samples?filter=wrong` (returns `FileResponse`) |
| Baseline benchmark | Computed by `compute_benchmark()` at the end of `run_eval`, stored in `result.benchmark` and delivered with the details |
| Real-time push | WebSocket `eval_task_log` / `eval_task_progress` / `eval_task_result` (per-sample, front-end accumulation capped at 500); after `done`, the API pagination is authoritative |

Persisted files: `evals/<task_id>/result.json` (results), `samples.jsonl` (per-sample traceability), `task.json` / `run.json` (main record / run record).

## 11. FAQ

**Question: Why can't I see the results after clicking a task?**
The list snapshot does not include `result`; only after clicking does the front-end send `GET /tasks/{id}` to fetch the full details. While the task is running, only the progress and log are shown, and the results cards appear after completion.

**Question: What are the criteria for the evaluation conclusion?**
"Abnormal" takes precedence (`total=0` or the invalid share > 0.2) → then "Accuracy Drop" (baseline `diff_pp < -5pp`) → otherwise "Pass".

**Question: What is the difference between the "evaluation conclusion" and the "baseline benchmark conclusion"?**
`result.conclusion` is the final enum **Pass / Accuracy Drop / Abnormal**; `benchmark.conclusion` is comparison wording relative to the open-source baselines (better than / on par with / clearly worse than). The two are independent — do not mix them up.

**Question: Why isn't the token statistics card shown?**
Only Serving mode collects `usage`; in Native mode `result.tokens` is `null`, and the card is automatically hidden.

**Question: How do I use the wrong-answer set?**
The wrong-answer set is a JSONL containing `prompt`/`output`/`answer`/verdict, and can be used directly for error analysis, bad-case review, or feeding back into fine-tuning training.