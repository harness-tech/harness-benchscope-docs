---
title: "Tutorial: Threshold Testing"
---

# Tutorial: Threshold Testing

When the **business SLA** is known, use *threshold probing* to find the maximum concurrency (`best_concurrency`) that satisfies the conditions. Instead of guessing at fixed concurrency levels, threshold mode searches automatically.

## Set Business Metrics

First, define the SLA in concrete numbers. For example, a typical interactive-SLA requirement is:

- **TTFT ≤ 200 ms** (first token responds quickly)
- **TPOT ≤ 100 ms** (streaming stays smooth)

These become your thresholds.

## Web UI

On the **Performance Testing → Create Task** page:

1. Choose **Threshold Mode**.
2. Set the model and service address (Provider).
3. Enter the thresholds — TTFT ≤ 200 ms and TPOT ≤ 100 ms — and the search upper limit.
4. Preview the command and start.

## CLI

The equivalent command:

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

## Probing Strategy Recap

1. Stress-test starting from **1 concurrency** and increasing by **powers of 2** (1, 2, 4, 8, …).
2. After finding the **first point that fails the threshold**, **bisect** within the adjacent interval `(lo, hi]`.
3. Output the **metrics for each tested concurrency** along with `best_concurrency`.

```console
# Hypothetical probe output
concurrency=1    ttft=87ms  tpot=19ms  ✓
concurrency=2    ttft=95ms  tpot=21ms  ✓
concurrency=4    ttft=118ms tpot=27ms  ✓
concurrency=8    ttft=161ms tpot=48ms  ✓
concurrency=16   ttft=243ms tpot=89ms  ✗
# bisecting (8, 16]
concurrency=12   ttft=201ms tpot=76ms  ✗
concurrency=10   ttft=188ms tpot=64ms  ✓
best_concurrency = 10
```

Here 10 is the maximum concurrency that still satisfies both thresholds.

## Interpreting the Results

- **`best_concurrency`** is the maximum concurrency that satisfies **all** threshold conditions.
- If it **still satisfies at the search upper limit**, the system meets the target even at that ceiling — consider raising the cap if you want to probe further.
- You can adjust the **evaluation statistic** (`--ttft-statistic p99`, etc.) to fit different business criteria. For example, a strict SLA might judge on `p99` instead of `mean`.

| Statistic | When to use |
| --- | --- |
| `mean` | Typical / average behavior |
| `median` | Robust to outliers |
| `p99` | Worst-case (tail) latency, for strict SLAs |

<div class="tip">

**tip**：

Threshold mode is efficient — it doubles up to the first failure and then bisects, so the number of actual stress-test runs stays small even with a large search cap.

</div>

## Related

- [Performance Testing](/en/docs/performance/) — the two modes explained
- [Concurrency Testing](/en/docs/performance/concurrency/) — fixed-level load testing
- [CLI Reference](/en/docs/cli/reference/) — full `benchscope perf` reference
