---
title: "View & Export Results"
description: "BenchScope performance results: Realtime Data table (24 columns / 13 by default), Best/BestPerf marking, 12 stat charts, Excel and log export, backend artifacts."
---

# View & Export Results

While a task is running (or after it finishes), you can view results in row 3 (Realtime Data) and row 4 (Statistics) of the performance page, and export Excel / log files.

## 1. Page Structure

```
┌──────────────────────────────────────────────────────────────────┐
│ Row 3  Realtime Data   [TPOT: 100ms] [Output: 0 tok/s] local thr │
│        Grouped table (group header row + data rows)              │
│        Table footer: [n rows] [Column settings ▾] [Download]     │
├──────────────────────────────────────────────────────────────────┤
│ Row 4  Statistics  [linkage toggle]   12 stat charts             │
│        (4 groups × 3 statistics)                                 │
└──────────────────────────────────────────────────────────────────┘
```

## 2. Results Table (Realtime Data)

The table is grouped by condition group (`case_id`): each group has one **group header row** (group name + row count; Threshold Mode appends the threshold condition text), and under it one row per request-count point. The table has **24 columns** in total, **13 shown by default**; the rest can be enabled in "Column settings":

| Column group | Columns (i18n titles) | Visible by default |
| --- | --- | --- |
| Task | Case (`label`), Requests, Concurrency, Successful (success rate %) | ✅ |
| Task (optional) | Successful requests, Failed requests, Benchmark duration (s), Total input tokens, Total generated tokens | ❌ |
| Throughput | Output token throughput (tok/s), Total token throughput (tok/s) | ✅ |
| Throughput (optional) | Request throughput (req/s), Peak output token throughput (tok/s), Peak concurrent requests | ❌ |
| TTFT | Mean / Median / P99 TTFT (ms) | ✅ |
| TPOT | Mean / Median / P99 TPOT (ms) | ✅ |
| ITL | Mean / Median / P99 ITL (ms) | ❌ |
| Status | Status | ✅ |

- **Status column**: `Failed` (red, the level failed to execute) / `Success` (green) + optional `BestPerf` / `Best` gold tags;
- **Row highlight**: `BestPerf` rows have a gold background, `Best` rows a green background;
- **Concurrency column**: shows `Inf` when `request-rate` is `inf`, and the actual concurrency value when `follow`;
- **Column settings**: the dropdown is grouped by Task / Throughput / TTFT / TPOT / ITL, with checkboxes controlling each column's visibility.

## 3. Best / BestPerf Marking

| Mark | Applicable mode | Threshold source | Rule |
| --- | --- | --- | --- |
| `Best` (green row) | Both modes | Local panel threshold (top-right of row 3, click the number to edit) | Among the rows in the group that satisfy **all** conditions (`TPOT-Mean ≤ TPOT threshold`; when the Output threshold is non-zero, also requires `output ≤ threshold`), mark the row with the maximum concurrency |
| `BestPerf` (gold row) | Threshold Mode only | Per-group threshold (configured in Step 1, independent per `case_id`) | Among the rows in the group that satisfy all configured conditions (`TTFT-statistic ≤`, `TPOT-statistic ≤`, `output ≤`), mark the row with the maximum concurrency |

Local panel thresholds: **TPOT** default `100` ms, **Output Token Threshold** default `0` tok/s (integer ≥ 0, click the number to edit, save on Enter/blur). This **only affects the table marking and is not written back to the task**; when all are 0, no marking is applied.

<div class="tip">

**Tip:**

On the direction of the output throughput threshold: `Best` / `BestPerf` are **frontend visual markers**, and their decision uniformly compares by "value ≤ threshold" (consistent with the `≤ X tok/s` display on the create page). In contrast, **the actual Threshold Mode stress-test decision** (backend) judges output throughput by a **lower bound** (`output_mean ≥ threshold` counts as meeting criteria, see [Concurrency & Threshold Modes](/en/docs/manual/performance/modes/)). The two compare output throughput in different directions — a current frontend/backend inconsistency. The marking is for reference only, and the final pass/fail is decided by the backend Threshold Mode result.

</div>

## 4. Stat Charts

The 12 charts in the Statistics panel (details in [Live Monitoring & Curves](/en/docs/manual/performance/live-metrics/)). After the task completes the curves are full and can be used to:

- **Throughput group**: observe the ramp-up and plateau of each group's throughput;
- **TTFT / TPOT / ITL groups**: locate the latency inflection point (the service capacity inflection point);
- **Multi-group comparison**: the same case within a group shares a color, so multiple length combinations can be compared within one chart.

## 5. Export and Download Details

| Operation | Entry point | Behavior |
| --- | --- | --- |
| Excel export | **Download** button in the row 3 footer | The frontend submits the currently displayed columns (including group header rows) as `headers + rows` to `POST /api/tasks/{task_id}/export`; the backend generates `realtime_{task_id}.xlsx` with openpyxl (bold headers, bold group header rows + light-blue fill) and writes it to `run_dir`; the browser downloads it (filename `realtime_{task_id}_{hhmmss}.xlsx`) |
| Log download | **Download** button at the top-right of the Logs panel | Pure frontend: assembles the current log buffer into `{task_id}_{hhmmss}.txt` and downloads it (no API call) |
| History backup | Datas → Perfs → **Backup** | `GET /api/logs/runs/{run_id}/backup` packages the whole run directory + terminal log into a zip download (can be imported again to restore) |

<div class="tip">

**Tip:**

The Excel export is "what you see is what you get": column order = the currently displayed columns, including group header rows; `Best` / `BestPerf` marks are written into the Status column as text.

</div>

## 6. Backend Execution Logic and Artifacts

| Artifact | Path | Description |
| --- | --- | --- |
| Task state | `~/.benchscope/perfs/tasks/{task_id}.json` | Task snapshot persistence (removed when the task is deleted) |
| Run metadata | `run_dir/run.json` | Full snapshot (with `rows`), refreshed as each level completes |
| mean summary CSV | `run_dir/{model}_X{gpu}.log` | CSV (with case block headers), **incrementally written per level** |
| p99 summary CSV | `run_dir/{model}_X{gpu}_p99.log` | Same as above, p99 basis |
| Case detail log | `run_dir/{model}_{case}_X{gpu}.log` | Raw engine output for each case |
| Summary Excel | `run_dir/benchmark-{DDMMYY}.xlsx` | Auto-generated at task end, marks `best` by each group's TPOT threshold |
| Per-request snapshots | `run_dir/live/*.json` | Final live frame per request (for review / Datas detail) |
| Manual export | `run_dir/realtime_{task_id}.xlsx` | Generated by the export API |
| Terminal log | `logs/perf_{run_id}_{MMDDHHMMSS}.log` | All terminal output; readable via `GET /api/tasks/{id}/logs` (default last 8000 lines) |

Execution flow (per request-count point): `_run_one()` runs the stress test → `_record_row()` appends to `rows` + incrementally writes the two CSVs + `persist()` + broadcasts `task_result`; after the task ends, `benchmark-*.xlsx` and `run.json` are generated and `task_done` is broadcast.

## 7. FAQ

**Question: Why does the results table keep growing in row count during execution?**
Each completed request-count point appends a row (`task_result` broadcast). The number of points in Threshold Mode is dynamic (decided by the scan strategy), so the total row count is only known at the end.

**Question: Do the Best marks remain after refreshing the page?**
Yes. The marks are computed in real time by the frontend from the persisted `rows` and thresholds; after a refresh the local panel thresholds reset to their defaults (TPOT=100 / Output=0), so `Best` may change, while `BestPerf` is unaffected (per-group thresholds are persisted with the task).

**Question: Can I export CSV directly?**
There is no standalone CSV export button, but the two summary CSVs (mean / p99) under `run_dir` are written incrementally in real time and can be previewed or downloaded from the Datas → Perfs file list; the Excel export corresponds to the current table view.

## 8. Related Docs

- [Live Monitoring & Curves](/en/docs/manual/performance/live-metrics/) — the 12 live curves during execution
- [Concurrency & Threshold Modes](/en/docs/manual/performance/modes/) — the scan logic of both modes
- [Performance Core Metrics](/en/docs/performance/metrics/) — column definitions
- [Data Manual](/en/docs/manual/datas/) — historical records and backup/import