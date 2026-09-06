---
title: "Concurrency Testing"
---

# Concurrency Testing

This section shows how to run a **concurrency test** against a deployed OpenAI-compatible inference service, and how to interpret the results. Concurrency testing answers: *how does throughput and latency change as load increases?* Use it to find the service's **best operating range**.

## Prerequisites

- **benchscope** is installed — see [Quick Start](/en/docs/quickstart/).
- A **usable inference service** is available — for example vLLM / SGLang at `http://127.0.0.1:8000`.

## Procedure

### Step 1: Confirm the service is reachable

```bash
curl http://127.0.0.1:8000/v1/models
```

<div class="tip">

**tip**：

If it returns the model list, the service is ready.

</div>

### Step 2: Create the test

**Via the Web UI**

1. Go to **Performance Testing → Create Task**.
2. Configure the **model** and **service address** under test (Provider).
3. Select **Concurrency Mode** and fill in the concurrency levels and request parameters.
4. After completing the three-step form (conditions → parameters → command preview), **preview the command** and start.
5. While it runs, watch the **table / curves / progress**, and export the artifacts when it finishes.

![Create a performance task](/images/benchscope-performance_create.png)

**Via the CLI**

The same test can be run directly from the terminal:

```bash
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024
```

Option reference:

| Option | Effect |
| --- | --- |
| `--model Qwen2.5-7B` | The model under test |
| `--base-url http://127.0.0.1:8000` | The inference service to hit |
| `--concurrency 8` | Stress with 8 concurrent workers |
| `--num-prompts 100` | 100 requests total |
| `--input-len 1024` | 1024 input tokens per request |
| `--output-len 1024` | 1024 output tokens per request |

### Step 3: Compare multiple concurrency levels

To observe the load curve, run several concurrency levels (for example 1, 2, 4, 8, 16) and compare the recorded metrics:

```bash
for c in 1 2 4 8 16; do
  benchscope perf --model Qwen2.5-7B --concurrency $c \
    --num-prompts 100 --input-len 1024 --output-len 1024 \
    --name "concurrency-$c"
done
```

### Step 4: Read the results

Observe the output metrics:

- **Throughput** (`output_mean` / `total_mean`) — the higher the better; it is the primary capacity indicator.
- **TTFT / TPOT / ITL** — latencies, the lower the better. TTFT affects perceived responsiveness, while TPOT / ITL affect streaming fluency.

Pay attention to the **gap between measured values and the expected SLA**, and adjust the concurrency or service configuration accordingly.

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

A typical pattern: throughput rises with concurrency until the service saturates; beyond that point, queuing and resource contention push TTFT / TPOT upward. This is how you locate the service's **best operating range**.

## FAQ

**Does higher concurrency always mean higher throughput?**
No. Concurrency first raises throughput, but past the service's capacity it drops (or latency degrades) because of queuing and contention on memory / compute.

**How do I watch the curves live in the UI?**
While a run is in progress, the table and curves refresh automatically; within a single concurrency point you can scroll continuously to observe fluctuation.

## Related

- [Performance](/en/docs/performance/) — the two modes explained
- [perf command](/en/docs/cli/perf/) — full `benchscope perf` reference
- [Threshold Testing](/en/docs/performance/threshold/) — find `best_concurrency` automatically
