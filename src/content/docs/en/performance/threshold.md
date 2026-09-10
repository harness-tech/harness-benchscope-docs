---
title: "Threshold Testing"
description: "How threshold testing works: define SLA thresholds and a search upper limit, then automatically find the maximum concurrency (best_concurrency) that satisfies all threshold conditions."
---

# Threshold Testing

When the **business SLA is known**, use threshold probing to automatically find the **maximum concurrency** (`best_concurrency`) that satisfies the conditions, answering "how much concurrency can this configuration sustain without exceeding the SLA". Unlike manually guessing fixed concurrency levels, threshold mode performs the search automatically.

## Defining the SLA

First, turn the SLA into concrete numbers. For example, typical requirements for an interactive application:

- **TTFT ≤ 200ms** (the first token responds promptly);
- **TPOT ≤ 100ms** (streaming output stays smooth).

These two are your threshold conditions.

<div class="tip">

**Tip:**

The threshold conditions can also include an **output throughput floor** (`--output-threshold`), requiring throughput not to fall below a certain value to count as passing. See the [perf Command](/en/docs/cli/perf/).

</div>

## CLI Command and Parameters

In threshold mode, specify the thresholds and the search upper limit to start:

```bash
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --mode threshold \
  --ttft-threshold-ms 200 --tpot-threshold-ms 100 \
  --max-concurrency-search 1024
```

| Parameter | Meaning |
| --- | --- |
| `--mode threshold` | Enable threshold probing |
| `--ttft-threshold-ms 200` | If the TTFT mean exceeds 200ms, this level is judged as not meeting the target |
| `--tpot-threshold-ms 100` | If the TPOT mean exceeds 100ms, this level is judged as not meeting the target |
| `--max-concurrency-search 1024` | Search upper limit (concurrency ceiling) |

## Probing Strategy

1. Start stress-testing from **1 concurrency** and increase by **powers of 2** (1, 2, 4, 8, …);
2. After finding the **first point that does not satisfy the threshold**, **bisect** within the adjacent interval;
3. Output the metrics of **each tested concurrency** along with `best_concurrency`.

```console
# Illustration of the probing process
Concurrency  1  : TTFT 45ms / TPOT 18ms  -> OK
Concurrency  2  : TTFT 58ms / TPOT 22ms  -> OK
Concurrency  4  : TTFT 90ms / TPOT 41ms  -> OK
Concurrency  8  : TTFT 155ms/ TPOT 78ms  -> OK
Concurrency 16  : TTFT 312ms/ TPOT 160ms -> FAIL
-> Bisecting interval (8, 16] ...
Concurrency 12  : TTFT 210ms/ TPOT 105ms -> FAIL
Concurrency 10  : TTFT 198ms/ TPOT 96ms  -> OK
best_concurrency = 10
```

In this example, 10 is the maximum concurrency that satisfies both thresholds at the same time.

## Interpreting the Results

- **`best_concurrency`** is the maximum concurrency that satisfies **all threshold conditions** (see [Performance Core Metrics](/en/docs/performance/metrics/) for the metric reference);
- If it is still satisfied at the **search upper limit**, the system still meets the target under that ceiling (you can raise the search upper limit to probe further);
- The evaluation statistic can be adjusted (`--ttft-statistic p99`, etc.) to fit **different business criteria** — for example, a strict SLA can switch from `mean` to `p99`.

<div class="info">

**Info:**

In threshold mode, each tested concurrency also outputs the full metric group (mean / median / p99 of TTFT / TPOT / ITL + throughput + request statistics); the run results list a "concurrency → output / total / ttft / tpot" comparison, making it easy to review the search process.

</div>

| Evaluation Statistic | Meaning | Best For |
| --- | --- | --- |
| `mean` | Mean | General business criteria |
| `median` | Median | Reducing the influence of extreme values |
| `p99` | 99th percentile | Businesses sensitive to tail latency (stricter) |

## Web UI

Create a threshold-mode stress-test task on the **Performance** page: select Threshold mode, fill in the TTFT / TPOT thresholds, the evaluation statistic, and the search upper limit, then preview the command and start; the run results automatically give `best_concurrency`.

<div class="tip">

**Tip:**

Threshold mode searches efficiently — it doubles until the first failing point, then bisects to converge, so even with a large search upper limit, the number of stress-test rounds stays small.

</div>

## FAQ

**Question: How large should the search upper limit be?**
Estimate it from the scale your business can accept; if unknown, start with 512–1024; the larger the upper limit, the longer the probe usually takes.

**Question: Why is `best_concurrency` 1?**
It means the threshold was already not satisfied at 1 concurrency (for example, a single request itself exceeds TTFT/TPOT); you need to investigate service performance first.

## Related Documentation

- [Performance Testing](/en/docs/performance/) — threshold mode principles and decision criteria
- [Performance Core Metrics](/en/docs/performance/metrics/) — complete metric reference (including best_concurrency)
- [perf Command](/en/docs/cli/perf/) — parameters exclusive to threshold mode
- [Concurrency Testing](/en/docs/performance/concurrency/) — manual level-by-level stress testing