---
title: "Data & Records (Datas)"
---

# Data & Records (Datas)

**Datas** records and organizes historical test artifacts and results, supporting **import / recovery**, **viewing**, and **analysis**. It is the single place where every performance and accuracy run is persisted for later inspection.

## Records Panel

Datas is organized into record tabs:

| Tab | Contents |
| --- | --- |
| **Perfs** | Performance testing records — includes high-level views such as Perf-Cases-Logs, Perf Datas, analysis panels, plus delete / backup / share and import recovery |
| **Evals** | Accuracy evaluation records — view, package, and import |
| **Analysis** | Data analysis (a placeholder in some versions) |

### Perfs details

Performance records include paginated record tables, a **best-test-record highlight** (best performance, gold **Best** marker), performance data details (mean / median / P99 triplets for Output / TTFT / TPOT / ITL), and multi-select records for **comparative analysis**.

![Performance record detail](/images/benchscope-datas-perfs_detail.png)

![Performance record statistics](/images/benchscope-datas-perfs_statistics.png)

## Import Backup

Datas supports restoring test data from packaged backups:

- **Performance** — packaged as a **flat zip** (containing `run.json` + logs + optional `metrics.json`), imported under **Datas → Perfs → Import Backup**.
- **Accuracy** — import the packaged file of the `evals` artifact directory.

<div class="tip">

**tip**：

The CLI commands `benchscope perf` and `benchscope eval` write the same artifacts that the Web UI produces — so you can run tests on a headless box, copy the zip, and import it into a BenchScope instance to view it graphically.

</div>

## Record Details

Each record supports deep inspection:

- **Per-request real-time samples** can be reviewed (the real-time panel on the second row of the performance page, plus the **Datas / Perfs details dialog**).
- **Online log preview and download**, with **Excel export** (mean / P99 summary).

## Typical Workflow

1. Run a performance or accuracy task (from the Web UI or the CLI).
2. Open **Datas** to find the record.
3. Drill into details — per-request snapshots, logs, statistics.
4. Export logs / Excel, or package a backup and share or import it elsewhere.

## Related

- [Configuration](/en/docs/install/configuration/) — artifact storage directories (`perfs_dir` / `evals_dir`)
- [Performance Testing](/en/docs/performance/) — how performance artifacts are produced
- [Accuracy Testing](/en/docs/accuracy/) — how accuracy artifacts are produced
