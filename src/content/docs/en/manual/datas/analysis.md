---
title: "Data Analysis"
description: "Datas data analysis manual: the Analysis tab's current status (coming soon), the statistical modes inside the Perfs detail (mean / median / P99), and the button operations and backend execution logic for chart linkage and row / group filters."
---

# Data Analysis

Data analysis is used to **extract statistical conclusions from performance metrics**: view metrics under different statistical modes (mean / median / P99), and use **Linkage** to synchronize hover tooltips across multiple statistical charts so you can quickly pinpoint performance inflection points.

## 1. Feature Overview

"Data analysis" in Datas comes in two parts:

- **Analysis tab** (`/datas/analysis`): currently a **coming soon** placeholder ("Data analysis features are being planned"), reserving the **cross-record comparison analysis** capability (select the records to compare).
- **Analysis capabilities inside the Perfs detail** (currently available):
  - Row 3 **Perf Datas data panel**: view the metric table in **Default / Mean / Median / P99** modes.
  - Row 4 **Statistical charts**: the **Linkage** toggle, filtering metric rows by TTFT / TPOT / ITL, and filtering by case group.

<div class="warning">

**Warning:**

Cross-record "comparison analysis" (selecting records to compare and comparing them side by side) is a **planned feature of the Analysis tab** and has not shipped in the current version. All currently available analysis is done inside the Perfs detail of a single record.

</div>

## 2. Page Structure

```
Analysis tab:
┌────────────────────────────────────┐
│            Coming soon              │
│       Data analysis is being planned │
└────────────────────────────────────┘

Perfs detail, row 3 (data panel):
┌──────────────────────────────────────────────────┐
│  Perf Datas        [Default][Mean][Median][P99]   │
│   [case group tabs]                               │
│   ┌ Metric table (columns switch by mode) ... [Details] ┐ │
└──────────────────────────────────────────────────┘

Perfs detail, row 4 (statistical charts):
┌──────────────────────────────────────────────────┐
│  Stat Charts  [Linkage ON]  [Default][TTFT][TPOT][ITL] │
│   Throughput: Output  Peak  Total  (tok/s)        │
│   TTFT: mean  median  p99  (ms)                   │
│   TPOT: mean  median  p99  (ms)                   │
│   ITL:  mean  median  p99  (ms)                   │
└──────────────────────────────────────────────────┘
```

![BenchScope Datas performance record statistics](/images/benchscope-datas-perfs_statistics.png)

## 3. Input Parameters and Field Constraints

| Field | Type | Constraints | Default | Description |
| --- | --- | --- | --- | --- |
| Data mode `mode` | enum | `default` / `mean` / `median` / `p99` | `default` | Statistical columns shown in the data panel |
| Linkage `linkage` | boolean | on / off | off | Whether statistical-chart tooltips are synchronized across charts |
| Metric rows `visible` | object | `throughput` / `ttft` / `tpot` / `itl`, each on / off | all on | Controls which metric rows are shown (the throughput row is always visible) |
| Case groups `groups` | array | Can be toggled as a whole (default / per group) | all enabled | Controls which case groups participate in the statistical charts |

### 3.1 Data Columns per Statistical Mode

| Mode | Data-table columns (after the Datas page hides the Case / Concurrency / Success / Status columns by default) |
| --- | --- |
| `default` | Requests, Output, Total, TTFT mean/median/p99, TPOT mean/median/p99 |
| `mean` (mean) | Requests, Output, Peak, Total, TTFT mean, TPOT mean, ITL mean |
| `median` (median) | Requests, Output, Peak, Total, TTFT median, TPOT median, ITL median |
| `p99` | Requests, Output, Peak, Total, TTFT p99, TPOT p99, ITL p99 |

## 4. Button Operations

1. **Data panel mode**: click **Default / Mean / Median / P99** to switch the metric table's statistical columns.
2. **Linkage toggle**: turn **Linkage** on / off in the statistical-chart header; when on, moving the mouse into any chart synchronously shows the tooltips of all charts in the same group.
3. **Metric row filter**: click **TTFT / TPOT / ITL** to show / hide the corresponding metric row; **Default** shows all rows with one click.
4. **Case group filter** (with multiple groups): a group row appears at the top of the statistical charts; click a group to hide / restore its curves; **Default** restores all groups.
5. **Details**: click at the end of a data-table row to open a dialog showing that request's Profile Progress / Real-Time Metrics.

## 5. Execution Steps (Reading the Statistical Conclusions of a Record)

1. Select a record on the Perfs page.
2. In row 3, choose a mode (e.g., **Median** for robust statistics, or **P99** for tail latency).
3. In row 4, turn on **Linkage**, move the mouse to a concurrency point, and observe throughput / TTFT / TPOT / ITL change in sync.
4. If you only care about latency, turn off **TTFT** or keep only **TPOT / ITL**.
5. With multiple case groups, use the group row to keep only the target group and reduce curve clutter.

## 6. Backend Execution Logic

- **Data source**: both the data table and the statistical charts are read from `rows[].metrics` in `run.json`. Each case × concurrency combination is one row, and `metrics` contains all metric keys: `output_mean`, `peakoutput_mean`, `total_mean`, `ttft_{mean,median,p99}`, `tpot_{mean,median,p99}`, `itl_{mean,median,p99}`, etc.
- **Mode switching**: pure frontend — selects the corresponding metric keys as columns based on `mode`, with no extra API calls.
- **Linkage**: pure frontend `echarts.connect('run-charts')` / `disconnect`, binding the ECharts instances in the same group to achieve tooltip linkage; turning it off unbinds them.
- **Row / group filtering**: pure frontend — filters `rows` by `visible` and the enabled groups, then redraws the curves.
- **(Optional) Summary endpoint**: `GET /api/logs/runs/{run_id}/summary?threshold=` can return `records_mean` / `records_p99` and the best value computed from `tpot_threshold_ms` (server-side aggregation when needed).

<div class="tip">

**Tip:**

"Linkage" only affects **tooltip linkage**; it does not change the curve data. The curves are always determined by `rows[].metrics`.

</div>

## 7. FAQ

**Question: The Analysis tab is empty?**
It is a placeholder (coming soon); cross-record comparison analysis is still being planned. For now, do single-record analysis inside the Perfs detail.

**Question: Linkage is not responding?**
Confirm the linkage toggle is on and at least one chart is visible. Linkage is established purely on the frontend via an ECharts connection; no refresh is needed.

**Question: A mode shows empty columns?**
The corresponding metric keys are missing from that record's `metrics` (for example, the engine did not produce ITL); the frontend displays `-`.

## 8. Related Docs

- [Performance Record Management](/en/docs/manual/datas/perfs/) — the page hosting the data panel
- [Datas Manual Overview](/en/docs/manual/datas/) — entry to the module
- [Performance Core Metrics (Reference)](/en/docs/performance/metrics/) — metric keys and definitions
- [API Reference](/en/docs/api/) — `/api/logs/runs/{id}/summary`