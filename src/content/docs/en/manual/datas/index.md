---
title: "Datas Manual Overview"
description: "Datas module manual overview: page structure, Perfs/Analysis sub-nav, the hidden Evals tab, data directories and the chapter index — the unified entry point for browsing historical performance / accuracy test records."
---

# Datas Manual Overview

**Datas (Data Management)** is the "archive" of BenchScope: it centrally displays all on-disk test artifacts and supports viewing, import / recovery, backup, and sharing. Once performance stress tests and accuracy evaluations finish, their records are registered here and remain accessible across sessions and service restarts.

<div class="info">

**Info:**

The Datas page is a read-only view of **persisted run records** (runs); it does not manage running tasks. To create / start / stop tasks, use the [Performance Testing](/en/docs/performance/) and [Accuracy Testing](/en/docs/manual/accuracy/) pages.

</div>

## 1. Page Structure

The Datas page consists of a **sub-navigation + sub-route content** area; the sub-nav offers two tabs:

```
┌──────────────────────────────────────────────┐
│  Datas sub-nav    [ Perfs ]   [ Analysis ]   │
├──────────────────────────────────────────────┤
│   (sub-route content area, switches per tab) │
└──────────────────────────────────────────────┘
```

| Tab | Route | Status | Description |
| --- | --- | --- | --- |
| Perfs | `/datas/perfs` | Available | Performance test records: list + detail panel (data table + statistical charts) |
| Analysis | `/datas/analysis` | Coming soon | Data analysis placeholder page; features are being planned |

<div class="warning">

**Warning:**

Early versions had an **Evals (accuracy evaluation records)** tab. It is now **hidden** — the route `/datas/evals` redirects to `/datas/perfs`, and the tab no longer appears in the sub-nav. Manage accuracy evaluation artifacts and results on the **Accuracy page** ([Accuracy Testing](/en/docs/manual/accuracy/)).

</div>

## 2. Routes and Entry Points

| Route | Behavior |
| --- | --- |
| `/datas` | Redirects to `/datas/perfs` (enters the Perfs page by default) |
| `/datas/perfs` | Performance record management page |
| `/datas/evals` | Redirects to `/datas/perfs` (Evals is hidden) |
| `/datas/analysis` | Data analysis placeholder page |
| `/datas/perfs?run_id=<id>` | Opens a record and auto-selects it (jump entry from the Dashboard "Details") |

## 3. Data Sources

All Datas records come from the on-disk artifacts under the local data root directory (default `~/.benchscope/`, overridable via `BENCHSCOPE_DATA_DIR`):

| Source | Directory | Contents |
| --- | --- | --- |
| Performance stress-test records | `perfs/<run_id>/` | `run.json` + `live/*.json` + summary / log files |
| Accuracy evaluation records | `evals/<run_id>/` | Accuracy task artifacts (managed on the Accuracy page) |
| Terminal output logs | `logs/perf_<run_id>_*.log` | Terminal logs captured while the task ran |
| Data analysis | `analysys/` | Data analysis directory (the Analysis feature is being planned) |

<div class="tip">

**Tip:**

The data analysis directory is named **`analysys`** by default. This is the built-in default name — do not rename it or mistype it as `analysis`.

</div>

## 4. Chapter Index

- [Performance Record Management](/en/docs/manual/datas/perfs/) — task records, detail panel, run directory, log files
- [Data Analysis](/en/docs/manual/datas/analysis/) — cross-record comparison analysis, linkage, mean / median
- [Import, Export, and Backup](/en/docs/manual/datas/import-export/) — backup zip, import / recovery, share PNG

## 5. Related Docs

- [Datas Overview (Reference)](/en/docs/data/) — Datas module concepts and metric definitions; [Performance Testing](/en/docs/performance/) — produces Perfs records
