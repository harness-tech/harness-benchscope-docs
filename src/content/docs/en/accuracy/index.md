---
title: "Overview"
description: "Overview of the BenchScope accuracy testing module: quantitative evaluation of model output correctness, native and serving modes, 9 built-in evaluation datasets with dedicated scorers, plus token estimation and open-source baseline benchmarking."
---

# Overview

The accuracy testing module performs **quantitative evaluation** of model outputs, supports both **native (Native)** and **serving (Serving)** modes, ships with **9 built-in evaluation datasets** (GSM8K / MMLU / CMMLU / C-Eval / MATH / HumanEval / MBPP / MT-Bench / GAOKAO-Bench) and dedicated scorers, and provides token estimation and open-source baseline benchmarking. It answers *how accurately the model performs on a given task*.

![BenchScope accuracy testing default screen](/images/benchscope-accuracy_default.png)

<div class="tip">

**Tip:**

Accuracy testing focuses on *whether the model output is correct*, complementing [Performance testing](/en/docs/performance/): performance answers *how fast it runs*, accuracy answers *how accurately it answers*.

</div>

## What's on This Page

- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — the complete definition of every metric (accuracy / sample statistics / per-scorer metrics / Token / baseline benchmark / conclusion)
- [Evaluation Modes](/en/docs/accuracy/modes/) — Native / Serving / Mock modes and Token estimation
- [Evaluation Datasets](/en/docs/accuracy/datasets/) — the built-in dataset catalog and selection
- [Scorers and Metrics](/en/docs/accuracy/scoring/) — scorers, metrics, and baseline benchmarking
- [Accuracy Evaluation](/en/docs/accuracy/guide/) — step-by-step operations

## Mode Overview

| Mode | Description | Dependencies |
| --- | --- | --- |
| Native | Loads local model weights directly (transformers / HF id) for offline evaluation | Optional dependency `accuracy-native` |
| Serving | Evaluates a deployed service through an OpenAI-compatible pipeline | None |
| Mock (integration) | No real service; verifies pipeline correctness | None |

<div class="info">

**Info:**

How do you choose a mode? Pick **Native** to evaluate local weights offline (no server needed); pick **Serving** to evaluate real online service performance (including the serving stack); use **Mock** to get the pipeline working first.

</div>

## FAQ

**Question: How do I choose between Native mode and Serving mode?**
Use Native to evaluate local weights offline (without starting a service); use Serving to evaluate a real online deployment pipeline (including the serving stack); use Mock if you only want to verify the pipeline.

**Question: Native mode startup is blocked?**
torch / transformers / peft were not detected. Run `pip install benchscope[accuracy-native]` and retry.

**Question: What is `conclusion` in the evaluation result?**
`conclusion` is the final evaluation conclusion, with exactly three possible values: **Pass / Accuracy Drop / Anomaly**. Total samples is 0 or the invalid ratio is > 20% → Anomaly; the main metric drops more than 5pp from the baseline (`diff_pp` < -5) → Accuracy Drop; otherwise → Pass. See [Accuracy Core Metrics](/en/docs/accuracy/metrics/) for details.

**Question: How do I locate individual error samples?**
Open `samples.jsonl` and inspect each sample's input, output, and scoring result to achieve sample-level traceability.

## Related

- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — the complete definition of metrics
- [eval command](/en/docs/cli/eval/) — complete parameters of the `eval` command
- [Accuracy Evaluation](/en/docs/accuracy/guide/) — step-by-step operations
- [Data and Statistics (Datas)](/en/docs/data/) — viewing and importing results
- [Settings](/en/docs/tools/settings/) — configuring Providers and Datasets