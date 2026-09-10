---
title: "Accuracy Core Metrics"
description: "All core metrics and key metrics for accuracy evaluation: accuracy / pass rate / sample statistics / per-subject / scorer-specific / token consumption / baseline benchmarking / conclusion, including metric meanings and determination rules."
---

# Accuracy Core Metrics

This page is the **complete reference** for accuracy evaluation metrics: it covers the core accuracy metrics, sample statistics, per-subject and error-cause analysis, per-scorer specialized metrics, token consumption statistics, baseline benchmarking, and the final conclusion. When you encounter metric names while reading the other accuracy documents ([Evaluation Modes](/en/docs/accuracy/modes/), [Scorers and Metrics](/en/docs/accuracy/scoring/)), you can look up their meanings on this page.

## Core Metrics

| Metric | Key | Unit | Meaning |
| --- | --- | --- | --- |
| Accuracy (core main metric) | `accuracy` | % | Correct sample count / total sample count; the **core main metric** of accuracy evaluation. |
| Pass rate | `pass_rate` | % | Valid parseable sample ratio = (total samples − invalid samples) / total samples; measures the proportion of answers that can be scored. |
| Total sample count | `total_samples` | count | Total number of samples actually executed in this evaluation run. |
| Correct sample count | `correct_samples` | count | Number of samples whose scoring result is correct. |
| Error sample count | `wrong_samples` | count | Number of samples that are scoreable but have an incorrect result. |
| Invalid sample count | `invalid_samples` | count | Number of samples that cannot be parsed / scored (format error, unanswered, etc.). |

<div class="tip">

**Tip:**

The roles of `accuracy` and `pass_rate`: **accuracy** answers *how many were answered correctly*, **pass_rate** answers *how many answers can be scored*. When pass_rate is significantly below 100%, you should first investigate the answer format (e.g. a choice question where the option letter was not output), rather than the model's capability.

</div>

## Per-Subject and Error-Cause Analysis

| Metric | Key | Unit | Meaning |
| --- | --- | --- | --- |
| Per-subject accuracy rate | `subjects` | % | Per-subject accuracy rate grouped by the dataset's `subject` field (samples with an empty `subject` do not participate), used to locate weak subjects. |
| Error-cause tag distribution | `error_tag_summary` | count | Attribution tag counts for error samples (e.g. "knowledge error"), used to locate weak capabilities. |

Per-subject accuracy rate is the data source for the **capability radar chart**, with radar dimensions: knowledge / math / code / dialogue (comprehensive datasets fall into the "comprehensive" dimension).

## Scorer-Specific Metrics

Different datasets are bound to different scorers (`choice` / `math` / `code` / `judge`); scorer-specific metrics are output according to the scorer type:

### math scorer (math type: GSM8K / MATH)

| Metric | Key | Unit | Meaning |
| --- | --- | --- | --- |
| Exact match rate | `exact_match` | % | Proportion of samples whose final math answer exactly matches the standard answer. |
| Math accuracy rate | `math_accuracy` | % | Main metric of math-type datasets, on the same basis as `exact_match`. |
| Answer parse rate | `answer_parse_rate` | % | Proportion of samples from which a scoreable answer can be extracted from the model's response; reflects answer format quality. |

### code scorer (code type: HumanEval / MBPP)

| Metric | Key | Unit | Meaning |
| --- | --- | --- | --- |
| pass@1 | `pass_at_1` | % | Proportion of samples that pass all test cases in a single generation; the main metric of code-type datasets. |
| Compilation pass rate | `compile_rate` | % | Proportion of samples whose generated code can be successfully compiled / executed. |
| Case pass rate | `case_pass_rate` | % | Overall test-case pass rate across all samples (passed cases / total cases), finer-grained than pass@1. |

### judge scorer (dialogue type: MT-Bench)

| Metric | Key | Unit | Meaning |
| --- | --- | --- | --- |
| MT-Bench total score | `mt_bench_score` | 0–10 | Average score of the two-turn dialogue by the LLM reviewer (first-turn average × 0.5 + second-turn average × 0.5); the main metric of dialogue-type datasets. |
| First-turn score | `first_turn_score` | 0–10 | Average review score of the first round of dialogue. |
| Second-turn score | `second_turn_score` | 0–10 | Average review score of the second round of dialogue (examines inheritance of the first-turn context). |
| Helpfulness dimension score | `dim_helpfulness` | 0–10 | Average score of the review's helpfulness dimension. |
| Truthfulness dimension score | `dim_truthfulness` | 0–10 | Average score of the review's truthfulness dimension. |
| Harmlessness dimension score | `dim_harmlessness` | 0–10 | Average score of the review's harmlessness dimension. |

> The `choice` scorer (MMLU / CMMLU / C-Eval / GAOKAO-Bench) has no additional specialized metrics; it relies on `accuracy` + per-subject accuracy rate.

## Token Consumption Statistics (Serving mode)

| Metric | Key | Unit | Meaning |
| --- | --- | --- | --- |
| Total input tokens | `prompt_tokens_total` | tokens | Total input (prompt) token count across all requests in this evaluation run. |
| Total output tokens | `completion_tokens_total` | tokens | Total output (completion) token count across all responses in this evaluation run. |
| Total token count | `total_tokens` | tokens | Total input + output token count, used for cost accounting. |
| Average input tokens per sample | `avg_prompt_tokens_per_sample` | tokens | Total input token count / total sample count. |
| Average output tokens per sample | `avg_completion_tokens_per_sample` | tokens | Total output token count / total sample count. |

> **Native mode has no Token statistics** (local offline inference, no online pipeline consumption); the `tokens` field is null.

## Baseline Benchmarking

Evaluation results are benchmarked against the **open-source baseline library** (10 built-in baseline models, see [Evaluation Modes → Baseline Library](/en/docs/accuracy/modes/)); the following fields are output:

| Metric | Key | Unit | Meaning |
| --- | --- | --- | --- |
| Benchmarked baseline | `baseline_used` | — | Name of the open-source baseline model that participates in the benchmark (best in the same size range in the baseline library / specified model). |
| Baseline difference | `diff_pp` | pp | Difference (in percentage points) between this run's main metric score and the baseline score; a positive value means better than the baseline. |
| Grade evaluation | `grade` | S/A/B/C | Rating based on the difference from the best baseline in the same size range: **S** ≥ 0; **A** ≥ -5; **B** ≥ -15; the rest are **C**. |

### Final Conclusion (conclusion)

| Conclusion | Determination Rule |
| --- | --- |
| Anomaly | Total samples = 0, or the invalid sample ratio is > 20%. |
| Accuracy Drop | The main metric drops more than 5pp from the baseline (`diff_pp` < -5). |
| Pass | All other cases. |

## Token Consumption Estimation (estimate)

Before evaluation, consumption is estimated from the dataset's sample count and average length, with the following fields:

| Field | Meaning |
| --- | --- |
| `prompt_tokens` / `completion_tokens` / `total_tokens` | Estimated input / output / total token count. |
| `est_seconds` | Estimated elapsed time (seconds). |
| `source` | Estimation source: built-in sample average (builtin) or character estimation (chars, for custom datasets). |
| `total_samples` | Number of samples participating in the estimate. |

After the evaluation ends, an **estimate vs actual** comparison is provided (deviation percentage = (actual − estimate) / estimate). The Native mode estimate is always 0 (no online pipeline consumption).

## Artifact Files

| File | Content |
| --- | --- |
| `task.json` | Task main table: mode / engine / model / LoRA / dataset / sampling parameters / progress / estimate / status. |
| `result.json` | Accuracy result: all core metrics + per-subject + specialized metrics + Token statistics + baseline benchmarking + conclusion. |
| `samples.jsonl` | Per-sample records: input / output / scoring status / error-cause tag / token count, used for sample-level traceability. |

## FAQ

**Question: accuracy is high but pass_rate is low — what does that mean?**
It means a large number of answers cannot be scored (format errors, not output in the standard answer form); prioritize fixing the answer format or the prompt, rather than doubting the model's capability.

**Question: How is grade evaluated?**
It is graded by the difference between this run's main metric score and the **best open-source baseline in the same size range**: S (not below the best baseline) / A (gap ≤ 5pp) / B (gap ≤ 15pp) / C (gap > 15pp).

**Question: When is the "Anomaly" conclusion given?**
When total samples is 0 (the evaluation was not actually executed) or the invalid sample ratio exceeds 20% (answers are widely unscoreable), the conclusion is "Anomaly"; you should first investigate the data and the pipeline.

**Question: Why does Native mode have no Token statistics?**
Native mode is local offline inference, does not go through the online service pipeline, has no API token consumption, and the `tokens` field is null.

## Related

- [Accuracy Testing Overview](/en/docs/accuracy/) — module overview
- [Evaluation Modes](/en/docs/accuracy/modes/) — Native / Serving / Mock and the baseline library
- [Evaluation Datasets](/en/docs/accuracy/datasets/) — dataset and scorer binding
- [Scorers and Metrics](/en/docs/accuracy/scoring/) — scoring flow and benchmarking
- [eval command](/en/docs/cli/eval/) — CLI output metrics cross-reference