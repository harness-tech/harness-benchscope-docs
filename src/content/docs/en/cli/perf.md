---
title: "perf"
description: "The benchscope perf command: stress testing in concurrency and threshold modes, with examples, parameters, probing strategy, and output metrics."
---

# perf

Runs a single stress test with the self-developed engine against an OpenAI-compatible inference service, outputting throughput and latency metrics.

```bash
benchscope perf --model MODEL [options]
```

**Mode (`--mode`)** has two values:

- `concurrency` (**default**): runs one stress test at the specified concurrency;
- `threshold`: starts from concurrency 1, increases by powers of 2, then refines with bisection, to find the maximum concurrency that satisfies the thresholds (`best_concurrency`).

## Common Examples

```console
# Concurrency mode: fixed concurrency 8, 100 requests per concurrency, 1024 input/output tokens each
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024

# Threshold mode: TTFT ≤ 200ms and TPOT ≤ 100ms, search for the maximum concurrency (upper limit 1024)
benchscope perf --model Qwen2.5-7B --mode threshold \
  --ttft-threshold-ms 200 --tpot-threshold-ms 100 --max-concurrency-search 1024
```

## Main Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `--engine` | str | `benchscope` | Engine id (default: the self-developed engine `benchscope`) |
| `--model` | str | **required** | Name of the model under test |
| `--base-url` | str | `http://127.0.0.1:8000` | Address of the inference service under test |
| `--api-key` | str | empty | API Key of the service under test (optional) |
| `--backend` | str | `openai-chat` | Interface protocol: `openai-chat` / `openai` |
| `--endpoint` | str | `/v1/chat/completions` | Request interface path |
| `--mode` | str | `concurrency` | Stress-test mode: `concurrency` / `threshold` |

**Request Scale and Load Parameters**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `--concurrency` | int | `1` | Number of concurrent workers (concurrency mode) |
| `--num-prompts` | int | `0` | Total number of requests (0 = follows the concurrency, one request per worker) |
| `--input-len` | int | `1024` | Number of input tokens |
| `--output-len` | int | `1024` | Number of output tokens |
| `--request-rate` | str | `inf` | Request rate (req/s; `inf` means no rate limiting) |
| `--num-warmups` | int | `0` | Number of warm-up requests (not counted in metrics) |
| `--chars-per-token` | float | `4.0` | Character / token approximation ratio (used to build the input length) |
| `--timeout` | float | `600.0` | Per-request timeout (seconds); a timeout counts as a failure |
| `--temperature` | float | `0.0` | Sampling temperature (recommended to fix at 0 for stress testing) |
| `--seed` | int | `0` | Random seed (0 = not fixed) |

## Threshold-Mode-Exclusive Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `--ttft-threshold-ms` | float | `0.0` | TTFT threshold (ms); `0` = do not evaluate |
| `--tpot-threshold-ms` | float | `100.0` | TPOT threshold (ms); `0` = do not evaluate |
| `--output-threshold` | float | `0.0` | Output throughput threshold (tok/s); judged as not satisfied when **below** this value; `0` = do not evaluate |
| `--ttft-statistic` | str | `mean` | Statistic for the TTFT threshold decision: `mean` / `median` / `p99` |
| `--tpot-statistic` | str | `mean` | Statistic for the TPOT threshold decision: `mean` / `median` / `p99` |
| `--max-concurrency-search` | int | `4096` | Upper limit of the threshold search: if the threshold is still satisfied at the limit, the limit becomes the best concurrency |
| `--max-requests` | int | `4096` | If the concurrency exceeds this limit during threshold probing, force termination (Finish) |

## Threshold Probing Strategy

1. Start from **1 concurrency** and increase by **powers of 2** (1, 2, 4, 8, …), stress-testing in steps;
2. If 1 concurrency already does not satisfy the threshold → the best concurrency is 1, and it ends;
3. If execution reaches `hi = 2^k` and it is not satisfied (`lo = 2^(k-1)` is satisfied) → **bisect** within `(lo, hi]` until two adjacent values remain; `lo` is the maximum concurrency satisfying the threshold;
4. If the search upper limit is reached and still satisfied → the upper limit is the best concurrency (normal termination).

Outputs the metrics of each tested concurrency (throughput / TTFT / TPOT / ITL) along with `best_concurrency`.

## Output Metrics

Each concurrency point outputs a set of metrics (see [Performance Core Metrics](/en/docs/performance/metrics/) for the complete reference):

| Metric | Meaning |
| --- | --- |
| `successful_requests` | Number of successful requests |
| `failed_requests` | Number of failed requests |
| `benchmark_duration` | Wall-clock duration of the stress test |
| `output_mean` (tok/s) | Output throughput (mean) |
| `peakoutput_mean` (tok/s) | Peak output throughput (provided under vLLM semantics; recorded as N/A when the engine does not support it) |
| `total_mean` (tok/s) | Total throughput (mean) |
| `req_per_s` (req/s) | Request throughput (requests completed per second) |
| `single_user` (tok/s) | Single-user throughput (derived as `1000 / TPOT(mean)`) |
| `ttft_mean` / `ttft_median` / `ttft_p99` (ms) | First-token latency (mean / median / 99th percentile) |
| `tpot_mean` / `tpot_median` / `tpot_p99` (ms) | Per-output-token latency (mean / median / 99th percentile) |
| `itl_mean` / `itl_median` / `itl_p99` (ms) | Token interval latency (mean / median / 99th percentile) |

Threshold mode additionally outputs `best_concurrency` (the maximum concurrency satisfying all threshold conditions).

## Run Example

```console
# Example output of a typical concurrency stress-test run
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

## Artifacts and Import

- Writes `run.json` (containing `task_id` / `kind: perf` / `summary`) + logs `perf_<run_id>_*.log` (written to `perfs_dir` / `logs_dir`).
- Packaged as a **flat zip** (`run.json` + terminal logs, with files placed directly at the zip root), importable in the Web UI under **Datas → Perfs → Import Backup**.

<div class="tip">

**Tip:**

The `run.json` generated by the CLI (containing the full summary) can be packaged and imported in the Web UI under **Datas → Perfs**; it is fully compatible with the artifacts of performance tasks created in the Web UI.

</div>

## Related Documentation

- [CLI Overview](/en/docs/cli/) — subcommand overview and quick start
- [serve Command](/en/docs/cli/serve/) — start the Web service
- [eval Command](/en/docs/cli/eval/) — accuracy evaluation
- [Performance Testing](/en/docs/performance/) — concurrency stress testing and threshold probing
- [Performance Core Metrics](/en/docs/performance/metrics/) — complete reference for output metrics
- [Accuracy Overview](/en/docs/accuracy/) — three-mode evaluation