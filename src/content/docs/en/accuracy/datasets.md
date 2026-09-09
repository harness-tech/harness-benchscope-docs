---
title: "Evaluation Datasets"
---

# Evaluation Datasets

BenchScope ships with **9 built-in evaluation datasets** covering knowledge / math / code / chat / comprehensive domains. Each dataset is bound to a dedicated scorer (`choice` / `math` / `code` / `judge`) with declared sample counts. To choose a dataset, pass a **built-in dataset id** (for example `mmlu` / `gsm8k`) or a **local JSONL path**.

| Dataset id | Name | Domain | Scorer | Metric | Samples |
| --- | --- | --- | --- | --- | --- |
| `gsm8k` | GSM8K | Math | `math` | exact_match | 7,473 |
| `mmlu` | MMLU | Knowledge | `choice` | accuracy | 14,079 |
| `cmmlu` | CMMLU | Knowledge | `choice` | accuracy | 11,960 |
| `c-eval` | C-Eval | Knowledge | `choice` | accuracy | 13,480 |
| `math` | MATH | Math | `math` | exact_match | 5,000 |
| `humaneval` | HumanEval | Code | `code` | pass@1 | 164 |
| `mbpp` | MBPP | Code | `code` | pass@1 | 974 |
| `mt-bench` | MT-Bench | Chat | `judge` | mt_bench | 80 |
| `gaokao-bench` | GAOKAO-Bench | Comprehensive | `choice` | accuracy | 2,000 |

See **Settings → Datasets** for the full list — [Settings](/en/docs/tools/settings/).

## Using a Built-in Dataset

Pass a built-in dataset id:

```console
# Example: evaluate 200 samples on GSM8K
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

## Using a Local JSONL

Pass a local JSONL path to evaluate against your own data:

```console
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset /path/to/my-data.jsonl --limit 100
```

## FAQ

**How do datasets map to scorers?**
Different datasets use different scorers (for example `choice` for multiple-choice, `math` for math, `code` for code generation). See [Scorers and Metrics](/en/docs/accuracy/scoring/).

**I cannot find the dataset I need?**
Import your own data via a local JSONL path.

## Related

- [Overview](/en/docs/accuracy/) — module overview
- [Scorers and Metrics](/en/docs/accuracy/scoring/) — how results are judged
- [Settings](/en/docs/tools/settings/) — configuring datasets
