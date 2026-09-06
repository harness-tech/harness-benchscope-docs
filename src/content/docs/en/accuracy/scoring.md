---
title: "Scorers and Metrics"
---

# Scorers and Metrics

Accuracy evaluation ships with several built-in scorers covering different task types, and outputs standard accuracy metrics, token consumption, and **open-source baseline comparison** results.

## Scorers

| Scorer | Task | Core metric |
| --- | --- | --- |
| `choice` | Choice-question scoring | `exact_match` |
| `math` | Math-question scoring | `math_accuracy` |
| `code` | Code-generation scoring | `pass_at_1` / `compile_rate` |
| `judge` | MT-Bench review | `mt_bench_score` (requires a judge model) |

## Output Metrics

- `accuracy` / `pass_rate` — overall correctness and pass rate.
- `dataset_metrics` — dataset-specific metrics (`math_accuracy` / `pass_at_1`, and so on).
- **Token consumption** — total tokens used by the run.
- **Baseline comparison** — `baseline_used` / `diff_pp` / `grade` / `conclusion`, comparing against an open-source baseline library with tier ratings.

### Baseline comparison

The run is compared against an **open-source baseline library** and rated with a tier:

| Field | Meaning |
| --- | --- |
| `baseline_used` | The baseline used (name / weight) |
| `diff_pp` | Percentage-point difference from the baseline |
| `grade` | Tier rating |
| `conclusion` | Verdict (pass / accuracy drop / flat / better than baseline, and so on) |

### Example result

```console
# Hypothetical result summary
accuracy:            87.5%
pass_rate:           92.0%
dataset_metrics:     { "math_accuracy": 0.875 }
tokens.total_tokens: 51200
benchmark.conclusion: pass (better than baseline)
```

## Artifacts

Each evaluation run is saved to `evals/eval-<MMDDhhmmss>/`:

| File | Contents |
| --- | --- |
| `task.json` | Task main table (aligned with the Web accuracy task structure) |
| `result.json` | Accuracy result, including metrics / baseline / conclusion |
| `samples.jsonl` | Per-sample traceability |

Records can be **viewed, packaged, and imported** under **Datas → Evals** in the Web UI.

![Accuracy results statistics](/images/benchscope-datas-perfs_statistics.png)

## FAQ

**What is `conclusion`?**
`conclusion` is the verdict comparing the run against a baseline (pass / accuracy drop / flat / better than baseline, and so on), determined together with `diff_pp` and `grade`.

**How do I locate individual wrong samples?**
Open `samples.jsonl` and inspect each sample's input, output, and scoring result — this enables sample-level traceability for error analysis.

**Can I compare different models?**
Yes. Evaluate each one and compare them against baselines via `conclusion` / `diff_pp`, or inspect them side by side in **Datas**.

## Related

- [Overview](/en/docs/accuracy/) — module overview
- [Evaluation Modes](/en/docs/accuracy/modes/) — Native / Serving / Mock
- [Datasets](/en/docs/accuracy/datasets/) — choosing an evaluation set
- [eval command](/en/docs/cli/eval/) — full `benchscope eval` reference
