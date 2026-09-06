---
title: "perf"
---

# perf

Runs a single stress test with the self-developed engine against an OpenAI-compatible inference service, outputting throughput and latency metrics.

```bash
benchscope perf --model MODEL [options]
```

Two modes are available via `--mode`:

- `concurrency` (**default**): runs a single concurrency test once.
- `threshold`: starts from 1 concurrency, increases by powers of 2 plus bisection, to find the maximum concurrency that satisfies the thresholds (`best_concurrency`).

## Examples

```console
# Concurrency mode: fixed concurrency 8, 100 requests per concurrency, 1024 input/output tokens
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024

# Threshold mode: TTFT <= 200ms and TPOT <= 100ms, search for max concurrency (cap 1024)
benchscope perf --model Qwen2.5-7B --mode threshold \
  --ttft-threshold-ms 200 --tpot-threshold-ms 100 --max-concurrency-search 1024
```

## Main arguments

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--engine` | str | `benchscope` | Engine id (default: the self-developed engine) |
| `--model` | str | **required** | Name of the model under test |
| `--base-url` | str | `http://127.0.0.1:8000` | Address of the inference service under test |
| `--api-key` | str | empty | API key of the service under test (optional) |
| `--backend` | str | `openai-chat` | Protocol: `openai-chat` / `openai` |
| `--endpoint` | str | `/v1/chat/completions` | Request API path |
| `--mode` | str | `concurrency` | Test mode: `concurrency` / `threshold` |

**Request scale & load**

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--concurrency` | int | `1` | Concurrency (concurrency mode) |
| `--num-prompts` | int | `0` | Total number of requests (0 = follow concurrency, one request per worker) |
| `--input-len` | int | `1024` | Number of input tokens per request |
| `--output-len` | int | `1024` | Number of output tokens per request |
| `--request-rate` | str | `inf` | Request rate (req/s; `inf` = no rate limit) |
| `--num-warmups` | int | `0` | Warm-up requests (not counted in metrics) |
| `--chars-per-token` | float | `4.0` | Character / token approximation ratio (for building input length) |
| `--timeout` | float | `600.0` | Per-request timeout (s); a timeout counts as a failure |
| `--temperature` | float | `0.0` | Sampling temperature (keep at 0 for benchmarking) |
| `--seed` | int | `0` | Random seed (0 = not fixed) |

## Arguments specific to threshold mode

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--ttft-threshold-ms` | float | `0.0` | TTFT threshold (ms); `0` = do not evaluate |
| `--tpot-threshold-ms` | float | `100.0` | TPOT threshold (ms); `0` = do not evaluate |
| `--output-threshold` | float | `0.0` | Output throughput threshold (tok/s); lower values are not satisfied, `0` = do not evaluate |
| `--ttft-statistic` | str | `mean` | TTFT evaluation statistic: `mean` / `median` / `p99` |
| `--tpot-statistic` | str | `mean` | TPOT evaluation statistic: `mean` / `median` / `p99` |
| `--max-concurrency-search` | int | `4096` | Threshold search upper limit; if still satisfied, this becomes the best concurrency |
| `--max-requests` | int | `4096` | Force-finish when concurrency exceeds this limit during threshold probing |

## Threshold probing strategy

1. Start from **1 concurrency** and increase by **powers of 2** (1, 2, 4, 8, …), stress-testing step by step.
2. If 1 concurrency already fails the threshold → the best concurrency is 1, and probing ends.
3. When `hi = 2^k` fails (while `lo = 2^(k-1)` satisfies) → bisect within `(lo, hi]` until two adjacent values remain; `lo` is the maximum concurrency satisfying the threshold.
4. If the search upper limit is still satisfied → the upper-limit concurrency is the best (normal termination).

Metrics for every tested concurrency are printed along with `best_concurrency`.

## Output metrics

| Metric | Meaning |
| --- | --- |
| `successful_requests` | Number of successful requests |
| `failed_requests` | Number of failed requests |
| `benchmark_duration` | Wall-clock duration of the benchmark |
| `output_mean` (tok/s) | Output throughput (mean) |
| `total_mean` (tok/s) | Total throughput (mean) |
| `ttft_mean` (ms) | First-token latency (mean) |
| `tpot_mean` (ms) | Per-output-token latency (mean) |
| `itl_mean` (ms) | Inter-token latency (mean) |

## Sample run

```console
# A typical concurrency-mode run
$ benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
    --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024
Benchmarking Qwen2.5-7B @ http://127.0.0.1:8000 (mode=concurrency, concurrency=8) ...
100%|████████████████████████████████████| 100/100 [00:45<00:00]
============================ Summary ============================
Successful requests: 100
Failed requests:     0
Benchmark duration:  45.23s
Output throughput:   112.4 tokens/s (output_mean)
Total throughput:    335.6 tokens/s (total_mean)
TTFT (mean):         92.5 ms
TPOT (mean):         34.2 ms
ITL  (mean):         33.9 ms
Saved run.json -> ~/.benchscope/perfs/run_<id>.json
```

## Artifacts

The run writes `run.json` (containing `task_id` / `kind: perf` / `summary`) plus terminal logs `perf_<run_id>_*.log` into `perfs_dir` / `logs_dir`. Package these as a **flat zip** (containing `run.json` + logs + optional `metrics.json`) and import them in the Web UI under **Datas → Perfs → Import Backup**.

<div class="tip">

**tip**：

The `run.json` produced by the CLI (including the full summary) can be packaged and imported directly in the Web UI under **Datas → Perfs**, fully compatible with performance tasks created in the UI.

</div>

## Related

- [CLI Overview](/en/docs/cli/) — sub-command overview and quick start
- [serve](/en/docs/cli/serve/) — start the Web service
- [eval](/en/docs/cli/eval/) — accuracy evaluation
- [Performance Testing](/en/docs/performance/) — Concurrency and Threshold modes
- [Accuracy Testing](/en/docs/accuracy/) — dual-mode evaluation
