---
title: "Overview"
---

# Overview

The performance testing page stress-tests an inference service and provides **two modes** — *Concurrency Mode* and *Threshold Mode* — while visualizing throughput, latency, and progress in real time.

- **Concurrency Mode** answers: *how does throughput and latency change as concurrency grows?*
- **Threshold Mode** answers: *given a business SLA, what is the maximum concurrency this setup can sustain?*

![Performance testing main interface](/images/benchscope-performance_perf_running.png)

<div class="tip">

**tip**：

Performance testing targets the **service chain** — whether the target is served by vLLM, SGLang, or any other OpenAI-compatible backend, you can stress-test and compare results through the same unified interface.

</div>

## In This Section

- [Concurrency Testing](/en/docs/performance/concurrency/) — apply pressure level by level and read the results to find the best operating range
- [Threshold Testing](/en/docs/performance/threshold/) — given a business SLA, search automatically for the maximum sustainable concurrency

## Mode Overview

| Mode | Description | Typical Use Cases |
| --- | --- | --- |
| **Concurrency Mode** | Applies pressure step by step at fixed concurrency levels, recording metrics for each concurrency in real time | Observe how the system’s curves change with load |
| **Threshold Mode** | Starts from 1 concurrency, increases by powers of 2 plus bisection, to automatically find the maximum concurrency satisfying the threshold conditions | Given a business SLA, find the optimal sustainable concurrency |

## Creating a Task

Open **Performance** and click **Create Task**. A **three-step form** (Step 1 Conditions / Step 2 Parameters / Step 3 Command Preview) drives the whole run:

![Create task form](/images/benchscope-performance_create.png)

1. **Step 1 — Conditions**: choose the model and service address (Provider), engine, and mode (concurrency / threshold).
2. **Step 2 — Parameters**: set concurrency levels, request counts, input/output token lengths (threshold mode also needs the SLA thresholds and search cap).
3. **Step 3 — Command preview**: review the exact command that will be executed, then start.

<div class="tip">

**tip**：

If you use a token-estimation capability, the create page shows an estimated token consumption (see the token display below):

![Create task — token configuration](/images/benchscope-performance_create_token.png)

</div>

## Concurrency Mode

Concurrency Mode applies pressure **level by level by concurrency**, feeding real-time results back to the running interface so you can observe how the service scales with load — and locate its **best operating range**. For a step-by-step walkthrough, see [Concurrency Testing](/en/docs/performance/concurrency/).

Running view:

![Performance running statistics](/images/benchscope-performance_perf_running_statistics.png)

## Threshold Mode

When the business SLA is known, Threshold Mode probes for the maximum concurrency that still satisfies the conditions (`best_concurrency`).

**Evaluation conditions** (all must hold for a level to pass):

- **TTFT ≤ threshold** (evaluated with the chosen statistic: mean / median / p99)
- **TPOT ≤ threshold** (mean / median / p99)
- **Output throughput ≥ threshold**

The probing strategy **starts from 1 concurrency and increases by powers of 2**, then **bisects** within the adjacent interval once the first failing point is found. For a step-by-step walkthrough, see [Threshold Testing](/en/docs/performance/threshold/).

<div class="info">

**info**：

The statistic used for each threshold is configurable (for example `--ttft-statistic p99`) to match different business criteria. See [perf command](/en/docs/cli/perf/).

</div>

## Artifacts and Import

- Each run is saved as `run.json` plus logs `perf_<run_id>_*.log`.
- Package the artifacts as a **flat zip**, importable under **Datas → Perfs → Import Backup** to restore historical runs across environments.

<div class="warning">

**warning**：

If the target address is wrong, requests time out, or the engine is unavailable, a run may fail or some requests may be counted as failed. Confirm the service is reachable (browser or `curl`) before starting a run.

</div>

## Related

- [Concurrency Testing](/en/docs/performance/concurrency/) — step-by-step walkthrough
- [Threshold Testing](/en/docs/performance/threshold/) — finding `best_concurrency`
- [perf command](/en/docs/cli/perf/) — the `benchscope perf` command
- [Settings](/en/docs/tools/settings/) — providers and bench engines
- [Datas](/en/docs/data/) — records, export, and import
