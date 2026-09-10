---
title: "Overview"
description: "Overview of the benchscope CLI: serve, perf, and eval subcommands, quick start, and FAQ."
---

# Overview

The `benchscope` CLI brings the Web platform's capabilities to the terminal: starting the service, concurrency stress testing, and accuracy evaluation each take a single command, and the resulting task artifacts are fully compatible with the Web.

```text
benchscope {serve,perf,eval} [subcommand options]
```

> The CLI does not provide a `--version` option; to check the version, use `pip show benchscope`, or visit `/api/version` in the Web UI.

<div class="info">

**Info:**

**Backward-compatible behaviour**: when `benchscope` is run with no arguments, or the first argument is an option (e.g. `--port 8080`), it falls back to starting the service, equivalent to `benchscope serve`.

</div>

## Command Overview

| Command | Purpose | Main Artifact |
| --- | --- | --- |
| [`benchscope serve`](/en/docs/cli/serve/) | Starts the Web service, opening the full platform at `http://127.0.0.1:8080` by default | — |
| [`benchscope perf`](/en/docs/cli/perf/) | Runs one performance stress test (concurrency or threshold mode), outputting throughput and latency metrics | `run.json` |
| [`benchscope eval`](/en/docs/cli/eval/) | Runs one accuracy evaluation (Serving / Native / Mock), outputting metrics such as accuracy / pass_rate | `evals/eval-<time>/` |

## Quick Start

```console
# Concurrency stress test: concurrency 8, 1024 input/output tokens each
$ benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
    --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024

# Accuracy evaluation: evaluate 200 samples on GSM8K against a deployed service
$ benchscope eval --mode serving --model Qwen2.5-7B \
    --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200

# Check the installed version (the CLI does not provide a --version option)
$ pip show benchscope
```

<div class="tip">

**Tip:**

CLI and Web task artifacts are fully compatible: all CLI artifacts can be packaged and restored in the Web UI under **Datas → Perfs → Import Backup**, just like tasks created in the Web UI.

</div>

## FAQ

**Question: What happens when `benchscope` is run without arguments?**
It is equivalent to `benchscope serve`, starting the Web platform directly.

**Question: Can the produced tasks be managed in the Web UI?**
Yes. CLI artifacts are fully compatible with Web tasks: performance artifacts can be viewed and imported under **Datas → Perfs**; accuracy artifacts are managed on the **Accuracy page**.

**Question: How do I choose the right command?**
Use [`serve`](/en/docs/cli/serve/) to start the service; use [`perf`](/en/docs/cli/perf/) to stress-test throughput / latency (including threshold probing); use [`eval`](/en/docs/cli/eval/) to evaluate accuracy.

## Related Documentation

- [Installation](/en/docs/install/) — environment requirements and startup
- [Performance Testing](/en/docs/performance/) — concurrency stress testing and threshold probing
- [Performance Core Metrics](/en/docs/performance/metrics/) — reference for perf output metrics
- [Accuracy Overview](/en/docs/accuracy/) — three-mode evaluation
- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — reference for eval output metrics
- [Data (Datas)](/en/docs/data/) — viewing and importing task artifacts