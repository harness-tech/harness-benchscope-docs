---
title: "Performance Testing"
---

# Performance Testing

The performance testing page stress-tests an inference service and supports **two modes**: *Concurrency Mode* and *Threshold Mode*. It is the core tool for understanding how a model service scales under load and whether it can meet a business SLA.

![Performance testing main interface](/images/benchscope-performance_default.png)

## Mode Overview

| Mode | Description | Typical Use Cases |
| --- | --- | --- |
| **Concurrency Mode** | Applies pressure step by step at fixed concurrency levels, recording metrics for each concurrency in real time | Observe how the system’s curves change with load |
| **Threshold Mode** | Starts from 1 concurrency, increases by powers of 2 plus bisection, to automatically find the maximum concurrency satisfying the threshold conditions | Given a business SLA, find the optimal sustainable concurrency |

## Concurrency Mode

Concurrency Mode applies pressure **level by level by concurrency**, feeding back in real time to the running interface:

- **Table** — throughput / TTFT / TPOT / ITL for each concurrency.
- **Curves** — multi-dimensional real-time statistics charts.
- **Progress** — progress updates in real time while running.

The per-concurrency panel updates in real time while running; within a single concurrency point, **continuous scrolling** is supported so you can watch the stream of requests live.

![Performance running view](/images/benchscope-performance_perf_running.png)

![Performance running statistics](/images/benchscope-performance_perf_running_statistics.png)

### Typical flow

1. Open **Performance** → create a task.
2. Configure the model and service address (Provider) under test.
3. Select **Concurrency Mode** and fill in the concurrency levels and request parameters.
4. Review the generated command and start.
5. Watch the table / curves / progress while it runs, then export the artifacts when it finishes.

## Threshold Mode

When the business SLA is known, Threshold Mode probes for the maximum concurrency that still satisfies the conditions (`best_concurrency`):

- Starts from **1 concurrency**, increasing by **powers of 2** (1, 2, 4, 8, …) for step-by-step stress testing.
- If **1 concurrency** already fails the threshold → the best concurrency is **1**, and probing ends.
- If `hi = 2^k` fails the threshold (while `lo = 2^(k-1)` satisfies it) → **bisect** within `(lo, hi]` until two adjacent values remain, where `lo` is the maximum concurrency satisfying the threshold.
- If the search upper limit is still satisfied → the upper-limit concurrency is the best (normal termination).

### Evaluation conditions

A concurrency level is considered to satisfy the thresholds when **all** of the following hold:

- **TTFT ≤ threshold** (evaluated with the chosen statistic: mean / median / p99)
- **TPOT ≤ threshold** (mean / median / p99)
- **Output throughput ≥ threshold**

<div class="tip">

**tip**：

Threshold search is efficient: instead of testing every concurrency between 1 and the cap, it doubles up to the first failure and then bisects — typically only a handful of stress-test runs are needed.

</div>

## Metric Definitions

| Metric | Meaning |
| --- | --- |
| Throughput (`output_mean` / `total_mean`) | Output / total throughput (tok/s) |
| TTFT (`ttft_mean`) | First-token latency (ms) |
| TPOT (`tpot_mean`) | Latency per output token (ms) |
| ITL (`itl_mean`) | Inter-token latency (ms) |

For third-party engines, metric availability is made explicit:

- **Available** → value is shown (blue).
- **Unavailable** → shown as **N/A** (gray-black).
- **Missing** → shown as a **gray dash**.

A fixed **11-metric snapshot contract** guarantees that every engine reports a well-defined set of metrics, even when some are not supported.

## Creating a Task

![Create task form](/images/benchscope-performance_create.png)

![Create task — token configuration](/images/benchscope-performance_create_token.png)

Creating a performance task uses a **three-step form**:

1. **Step 1 — Conditions**: choose the mode (concurrency / threshold) and the model / provider under test.
2. **Step 2 — Parameters**: set concurrency levels, request counts, input/output token lengths, and (for threshold mode) the SLA thresholds and search cap.
3. **Step 3 — Command preview**: review the exact command that will be executed, then start.

## Artifacts and Import

- Each run is saved as `run.json` plus logs `perf_<run_id>_*.log`.
- Package the artifacts as a **flat zip** (containing `run.json` + logs + optional `metrics.json`).
- Import the zip under **Datas → Perfs → Import Backup**, or run the CLI equivalent (`benchscope perf`) and import its output.

<div class="info">

**info**：

Performance records are persisted and remain viewable and downloadable on the **Datas** page even after you close the task. See [Datas](/en/docs/data/) for record management.

</div>

## Troubleshooting

- **No metrics for a third-party engine** — check whether the metric is *unavailable* (`N/A`) or *missing* (gray dash); the engine may simply not report it.
- **Concurrency mode returns immediately** — verify `--num-prompts` is not `0` unless you intend one request per worker.
- **Threshold mode finds 1 as best concurrency** — your service is already failing the SLA at a single concurrency; inspect TTFT / TPOT at level 1.
- **Timeouts counted as failures** — raise `--timeout` if your service is slow under load and failures are unexpected.

## Related

- [CLI Reference](/en/docs/cli/reference/) — the `benchscope perf` command
- [Concurrency Testing](/en/docs/performance/concurrency/) — step-by-step tutorial
- [Threshold Testing](/en/docs/performance/threshold/) — step-by-step tutorial
- [Datas](/en/docs/data/) — where performance records are stored and analyzed
- [Settings](/en/docs/tools/settings/) — providers and bench engines
