---
title: "Threshold Testing"
---

# Threshold Testing

When the **business SLA** is known, use *threshold probing* to find the maximum concurrency (`best_concurrency`) that satisfies the conditions. Instead of guessing at fixed concurrency levels, threshold mode searches automatically.

## Define the SLA

First, define the SLA in concrete numbers. For example, a typical interactive-SLA requirement is:

- **TTFT ≤ 200 ms** (first token responds quickly)
- **TPOT ≤ 100 ms** (streaming stays smooth)

These become your threshold conditions.

<div class="tip">

**tip**：

You can also add an **output-throughput floor** (`--output-threshold`), so a level only counts as passing when throughput stays above a minimum. See [perf command](/en/docs/cli/perf/).

</div>

## CLI Command and Options

Set the thresholds and the search upper limit:

```bash
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --mode threshold \
  --ttft-threshold-ms 200 --tpot-threshold-ms 100 \
  --max-concurrency-search 1024
```

| Option | Meaning |
| --- | --- |
| `--mode threshold` | Enable threshold probing |
| `--ttft-threshold-ms 200` | Fail a level if TTFT mean exceeds 200 ms |
| `--tpot-threshold-ms 100` | Fail a level if TPOT mean exceeds 100 ms |
| `--max-concurrency-search 1024` | Ceiling for the search |

## Probing Strategy

1. Stress-test starting from **1 concurrency** and increasing by **powers of 2** (1, 2, 4, 8, …).
2. After finding the **first point that fails the threshold**, **bisect** within the adjacent interval `(lo, hi]`.
3. Output the **metrics for each tested concurrency** along with `best_concurrency`.

```console
# Hypothetical probe output
Concurrency  1  : TTFT 45ms / TPOT 18ms  -> OK
Concurrency  2  : TTFT 58ms / TPOT 22ms  -> OK
Concurrency  4  : TTFT 90ms / TPOT 41ms  -> OK
Concurrency  8  : TTFT 155ms/ TPOT 78ms  -> OK
Concurrency 16  : TTFT 312ms/ TPOT 160ms -> FAIL
-> bisect within (8, 16] ...
Concurrency 12  : TTFT 210ms/ TPOT 105ms -> FAIL
Concurrency 10  : TTFT 198ms/ TPOT 96ms  -> OK
best_concurrency = 10
```

Here, 10 is the maximum concurrency that still satisfies both thresholds.

## Reading the Results

- **`best_concurrency`** is the maximum concurrency that satisfies **all** threshold conditions.
- If it **still satisfies at the search upper limit**, the system meets the target even at that ceiling — consider raising the cap to probe further.
- You can adjust the **evaluation statistic** (`--ttft-statistic p99`, etc.) to fit different business criteria. For example, a strict SLA might judge on `p99` instead of `mean`.

| Statistic | When to use |
| --- | --- |
| `mean` | Typical / average behavior |
| `median` | Robust to outliers |
| `p99` | Worst-case (tail) latency, for strict SLAs |

## Web UI

On the **Performance Testing → Create Task** page:

1. Choose **Threshold Mode**.
2. Set the model and service address (Provider).
3. Enter the thresholds — TTFT ≤ 200 ms and TPOT ≤ 100 ms — plus the evaluation statistic and the search upper limit.
4. Preview the command and start. The run automatically reports `best_concurrency`.

<div class="tip">

**tip**：

Threshold mode is efficient — it doubles up to the first failure and then bisects, so the number of actual stress-test runs stays small even with a large search cap.

</div>

## FAQ

**How large should the search cap be?**
Estimate from the scale your business can tolerate; if unknown, start around 512–1024. A larger cap usually means a longer probe.

**Why is `best_concurrency` 1?**
The service already fails the threshold at a single concurrency (for example, a single request itself exceeds TTFT/TPOT). Investigate service performance first.

## Related

- [Performance](/en/docs/performance/) — the two modes explained
- [perf command](/en/docs/cli/perf/) — threshold-mode specific options
- [Concurrency Testing](/en/docs/performance/concurrency/) — fixed-level load testing
