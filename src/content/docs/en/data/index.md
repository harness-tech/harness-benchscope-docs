---
title: "Overview"
description: "Overview of the Datas panel: manage historical performance stress-test and accuracy evaluation artifacts, with viewing, comparative analysis, backup, and import."
---

# Overview

**Datas** records and organizes historical test artifacts and results, supporting import / recovery, viewing, and analysis. It is the "archive" for all performance stress-test and accuracy evaluation results.

![BenchScope Datas performance record detail](/images/benchscope-datas-perfs_detail.png)

<div class="tip">

**Tip**:

Datas is the persistent view of all your historical tests: performance / accuracy artifacts produced in the Web UI or the [CLI](/en/docs/cli/) are all registered here — viewable, importable, and exportable.

</div>

## Record Panels

Datas provides multiple record panels by type, each panel corresponding to one category of test artifact:

### Perfs (Performance Test Records)

- Paginated record table + **best-test-record highlight** (best performance, gold **Best** marker);
- **Perf Datas**: performance data details — **mean / median / p99** triplets for Output / TTFT / TPOT / ITL;
- **Perf-Cases-Logs** equal-height panels: view organized by test case;
- **Analysis panel**: multi-select records for **comparative analysis**;
- Actions: delete / backup / share / **import recovery**.

### Evals (Accuracy Evaluation Records)

The Evals sub-tab is currently **hidden** (the route `/datas/evals` redirects to `/datas/perfs`); manage accuracy evaluation artifacts and results on the **Accuracy page** (task list + details + sample viewing).

### Analysis (Data Analysis)

The data analysis panel (organizes performance results by analysis dimension; the data directory is `~/.benchscope/analysys/`).

## Import Backup

Datas supports restoring historical records from packaged backups:

- **Performance**: the backup is a **flat zip** (files directly at the zip root: `run.json` + terminal logs), imported under **Datas → Perfs → Import Backup**; task ID consistency is verified on import, and existing records are not imported twice.
- **Accuracy**: the artifacts are under `~/.benchscope/evals/eval-<time>/` (`task.json` / `result.json` / `samples.jsonl`), migrated together with the whole data directory.

```bash
# Example of packaging a performance task artifact (package manually as a flat zip, then import)
cd ~/.benchscope/perfs/<run_id>
zip perf-backup.zip run.json
# Package the terminal logs (located in the logs directory) as well:
zip perf-backup.zip ../logs/perf_<run_id>_*.log
```

> In the Web interface you can directly use the **Backup** button to download the auto-generated flat zip (`{run_id}.zip`), without manual packaging.

<div class="info">

**Info**:

The artifacts written to disk by the CLI commands `benchscope perf` / `benchscope eval` are completely identical to those of the Web UI. You can run tests on a headless machine, package a zip, and then import it into your local BenchScope instance to view it graphically.

</div>

<div class="warning">

**Warning**:

Importing a backup is used to migrate historical records between different machines / environments. What is imported is the artifact package, not the entire data directory.

</div>

## Record Details

Every record supports in-depth viewing:

- **Single-request real-time snapshots** can be replayed (the real-time panel on the second row of the performance page + the Datas / Perfs details dialog).
- **Logs** can be previewed and downloaded online.
- **Excel export**: aggregated by mean / P99 (with group title rows and Best / BestPerf markers).

Performance record detail page:

![BenchScope Datas performance record statistics](/images/benchscope-datas-perfs_statistics.png)

### Performance Statistics Example

| Metric | mean | median | p99 |
| --- | --- | --- | --- |
| Output (tok/s) | 112.4 | 110.8 | 96.5 |
| TTFT (ms) | 92.5 | 71.3 | 205.1 |
| TPOT (ms) | 34.2 | 33.1 | 58.7 |
| ITL (ms) | 33.9 | 32.7 | 58.6 |

## Data Sources

All Datas records come from artifacts persisted under the local data root directory (see [Configuration](/en/docs/install/configuration/)):

| Source | Data directory |
| --- | --- |
| Performance stress testing | `~/.benchscope/perfs/` (`run.json` + logs) |
| Accuracy evaluation | `~/.benchscope/evals/eval-<time>/` (task / result / samples) |
| Data analysis | `~/.benchscope/analysys/` (built-in default directory name) |

## FAQ

**Question: I can't find a historical task?**
Confirm the data root directory has not been cleaned / `BENCHSCOPE_DATA_DIR` has not been switched; you can also restore it by importing a backup.

**Question: The structure is malformed after import?**
Confirm the zip is flat (the root directly contains `run.json` / logs, etc.); nested directories may cause the import to fail.

## Related Docs

- [Performance Testing](/en/docs/performance/) — produces Perfs records
- [Performance Core Metrics](/en/docs/performance/metrics/) — Perfs metrics and export-column definitions
- [Overview](/en/docs/accuracy/) — produces accuracy evaluation artifacts
- [Configuration](/en/docs/install/configuration/) — artifact storage directories
- [Settings](/en/docs/tools/settings/) — data directories and Cache Paths