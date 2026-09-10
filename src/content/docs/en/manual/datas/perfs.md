---
title: "Performance Record Management"
description: "Datas → Perfs page operations manual: task record list, detail panel (Perf/Cases/Logs info, data panel, statistical charts), and the view / preview / download / copy operations and backend execution logic for run directories and log files."
---

# Performance Record Management

The Perfs page is the core page of Datas, used to **browse all historical performance test records** and drill into each record's configuration, metric data, statistical charts, and log files. The record list sits on the left; the detail panel for the selected record sits on the right.

![BenchScope Datas performance record detail](/images/benchscope-datas-perfs_detail.png)

## 1. Feature Overview

- Left **task records** list: shows all performance run records (runs), ordered by `run_id` descending, with refresh and import support.
- Right **detail panel**: shows the selected record's task info, Perf info, Cases info, Logs info, data panel (Perf Datas), and statistical charts.
- Per-record actions: **Delete**, **Backup**, **Share** (PNG), log **Preview / Download**, run-directory **Copy**.

<div class="info">

**Info:**

The Perfs page only shows **performance** records (`kind=perf`). Accuracy evaluation records also appear in the backend `/api/logs/runs` list, but accuracy artifacts are managed on the [Accuracy page](/en/docs/manual/accuracy/) (the Evals tab is hidden).

</div>

## 2. Page Structure

```
┌───────────────────┬─────────────────────────────────────────────────────┐
│  Records           │  <run_id>                              [Delete][Backup][Share] │
│  [Import][Refresh] │  Task status    Model    Start time    End time        │
│ ┌───────────────┐  ├────────────┬────────────┬───────────────────────────┤
│ │ run-abc...    │  │ Perf Info  │ Cases Info │ Logs Info                 │
│ │ vLLM   Done   │  │ model      │ g0 512/... │ runDir          [Copy]    │
│ │ Qwen   ...    │  │ framework  │ g1  ...    │ summary       [Download]  │
│ ├───────────────┤  │ mode       │            │ Log files:                │
│ │ run-def...    │  │ dataset    │            │  a.log  [Preview][Download]│
│ │ SGLang  ...   │  │ concurrency│            │  b.log  [Preview][Download]│
│ └───────────────┘  │ requests   │            │                           │
│                    ├────────────┴────────────┴───────────────────────────┤
│ (click an item to │  Perf Datas    [Default][Mean][Median][P99]          │
│  to load details) │  [case group tabs]  Metric table ... [Details]       │
│                   ├─────────────────────────────────────────────────────┤
│                   │  Stat Charts  [Linkage][Default][TTFT][TPOT][ITL]    │
│                   │  Throughput / TTFT / TPOT / ITL: 4 rows x 3 charts   │
│                   └─────────────────────────────────────────────────────┘
└───────────────────┴─────────────────────────────────────────────────────┘
```

## 3. Input Parameters and Field Constraints

The Perfs page is **selection-driven** (no form fields); the main interactive parameters are:

| Field | Type | Constraints | Default | Description |
| --- | --- | --- | --- | --- |
| `run_id` | string | Single-level directory name; must not contain `/` `\` `..` | — | Record identifier; can be passed via the URL `?run_id=` for auto-selection |
| `name` (log file) | string | Must be located under the run directory or `logs/` | — | Previews / downloads the specified file |
| `tail` (preview lines) | int | ≥ 1 | 500 | Number of trailing lines returned on preview |
| Data mode `mode` | enum | `default` / `mean` / `median` / `p99` | `default` | Controls the statistical columns shown in the data table |
| Status `status` | enum | `pending` / `running` / `done` / `stopped` / `error` | — | Record run status (read-only display) |
| Task mode `mode` | enum | `concurrency` / `threshold` | — | Concurrency mode / threshold mode (read-only display) |
| `request_rate` | string / number | `inf` or a custom positive number | `inf` | Request rate; `inf` = unlimited |

## 4. Button Operations

### 4.1 Left Record Panel
1. **Import** (upload icon): opens the import drawer to restore a record from a backup zip → see [Import, Export, and Backup](/en/docs/manual/datas/import-export/).
2. **Refresh** (circular icon): re-fetches the record list (`GET /api/logs/runs`).
3. **Click a record item**: loads that record's detail (`GET /api/logs/runs/{run_id}` + `GET /api/logs/runs/{run_id}/live`).

### 4.2 Detail Panel (Row 1)
1. **Delete**: shows a confirmation dialog; on confirm, deletes the entire record (`DELETE /api/logs/runs/{run_id}`).
2. **Backup**: shows a confirmation dialog; on confirm, packages and downloads `{run_id}.zip` (`GET /api/logs/runs/{run_id}/backup`).
3. **Share**: shows a confirmation dialog; on confirm, renders the full detail page as a PNG and downloads it (pure frontend `html2canvas`).

### 4.3 Logs Info Panel
1. **Copy run directory**: copies the `run_dir` path to the clipboard.
2. **Download summary**: downloads `run.summary.xlsx` (falls back to `run.json` when absent).
3. **Preview log file**: opens a dialog showing the tail of the file (`GET .../preview?name=`).
4. **Download log file**: downloads the specified file (`GET .../download?name=`).

### 4.4 Data Panel (Perf Datas)
1. Switch the statistical mode at the top: **Default / Mean / Median / P99**.
2. Switch tabs by case group.
3. Click **Details** at the end of a row: opens a dialog showing that request's Profile Progress / Real-Time Metrics (from the `live` snapshot).

## 5. Execution Steps (Viewing a Record)

1. Navigate to **Datas → Perfs**.
2. Click the target record in the left list (or click **Refresh** first).
3. On the right, review status / model / start–end time in row 1.
4. In row 2, check the Perf / Cases / Logs info in the three panels; you can copy the run directory, and preview or download logs.
5. In row 3 (Perf Datas), switch the statistical mode, browse the metric table by case group, and click **Details** for the live snapshot.
6. In row 4 (statistical charts), turn on **Linkage** and filter by TTFT / TPOT / ITL (see [Data Analysis](/en/docs/manual/datas/analysis/)).

## 6. Backend Execution Logic

| Operation | API | Processing logic |
| --- | --- | --- |
| Load list | `GET /api/logs/runs` | Scans `perfs/`, `evals/` (and the legacy `logs/`) for directories containing `run.json`, attaches terminal logs `logs/{kind}_{run_id}_*.log`, dedupes, and returns in descending `run_id` order |
| Load detail | `GET /api/logs/runs/{run_id}` | Parses `run.json` + lists directory files + attaches terminal logs |
| Load live snapshot | `GET /api/logs/runs/{run_id}/live` | Reads `run_dir/live/*.json` (per-request Profile / Real-Time snapshots) |
| Delete | `DELETE /api/logs/runs/{run_id}` | Deletes the run directory + the corresponding terminal logs |
| Backup | `GET /api/logs/runs/{run_id}/backup` | Packages all files in the run directory + terminal logs into a flat zip and returns it |
| Preview | `GET /api/logs/runs/{run_id}/preview?name=&tail=500` | Text files only; returns the trailing `tail` lines |
| Download | `GET /api/logs/runs/{run_id}/download?name=` | Validates the path, then returns the file |

<div class="tip">

**Tip:**

Record details are read primarily from the on-disk **`run.json`** (which contains all metric keys in `rows[].metrics`, such as `output_mean`, `ttft_p99`, `tpot_median`); the frontend renders the data table and statistical charts from it. Live snapshots are read from **`live/*.json`**.

</div>

## 7. FAQ

**Question: The list is empty or I can't find a certain task?**
Confirm the data root directory has not been cleaned and `BENCHSCOPE_DATA_DIR` has not been switched to another location; you can also use **Import** to restore from a backup (see [Import, Export, and Backup](/en/docs/manual/datas/import-export/)).

**Question: Clicking "Details" shows no real-time metrics?**
The record has no per-request persisted `live/*.json` snapshots (for example, a run not performed with the built-in engine). In that case only the minimal Profile constructed from the row metrics is shown, and Real-Time Metrics is empty / N-A.

**Question: Can I delete a task that is still running?**
The Perfs page deletes the **persisted record** directory; stop a running task on the performance testing page first, then delete it, to avoid file locks.

## 8. Related Docs

- [Datas Manual Overview](/en/docs/manual/datas/) — entry to the Datas module
- [Data Analysis](/en/docs/manual/datas/analysis/) — statistical modes, linkage
- [Import, Export, and Backup](/en/docs/manual/datas/import-export/) — backup / import / share
- [Performance Testing (Reference)](/en/docs/performance/) — metric definitions
- [API Reference](/en/docs/api/) — full `/api/logs/*` routes