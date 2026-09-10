---
title: "Concurrency & Threshold Modes"
description: "BenchScope performance testing two modes: concurrency mode (multi-level stress test) and threshold mode (auto search max concurrency) — parameter differences, field constraints, execution and scan logic."
---

# Concurrency & Threshold Modes

Performance testing provides two modes; the mode tag in the top-right of the creation wizard and in the task detail Cases panel reflects the current mode:

- **Concurrency Mode (`concurrency`)**: stress-tests a preset set of request-count levels in sequence, answering "how do throughput and latency change with concurrency";
- **Threshold Mode (`threshold`)**: starts probing from concurrency 1 by doubling, then bisects once a threshold is exceeded, automatically finding the maximum concurrency that satisfies the conditions, answering "how much concurrency can this configuration sustain at most".

## 1. Feature Overview

| Item | Concurrency Mode | Threshold Mode |
| --- | --- | --- |
| Core input | Request-count condition (set of positive integers) | Three per-group thresholds + Max Requests |
| Execution path | Known in advance: case × request-count matrix | Dynamic: 1, 2, 4, … + bisection |
| Progress denominator | Number of cases × request-count levels | Number of cases (concurrency points probed dynamically, not in the denominator) |
| End condition | All matrix points run | Each group finds its optimal concurrency, or hits the cap / exceeds the limit |
| Command preview | Full command list | Only the first command at concurrency 1 |
| Best marking | Local panel threshold → `Best` | Per-group threshold → `BestPerf` |

## 2. Concurrency Mode

### 2.1 Parameters

| Parameter | Location | Type/Constraint | Default | Description |
| --- | --- | --- | --- | --- |
| Request-count condition | Step 1 · condition groups | Set of positive integers, auto-deduplicated ascending; group 1 required | `1,2,4,8,16,32,40,64,128` | Each value is one "request-count" level (concurrency level) |
| Input / Output | Step 1 · condition groups | Integer; resets to 1024 if ≤ 0 | 1024 / 1024 | Per-group length combination (multiple groups allowed) |
| `num-prompts` | Step 2 · engine parameters | Integer ≥ 0; 0 = follow concurrency | 0 | Actual request count per level; when 0, request count = the concurrency level value |
| `request-rate` | Step 2 · engine parameters | `inf` or a positive number (req/s) | `inf` | Request rate for this run; `inf` = full speed |

### 2.2 Execution Logic

1. The backend `TaskManager._execute()` iterates `cases` (each condition group) in sequence.
2. Within each case it iterates `concurrency_list` (i.e. the request-count condition) in sequence, calling `_run_one()` to run one round of stress test per level.
3. After each level completes, `_record_row()`: appends a row to `rows`, incrementally writes the summary CSV, persists, and broadcasts `task_result` over WebSocket (the table/curves append in real time).
4. An `inf` in `concurrency_list` is mapped to `max_concurrency_search` (default 256) and run as the highest concurrency level.

<div class="info">

**Info:**

Execution order: cases run in condition-group list order, and within a group in request-count list order. Cases panel tag colors: green = done, blue = running, gray = pending.

</div>

## 3. Threshold Mode

### 3.1 Parameters

| Parameter | Location | Type/Constraint | Default | Description |
| --- | --- | --- | --- | --- |
| TTFT threshold | Step 1 · per group | Statistic `mean/median/p99` + integer ≥ 0 | `mean` + 0 | Meets criteria only when `TTFT-statistic ≤ threshold`; `0` = not participating |
| TPOT threshold | Step 1 · per group | Same as above | `mean` + 100 | Meets criteria only when `TPOT-statistic ≤ threshold`; `0` = not participating |
| Output throughput threshold | Step 1 · per group | Integer ≥ 0 (tok/s) | 0 | Meets criteria only when `output_mean ≥ threshold` (throughput judged by a **lower bound**); `0` = not participating |
| Max Requests | Step 1 | Integer ≥ 1 | 4096 | If the next run's request count exceeds it → the task is forced to end (`Finish`) |
| Search cap | `max_concurrency_search` (backend field) | Integer | 4096 | Still meeting criteria when doubled up to the cap → the cap is the optimal concurrency |

<div class="warning">

**Warning:**

Note on threshold direction: TTFT / TPOT are latency metrics and are judged by an **upper bound** (`TTFT-statistic > threshold` / `TPOT-statistic > threshold` means not meeting criteria — lower is better); output throughput is a throughput metric and is judged by a **lower bound** (`output_mean < threshold` means not meeting criteria — higher is better). At least one item per group must be non-zero, otherwise creation validation fails.

</div>

### 3.2 Scan Logic (executed independently per condition group)

`TaskManager._execute_case_threshold()`:

1. **Start point**: run concurrency 1 first; if it already fails to meet criteria → 1 is optimal and the group ends (scenario 1).
2. **Doubling probe**: 1 → 2 → 4 → 8 …, each tested concurrency is appended to `concurrency_list` and broadcasts `task_snapshot` (the Cases panel request-count tags grow in real time).
   - Next level's request count > `max_requests` → `forced_finish`: **the whole task ends**, and the status shows **Finish** (not Done);
   - Next level's request count > search cap and the current still meets criteria → the cap is the optimal concurrency and the group ends.
3. **Bisection convergence**: after a level fails to meet criteria, bisect within `(lo, hi]`, testing `(lo+hi)//2` each time, until `hi - lo == 1`; **lo is the maximum concurrency that satisfies all thresholds**.
4. **Failure tolerance**: a single level's execution exception (an error row) is not counted as a threshold violation, and probing continues upward.

```
# Scan process illustration (TTFT-Mean ≤ 200ms, TPOT-Mean ≤ 100ms)
conc 1 OK → conc 2 OK → conc 4 OK → conc 8 OK
conc 16 FAIL → bisect (8, 16]
conc 12 FAIL → conc 10 OK → (10, 12]: conc 11 FAIL
→ lo = 10 is the optimal concurrency for this group (marked BestPerf in the results table)
```

## 4. Mode Comparison

| Dimension | Concurrency Mode | Threshold Mode |
| --- | --- | --- |
| Progress bar (Perf panel) | done/total, total = case × request-count | done/total, total = number of cases |
| Cases panel request-count tags | Shows all request counts (ascending) | Shows only tested request counts (unexecuted shown as `Pending`) |
| Group title/tag extra info | No threshold text | Shows the group's threshold conditions (e.g. `TTFT-Mean ≤ 200ms · TPOT-Mean ≤ 100ms`) |
| Task end status | `done` | `done` (reached cap) or `Finish` (forced end) |
| Results table marking | `Best` (local panel threshold) | `BestPerf` (per-group threshold) |

## 5. FAQ

**Question: What does "next run's request count" mean in Threshold Mode?**
It is the concurrency value of the next probe level (when `num-prompts=0`, request count = concurrency). When it exceeds `max_requests`, the task immediately ends and is marked `Finish`, preventing the doubling probe from consuming too many requests.

**Question: Can different length combinations use different thresholds?**
Yes. Thresholds are stored independently per condition group (`case_id`); each group's scan, Cases panel display, and BestPerf marking are independent of the others.

**Question: What is the result if doubling reaches the search cap while still meeting criteria?**
The search cap (default 4096) is the optimal concurrency and is marked BestPerf; to keep probing, raise the cap via the backend field `max_concurrency_search`.

**Question: Does a failed level affect the scan?**
No. A failed row is recorded in the results table as `Failed`, but it is not counted as a threshold violation, and probing continues upward.

## 6. Related Docs

- [Create a Benchmark Task](/en/docs/manual/performance/create-task/) — parameter entry point
- [Live Monitoring & Curves](/en/docs/manual/performance/live-metrics/) — observing progress and metrics during execution
- [View & Export Results](/en/docs/manual/performance/results/) — BestPerf marking and export
- [Threshold Benchmark Reference](/en/docs/performance/threshold/) — principles and CLI parameters