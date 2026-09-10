---
title: "Datasets & Modes"
description: "A detailed look at the Accuracy module's 9 built-in evaluation datasets, Serving/Native dual mode, and 4 types of scorers, including input parameters, field constraints, and backend logic."
---

# Datasets & Modes

In accuracy evaluation, the **dataset** determines what is evaluated, the **mode** determines how inference runs, and the **scorer** determines how correctness is judged. All three are configured in the creation wizard's **Step 1 (Dataset selection)** and **Step 2 (Mode & Model)**.

<div class="info">

**Info:**

**There are 9 built-in datasets in total** (all with `eval` metadata); plus 3 performance datasets (sharegpt / alpaca / dolly) that are used exclusively for performance testing and do not appear in the accuracy wizard.

</div>

## 1. Page Structure

- **Step 1 dataset panel**: dataset source (builtin / local JSONL) → dataset dropdown → metadata (category accDatasetCat / scorer accDatasetScorer / samples accDatasetSize / download status) → preview dataset (accPreviewBtn) → sample limit (accLimit).
- **Step 2 mode panel**: test mode (accModes, Serving link accModeServing / Native accModeNative) → eval engine (accEngine) → (Serving) inference Provider (accProvider).

```
┌──────────────────────────────────────────────────────────┐
│ Step 1: Dataset panel                                    │
│  Dataset source (builtin / local JSONL)                  │
│  → Dataset dropdown → Metadata (category / scorer /      │
│    samples / download status) → Preview → Sample limit   │
├──────────────────────────────────────────────────────────┤
│ Step 2: Mode panel                                       │
│  Test mode (Serving link / Native) → Eval engine         │
│  → (Serving) Inference Provider                          │
└──────────────────────────────────────────────────────────┘
```

## 2. Input Parameters

| Field | Identifier | Type | Default | Description |
| --- | --- | --- | --- | --- |
| Dataset source | `accDatasetSource` | Radio `builtin`/`path` | `builtin` | Built-in eval datasets / local JSONL path |
| Eval dataset | `datasetId` | Dropdown (searchable) | — | Required for builtin; candidates are the 9 built-in + imported custom datasets |
| Local JSONL path | `datasetPath` | Input | — | Required for local; must be an existing valid JSONL |
| Sample limit | `limit` | Number | `0` | 0 = full dataset; seeded sampling is reproducible |
| Test mode | `mode` | Radio `serving`/`native` | `serving` | Serving link / Native |
| Eval engine | `engineId` | Dropdown | `benchscope` | With `eval` capability: benchscope / native-hf / mock |
| Inference Provider | `providerId` | Dropdown | Active provider | Shown only for `serving` |

## 3. Field Constraints

| Field | Required | Constraint / Enum |
| --- | --- | --- |
| `datasetId` | Required for built-in source | One of the 9 built-in ids or an imported custom id |
| `datasetPath` | Required for local source | Existing valid JSONL; standard fields `question`/`answer` (optional `choices`/`subject`, code-style `prompt`/`test`/`entry_point`, dialogue-style `turns`) |
| `limit` | Optional | Integer ≥ 0, 0 = full dataset |
| `mode` | Required | Enum `serving` / `native` |
| `engineId` | Required | Engine with `eval` capability; disabled when the environment check is FAIL |

<div class="warning">

**Warning:**

**MT-Bench (`mt-bench`) has the `judge` scorer**: the judge model must be invoked via the Serving link, so this dataset **only supports Serving mode**; Native mode will report "Native mode does not support judge datasets yet".

</div>

## 4. Built-in Datasets (9)

| id | Name | Category | Scorer | Primary metric | Samples |
| --- | --- | --- | --- | --- | --- |
| `mmlu` | MMLU | knowledge | `choice` | `accuracy` | 14079 |
| `cmmlu` | CMMLU | knowledge | `choice` | `accuracy` | 11960 |
| `c-eval` | C-Eval | knowledge | `choice` | `accuracy` | 13480 |
| `gsm8k` | GSM8K | math | `math` | `exact_match` | 7473 |
| `math` | MATH | math | `math` | `exact_match` | 5000 |
| `humaneval` | HumanEval | code | `code` | `pass@1` | 164 |
| `mbpp` | MBPP | code | `code` | `pass@1` | 974 |
| `mt-bench` | MT-Bench | conversation | `judge` | `mt_bench` | 80 |
| `gaokao-bench` | GAOKAO-Bench | comprehensive | `choice` | `accuracy` | 2000 |

## 5. Serving / Native Dual Mode

| Dimension | Serving link | Native |
| --- | --- | --- |
| `mode` value | `serving` | `native` |
| Typical engines | `benchscope` / `mock` | `native-hf` |
| Inference method | Real service link — inference requests are proxied to the active Provider's OpenAI-compatible API | Load model weights locally for offline inference (transformers) |
| Environment dependencies | None (only a reachable Provider is required) | `torch` + `transformers` (+ CUDA), `pip install 'benchscope[accuracy-native]'` |
| Token statistics | Yes (usage collected per request; missing values approximated by chars/4) | No (capability boundary) |
| Token estimation | Yes (strong reminder before start) | Always 0 |
| LoRA | `loraName` requests the server-registered adapter | `loraPath` loaded via peft merge |
| Suitable for | Online services / remote model acceptance | Local weights / no-server scenarios |

## 6. Scorers (4)

| Scorer | Applicable datasets | Scoring logic | Result status |
| --- | --- | --- | --- |
| `choice` | mmlu / cmmlu / c-eval / gaokao-bench | Multi-strategy extraction of the option letter (A–H), compared against the reference answer | correct / wrong (knowledge error) / invalid (format error) |
| `math` | gsm8k / math | Extract the final answer (`\boxed{}` / explicit marker / last-line number), normalize, then compare for equivalence | correct / wrong (reasoning error) / invalid (format error) |
| `code` | humaneval / mbpp | Extract the code, execute in a restricted subprocess sandbox (`-I` isolated, 10s timeout), all test cases must pass | correct / wrong (execution error) / invalid (format error) |
| `judge` | mt-bench | LLM-as-judge scores each turn (1–10 + helpfulness/truthfulness/harmlessness), mean ≥ 6 is judged correct | correct / wrong / invalid (judgment failure) |

## 7. Operation Steps (Button Operations)

1. Enter Step 1 of the creation wizard and select the **dataset source** (default is builtin).
2. For builtin: choose one of the 9 built-in datasets from the dropdown and verify category / scorer / samples / download status; when not yet downloaded, "Auto-download on start" is shown.
3. For local: fill in the JSONL path (it must exist on a server-accessible path).
4. (Optional) Click **Preview** to view the first 5 samples and confirm the field mapping is correct.
5. Set the **sample limit** (sampling is recommended for large sample sizes, e.g. `limit=200`).
6. In Step 2, select the **test mode** and the **eval engine**; (Serving) select the Provider.
7. Click **Next** to enter preview & start.

## 8. Backend Execution Logic

- **Dataset list**: `GET /api/accuracy/datasets` reads all entries with an `eval` section in `configs/datasets.yaml` + imported custom datasets under `datasets_dir/eval_custom/`, and marks the `downloaded` status.
- **Dataset preview**: `POST /api/accuracy/datasets/preview` resolves the reference → normalizes samples (`standardize_samples`) → filters evaluable samples (`filter_samples`) → builds prompts, returning the first 5.
- **Engine environment check**: `GET /api/accuracy/engines/{id}/env-check` validates the engine's `requires` dependencies; `native` adds a `torch.cuda.is_available()` check.
- **Download cache**: built-in datasets are downloaded to `datasets_dir/<id>/` on first evaluation according to `source` (modelscope / url); `.json` is automatically converted to `.jsonl`, and the artifact is verified to be parseable (to prevent an error page from being treated as a dataset).
- **Scoring routing**: `run_eval` fetches the corresponding scorer from the scorer registry based on the dataset's `eval.scorer`; unknown names fall back to `math`.

## 9. FAQ

**Question: How do I add a custom dataset?**
Two ways: ① reference a local JSONL path directly (`datasetPath`); ② upload and import via `POST /api/accuracy/datasets/import`, persisted to `datasets_dir/eval_custom/`. Standard fields `question`/`answer`, optional `choices`/`subject`.

**Question: What happens if a dataset has not been downloaded?**
The backend auto-downloads it on the first evaluation (ModelScope preferred); while downloading, the "Auto-download on start" tag is shown; if the download fails, the task is set to `error`.

**Question: Can Serving and Native results be compared directly?**
The two use different inference chains (online API vs local weights); the metric definitions are consistent but the values may differ. It is recommended to compare the same model in the same mode, or to use the "Native vs Serving consistency" comparison capability to verify.

**Question: How is the scorer determined?**
It is bound by the dataset's `eval.scorer` (fixed for built-in datasets); for custom datasets it is auto-detected from the sample fields (choices→choice / test→code / turns→judge / default math).