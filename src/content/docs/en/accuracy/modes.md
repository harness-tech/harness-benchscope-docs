---
title: "Evaluation Modes"
---

# Evaluation Modes

Accuracy evaluation supports three modes — **Native**, **Serving**, and **Mock** (integration testing) — and can **estimate token consumption** before a run for cost control. The key to choosing a mode is whether a real service is available and whether you need to evaluate local weights offline.

## Native Mode

Native Mode loads **local weights** or an **HF model id** for offline evaluation and supports **LoRA adapters**. Install the optional dependency first:

```bash
pip install benchscope[accuracy-native]
```

```console
# Example: evaluate a local / HF model on MMLU with 100 samples
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100
```

<div class="warning">

**warning**：

Native mode does **not** force the installation of torch / transformers. It only **detects existing dependencies** and blocks the run if they are not satisfied — install `benchscope[accuracy-native]` to enable it.

</div>

### Using LoRA Adapters (optional)

```bash
benchscope eval --mode native --model Qwen/Qwen2.5-7B \
  --lora-path /path/to/adapter --dataset gsm8k --limit 100
```

## Serving Mode

Serving Mode evaluates through an **OpenAI-compatible pipeline**. The service under test defaults to the **global Provider configuration** when no explicit base URL is given.

```console
# Example: evaluate a deployed service on GSM8K with 200 samples
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

<div class="info">

**info**：

Serving Mode has **no extra dependencies** and sends every request through the real service pipeline (including token consumption), so the results reflect production behavior.

</div>

## Mock Integration Testing

When no real service is available, use **Mock** mode to verify that the evaluation pipeline itself is wired correctly (commonly used for development / CI integration):

```console
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

The mock answers with a configurable correctness rate (`--mock-correct-rate`, default `0.7`), letting you sanity-check the whole loop end to end.

## Token Estimation

Before evaluation, you can **estimate the total token consumption** for cost control:

- Serving Mode supports **full token-consumption estimation**;
- An **explicit warning** is shown when the estimate exceeds expectations;
- After the run, the **actual token statistics** are reported and compared against the estimate.

<div class="tip">

**tip**：

When the dataset is large or the model is expensive, first run a small sample with `--limit` (for example 100–200) to confirm the pipeline and scoring work, then launch the full evaluation.

</div>

## FAQ

**How do I avoid blowing the cost budget?**
First validate the pipeline and scoring with a small sample (`--limit 100`); once it looks right, run the full evaluation. Serving Mode also estimates tokens and warns before you overshoot.

**The run is blocked partway?**
Serving Mode checks service reachability; Native Mode checks local dependencies. If dependencies are missing, install `benchscope[accuracy-native]` and retry.

## Related

- [Overview](/en/docs/accuracy/) — module overview
- [Datasets](/en/docs/accuracy/datasets/) — choosing an evaluation set
- [Scorers and Metrics](/en/docs/accuracy/scoring/) — interpreting results
- [eval command](/en/docs/cli/eval/) — full `benchscope eval` reference
