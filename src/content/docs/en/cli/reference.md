---
title: "CLI Reference"
---

# CLI Reference

`benchscope` provides three sub-commands:

| Sub-command | Purpose |
| --- | --- |
| `serve` | Start the Web service |
| `perf` | Performance testing (stress test) |
| `eval` | Accuracy evaluation |

When you pass **no arguments**, or the *first* argument is an option (for example `--port`), the CLI falls back to the backward-compatible **“start service”** behaviour — equivalent to running `benchscope serve`.

<div class="tip">

**tip**：

The examples on this page use short model names such as `Qwen2.5-7B`; replace them with whatever model your target service exposes.

</div>

## Start Service (`serve`)

```bash
benchscope serve [--host HOST] [--port PORT] [--no-browser] [--debug]
```

| Argument | Default | Description |
| --- | --- | --- |
| `--host` | `0.0.0.0` | Listening address |
| `--port` | `8080` | Listening port |
| `--no-browser` | off | Do not automatically open the browser |
| `--debug` | off | Enable debug logging |

Example:

```bash
benchscope serve --host 127.0.0.1 --port 9090 --no-browser
```

## Performance Testing (`perf`)

```bash
benchscope perf --model MODEL [options]
```

Runs a single stress test with the self-developed engine against an OpenAI-compatible inference service, outputting throughput and latency metrics. Two modes are available:

- `--mode concurrency` (**default**): runs a single concurrency test once.
- `--mode threshold`: starts from 1 concurrency, increases by powers of 2 plus bisection, to find the maximum concurrency that satisfies the thresholds (`best_concurrency`).

### Examples

```bash
# Concurrency mode: fixed concurrency 8, 100 requests per concurrency, 1024 input/output tokens
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024

# Threshold mode: TTFT <= 200ms and TPOT <= 100ms, search for max concurrency (cap 1024)
benchscope perf --model Qwen2.5-7B --mode threshold \
  --ttft-threshold-ms 200 --tpot-threshold-ms 100 --max-concurrency-search 1024
```

### Main arguments

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--engine` | str | `benchscope` | Engine id (default: the self-developed engine) |
| `--model` | str | **required** | Name of the model under test |
| `--base-url` | str | `http://127.0.0.1:8000` | Address of the inference service under test |
| `--api-key` | str | empty | API key of the service under test (optional) |
| `--backend` | str | `openai-chat` | Protocol: `openai-chat` / `openai` |
| `--endpoint` | str | `/v1/chat/completions` | Request API path |
| `--mode` | str | `concurrency` | Test mode: `concurrency` / `threshold` |
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

### Arguments specific to threshold mode

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--ttft-threshold-ms` | float | `0.0` | TTFT threshold (ms); `0` = do not evaluate |
| `--tpot-threshold-ms` | float | `100.0` | TPOT threshold (ms); `0` = do not evaluate |
| `--output-threshold` | float | `0.0` | Output throughput threshold (tok/s); lower values are not satisfied, `0` = do not evaluate |
| `--ttft-statistic` | str | `mean` | TTFT evaluation statistic: `mean` / `median` / `p99` |
| `--tpot-statistic` | str | `mean` | TPOT evaluation statistic: `mean` / `median` / `p99` |
| `--max-concurrency-search` | int | `4096` | Threshold search upper limit; if still satisfied, this becomes the best concurrency |
| `--max-requests` | int | `4096` | Force-finish when concurrency exceeds this limit during threshold probing |

### Output metrics

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

### Threshold probing strategy

1. Start from **1 concurrency** and increase by **powers of 2** (1, 2, 4, 8, …), stress-testing step by step.
2. If 1 concurrency already fails the threshold → the best concurrency is 1, and probing ends.
3. When `hi = 2^k` fails (while `lo = 2^(k-1)` satisfies) → bisect within `(lo, hi]` until two adjacent values remain; `lo` is the maximum concurrency satisfying the threshold.
4. If the search upper limit is still satisfied → the upper-limit concurrency is the best (normal termination).

Metrics for every tested concurrency are printed along with `best_concurrency`.

### Artifacts

The run writes `run.json` (containing `task_id` / `kind: perf` / `summary`) plus terminal logs `perf_<run_id>_*.log` into `perfs_dir` / `logs_dir`. Package these as a **flat zip** (containing `run.json` + logs + optional `metrics.json`) and import them in the Web UI under **Datas → Perfs → Import Backup**.

## Accuracy Evaluation (`eval`)

```bash
benchscope eval --model MODEL --dataset DATASET [options]
```

Runs an accuracy evaluation (Serving / Native / Mock) and outputs metrics such as `accuracy` / `pass_rate`. The dataset can be a **built-in id** (`mmlu` / `gsm8k` …) or a **local JSONL file path**.

### Examples

```bash
# Serving mode: evaluate an OpenAI-compatible deployed pipeline
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200

# Native mode: evaluate local transformers weights / HF id offline
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100

# Mock integration testing: verify the pipeline without a real service
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

### Main arguments

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--engine` | str | `benchscope` | Accuracy engine id (`benchscope`=serving / `native-hf`=native / `mock`=integration) |
| `--mode` | str | `serving` | Evaluation mode: `serving` (pipeline) / `native` (local weights) |
| `--model` | str | **required** | Model under test (Native accepts a weights path or an HF id) |
| `--lora-path` | str | empty | Path to a LoRA fine-tuned adapter (optional) |
| `--lora-name` | str | empty | Server-side registered name of the LoRA model (Serving request-side model, optional) |
| `--dataset` | str | **required** | Built-in dataset id (`mmlu` / `gsm8k` …) or local JSONL path |
| `--base-url` | str | empty | Service address (Serving; defaults to the global Provider config when omitted) |
| `--api-key` | str | empty | API key of the service under test (optional) |
| `--limit` | int | `0` | Sample sampling limit (0 = all samples) |
| `--seed` | int | `1234` | Global random seed (sampling and generation, fixed for reproducibility) |
| `--temperature` | float | `0.0` | Sampling temperature |
| `--top-p` | float | `1.0` | Nucleus sampling probability |
| `--max-tokens` | int | `512` | Maximum output tokens per sample |
| `--concurrency` | int | `4` | Number of concurrent inferences |
| `--judge-model` | str | empty | MT-Bench judge model (used by the judge dataset) |
| `--mock-correct-rate` | float | `0.7` | Mock engine correctness rate (0–1) |
| `--name` | str | empty | Task name (optional) |
| `--use-mock-env` | flag | off | Mock environment marker (for integration testing) |

### Output metrics

| Metric | Meaning |
| --- | --- |
| `accuracy` (%) | Overall correctness |
| `pass_rate` (%) | Pass rate |
| `total_samples` / `correct_samples` | Total samples / correct count |
| `wrong_samples` / `invalid_samples` | Wrong count / invalid count |
| `dataset_metrics` | Dataset-specific metrics (`exact_match` / `math_accuracy` / `pass_at_1` / `compile_rate` / `mt_bench_score`, etc.) |
| `tokens.total_tokens` | Total tokens consumed |
| `benchmark` | Baseline comparison (`baseline_used.name` / `diff_pp` / `grade` / `conclusion`) |
| `conclusion` | Conclusion (pass / accuracy drop / flat / better than baseline, etc.) |

### Artifacts

Artifacts are written to `evals/eval-<MMDDhhmmss>/` and contain:

- `task.json` — the task main table, aligned with the Web accuracy task structure
- `result.json` — the accuracy result, including metrics / baseline / conclusion
- `samples.jsonl` — per-sample traceability

A terminal log `logs/eval_<task_id>_<time>.log` is also written. View or package-import these under **Datas → Evals** in the Web UI.

## See Also

- Full argument sources: `docs/options/benchscope-perf-cli-options.md` and `docs/options/benchscope-eval-cli-options.md` in the repository
- Tutorials: [Concurrency Testing](/en/docs/performance/concurrency/), [Threshold Testing](/en/docs/performance/threshold/), [Accuracy Evaluation](/en/docs/accuracy/guide/)
- [Quick Start](/en/docs/quickstart/) — installing and launching
