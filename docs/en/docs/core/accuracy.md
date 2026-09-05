# Accuracy Testing

The accuracy testing module performs **quantitative evaluation of model outputs**, supporting both **Native** and **Serving** modes, and ships with multiple built-in evaluation datasets and scorers. It answers the question: *how correct is my model on a given task?*

![Accuracy testing main interface](/images/benchscope-accuracy_default.png)

## Mode Overview

| Mode | Description | Dependencies |
| --- | --- | --- |
| **Native** | Loads local model weights directly (transformers / HF id) for offline evaluation | Optional dependency `accuracy-native` (torch / transformers / peft) |
| **Serving** | Evaluates a deployed service through an OpenAI-compatible pipeline | None |
| **Mock** (integration testing) | No real service; verifies the correctness of the evaluation pipeline | None |

::: tip
Choose **Native** when you want to evaluate a local checkpoint without starting a server, and **Serving** when you want to evaluate the exact behavior of your deployed service (including its serving stack).
:::

## Built-in Evaluation Datasets

- Ships with **9 evaluation datasets** such as MMLU and GSM8K, covering knowledge / math / code / chat / Chinese domains — see the Accuracy page in the Web UI for the full list.
- You can pass a **built-in dataset id** (for example `mmlu` / `gsm8k`) or a **local JSONL path**.

### Dataset examples

| Domain | Examples |
| --- | --- |
| Knowledge | MMLU |
| Math | GSM8K |
| Code | HumanEval / MBPP (sandboxed `pass@1`) |
| Chat / judge | MT-Bench (LLM-as-judge) |
| Chinese | Various Chinese-language datasets included in the built-in set |

## Scorers and Metrics

Multiple built-in scorers cover different task types:

| Scorer | Task | Core metric |
| --- | --- | --- |
| `choice` | Choice-question scoring | `exact_match` |
| `math` | Math-question scoring | `math_accuracy` |
| `code` | Code-generation scoring | `pass_at_1` / `compile_rate` |
| `judge` | MT-Bench review | `mt_bench_score` (requires a judge model) |

Output metrics include:

- `accuracy` / `pass_rate` — overall correctness and pass rate
- `dataset_metrics` — dataset-specific metrics (for example `math_accuracy`, `pass_at_1`)
- **Token consumption** — total tokens used by the run
- **Baseline comparison** — `baseline_used` / `diff_pp` / `grade` / `conclusion`, comparing the run against an open-source baseline library with tier ratings and a capability radar chart.

## Native Mode

Native Mode loads **local weights** or an **HF model id** for offline evaluation, and supports **LoRA adapters**.

Install the optional dependency first:

```bash
pip install benchscope[accuracy-native]
```

Example:

```bash
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100
```

::: warning
Native mode does **not** force the installation of torch / transformers. It only **detects existing dependencies** and blocks the run if they are not satisfied — install `benchscope[accuracy-native]` to enable it.
:::

## Serving Mode

Serving Mode evaluates through an **OpenAI-compatible pipeline**. The service under test defaults to the **global Provider configuration** when no explicit base URL is given.

```bash
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

This evaluates the exact deployed pipeline — request path, sampling, serving backend — so results reflect production behavior.

## Mock Integration Testing

When no real service is available, use **Mock** mode to verify that the evaluation pipeline itself is wired correctly:

```bash
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

The mock answers with a configurable correctness rate (`--mock-correct-rate`, default `0.7`), letting you sanity-check the whole loop end to end.

## Token Estimation

Before evaluation, you can **estimate the total token consumption** for cost control. The estimator gives a strong estimate plus reminders; after the run, the **actual token statistics** are reported. Use this to size a budget before launching a full evaluation.

## Artifacts

Each evaluation run is saved to `evals/eval-<MMDDhhmmss>/`:

| File | Contents |
| --- | --- |
| `task.json` | Task main table (aligned with the Web accuracy task structure) |
| `result.json` | Accuracy result, including metrics / baseline / conclusion |
| `samples.jsonl` | Per-sample traceability |

Records can be **viewed, packaged, and imported** under **Datas → Evals** in the Web UI.

## Interpreting the Results

- `accuracy` / `pass_rate` — the headline numbers for correctness.
- `dataset_metrics` — how the model performs on the specific scorer (for example `math_accuracy`, `pass_at_1`).
- `benchmark` — comparison against open-source baselines: `baseline_used.name`, `diff_pp`, `grade`, `conclusion`.
- `samples.jsonl` — open it to **locate individual wrong samples** for error analysis.

## Related

- [CLI Reference](../get-started/cli.md) — the `benchscope eval` command
- [Accuracy Evaluation](../tutorials/accuracy-guide.md) — step-by-step tutorial
- [Datas](datas.md) — where accuracy records are stored
- [Settings](settings.md) — providers, models, datasets, and baselines
