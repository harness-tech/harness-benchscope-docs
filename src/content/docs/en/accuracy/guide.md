---
title: "Accuracy Guide"
---

# Accuracy Guide

This tutorial demonstrates how to evaluate model outputs for **accuracy**, in two modes: **Serving mode** (the deployed pipeline) and **Native mode** (local weights), then how to interpret the result metrics, baseline comparison, and sample-level traceability.

## Prerequisites

- benchscope installed (see [Quickstart](/en/docs/quickstart/));
- Serving Mode needs a deployed OpenAI-compatible service;
- Native Mode needs the optional dependency `benchscope[accuracy-native]`.

## Serving Mode

Evaluate the **deployed service pipeline** — this reflects what your users actually get, including the serving stack:

```bash
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

| Option | Meaning |
| --- | --- |
| `--mode serving` | Evaluate through the OpenAI-compatible pipeline |
| `--model` | The model name under test |
| `--base-url` | The service to evaluate (defaults to the global Provider config when omitted) |
| `--dataset gsm8k` | Built-in dataset id |
| `--limit 200` | Sample at most 200 examples |

## Native Mode

Load **local weights** for offline evaluation — useful for checking a checkpoint before deployment. The optional dependency must be installed first:

```bash
pip install benchscope[accuracy-native]
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100
```

<div class="warning">

**warning**：

Native mode requires `torch` / `transformers` to be present. Install `benchscope[accuracy-native]`; otherwise the run is blocked with an environment-validation error.

</div>

### Using LoRA Adapters (optional)

```bash
benchscope eval --mode native --model Qwen/Qwen2.5-7B \
  --lora-path /path/to/adapter --dataset gsm8k --limit 100
```

## Mock Integration Testing

When no real service is available, verify the **pipeline wiring** with Mock mode:

```bash
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

The mock replies at a configurable correctness rate (`--mock-correct-rate`, default `0.7`), so you can confirm the whole evaluation loop works before pointing it at a real model.

## Interpreting the Results

- `accuracy` / `pass_rate` — overall accuracy and pass rate.
- `dataset_metrics` — dataset-specific metrics (`math_accuracy` / `pass_at_1`, and so on).
- `benchmark` — comparison against baselines: `baseline_used.name`, `diff_pp`, `grade`, `conclusion`.
- `samples.jsonl` — sample-level traceability, so you can **locate individual wrong samples** for error analysis.

```console
# Hypothetical result summary
accuracy: 78.5%
pass_rate: 78.5%
dataset_metrics.math_accuracy: 0.741
tokens.total_tokens: 48120
benchmark.baseline_used.name: gsm8k-qwen2.5-7b
benchmark.conclusion: flat (within tolerance)
```

## Web Operations

On the **Accuracy Testing** page in the Web UI:

1. Create an evaluation task (choose Native or Serving mode).
2. Choose the **dataset** and **scorer**.
3. Optionally **estimate tokens** for cost control.
4. Start the run.
5. View the results under **Datas → Evals**.

![Accuracy testing page](/images/benchscope-accuracy_default.png)

## Common Questions

**Q: How do I avoid blowing the cost budget?**
First validate the pipeline and scoring with a small sample (`--limit 100`); once it looks right, run the full evaluation. Serving Mode also estimates tokens and warns before you overshoot.

**Q: Can I compare different models?**
Yes. Evaluate each one and compare them against baselines via `conclusion` / `diff_pp`, or inspect them side by side in **Datas**.

**Q: The run is blocked partway?**
Serving Mode checks service reachability; Native Mode checks local dependencies. If dependencies are missing, install `benchscope[accuracy-native]` and retry.

## Related

- [Accuracy Testing](/en/docs/accuracy/) — modes, datasets, scorers, artifacts
- [eval command](/en/docs/cli/eval/) — full `benchscope eval` reference
- [Datas](/en/docs/data/) — records, export, and import
- [Settings](/en/docs/tools/settings/) — baselines, datasets, and providers
