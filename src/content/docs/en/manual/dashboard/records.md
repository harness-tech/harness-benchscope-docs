---
title: "Test Records"
description: "Dashboard test records panel: the latest 8 performance test records, column field and status enum constraints, Detail / More / Refresh button operations, and Perf request details and file downloads on the Datas/Perfs detail landing page."
---

# Test Records

The second row of the Dashboard is the full-width **Test Records** panel (card title displayed as **Perf Records**, i18n key `perfTestRecords`), listing the **latest 8** performance test records: no pagination, no search box, read-only display. Clicking **Detail** jumps to Datas → Perfs to view request details and download files.

## 1. Feature Description

- Displays the Run ID, model, framework, status, and start time of the latest 8 performance records.
- Provides three entry points: an inline **Detail** per row (jumps to the corresponding task detail), a header **More** (full record list), and a header **Refresh** (re-fetches data).
- Accuracy records (`kind = eval`) are filtered out on the frontend and are not shown in this panel; the Eval Records panel is currently hidden.

<div class="warning">

**Warning:**

This panel only lists **performance** records. The Datas sub-nav currently has only two tabs, Perfs and Analysis (the Evals tab is hidden; the `/datas/evals` route redirects to `/datas/perfs`). Manage accuracy test tasks and results on the Accuracy page.

</div>

## 2. Page Structure

```
┌────────────────────────────────────────────────────────────────────┐
│ Perf Records (perfTestRecords)        [Refresh] [More]             │
├────────────────────────────────────────────────────────────────────┤
│ Run ID    │ Model       │ Framework │ Status │ Time     │ Detail   │
│ run-2026… │ deepseek-…  │ vLLM      │ Done   │ 09-09 …  │ Detail   │
│ run-2025… │ qwen-…      │ SGLang    │ Running│ 09-08 …  │ Detail   │
│ (max 8 rows, no pagination, no search box)                         │
├────────────────────────────────────────────────────────────────────┤
│                               *Only the latest 8 records are shown │
└────────────────────────────────────────────────────────────────────┘
```

- The top-right of the card header holds two text buttons: **Refresh** (with a reload icon, i18n key `refresh`) and **More** (i18n key `more`).
- Each table row carries one text button: **Detail** (i18n key `detail`).
- The footer right side shows the fixed hint `*Only the latest 8 records are shown` (i18n key `latest8Hint`).

## 3. Input Parameters and Field Constraints

### 3.1 Input Parameters

| Field | i18n key | Type | Required | Constraints | Description |
| --- | --- | --- | --- | --- | --- |
| Model search | `searchModel` | Text input (reserved) | Optional | Placeholder `Search model...`; **not rendered** in the current version | `en.js` reserves this placeholder to filter records by model name; the current test records panel is a pure read-only table with no search box |

The panel has no other input fields: records are returned by the backend in one shot, with no query parameters, no pagination, and no sorting controls.

### 3.2 Displayed Column Constraints

| Column | Returned field | Constraints / enum |
| --- | --- | --- |
| Run ID | `run_id` | Record directory name, globally unique; column width 140 px, truncated beyond 40 characters on the detail page |
| Model | `meta.model` | Model name recorded in `run.json`; displays `-` when missing |
| Framework | `meta.framework` | `framework_name` in `run.json`; `vLLM` is displayed in blue, others (e.g. `SGLang`) in purple; displays `-` when missing |
| Status | `meta.status` | Enum `pending` / `running` / `done` / `stopped` / `error`; `done` → Done (green), `error` → Error (red), `stopped` → Stopped (orange), `running` and `pending` → Running |
| Time | `meta.started_at` | Start time (`YYYY-MM-DD HH:MM:SS`); displays `-` when missing |
| Detail | — | Text button, navigates to `/datas/perfs?run_id=<run_id>` and auto-selects that task |

## 4. Operation Steps

1. Open the Dashboard (route `/dashboard`); the test records panel automatically loads the latest 8 performance records.
2. **View details**: click **Detail** on a row → jumps to Datas → Perfs and auto-selects that task (the URL becomes `/datas/perfs?run_id=<run_id>`).
3. **View the full list**: click the header **More** → jumps to `/datas/perfs` (the full record list on the left; any task can be opened).
4. **Refresh**: click the header **Refresh** → re-fetches `GET /api/logs/runs` and `GET /api/dashboard/stats`, updating the table and the Statistics Overview.
5. **Perf request detail** (Datas/Perfs page): in the **Perf Datas** panel, click the detail action on a request row → the **Perf Request Detail** (`perfDetail`) dialog opens, showing that request's Profile Progress / Real-Time Metrics.
6. **Download** (Datas/Perfs page): in the **Logs Info** box, click the download icon on the **Summary** row (prefers `run.summary.xlsx`, falling back to `run.json` when missing) or on any log file row → the browser downloads the corresponding file.

<div class="tip">

**Tip:**

The current Dashboard does not offer a search by model name. To find records for a given model, click **More** to open the full list under Datas → Perfs (in descending Run ID order), or scan the Model column in the list.

</div>

## 5. Backend Execution Logic

### 5.1 Panel Load (page open / **Refresh** click)

| Order | Frontend | Backend | Description |
| --- | --- | --- | --- |
| 1 | `loadRuns()` | `GET /api/logs/runs` | The backend iterates `~/.benchscope/perfs` and `~/.benchscope/evals` (legacy subdirectories under `~/.benchscope/logs` are included as well when they contain a `run.json`), reads each directory's `run.json`, and returns `runs[]` sorted by `run_id` descending |
| 2 | Frontend filter | — | Filters out accuracy records with `meta.kind === 'eval'` or a `dir` containing `/evals`, and renders the table with the first 8 |
| 3 | `loadStats()` | `GET /api/dashboard/stats` | Synchronously refreshes the performance / accuracy counters in the Statistics Overview |

`GET /api/logs/runs` returns the following for each record: `run_id` (directory name), `dir` (absolute path), `files[]` (all files in the directory + terminal logs `{kind}_{run_id}_*.log` under `~/.benchscope/logs/`), and `meta` (kind / framework / model / status / started_at / finished_at / summary).

### 5.2 **Detail** Navigation

`router.push({ path: '/datas/perfs', query: { run_id } })` → Datas/Perfs' `onMounted` runs `loadRuns()` first, then `selectRunFromQuery`:

1. `GET /api/logs/runs/{run_id}` → returns `{run_id, dir, files[], run}` (the full `run.json`), rendering Perf Info / Cases Info / Logs Info / Perf Datas / statistics charts.
2. `GET /api/logs/runs/{run_id}/live` → reads the per-request persisted real-time snapshots in `run_dir/live/*.json`, indexed by `reqKey` (label/case + case_id + concurrency), used by the Perf request detail.

### 5.3 Perf Request Detail (`perfDetail`)

Clicking a request row's detail triggers `openDetail(row)`:

- If the row has a `live` snapshot: the snapshot's Profile Progress / Real-Time Metrics are shown directly.
- If not (e.g. a run of a non-builtin engine): a minimal snapshot is constructed from that row's `metrics` (benchmark_duration, successful/failed requests, req_per_s, output_mean), and Real-Time Metrics is displayed empty.

### 5.4 File Download

- **Single file**: the frontend runs `window.open('/api/logs/runs/{run_id}/download?name=<filename>')` → the backend `FileResponse` returns the original file.
- **Summary**: prefers `run.summary.xlsx`; if `run.json` has no `summary.xlsx`, `run.json` is downloaded instead.
- **Full backup**: the **Backup** button in the Datas/Perfs header → `GET /api/logs/runs/{run_id}/backup`, which packs the run directory + terminal logs into a zip for download (the zip can be restored via the **Import Record** entry).

## 6. FAQ

**Question: Why are only 8 records shown?**

The panel footer states `*Only the latest 8 records are shown` explicitly. The frontend takes the first 8 records in descending `run_id` order, with no pagination. Use **More** to reach the full list under Datas → Perfs.

**Question: Why can't I see accuracy test records?**

The test records panel lists performance records only: records with `kind = eval` are filtered out on the frontend. The Eval Records panel and the Evals tab in Datas are currently hidden (the `/datas/evals` route redirects to `/datas/perfs`). Manage accuracy tasks and results on the Accuracy page.

**Question: Why does the status display as "Running"?**

The status enum is `pending` / `running` / `done` / `stopped` / `error`; the frontend displays both `pending` and `running` as **Running**, and `done` / `error` / `stopped` as **Done** / **Error** / **Stopped** respectively.

**Question: Is there a search box to filter by model name?**

Not rendered in the current version: the `searchModel` key in `en.js` (placeholder `Search model...`) is a reserved item. Click **More** to open Datas → Perfs and locate the target model manually via the Model column.

**Question: Where do I download result files?**

The Dashboard panel itself has no download button. After **Detail** jumps to Datas → Perfs, click the download icon on the summary or a log file in the **Logs Info** box, or use the header **Backup** button to download all files as a package.