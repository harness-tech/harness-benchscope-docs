---
title: "Scorers and Metrics"
description: "The accuracy evaluation scorers in detail: applicable tasks and metrics for the choice / math / code / judge scorers, an output-metrics overview, baseline-benchmarking fields, and final-conclusion rules."
---

# Scorers and Metrics

Accuracy evaluation ships with multiple built-in scorers covering different task types, and outputs standard accuracy metrics, token consumption, and **open-source baseline benchmarking** results.

## Scorers

| Scorer | Applicable Task | Metric |
| --- | --- | --- |
| `choice` | Choice questions | exact_match |
| `math` | Math questions | math_accuracy |
| `code` | Code generation | pass_at_1 / compile_rate |
| `judge` | MT-Bench review | mt_bench_score (judge-model required) |

## Output Metrics

See [Accuracy Core Metrics](/en/docs/accuracy/metrics/) for the definition of all metrics; the following is an overview:

- `accuracy` / `pass_rate` — core main metrics: overall accuracy rate and pass rate;
- `total_samples` / `correct_samples` / `wrong_samples` / `invalid_samples` — sample statistics;
- `subjects` — per-subject accuracy rate (data source for the capability radar chart, dimensions: knowledge / math / code / dialogue / comprehensive);
- `error_tag_summary` — error-cause tag distribution (attribution of error samples);
- `dataset_metrics` — scorer-specific metrics: math type (`exact_match` / `math_accuracy` / `answer_parse_rate`), code type (`pass_at_1` / `compile_rate` / `case_pass_rate`), judge type (`mt_bench_score` / `first_turn_score` / `second_turn_score` / `dim_helpfulness` / `dim_truthfulness` / `dim_harmlessness`);
- **Token consumption** (Serving mode) — `prompt_tokens_total` / `completion_tokens_total` / `total_tokens` / per-sample average;
- **Baseline benchmarking** — `baseline_used` / `diff_pp` / `grade` / `conclusion`, compared against the open-source baseline library with a grade evaluation issued.

### Baseline Benchmarking (Baseline)

Evaluation results are benchmarked against the **open-source baseline library** (10 built-in baseline models, see [Evaluation Modes → Open-Source Baseline Library](/en/docs/accuracy/modes/)) to produce a grade evaluation and capability comparison:

| Field | Meaning |
| --- | --- |
| `baseline_used` | Name of the baseline model used (best in the same size range / specified model) |
| `diff_pp` | Difference from the baseline score (percentage points); a positive value means better than the baseline |
| `grade` | Grade evaluation: S (≥ 0) / A (≥ -5) / B (≥ -15) / C (the rest), based on the difference from the best baseline in the same size range |
| `conclusion` | Final conclusion: one of three — **Pass / Accuracy Drop / Anomaly** (rules in the table below) |

### Final Conclusion Determination Rules

| Conclusion | Determination Rule |
| --- | --- |
| Anomaly | Total samples = 0, or the invalid sample ratio is > 20% |
| Accuracy Drop | The main metric drops more than 5pp from the baseline (`diff_pp` < -5) |
| Pass | All other cases |

### Result Example

```console
accuracy:            87.5%
pass_rate:           92.0%
dataset_metrics:     { "math_accuracy": 0.875 }
tokens.total_tokens: 51200
benchmark.conclusion: Pass (better than baseline)
```

## Artifacts

Saved to `evals/eval-<MMDDhhmmss>/`:

- `task.json` — the task main table, aligned with the Web accuracy task structure (mode / engine / model / LoRA / dataset / sampling parameters / progress / estimate / status);
- `result.json` — the accuracy result, containing all core metrics / per-subject / specialized metrics / Token statistics / benchmark / conclusion;
- `samples.jsonl` — per-sample traceability (input / output / scoring status / error-cause tag / token count).

Accuracy evaluation artifacts are managed on the **Accuracy** page (task list + details + sample viewing).

![BenchScope accuracy result statistics](/images/benchscope-datas-perfs_statistics.png)

## FAQ

**Question: What is `conclusion` in the evaluation result?**
`conclusion` is the final evaluation conclusion, with exactly three possible values: **Pass / Accuracy Drop / Anomaly**. Total samples is 0 or the invalid ratio is > 20% → Anomaly; the main metric drops more than 5pp from the baseline (`diff_pp` < -5) → Accuracy Drop; otherwise → Pass.

**Question: How do I locate individual error samples?**
Open `samples.jsonl` and inspect each sample's input, output, scoring status, and error-cause tag to achieve sample-level traceability; `error_tag_summary` provides a summary of the error-cause distribution.

**Question: Can I compare different models?**
Yes. Evaluate each one separately, then benchmark against the baseline with `diff_pp` / `grade`, or compare the results of two tasks side by side on the Accuracy page.

## Related

- [Overview](/en/docs/accuracy/) — module overview
- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — the complete definition of all metrics
- [Evaluation Modes](/en/docs/accuracy/modes/) — Native / Serving / Mock and the baseline library
- [Evaluation Datasets](/en/docs/accuracy/datasets/) — selecting an evaluation set
- [eval command](/en/docs/cli/eval/) — complete parameters for `eval`