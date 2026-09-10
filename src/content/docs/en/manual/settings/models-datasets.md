---
title: Models and Datasets Management
description: 'Operations manual for the Settings "Models" and "Datasets" panels: browsing the model-vendor catalog, downloading and caching built-in datasets, input parameters, and backend execution logic.'
---

# Models and Datasets Management

The **Models** panel (menu key `modelsTab`) provides a **model-vendor catalog** (grouped into Domestic / International, read-only browsing); the **Datasets** panel (menu key `datasetsTab`) provides the **built-in dataset cache** (12 in total: 9 accuracy + 3 performance, each downloadable to the local cache directory with one click).

## 1. Feature Overview

- **Model-vendor catalog**: browse the model vendors supported by vLLM (Domestic / International); click a vendor to view its model cards (description / precision / link / download command). Data comes from the backend `GET /api/config/model-catalog` (`benchscope/configs/models.yaml`).
- **Model-card details**: The frontend matches the model name against the built-in model catalog (`web/src/data/modelCatalog.js`, 6 commonly used models) and displays the introduction, supported data precision, access link, and download command; models not listed show "No catalog details available for this model".
- **Built-in dataset cache**: click to download a built-in dataset, which is cached into the `~/.benchscope/datasets` directory (`datasets_dir`, viewable in [General Settings](/en/docs/manual/settings/general/)).
- **Cache status**: Each dataset card shows a Cached (`datasetCached`, green) / Not cached (`datasetNotCached`) badge.

<div class="info">
**Info:** Both panels are **read-only browsing + single-button operations** and offer no form inputs; model catalog data comes from `benchscope/configs/models.yaml`, and the dataset cache directory is `datasets_dir` (default `~/.benchscope/datasets`, viewable in [General Settings](/en/docs/manual/settings/general/)).
</div>

## 2. Page Structure

```
[Models panel]                              [Datasets panel]
+--------------------------------------+  +--------------------------------------+
| Model-vendor catalog (builtinModels) |  | Built-in datasets (builtinDatasets)  |
| Browse vLLM-supported vendors...     |  | Click to download datasets...        |
| [Domestic] [International] (groups)  |  | (datasetsHint)                       |
| (vendor chips, selected = highlight) |  | [All] [Chat] [Instruction] [Math]    |
+--------------------------------------+  | [Acc.Knowledge] [Acc.Math] ...       |
| Vendor title (e.g. DeepSeek)         |  +--------------------------------------+
| + Model cards (one per model) +      |  | Dataset cards (one per dataset,      |
| | DeepSeek-V3          [Details] |   |  | full-page scroll)                    |
| | Introduction...                 |   |  | + MMLU        [Cached/Not cached]   |
| | Supported precision [BF16]...   |   |  | | [Download]                        |
| | Access link  https://...        |   |  | | Description...                    |
| | Download cmd huggingface...     |   |  | | Access link https://modelscope... |
| +---------------------------------+   |  | | Download cmd modelscope download..|
+--------------------------------------+  | +------------------------------------+
                                          +--------------------------------------+
```

| Area | Control | Description |
| --- | --- | --- |
| Models - Category bar | Group titles (Domestic / International) + vendor chips | Click a vendor chip to switch the model list below (the first vendor is selected by default) |
| Models - Model card | Name, details link, introduction, precision tag, access link, download command (copyable) | Shows a muted hint when no catalog entry matches |
| Datasets - Category bar | "All" + 8 category chips (with counts) | Click a chip to filter the dataset cards below |
| Datasets - Dataset card | Name, Cached/Not-cached tag, download button, description, access link, download command (copyable) | The download button enters a loading state and the status refreshes when it finishes |

## 3. Input Parameters

Both panels are **read-only browsing + single-button operations** with no form inputs; the only explicit parameter is the dataset id of the download API:

| Endpoint | Parameter | Type | Constraint | Description |
| --- | --- | --- | --- | --- |
| `GET /api/config/model-catalog` | None | — | — | Returns the model-vendor catalog `groups` |
| `GET /api/config/datasets` | None | — | — | Returns `categories` + `datasets` (including cache status) |
| `POST /api/config/datasets/download` | `id` | String | Required; enum of the 12 built-in dataset ids (see table below) | Downloads the given dataset to `datasets_dir/<id>/` |

**12 built-in datasets** (9 accuracy + 3 performance):

| id | Name | Category | Type | Download source |
| --- | --- | --- | --- | --- |
| `mmlu` | MMLU | `accuracy-knowledge` | Accuracy | ModelScope (`opencompass/mmlu`) |
| `cmmlu` | CMMLU | `accuracy-knowledge` | Accuracy | ModelScope (`opencompass/cmmlu`) |
| `c-eval` | C-Eval | `accuracy-knowledge` | Accuracy | ModelScope (`opencompass/ceval-exam`) |
| `gsm8k` | GSM8K | `accuracy-math` | Accuracy | HuggingFace URL (`openai/gsm8k`) |
| `math` | MATH | `accuracy-math` | Accuracy | ModelScope (`opencompass/math`) |
| `humaneval` | HumanEval | `accuracy-code` | Accuracy | ModelScope (`opencompass/humaneval`) |
| `mbpp` | MBPP | `accuracy-code` | Accuracy | ModelScope (`opencompass/mbpp`) |
| `mt-bench` | MT-Bench | `accuracy-chat` | Accuracy | ModelScope (`opencompass/mt_bench`) |
| `gaokao-bench` | GAOKAO-Bench | `accuracy-mix` | Accuracy | ModelScope (`opencompass/gaokao-bench`) |
| `sharegpt` | ShareGPT | `chat` | Performance | ModelScope (`gliang1001/ShareGPT_V3_unfiltered_cleaned_split`) |
| `alpaca` | Alpaca | `instruction` | Performance | HuggingFace URL (`tatsu-lab/alpaca`) |
| `dolly` | Dolly | `instruction` | Performance | HuggingFace URL (`databricks/databricks-dolly-15k`) |

The 8 category chips are: `chat` (Chat), `instruction` (Instruction Tuning), `math` (Math Reasoning), `accuracy-knowledge` (Accuracy - Knowledge), `accuracy-math` (Accuracy - Math), `accuracy-code` (Accuracy - Code), `accuracy-chat` (Accuracy - Chat), `accuracy-mix` (Accuracy - Mixed).

## 4. Operating Steps

### 4.1 Browsing the Model-Vendor Catalog

1. Click **Models** in the left menu.
2. In the category bar, select a group (Domestic / International) and click a vendor chip (e.g. DeepSeek, Qwen, OpenAI).
3. Review the model cards under that vendor: click **Details** to jump to the model homepage (new tab); click the copy icon next to the download command to copy the `huggingface-cli download ...` command; the access link is also clickable.
4. Switch vendor chips to reload the corresponding model list.

### 4.2 Downloading Built-in Datasets

1. Click **Datasets** in the left menu.
2. In the category bar, select "All" or a specific category chip to filter the list.
3. On the target dataset card, click the **Download** button in the top-right corner (the button enters a loading state).
4. When the download finishes, the card badge changes from Not cached to Cached (green); you can click Download again to overwrite and refresh.
5. To import offline, copy the download command at the bottom of the card (e.g. `modelscope download --dataset opencompass/mmlu --local_dir ./mmlu`) and run it in a server terminal.

## 5. Backend Execution Logic

### 5.1 Loading the Vendor Catalog

`GET /api/config/model-catalog` → the backend reads `benchscope/configs/models.yaml` with `yaml.safe_load` and returns `{"groups": [{key: "cn"|"intl", name_zh, name_en, providers: [{key, name, homepage, models: [...]}]}]}`; a missing file returns 404, a parse failure returns 500. The frontend selects the first vendor by default.

### 5.2 Loading Datasets and Cache Status

`GET /api/config/datasets` → the backend:

1. Parses `benchscope/configs/datasets.yaml` via `load_builtin_datasets()` (12 dataset definitions + 8 categories).
2. Calls `dataset_status(ds, cache_root)` for each dataset: checks whether `datasets_dir/<id>/` exists and produces `status: {cached: bool}`.
3. Returns `{"categories": [...], "datasets": [{id, name, category, description, url, download, status: {cached}}]}`.

### 5.3 Downloading a Dataset

`POST /api/config/datasets/download` (body `{"id": "mmlu"}`) → the backend calls `download_builtin_dataset(ds, state.config.datasets_dir)`:

| Source type (`source.type`) | Handling |
| --- | --- |
| `modelscope` | Downloads `source.dataset_id` from ModelScope into `datasets_dir/<id>/` |
| `url` | Fetches files from `source.url` into `datasets_dir/<id>/` |

- An unknown `id` returns **404**; a download error returns **502** (the detail includes the reason).
- On success, the frontend re-runs `loadDatasets()` to refresh the cache status.

## 6. Frequently Asked Questions

**Question: Where are datasets cached?**

In `datasets_dir`, which defaults to `~/.benchscope/datasets`; each dataset occupies one subdirectory (`datasets_dir/<id>/`). The directory is viewable in the cache-path panel of [General Settings](/en/docs/manual/settings/general/) (read-only, follows Root Dir).

**Question: Can the Models panel add or remove models?**

No. The Models panel is a **read-only vendor catalog** (data from `benchscope/configs/models.yaml`) with no add/remove entry points; to add model details you must edit the yaml file. Actual model usage (load testing / accuracy evaluation) is chosen on the new-task page; see [Performance Testing](/en/docs/performance/) and [Accuracy Testing](/en/docs/accuracy/).

**Question: A dataset shows "Not cached" but the download command can be copied — what is the relationship?**

"Cached / Not cached" only reflects whether the local `datasets_dir/<id>/` exists; the "download command" is for manual downloading in a server terminal (e.g. when the intranet cannot reach the WebUI). Clicking **Download** in the WebUI and running the download command have the same effect — both land in `datasets_dir/<id>/`.