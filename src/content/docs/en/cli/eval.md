---
title: "eval"
description: "The benchscope eval command: accuracy evaluation in Serving, Native, and Mock modes, with examples, parameters, and output metrics."
---

# eval

Runs one accuracy evaluation (Serving / Native / Mock), outputting metrics such as accuracy / pass_rate.

```bash
benchscope eval --model MODEL --dataset DATASET [options]
```

The dataset can be passed as a built-in id (`mmlu` / `gsm8k` ...) or a local JSONL path.

## Common Examples

```console
# Serving pipeline evaluation: evaluate a deployed OpenAI-compatible service
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200

# Native evaluation: offline evaluation with local transformers weights / HF id
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100

# Mock integration test: verify the pipeline without a real service
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

## Main Parameters

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `--engine` | str | `benchscope` | Accuracy engine id (`benchscope`=serving / `native-hf`=native / `mock`=integration) |
| `--mode` | str | `serving` | Evaluation mode: `serving` (pipeline) / `native` (local weights) |
| `--model` | str | **required** | Name of the model under test (Native accepts a local weights path or an HF id) |
| `--dataset` | str | **required** | Built-in dataset id (mmlu / gsm8k / ...) or a local JSONL path |

**Service and Model Adaptation**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `--lora-path` | str | empty | Path to the LoRA fine-tuned delta model (adapter) (optional) |
| `--lora-name` | str | empty | Server-side registered name of the LoRA delta model (the model on the Serving request side; optional) |
| `--base-url` | str | empty | Address of the service under test (Serving; defaults to the global Provider config) |
| `--api-key` | str | empty | API Key of the service under test (optional) |

**Sampling and Generation**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `--limit` | int | `0` | Sample cap (0 = full set) |
| `--seed` | int | `1234` | Global random seed (sampling and generation; fixed for reproducibility) |
| `--temperature` | float | `0.0` | Sampling temperature |
| `--top-p` | float | `1.0` | Nucleus sampling probability |
| `--max-tokens` | int | `512` | Maximum output tokens per sample |
| `--concurrency` | int | `4` | Number of concurrent inferences |

**Judging / Integration / Naming**

| Parameter | Type | Default | Description |
| --- | --- | --- | --- |
| `--judge-model` | str | empty | MT-Bench judging model (for the judge dataset) |
| `--mock-correct-rate` | float | `0.7` | Correctness rate of the mock engine (0-1) |
| `--name` | str | empty | Task name (optional) |
| `--use-mock-env` | flag | off | Mock environment marker (for integration testing) |

## Output Metrics

All metrics are output (see [Accuracy Core Metrics](/en/docs/accuracy/metrics/) for the complete reference):

| Metric | Meaning |
| --- | --- |
| `accuracy` (%) | Overall correctness (the primary metric) |
| `pass_rate` (%) | Pass rate (share of valid, parseable samples) |
| `total_samples` / `correct_samples` | Total samples / correct count |
| `wrong_samples` / `invalid_samples` | Wrong count / invalid count |
| `subjects` (%) | Per-subject correctness (grouped by the dataset's `subject` field) |
| `error_tag_summary` | Error-cause tag distribution (attribution of wrong samples) |
| `dataset_metrics` | Grader-specific metrics (math: `exact_match` / `math_accuracy` / `answer_parse_rate`; code: `pass_at_1` / `compile_rate` / `case_pass_rate`; judge: `mt_bench_score` / `first_turn_score` / `second_turn_score` / `dim_helpfulness` / `dim_truthfulness` / `dim_harmlessness`) |
| `tokens.total_tokens` | Total tokens consumed (Serving mode; null in Native mode) |
| `benchmark` | Baseline benchmarking (`baseline_used` / `diff_pp` / `grade` / `conclusion`) |
| `conclusion` | Conclusion (pass / accuracy drop / anomaly) |

## Run Example

```console
# Example output of a typical Serving evaluation run
$ benchscope eval --mode serving --model Qwen2.5-7B \
    --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
Evaluating Qwen2.5-7B on gsm8k (mode=serving, limit=200) ...
100%|████████████████████████████████████| 200/200 [00:50<00:00]
===================== Accuracy Summary =====================
accuracy:            87.5%
pass_rate:           92.0%
total_samples:       200
correct_samples:     175
wrong_samples:       25
invalid_samples:     0
dataset_metrics:     { "math_accuracy": 87.5 }
tokens.total_tokens: 51200
conclusion:          pass
Saved -> ~/.benchscope/evals/eval-<time>/ (task.json / result.json / samples.jsonl)
```

## Artifacts and Import

Artifacts are written to `evals/eval-<MMDDhhmmss>/`:

- `task.json` — the main task file, aligned with the Web accuracy task structure;
- `result.json` — the accuracy result, including metrics / benchmark / conclusion;
- `samples.jsonl` — per-sample traceability.

It also writes a terminal log `logs/eval_<task_id>_<time>.log`. All artifacts can be viewed and managed on the Web UI's **Accuracy page** (task list + details + sample viewer).

## Related Documentation

- [CLI Overview](/en/docs/cli/) — subcommand overview and quick start
- [serve Command](/en/docs/cli/serve/) — start the Web service
- [perf Command](/en/docs/cli/perf/) — performance stress testing
- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — complete reference for output metrics
- [Accuracy Overview](/en/docs/accuracy/) — three-mode evaluation