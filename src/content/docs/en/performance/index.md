---
title: "Overview"
description: "Overview of BenchScope performance testing: the Concurrency and Threshold stress-test modes, the task creation workflow, and where to go next."
---

# Overview

Performance testing stress-tests a deployed inference service in two modes — **Concurrency Mode** and **Threshold Mode** — with real-time visualization of throughput, latency, and run progress.

- **Concurrency Mode** answers: *as concurrency grows, how do throughput and latency change?*
- **Threshold Mode** answers: *given a business SLA, what is the maximum concurrency this configuration can sustain?*

![BenchScope performance testing main interface (running)](/images/benchscope-performance_perf_running.png)

<div class="tip">

**Tip:**

Performance testing targets the **service chain** — whether the target service is provided by vLLM, SGLang, or any other OpenAI-compatible backend, you can stress-test and compare results through a unified interface.

</div>

## On This Page

- [Performance Core Metrics](/en/docs/performance/metrics/) — the complete reference for all metrics (TTFT / TPOT / ITL / throughput / request statistics / export columns)
- [Concurrency Testing](/en/docs/performance/concurrency/) — apply load level by level, interpret the results, and find the best operating range
- [Threshold Testing](/en/docs/performance/threshold/) — given a business SLA, automatically search for the maximum sustainable concurrency

## Mode Overview

| Mode | Description | Typical Scenario |
| --- | --- | --- |
| Concurrency | Runs a fixed set of concurrency levels in sequence, recording each level's metrics in real time | Observe how the system's curves change as load varies |
| Threshold | Starts from 1 concurrency and increases by powers of 2 + bisection to automatically find the maximum concurrency that satisfies the threshold conditions | The business SLA is known; find the optimal sustainable concurrency |

## Creating a Task

Go to the **Performance** page, click **Create Task**, and start a stress test through the three-step form (Step 1 Conditions / Step 2 Parameters / Step 3 Command Preview):

![BenchScope create performance task](/images/benchscope-performance_create.png)

1. **Step 1 Conditions**: choose the model under test and the service address (Provider), the engine, and the mode (concurrency / threshold).
2. **Step 2 Parameters**: fill in the concurrency, input/output tokens, request count, and other parameters (threshold mode also requires the SLA thresholds and the search upper limit).
3. **Step 3 Command Preview**: review the equivalent CLI command, then start the run.

<div class="tip">

**Tip:**

If you use the token-estimation capability, the create page shows a consumption estimate (see the token display below):

![BenchScope create task token display](/images/benchscope-performance_create_token.png)

</div>

## Concurrency Mode

Applies load at each concurrency level in sequence; each level's metrics feed back in real time to the table, curves, and progress, so you can see how the service behaves under load and find the **best operating range**. For step-by-step instructions, see [Concurrency Testing](/en/docs/performance/concurrency/).

Main interface while running:

![BenchScope performance testing running statistics](/images/benchscope-performance_perf_running_statistics.png)

## Threshold Mode

When the business SLA is known, threshold probing automatically finds the **maximum concurrency** (`best_concurrency`) that satisfies all threshold conditions.

**Decision criteria** (all must be met to pass):

- TTFT ≤ threshold (`mean` / `median` / `p99`);
- TPOT ≤ threshold (`mean` / `median` / `p99`);
- Output throughput ≥ threshold.

The probing strategy **increases by powers of 2 starting from 1 concurrency**; after finding the first point that does not satisfy the conditions, it **bisects** the adjacent interval to converge. For step-by-step instructions, see [Threshold Testing](/en/docs/performance/threshold/).

<div class="info">

**Info:**

The statistic used for threshold decisions can be adjusted via parameters (e.g. `--ttft-statistic p99`) to fit different business criteria. See the [perf Command](/en/docs/cli/perf/).

</div>

## Artifacts and Import

- Writes `run.json` to disk plus log files `perf_<run_id>_*.log`;
- Packaged as a **flat zip**, importable under **Datas → Perfs → Import Backup** to restore historical stress-test records across environments.

<div class="warning">

**Warning:**

During a stress test, if the service address under test is wrong, requests time out, or the engine is unavailable, the task may fail or some requests may be counted as failed. First confirm the service is reachable via a browser / curl before starting the stress test.

</div>

## Related Documentation

- [Performance Core Metrics](/en/docs/performance/metrics/) — complete metric reference and export columns
- [Concurrency Testing](/en/docs/performance/concurrency/) — step-by-step instructions
- [Threshold Testing](/en/docs/performance/threshold/) — finding the optimal concurrency
- [perf Command](/en/docs/cli/perf/) — full parameters of the `perf` command
- [Settings](/en/docs/tools/settings/) — configure Provider and Bench Engines
- [Data & Statistics (Datas)](/en/docs/data/) — historical records and import