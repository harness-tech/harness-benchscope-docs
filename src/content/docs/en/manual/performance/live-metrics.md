---
title: "Live Monitoring & Curves"
description: "BenchScope performance testing live monitoring: Profile Progress panel, Real-Time Metrics table, 12 live curves, and the WebSocket data stream."
---

# Live Monitoring & Curves

While a task is running, row 2 of the performance page (Profile Progress + Real-Time Metrics) and row 4 (Statistics, 12 charts) refresh in real time. Data is pushed over WebSocket (`/ws`), so the frontend does not need to poll.

## 1. Page Structure

```
┌─────────────────────────────────────────────────────────────┐
│ Row 2  Profile Progress (left 36%) | Real-Time Metrics      │
│        (right 64%)                                          │
├─────────────────────────────────────────────────────────────┤
│ Row 4  Statistics: 4 metric groups × 3 statistics =         │
│        12 charts (linkage toggle)                           │
└─────────────────────────────────────────────────────────────┘
```

**Snapshot source** (row 2 renders by "current active request", highest priority first):

1. The request-count tag selected by clicking in the Cases panel (reviewing a historical request, status shown as `Completed`);
2. The request currently executing (status shown as `Profiling`);
3. Default: the last completed request.

## 2. Profile Progress

Shows the status and progress of the current request (single-request basis):

| Item | Content | Data source |
| --- | --- | --- |
| Current status | `Profiling` (running) / `Completed` (done or reviewing) | Task status + whether a review is selected |
| Right of title | `case#g{case_id} · {concurrency} req` | Current execution position |
| Profiling progress bar | Current request `completed/total` % | `task_live.stats` |
| Records progress bar | Same as above (current-request basis) | `task_live.stats` |
| Progress | `completed / total requests (pct%)` | Live snapshot of the current request (`-` when no snapshot) |
| Errors | `errors / completed (pct%)`, highlighted red when > 0 | Same as above |
| Request Rate | `req_per_s requests/s` | Same as above |
| Processing Rate | `completed/t records/s` | Same as above |
| Elapsed | `m ss` (shown as `h mm` when ≥ 1h) | Snapshot `t` (seconds elapsed) |
| ETA | `(t/completed) × (total-completed)`, shown as `x.x s` when < 120s | Estimated from completion progress; shows `0s` when the request is done, `-` when no snapshot |

## 3. Real-Time Metrics

A table of **11 metrics × 7 statistics** (columns: `avg/min/max/p99/p90/p50/std`), refreshed every second with the `task_live` stream while running:

| Group | Metric | Unit | Meaning |
| --- | --- | --- | --- |
| Latency | `TTFT` | ms | First-token latency |
| Latency | `TTST` | ms | First-2-tokens latency (first time 2 output tokens accumulate) |
| Latency | `TPOT` | ms | Per-output-token latency |
| Latency | `Req Latency` | ms | Request end-to-end latency |
| Latency | `ITL` | ms | Inter-token latency |
| Throughput | `Output TPS/User` | tok/s | Per-user generation rate |
| Throughput | `Output TPS` | tok/s | Total output throughput |
| Throughput | `Req/sec` | req/s | Request completion rate |
| Throughput | `Requests` | count | Completed request count (only the `avg` column is computable) |
| Length | `OSL` | tokens | Output sequence length |
| Length | `ISL` | tokens | Input sequence length |

Cell states: **blue number** = value computed; **gray dash `-`** = computable but no value yet; **gray-black `N/A`** = not computable.

<div class="info">

**Info:**

Native engine availability: vLLM/SGLang native engines have no per-request real-time stream; the snapshot is built by aggregating at the end of each level — only `avg/p50/p99` are available (other statistics are `N/A`); `TTST` and `Output TPS/User` are unavailable throughout (the whole row is `N/A`). The in-house Bench CLI engine provides all distribution statistics every second.

</div>

<div class="info">

**Info:**

i18n also keeps keys for **unit conversion (ms/tok ↔ s/k)**, **Trend column**, **group headers (latency/throughput/length)** and **copy current snapshot**; these are not enabled in the current UI, and the table displays in raw ms/tok units.

</div>

## 4. 12 Live Curves

The Statistics panel (row 4) has **12 line charts**: 4 metric groups × `Mean/Median/P99`, x-axis is request count (ascending), one curve per condition group (case):

| Group | Three charts (keys) | Unit |
| --- | --- | --- |
| Throughput | `output_mean` / `peakoutput_mean` / `total_mean` | tok/s |
| TTFT | `ttft_mean` / `ttft_median` / `ttft_p99` | ms |
| TPOT | `tpot_mean` / `tpot_median` / `tpot_p99` | ms |
| ITL | `itl_mean` / `itl_median` / `itl_p99` | ms |

- **Real-time growth**: each time a request-count point completes, `rows` gains a row, each chart auto-appends a data point, and the curves build up gradually during execution;
- **Group coloring**: each group uses an 8-color palette; the same case within a group has a consistent color, easing multi-group comparison;
- **Linkage toggle**: the `linkage` toggle at the top-right of the panel (default on); when on, hovering any chart shows the same x-axis tooltip across all 12 charts.

## 5. Button Operations

1. **Review any request**: click any request-count tag in the Cases panel (a blue outline marks the selection) and row 2 switches to that request's snapshot; click again to deselect and restore the running view.
2. **Linkage toggle**: flip the `linkage` toggle at the top-right of the Statistics panel to enable/disable the 12-chart tooltip linkage.
3. **Log follow**: the Logs panel and Cases panel auto-scroll to the bottom during execution; after manual scroll-up, the log stops following (it returns to the bottom when new content arrives).

The live monitoring flow, from connection to render:

1. Open the performance page while a task is running; the frontend connects to the WebSocket at `/ws`.
2. On connect, the backend first pushes `status` and all `task_snapshot` events.
3. While running, the engine streams live stats: the in-house engine calls `live_cb` every second (native engines use a 1-second ticker thread per level), broadcasting `task_live`.
4. The frontend renders row 2 (Profile Progress + Real-Time Metrics) from the current-request snapshot and appends points to the 12 Statistics curves.
5. Each completed request-count point is cached per `case_id + concurrency` and, at level end, persisted to a live snapshot file; logs stream via `task_log`.

## 6. Backend Execution Logic

| Stage | Mechanism |
| --- | --- |
| WS connection | After connecting to `/ws`, first pushes `status` and all `task_snapshot`; auto-reconnects 3 seconds after a drop |
| In-house engine real-time stream | `run_builtin_bench` calls back `live_cb` every second: computes distribution statistics for 10 metrics from completed records, broadcasts `task_live` (with `t/completed/total/errors/req_per_s/output_tps/metrics`) |
| Native engine real-time stream | A 1-second ticker thread per level broadcasts `task_live`; progress parsed from `benchscope-live-done k/N` log lines (only Mock output contains that line; with real vLLM/SGLang only Elapsed advances) |
| Per-request cache | The frontend caches the latest snapshot by `case_id + concurrency` (`liveReq`); after the task ends, you can click to review |
| Snapshot persistence | At each level's completion, the final frame is written to `run_dir/live/<label#gid__c<conc>>.json`; after the task ends (`done`/`stopped`/`error`), the frontend calls `GET /api/logs/runs/{run_id}/live` to backfill |
| Log stream | Each line of engine output broadcasts `task_log`; the frontend keeps the most recent 8000 lines |

## 7. FAQ

**Question: Why are there so many N/A in the Real-Time Metrics table?**
Native engines (vLLM/SGLang) have no per-request real-time stream; the snapshot is back-derived by aggregating at each level's end: only `avg/p50/p99` are available, and `TTST` and `Output TPS/User` are not provided by the engine. Switching to the in-house Bench CLI engine yields all distribution statistics.

**Question: Do the curves remain after the task ends?**
Yes. Each request-count result is persisted in `rows` (written to disk with `run.json`); after the task ends, the frontend backfills the per-request persisted snapshots (`/api/logs/runs/{run_id}/live`), so row 2 can review historical requests.

**Question: What is the difference between ETA and Elapsed?**
Elapsed is the actual time from start to now; ETA estimates the remaining time as "elapsed ÷ completion ratio", and shows `-` when not running or when completion is 0.

## 8. Related Docs

- [Performance Overview](/en/docs/manual/performance/) — page structure and task state machine
- [View & Export Results](/en/docs/manual/performance/results/) — final results table and export
- [Performance Core Metrics](/en/docs/performance/metrics/) — metric definitions