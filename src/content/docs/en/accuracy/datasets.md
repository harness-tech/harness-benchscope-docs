---
title: "Evaluation Datasets"
description: "The 12 built-in BenchScope datasets: 9 accuracy evaluation datasets (bound to scorers and main metrics) and 3 performance stress-test datasets, with categories, sample counts, and usage examples."
---

# Evaluation Datasets

BenchScope ships with **12 built-in datasets**: **9 accuracy evaluation datasets** (bound to scorers and sample-count declarations, usable for accuracy evaluation) and **3 performance stress-test datasets** (providing real dialogue data for stress testing), covering categories such as knowledge / math / code / dialogue / comprehensive / instruction. To select a dataset, pass a **built-in dataset id** (`mmlu` / `gsm8k`, etc.) or a **local JSONL path** directly.

## Accuracy Evaluation Datasets (9)

Each evaluation dataset is bound to a dedicated scorer (`choice` / `math` / `code` / `judge`) and a main metric; see [Accuracy Core Metrics](/en/docs/accuracy/metrics/) for the definition of the specialized metrics:

| Dataset id | Name | Category | Scorer | Main Metric | Sample Count |
| --- | --- | --- | --- | --- | --- |
| `mmlu` | MMLU | Knowledge | `choice` | accuracy | 14,079 (57 subjects) |
| `cmmlu` | CMMLU | Knowledge | `choice` | accuracy | 11,960 (67 subjects) |
| `c-eval` | C-Eval | Knowledge | `choice` | accuracy | 13,480 (52 subjects) |
| `gsm8k` | GSM8K | Math | `math` | exact_match | 7,473 |
| `math` | MATH | Math | `math` | exact_match | 5,000 |
| `humaneval` | HumanEval | Code | `code` | pass@1 | 164 |
| `mbpp` | MBPP | Code | `code` | pass@1 | 974 |
| `mt-bench` | MT-Bench | Dialogue | `judge` | mt_bench | 80 questions (160 turns) |
| `gaokao-bench` | GAOKAO-Bench | Comprehensive | `choice` | accuracy | 2,000 (objective-question subset) |

## Performance Stress-Test Datasets (3)

These datasets provide real dialogue data for performance stress testing (ShareGPT mode) and are not bound to scorers:

| Dataset id | Name | Category | Description |
| --- | --- | --- | --- |
| `sharegpt` | ShareGPT | Dialogue | ShareGPT dialogue dataset (auto-downloaded by ModelScope), used for ShareGPT-mode benchmarking. |
| `alpaca` | Alpaca | Instruction fine-tuning | Stanford Alpaca instruction fine-tuning dataset (52K dialogue samples), dialogue-format benchmarking. |
| `dolly` | Dolly | Instruction fine-tuning | Databricks Dolly-15k instruction fine-tuning dataset (15K samples), dialogue-format benchmarking. |

For the complete list (including download sources and categories), see [Settings → Datasets](/en/docs/tools/settings/).

## Using a Built-in Dataset

Just pass a built-in dataset id:

```console
# Example: evaluate 200 samples on GSM8K
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

## Using a Local JSONL

Pass a local JSONL path and evaluate with your own data:

```console
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset /path/to/my-data.jsonl --limit 100
```

## FAQ

**Question: How do datasets correspond to scorers?**
Different datasets apply to different scorers (e.g. choice questions use `choice`, math uses `math`, code uses `code`). See [Scorers and Metrics](/en/docs/accuracy/scoring/) for details.

**Question: Can't find the evaluation set I need?**
You can import your own data via a local JSONL to participate in the evaluation.

## Related

- [Overview](/en/docs/accuracy/) — module overview
- [Scorers and Metrics](/en/docs/accuracy/scoring/) — how results are judged
- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — the specialized metric definition for each scorer
- [Settings](/en/docs/tools/settings/) — configuring Datasets