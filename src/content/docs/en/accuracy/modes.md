---
title: "Evaluation Modes"
description: "The three accuracy evaluation modes: Native, Serving, and Mock integration testing, with running commands, the built-in open-source baseline library (10 baseline models), and token estimation."
---

# Evaluation Modes

Accuracy evaluation supports three modes — **native (Native)**, **serving (Serving)**, and **Mock (integration)** — and can **estimate token consumption** before a run to control costs. The key to choosing a mode is whether you already have a real service and whether you need to evaluate local weights offline.

## Native Mode

Native mode loads local weights or an HF model id for offline evaluation and supports LoRA adapters. Install the optional dependency first:

```bash
pip install benchscope[accuracy-native]
```

```console
# Example: evaluate 100 samples of a local / HF model on MMLU
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100
```

<div class="warning">

**Warning:**

Native mode does **not force-install** torch / transformers — it only detects existing dependencies and **directly blocks** the run if they are missing, prompting installation rather than running in a broken state. Make sure the required dependencies are installed before starting the evaluation.

</div>

### Using a LoRA Adapter (optional)

```bash
benchscope eval --mode native --model Qwen/Qwen2.5-7B \
  --lora-path /path/to/adapter --dataset gsm8k --limit 100
```

## Serving Mode

Serving mode evaluates a deployed service through an OpenAI-compatible pipeline; the address of the service under test defaults to the global Provider configuration.

```console
# Example: evaluate 200 samples of a deployed service on GSM8K
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

<div class="info">

**Info:**

Serving mode has no extra dependencies, and every request during evaluation goes through the real service pipeline (including token consumption), reflecting real online behavior.

</div>

## Mock Integration

Without a real service, verify pipeline correctness (often used for development / CI integration):

```console
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

You can adjust the mock correctness rate via `--mock-correct-rate` (default `0.7`) to simulate different evaluation results.

## Open-Source Baseline Library

Evaluation results are benchmarked against the **built-in open-source baseline library** (currently 10 baseline models), for horizontal comparison and grading:

| Baseline Model | Parameters | Group | Covered Datasets |
| --- | --- | --- | --- |
| Llama-3-8B | 8B | General | MMLU / GSM8K / MATH / HumanEval / MBPP / CMMLU / C-Eval / MT-Bench |
| Llama-3-70B | 70B | General | Same as above |
| Qwen2-7B | 7B | General | Same as above |
| Qwen2-14B | 14B | General | Same as above |
| Qwen2-72B | 72B | General | Same as above |
| InternLM2-7B | 7B | General | Same as above |
| Mistral-7B | 7B | General | Same as above |
| Qwen2-Chinese | 7B | Chinese-specific | MMLU / CMMLU / C-Eval / GSM8K / MT-Bench |
| Llama3-CN | 8B | Chinese-specific | Same as above |
| Zephyr-7B | 7B | Chinese-specific | MMLU / GSM8K / MATH / HumanEval / MBPP / MT-Bench |

Baseline scores are **approximate reference values** from public technical reports / leaderboards (mostly instruct / chat baselines), used for horizontal benchmarking and not to be cited as an official baseline; administrators can update the baseline library via `PUT /api/accuracy/baselines`. See [Accuracy Core Metrics → Baseline Benchmarking](/en/docs/accuracy/metrics/) for the rating rules (S / A / B / C and `diff_pp`).

## Token Estimation

Before evaluation starts, you can **estimate the total tokens to be consumed** for cost control:

- Serving mode supports a **full token-consumption estimate** (fields: `prompt_tokens` / `completion_tokens` / `total_tokens` / `est_seconds` / `source`);
- Both the creation page (Web) and `benchscope eval` (CLI) display the estimate before launch and issue a **strong warning** when it exceeds expectations;
- After the evaluation ends, an **estimate vs actual comparison** is provided (deviation percentage = (actual − estimate) / estimate);
- The Native mode estimate is always 0 (local offline inference, no online pipeline consumption).

See [Accuracy Core Metrics → Token Consumption Estimation](/en/docs/accuracy/metrics/) for details.

<div class="tip">

**Tip:**

When the dataset is large or the model is expensive, first sample with `--limit` (e.g. 100–200 items) for a small-scale validation, then run the full evaluation once the pipeline and scoring are confirmed normal.

</div>

## FAQ

**Question: How do I quickly avoid cost overruns?**
First sample with `--limit 100` to validate the pipeline and scoring, then run the full evaluation once it is normal; Serving mode performs token estimation and issues strong warnings.

**Question: What if the evaluation is blocked partway through?**
Serving checks service reachability, Native checks local dependencies; if dependencies are missing, install `benchscope[accuracy-native]` as prompted and retry.

## Related

- [Overview](/en/docs/accuracy/) — module overview
- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — the complete definition of all metrics
- [Evaluation Datasets](/en/docs/accuracy/datasets/) — choosing an evaluation set
- [Scorers and Metrics](/en/docs/accuracy/scoring/) — interpreting results
- [eval command](/en/docs/cli/eval/) — complete parameters for `eval`