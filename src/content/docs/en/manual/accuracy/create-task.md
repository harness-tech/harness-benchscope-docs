---
title: "Create an Evaluation Task"
description: "A step-by-step guide to the Accuracy three-step creation wizard: dataset selection → mode & model → preview & start, covering input parameters, field constraints, button operations, and backend execution logic."
---

# Create an Evaluation Task

The entry point for creating an accuracy task is the **Create Accuracy Task (accCreateTask)** button in the top-right of the accuracy page (the primary button on the intro page). After entering `/accuracy/create`, you see a **three-step wizard** (`AccuracyCreateView.vue`) completed in this order: "Dataset selection → Mode & model → Preview & start".

<div class="info">

**Info:**

**Step bar**: the top of the page is an `a-steps` three-step bar (accStepDataset / accStepModel / accStepPreview); the bottom action bar shows "Previous / Next / Start accuracy evaluation task" depending on the current step.

</div>

## 1. Page Structure

```
┌──────────────────────────────────────────────────────────┐
│ [Create Accuracy Task]                        [Back]     │
│  ① Dataset ──── ② Mode & Model ──── ③ Preview & Start   │
├──────────────────────────────────────────────────────────┤
│  Step 1: Dataset source (builtin/local JSONL) + dataset  │
│          + meta (category/scorer/samples/download status)│
│          + sample limit                                  │
│  Step 2: Test mode + eval engine + Provider + model      │
│          + LoRA + seed/temperature/top_p/maxTokens/      │
│          concurrency + judge model                       │
│  Step 3: Parameter summary + equivalent CLI command      │
│          + token consumption estimate reminder           │
├──────────────────────────────────────────────────────────┤
│                                  [Previous] [Next/Start] │
└──────────────────────────────────────────────────────────┘
```

## 2. Input Parameters

### 2.1 Step 1 — Dataset (accStepDataset)

| Field | Identifier | Type | Default | Description |
| --- | --- | --- | --- | --- |
| Dataset source | `accDatasetSource` | Radio `builtin`/`path` | `builtin` | Built-in eval datasets (accDatasetBuiltin) / local JSONL path (accDatasetPath) |
| Eval dataset | `datasetId` | Dropdown (searchable) | — | Required when source is builtin; candidates come from `GET /api/accuracy/datasets` |
| Category / Scorer / Samples | `accDatasetCat`/`accDatasetScorer`/`accDatasetSize` | Read-only | — | Shown after selection: `category_name` / `eval.scorer` / `total_samples` |
| Download status | `accDatasetReady`/`accDatasetNeedDownload` | Read-only tag | — | Cached download (green) / auto-download on start (orange) |
| Local JSONL path | `datasetPath` | Input | — | Required when source is local; must be an existing valid JSONL |
| Sample limit | `limit` | Number | `0` | 0 = full dataset; sampling is seeded and reproducible |

After selecting a dataset, you can click **Preview** (`accPreviewBtn`) to view the first 5 samples (question `accDatasetQuestion` / Prompt `accPromptCol` / reference answer `accAnswerCol`).

### 2.2 Step 2 — Mode & Model (accStepModel)

| Field | Identifier | Type | Default | Description |
| --- | --- | --- | --- | --- |
| Test mode | `mode` | Radio `serving`/`native` | `serving` | Serving link (accModeServing) / Native (accModeNative) |
| Eval engine | `engineId` | Dropdown | `benchscope` | Only engines with `eval` capability are listed (benchscope / native-hf / mock) |
| Inference Provider | `providerId` | Dropdown | Active provider | Shown only for `serving`; candidates come from `GET /api/providers` |
| Model under test | `model` | Dropdown / Input | — | Vendor catalog (accModelCatalog) or custom (accModelCustom), required |
| LoRA model path | `loraPath` | Input | — | Optional; merged via peft on Native, requests the server-side adapter on Serving |
| LoRA server-side name | `loraName` | Input | — | Optional, `serving` only; request name of the server-registered adapter |
| Seed | `seed` | Number | `1234` | Random seed for sampling and generation |
| Temperature | `temperature` | Number | `0.0` | Sampling temperature |
| top_p | `topP` | Number | `1.0` | Nucleus sampling probability |
| Max output tokens | `maxTokens` | Number | `512` | Max output tokens per sample |
| Concurrency | `concurrency` | Number | `4` | Shown only for `serving` |
| Judge model | `judgeModel` | Input | — | Shown when the selected dataset's scorer is `judge` (MT-Bench) |

### 2.3 Step 3 — Preview & Start (accStepPreview)

Read-only summary plus hint blocks:

- **Parameter summary**: dataset / mode / engine / model / LoRA / `seed · temp · top_p · max`.
- **Equivalent CLI command (accCmdHint)**: copyable `benchscope eval --engine <id> --model <m> --dataset <ds> [--lora-path] [--lora-name] [--limit] [--seed] [--judge-model]`.
- **Token consumption estimate reminder (accEstimateTitle, serving only)**: currently selected dataset (accEstimateDataset), estimated total tokens for this evaluation (accEstimateTotal), input (accEstimateIn) / output (accEstimateOut), sample count and basis (accEstimateSamples).

## 3. Field Constraints

| Field | Required | Constraint / Enum | Default |
| --- | --- | --- | --- |
| `datasetId` | Required for built-in source | Enum: built-in or imported custom dataset id | — |
| `datasetPath` | Required for local source | Must exist and be a valid JSONL | — |
| `limit` | Optional | Integer ≥ 0 | 0 |
| `mode` | Required | Enum `serving` / `native` | serving |
| `engineId` | Required | Engine with `eval` capability; disabled when the environment check is FAIL | benchscope |
| `providerId` | Required for `serving` | An existing Provider | Active provider |
| `model` | Required | Non-empty string | — |
| `loraPath` / `loraName` | Optional | Path / name (`loraName` only for `serving`) | — |
| `seed` | Optional | Integer | 1234 |
| `temperature` | Optional | 0 – 2, step 0.1 | 0.0 |
| `topP` | Optional | 0 – 1, step 0.1 | 1.0 |
| `maxTokens` | Required | Integer ≥ 1 | 512 |
| `concurrency` | Optional for `serving` | Integer ≥ 1 | 4 |
| `judgeModel` | Conditionally required | Required when scorer=`judge` and mode is `serving` | — |

## 4. Operation Steps

**Enter the wizard**
1. On the accuracy page, click the **Create Accuracy Task** button to enter `/accuracy/create`.

**Step 1 — Dataset**
2. Select the **dataset source**: default is "Built-in eval datasets"; for local data, switch to "Local JSONL path".
3. For builtin: select the **eval dataset** and verify category / scorer / samples / download status; for local: fill in the JSONL path.
4. (Optional) Click **Preview** to view the first 5 samples.
5. Fill in the **sample limit** (0 = full dataset).
6. Click **Next** (the button is disabled if no dataset is selected).

**Step 2 — Mode & Model**
7. Select the **test mode**: Serving link (default) / Native.
8. Select the **eval engine** (switching triggers the environment check).
9. (Serving) Select the **inference Provider**.
10. Select the **model under test** (vendor catalog / custom).
11. (Optional) Fill in the LoRA path; (Serving, optional) fill in the LoRA server-side registration name.
12. Set seed / temperature / top_p / max output tokens; (Serving) set the concurrency.
13. (MT-Bench) Fill in the **judge model**.
14. Click **Next**.

**Step 3 — Preview & Start**
15. Verify the parameter summary and the **equivalent CLI command** (can be copied and executed).
16. (Serving) View the **token consumption estimate reminder**.
17. Click **Start accuracy evaluation task**; (Serving with estimate > 0) click **Confirm & Start (accReminderConfirm)** in the dialog.
18. After a successful start, you automatically return to the accuracy task list page, and the task enters the running state.

## 5. Backend Execution Logic

**Page load (onMounted)**: fires 4 requests in parallel — `GET /api/accuracy/datasets` (datasets), `GET /api/accuracy/engines` (engines, filtered by `eval`), `GET /api/providers` (Providers), `GET /api/model-catalog` (vendor model catalog).

**Interaction triggers**:

| Action | API |
| --- | --- |
| Preview dataset | `POST /api/accuracy/datasets/preview` (`{id}` or `{path}`) |
| Switch engine | `GET /api/accuracy/engines/{engine_id}/env-check` |
| Enter Step 3 (serving) | `GET /api/accuracy/estimate` (`dataset_id`/`path`/`limit`/`mode`/`max_tokens`) |

**Start (`POST /api/accuracy/tasks`)**:
1. Parameter validation: `model` must be non-empty; either `dataset.id` or `dataset.path` is required.
2. Dataset validation: `path` must exist; `id` must be registered (builtin or imported).
3. `create_task()`: generate `task_id` (`eval-MMDD-HHMMSS`), determine mode by engine capability (native-hf→native, otherwise→serving), persist `task.json` + `run.json`.
4. `start_task()`: set to `running`; (serving) run token estimation first; start a daemon thread.
5. `run_eval()` inside the thread: load samples → build prompts → batch inference (serving via aiohttp concurrency / native via transformers) → scoring → metrics aggregation → baseline benchmarking → conclusion.
6. Push `eval_task_log` / `eval_task_progress` / `eval_task_result` in real time over WebSocket.
7. On completion, persist `result.json` / `samples.jsonl` and set the status.

## 6. FAQ

**Question: Why is the "Next" button grayed out?**
It is disabled when no dataset is selected in Step 1, or no model is filled in in Step 2 (for MT-Bench under Serving, the judge model is also required); when an engine's environment check is FAIL, that engine is also disabled.

**Question: What should I do if Native mode reports that the environment check did not pass?**
The Native engine requires `torch` + `transformers` (and detects CUDA). Install with `pip install 'benchscope[accuracy-native]'` and re-enter the wizard, or switch to Serving mode.

**Question: What is the equivalent CLI command for?**
The `benchscope eval` command generated in Step 3 shares the same evaluation core as the Web task; copy it and run it directly in the terminal — handy for scripting and reproduction.

**Question: Does the token estimation reminder appear in Native mode?**
No. Native mode has no online serving consumption, so the estimate is always 0 and no confirmation dialog is shown at start.