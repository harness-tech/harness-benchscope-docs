---
title: "Overview"
---

# Overview

The accuracy testing module performs **quantitative evaluation of model outputs**, supporting both **Native** and **Serving** modes, and ships with multiple built-in evaluation datasets and scorers. It answers the question: *how correct is my model on a given task?*

![Accuracy testing main interface](/images/benchscope-accuracy_default.png)

<div class="tip">

**tip**：

Accuracy focuses on **whether the model output is correct**, complementing [Performance testing](/en/docs/performance/): performance answers *how fast*, accuracy answers *how accurate*.

</div>

## In This Section

- [Evaluation Modes](/en/docs/accuracy/modes/) — Native / Serving / Mock modes and token estimation
- [Datasets](/en/docs/accuracy/datasets/) — built-in datasets and picking one
- [Scorers and Metrics](/en/docs/accuracy/scoring/) — scorers, metrics, and baseline comparison
- [Accuracy Guide](/en/docs/accuracy/guide/) — step-by-step tutorial

## Mode Overview

| Mode | Description | Dependencies |
| --- | --- | --- |
| **Native** | Loads local model weights directly (transformers / HF id) for offline evaluation | Optional dependency `accuracy-native` |
| **Serving** | Evaluates a deployed service through an OpenAI-compatible pipeline | None |
| **Mock** (integration testing) | No real service; verifies the correctness of the evaluation pipeline | None |

<div class="info">

**info**：

How to choose? Pick **Native** to evaluate a local checkpoint offline without starting a server, **Serving** to evaluate the exact behavior of your deployed service (including its serving stack), and **Mock** to validate the pipeline wiring first.

</div>

## Common Questions

**Q: Native or Serving — which should I use?**
Use **Native** for offline evaluation of a local checkpoint (no server), **Serving** to evaluate the real deployed pipeline (including its serving stack), and **Mock** just to verify the pipeline wiring.

**Q: Native Mode is blocked at startup?**
`torch` / `transformers` / `peft` were not detected. Run `pip install benchscope[accuracy-native]` and retry.

**Q: What is `conclusion`?**
`conclusion` is the verdict comparing the run against a baseline (pass / accuracy drop / flat / better than baseline, and so on), determined together with `diff_pp` and `grade`.

**Q: How do I locate individual wrong samples?**
Open `samples.jsonl` and inspect each sample's input, output, and scoring result — this enables sample-level traceability for error analysis.

## Related

- [eval command](/en/docs/cli/eval/) — the `benchscope eval` command
- [Accuracy Guide](/en/docs/accuracy/guide/) — step-by-step tutorial
- [Datas](/en/docs/data/) — where accuracy records are stored
- [Settings](/en/docs/tools/settings/) — providers, models, datasets, and baselines
