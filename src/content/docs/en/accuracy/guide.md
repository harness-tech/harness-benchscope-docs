---
title: "Tutorial: Accuracy Evaluation"
---

# Tutorial: Accuracy Evaluation

This tutorial demonstrates how to evaluate model outputs for **accuracy**, in two modes: **Serving mode** (the deployed pipeline) and **Native mode** (local weights).

## Serving Mode

Evaluate the **deployed service pipeline** — this reflects what your users actually get, including the serving stack:

```bash
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

| Option | Meaning |
| --- | --- |
| `--mode serving` | Evaluate through the OpenAI-compatible pipeline |
| `--base-url http://127.0.0.1:8000` | The service to evaluate (defaults to the global Provider config when omitted) |
| `--dataset gsm8k` | The evaluation dataset |
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

## Mock Integration Testing

When no real service is available, verify the **pipeline wiring** with Mock mode:

```bash
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

The mock replies at a configurable correctness rate (`--mock-correct-rate`, default `0.7`), so you can confirm the whole evaluation loop works before pointing it at a real model.

## Web Operations

On the **Accuracy Testing** page in the Web UI:

1. Create an evaluation task (choose Native or Serving mode).
2. Choose the **dataset** and **scorer**.
3. Optionally **estimate tokens** for cost control.
4. Start the run.
5. View the results under **Datas → Evals**.

![Accuracy testing page](/images/benchscope-accuracy_default.png)

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

## Related

- [Accuracy Testing](/en/docs/accuracy/) — modes, datasets, scorers, artifacts
- [CLI Reference](/en/docs/cli/reference/) — full `benchscope eval` reference
- [Datas](/en/docs/data/) — records, export, and import
- [Settings](/en/docs/tools/settings/) — baselines, datasets, and providers
