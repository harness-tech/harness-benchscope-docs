# Tutorial: Concurrency Testing

This tutorial demonstrates how to run a **concurrency test** against a deployed OpenAI-compatible inference service, and how to interpret the results. Concurrency testing answers: *how does throughput and latency change as load increases?*

## Prerequisites

- **benchscope** is installed — see [Quick Start](../get-started/quickstart.md).
- A **usable inference service** is available — for example vLLM / SGLang at `http://127.0.0.1:8000`.

## Method 1: Web UI

1. Go to **Performance Testing → Create Task**.
2. Configure the **model** and **service address** under test (Provider).
3. Select **Concurrency Mode** and fill in the concurrency levels and request parameters.
4. After completing the three-step form (conditions → parameters → command preview), **preview the command** and start.
5. While it runs, watch the **table / curves / progress**, and export the artifacts when it finishes.

![Create a performance task](/images/benchscope-performance_create.png)

## Method 2: CLI

The same test can be run directly from the terminal:

```bash
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024
```

What this does:

| Option | Effect |
| --- | --- |
| `--model Qwen2.5-7B` | The model under test |
| `--base-url http://127.0.0.1:8000` | The inference service to hit |
| `--concurrency 8` | Stress with 8 concurrent workers |
| `--num-prompts 100` | 100 requests total |
| `--input-len 1024` | 1024 input tokens per request |
| `--output-len 1024` | 1024 output tokens per request |

Run several concurrency levels (for example 1, 4, 8, 16) and compare the metrics to see how the service scales.

## Interpreting the Results

Observe the output metrics:

- **Throughput** (`output_mean`) — the higher the better; it is the primary capacity indicator.
- **TTFT / TPOT / ITL** — latencies; the lower the better. TTFT affects perceived responsiveness, while TPOT / ITL affect streaming fluency.

Pay attention to the **gap between measured values and the expected SLA**, and adjust the concurrency or the service configuration accordingly. Typical observations:

- Throughput rises with concurrency until the service saturates, then plateaus or drops.
- Latencies (TTFT / TPOT) tend to rise as concurrency grows — find the point where the trade-off is acceptable.

```console
$ benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
    --concurrency 8 --num-prompts 100
# ... after the run ...
successful_requests: 100
failed_requests:     0
benchmark_duration:  48.6 s
output_mean:         172.4 tok/s
total_mean:          344.8 tok/s
ttft_mean:           82.1 ms
tpot_mean:           18.3 ms
itl_mean:            16.9 ms
```

## Related

- [Performance Testing](../core/performance.md) — the two modes explained
- [Threshold Testing](perf-threshold.md) — when you have an SLA, find `best_concurrency`
- [CLI Reference](../get-started/cli.md) — full `benchscope perf` reference
- [Datas](../core/datas.md) — records, export, and import
