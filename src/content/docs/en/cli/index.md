---
title: "Overview"
---

# Overview

The `benchscope` command-line brings the platform's capabilities to your terminal: start the service, run performance testing and accuracy evaluation — all with a single command, producing artifacts fully compatible with the Web UI.

```text
benchscope [--version] {serve,perf,eval} [subcommand options]
```

<div class="info">

**info**：

**Backward-compatible behaviour**：When you pass **no arguments**, or the *first* argument is an option (for example `--port 8080`), the CLI falls back to the "start service" behaviour — equivalent to running `benchscope serve`.

</div>

## Command overview

| Command | Purpose | Main artifacts |
| --- | --- | --- |
| [`benchscope serve`](/en/docs/cli/serve/) | Starts the Web service, opening the full platform at `http://127.0.0.1:8080` by default | — |
| [`benchscope perf`](/en/docs/cli/perf/) | Runs one performance test (Concurrency / Threshold mode), printing throughput and latency metrics | `run.json` |
| [`benchscope eval`](/en/docs/cli/eval/) | Runs one accuracy evaluation (Serving / Native / Mock), printing accuracy / pass_rate metrics | `evals/eval-<time>/` |

## Quick start

```console
$ benchscope --version
benchscope 1.1.0

# Concurrency test: 8 concurrent, 1024 in / 1024 out tokens
$ benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
    --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024

# Accuracy evaluation: 200 samples of GSM8K against a deployed service
$ benchscope eval --mode serving --model Qwen2.5-7B \
    --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

<div class="tip">

**tip**：

CLI and Web task artifacts are fully compatible: you can package any CLI output and restore it in the Web UI via **Datas → Perfs / Evals → Import backup**, exactly like a task created in the UI.

</div>

## FAQ

**Q: What happens when `benchscope` runs with no arguments?**

A: It behaves like `benchscope serve`, launching the Web platform directly.

**Q: Can CLI-created tasks be managed in the Web UI?**

A: Yes. CLI artifacts are fully equivalent to Web tasks and can be viewed or packaged-imported under **Datas → Perfs / Evals**.

**Q: Which command should I pick?**

A: Use [`serve`](/en/docs/cli/serve/) to start the service, [`perf`](/en/docs/cli/perf/) for throughput / latency stress testing (including threshold probing), and [`eval`](/en/docs/cli/eval/) for accuracy evaluation.

## Related

- [Install](/en/docs/install/) — environment requirements and startup
- [Performance Testing](/en/docs/performance/) — Concurrency and Threshold modes
- [Accuracy Testing](/en/docs/accuracy/) — dual-mode evaluation
- [Data (Datas)](/en/docs/data/) — viewing and importing task artifacts
