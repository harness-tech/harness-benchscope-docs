---
title: "Accuracy Evaluation"
description: "A hands-on guide to accuracy evaluation: running commands and parameters for Serving, Native, and Mock modes, interpreting result metrics, baseline comparison, and sample-level traceability, plus the three-step Web form."
---

# Accuracy Evaluation

This section demonstrates how to perform **accuracy evaluation** on model outputs (Serving mode and Native mode), and how to interpret result metrics, benchmark against baselines, and perform sample-level traceability.

## Prerequisites

- benchscope installed (see [Quickstart](/en/docs/quickstart/));
- Serving mode requires a deployed OpenAI-compatible service;
- Native mode requires installing the optional dependency `benchscope[accuracy-native]`.

## Serving Mode

Evaluate the deployed service pipeline — this reflects the behavior users actually receive online, **including the serving stack**:

```bash
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

| Parameter | Description |
| --- | --- |
| `--mode serving` | Evaluate through the OpenAI-compatible pipeline (default) |
| `--model` | Name of the model under test |
| `--base-url` | Service address (defaults to the global Provider configuration) |
| `--dataset gsm8k` | Built-in dataset id |
| `--limit 200` | Sample 200 items |

## Native Mode

Load local weights for offline evaluation (requires installing the optional dependency):

```bash
pip install benchscope[accuracy-native]
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100
```

<div class="warning">

**Warning:**

Native mode detects the local torch / transformers dependencies and, if they are missing, directly blocks the run and prompts installation, rather than running in a broken state.

</div>

### Using a LoRA Adapter (optional)

```bash
benchscope eval --mode native --model Qwen/Qwen2.5-7B \
  --lora-path /path/to/adapter --dataset gsm8k --limit 100
```

## Mock Integration

Without a real service, verify the pipeline:

```bash
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

You can adjust the correctness rate via `--mock-correct-rate 0.85` to simulate different evaluation results (for integration testing).

## Interpreting the Results

See [Accuracy Core Metrics](/en/docs/accuracy/metrics/) for the definition of all metrics; the commonly used metrics are as follows:

- **`accuracy` / `pass_rate`**: core main metrics — overall accuracy rate and pass rate;
- **`subjects` / `error_tag_summary`**: per-subject accuracy rate (capability radar) and error-cause tag distribution;
- **`dataset_metrics`**: scorer-specific metrics (`exact_match` / `math_accuracy` / `pass_at_1` / `compile_rate` / `mt_bench_score`, etc.);
- **`tokens`** (Serving mode): input / output / total token counts and the per-sample average;
- **`benchmark`**: baseline benchmarking (`baseline_used` / `diff_pp` / `grade`);
- **`conclusion`**: final conclusion (Pass / Accuracy Drop / Anomaly);
- **`samples.jsonl`**: sample-level traceability, allowing you to locate individual error samples.

```console
accuracy:            87.5%
pass_rate:           92.0%
total_samples:       200
correct_samples:     175
wrong_samples:       25
dataset_metrics:     { "math_accuracy": 87.5 }
tokens.total_tokens: 51200
conclusion:          Pass
```

## Web Operations

Create an evaluation task on the **Accuracy Testing** page of the Web UI (a three-step form):

1. **Step 1: Dataset** — pick a built-in evaluation dataset (or a local JSONL) and the sampling cap (limit);
2. **Step 2: Mode and Engine** — pick the Native / Serving mode and the accuracy engine (`benchscope` / `native-hf` / `mock`);
3. **Step 3: Preview and Confirm** — review the task parameters and the **Token consumption estimate** (a strong warning when the threshold is exceeded), then confirm to start;
4. View the task progress, result metrics, per-subject breakdown, and baseline benchmarking on the **Accuracy** page.

![BenchScope accuracy testing default screen](/images/benchscope-accuracy_default.png)

## FAQ

**Question: How do I quickly avoid cost overruns?**
First sample with `--limit 100` to validate the pipeline and scoring, then run the full evaluation once it is normal; Serving mode performs token estimation and issues strong warnings.

**Question: Can I compare different models?**
Yes. Evaluate each one separately, then benchmark against the baseline with `diff_pp` / `grade`, or compare the results of multiple tasks side by side on the Accuracy page.

**Question: What if the evaluation is blocked partway through?**
Serving checks service reachability, Native checks local dependencies; if dependencies are missing, install `benchscope[accuracy-native]` as prompted and retry.

## Related

- [Overview](/en/docs/accuracy/) — the three modes and scorers in detail
- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — the complete definition of all metrics
- [eval command](/en/docs/cli/eval/) — complete parameters for `eval`
- [Evaluation Modes](/en/docs/accuracy/modes/) — Native / Serving / Mock and the baseline library