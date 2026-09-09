---
title: "Overview"
---

# Overview

**Datas** records and organizes historical test artifacts and results, supporting **import / recovery**, **viewing**, and **analysis**. It is the single place where every performance and accuracy run is persisted for later inspection.

![BenchScope Datas performance record detail](/images/benchscope-datas-perfs_detail.png)

<div class="tip">

**tip**：

Datas is your persistent view over every historical test: artifacts produced by the Web UI or the [CLI](/en/docs/cli/) are all registered here — viewable, importable, and exportable.

</div>

## Records Panel

Datas is organized into record tabs, one per artifact type:

### Perfs (performance records)

- Paginated record table with a **best-test-record highlight** (best performance, gold **Best** marker);
- **Perf Datas**: performance data details — **mean / median / P99** triplets for Output / TTFT / TPOT / ITL;
- **Perf-Cases-Logs** high-level view, grouped per use case;
- **Analysis panel**: multi-select records for **comparative analysis**;
- Actions: delete / backup / share / **import recovery**.

### Evals (accuracy records)

- View accuracy evaluation artifacts and results;
- Supports packaged import.

### Analysis (data analysis)

- Data analysis panel (a placeholder in some versions).

## Import Backup

Datas supports restoring test data from packaged backups:

- **Performance** — packaged as a **flat zip** (containing `run.json` + logs + optional `metrics.json`), imported under **Datas → Perfs → Import Backup**.
- **Accuracy** — import the packaged file of the `evals` artifact directory.

```bash
# Example: package a performance task artifact manually before import
cd ~/.benchscope/perfs/<run_id>
zip -r perf-backup.zip run.json perf_<run_id>_*.log metrics.json
```

<div class="info">

**info**：

The CLI commands `benchscope perf` and `benchscope eval` write exactly the same artifacts the Web UI produces. You can run tests on a headless box, copy the zip, and import it into a BenchScope instance to view it graphically.

</div>

<div class="warning">

**warning**：

Importing a backup is meant to migrate historical records between machines / environments. It imports the artifact package — not the entire data directory.

</div>

## Record Details

Each record supports deep inspection:

- **Per-request real-time snapshots** can be reviewed (the real-time panel on the second row of the performance page, plus the **Datas / Perfs details dialog**).
- **Online log preview and download**.
- **Excel export**: aggregated by mean / P99 summary (with group title rows and Best / BestPerf markers).

Performance record statistics page:

![BenchScope Datas performance record statistics](/images/benchscope-datas-perfs_statistics.png)

### Sample performance statistics

| Metric | mean | median | p99 |
| --- | --- | --- | --- |
| Output (tok/s) | 112.4 | 110.8 | 96.5 |
| TTFT (ms) | 92.5 | 71.3 | 205.1 |
| TPOT (ms) | 34.2 | 33.1 | 58.7 |
| ITL (ms) | 33.9 | 32.7 | 58.6 |

## Data Sources

All Datas records come from artifacts persisted under your local data root (see [Configuration](/en/docs/install/configuration/)):

| Source | Data directory |
| --- | --- |
| Performance testing | `~/.benchscope/perfs/` (`run.json` + logs) |
| Accuracy evaluation | `~/.benchscope/evals/eval-<timestamp>/` (task / result / samples) |
| Data analysis | `~/.benchscope/analysis/` |

## FAQ

**Question: I can't find a historical task.**
Check that the data root hasn't been cleaned or `BENCHSCOPE_DATA_DIR` hasn't changed; you can also restore it by importing a backup.

**Question: The structure is malformed after import.**
Make sure the zip is flat (the root directly contains `run.json` / logs, etc.); nested directories can cause import to fail.

## Related

- [Performance Testing](/en/docs/performance/) — produces Perfs records
- [Accuracy Testing](/en/docs/accuracy/) — produces Evals records
- [Configuration](/en/docs/install/configuration/) — artifact storage directories
- [Settings](/en/docs/tools/settings/) — data directory and cache paths
