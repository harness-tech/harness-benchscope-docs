---
title: "eval"
---

# eval

Runs an accuracy evaluation (Serving / Native / Mock) and outputs metrics such as `accuracy` / `pass_rate`.

```bash
benchscope eval --model MODEL --dataset DATASET [options]
```

The dataset can be a **built-in id** (`mmlu` / `gsm8k` …) or a **local JSONL file path**.

## Examples

```console
# Serving mode: evaluate a deployed OpenAI-compatible pipeline
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200

# Native mode: evaluate local transformers weights / HF id offline
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100

# Mock integration testing: verify the pipeline without a real service
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

## Main arguments

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--engine` | str | `benchscope` | Accuracy engine id (`benchscope`=serving / `native-hf`=native / `mock`=integration) |
| `--mode` | str | `serving` | Evaluation mode: `serving` (pipeline) / `native` (local weights) |
| `--model` | str | **required** | Model under test (Native accepts a weights path or an HF id) |
| `--dataset` | str | **required** | Built-in dataset id (`mmlu` / `gsm8k` …) or local JSONL path |

**Service & model adaptation**

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--lora-path` | str | empty | Path to a LoRA fine-tuned adapter (optional) |
| `--lora-name` | str | empty | Server-side registered name of the LoRA model (Serving request-side model, optional) |
| `--base-url` | str | empty | Service address (Serving; defaults to the global Provider config when omitted) |
| `--api-key` | str | empty | API key of the service under test (optional) |

**Sampling & generation**

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--limit` | int | `0` | Sample sampling limit (0 = all samples) |
| `--seed` | int | `1234` | Global random seed (sampling and generation, fixed for reproducibility) |
| `--temperature` | float | `0.0` | Sampling temperature |
| `--top-p` | float | `1.0` | Nucleus sampling probability |
| `--max-tokens` | int | `512` | Maximum output tokens per sample |
| `--concurrency` | int | `4` | Number of concurrent inferences |

**Judge / integration / naming**

| Argument | Type | Default | Description |
| --- | --- | --- | --- |
| `--judge-model` | str | empty | MT-Bench judge model (used by the judge dataset) |
| `--mock-correct-rate` | float | `0.7` | Mock engine correctness rate (0–1) |
| `--name` | str | empty | Task name (optional) |
| `--use-mock-env` | flag | off | Mock environment marker (for integration testing) |

## Output metrics

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

## Sample run

```console
# A typical Serving-mode run
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
dataset_metrics:     { "math_accuracy": 0.875 }
tokens.total_tokens: 51200
conclusion:          pass (better than baseline)
Saved -> ~/.benchscope/evals/eval-<time>/ (task.json / result.json / samples.jsonl)
```

## Artifacts

Artifacts are written to `evals/eval-<MMDDhhmmss>/` and contain:

- `task.json` — the task main table, aligned with the Web accuracy task structure
- `result.json` — the accuracy result, including metrics / baseline / conclusion
- `samples.jsonl` — per-sample traceability

A terminal log `logs/eval_<task_id>_<time>.log` is also written. View or package-import these under **Datas → Evals** in the Web UI.

## Related

- [CLI Overview](/en/docs/cli/) — sub-command overview and quick start
- [serve](/en/docs/cli/serve/) — start the Web service
- [perf](/en/docs/cli/perf/) — performance testing
- [Performance Testing](/en/docs/performance/) — Concurrency and Threshold modes
- [Accuracy Testing](/en/docs/accuracy/) — dual-mode evaluation
