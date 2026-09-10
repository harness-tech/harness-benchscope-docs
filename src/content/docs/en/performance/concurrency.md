---
title: "Concurrency Testing"
description: "Step-by-step guide to concurrency stress testing: verify the service, create a task via the Web UI or CLI, compare concurrency levels, and interpret the results."
---

# Concurrency Testing

This section shows how to run a **concurrency stress test** against a deployed OpenAI-compatible inference service: observe how throughput and latency change under different concurrency loads, and find the **best operating range**.

## Prerequisites

- benchscope is installed (see [Quick Start](/en/docs/quickstart/));
- A running inference service (e.g. vLLM / SGLang) is available at `http://127.0.0.1:8000`.

## Procedure

### Step 1: Confirm the service is reachable

Before starting, quickly confirm the service is reachable with curl:

```bash
curl http://127.0.0.1:8000/v1/models
```

<div class="tip">

**Tip:**

If it returns the model list, the service is available.

</div>

### Step 2: Create the stress-test task

**Via the Web UI**

1. Go to **Performance** → **Create Task**;
2. Configure the **model under test** and the **service address** (Provider);
3. Select **Concurrency** and fill in the concurrency levels and request parameters;
4. After completing the three-step form, **preview the command** and **start**;
5. While running, view the **table / curves / progress**; after it finishes, **export the artifacts**.

![BenchScope performance testing create task](/images/benchscope-performance_create.png)

**Via the CLI**

The same stress test can be run directly from the command line:

```bash
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024
```

Parameter reference:

| Parameter | Description |
| --- | --- |
| `--model` | The model under test |
| `--base-url` | Service address (default `http://127.0.0.1:8000`) |
| `--concurrency` | Number of concurrent workers (8 in this example) |
| `--num-prompts` | Total number of requests (100) |
| `--input-len` / `--output-len` | Input / output token counts (1024 each) |

### Step 3: Compare multiple concurrency levels

To observe the load curve, run the benchmark at several concurrency levels (e.g. 1 / 2 / 4 / 8 / 16), recording and comparing the metrics level by level:

```bash
for c in 1 2 4 8 16; do
  benchscope perf --model Qwen2.5-7B --concurrency $c \
    --num-prompts 100 --input-len 1024 --output-len 1024 \
    --name "concurrency-$c"
done
```

### Step 4: Interpret the results

Each concurrency point outputs a set of metrics (see [Performance Core Metrics](/en/docs/performance/metrics/) for the complete reference):

- **Latency**: `ttft_mean` / `tpot_mean` / `itl_mean` (plus `median` and `p99` statistics) — **lower is better**; TTFT affects first-token response, while TPOT / ITL affect streaming smoothness;
- **Throughput**: `output_mean` (output throughput) / `peakoutput_mean` (peak output throughput) / `total_mean` (total token throughput) / `req_per_s` (request throughput) — **higher is better**;
- **Derived value**: `single_user` = `1000 / TPOT(mean)`, approximating the single-user generation rate;
- **Request statistics**: `successful_requests` / `failed_requests` / `benchmark_duration`, etc.

```console
Successful requests: 100
Failed requests:     0
Benchmark duration:  45.23s
Output throughput:   112.4 tokens/s (output_mean)
Total throughput:    335.6 tokens/s (total_mean)
TTFT (mean):         92.5 ms
TPOT (mean):         34.2 ms
ITL  (mean):         33.9 ms
```

Focus on the gap between the measured values and the **expected SLA**, and adjust the concurrency or service configuration accordingly.

A typical pattern of concurrency growth: at low concurrency, throughput rises with concurrency; it saturates beyond a certain level; then queuing and contention start to degrade TTFT / TPOT — use this pattern to identify the system's **best operating range**.

## FAQ

**Question: Does higher concurrency always mean higher throughput?**
Not necessarily. Raising concurrency first lifts throughput, but once it exceeds the service's capacity it drops or latency degrades due to queuing and GPU memory / compute contention.

**Question: How do I watch the real-time curves in the Web UI?**
While a concurrency stress test is running, the table and curves refresh automatically; within a single concurrency point, the curve scrolls continuously so you can observe the fluctuation.

## Related Documentation

- [Performance Testing](/en/docs/performance/) — in-depth guide to both modes
- [Performance Core Metrics](/en/docs/performance/metrics/) — complete metric reference
- [perf Command](/en/docs/cli/perf/) — full parameters of `perf`
- [Threshold Testing](/en/docs/performance/threshold/) — automatically finding the optimal concurrency