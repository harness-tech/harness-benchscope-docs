---
title: "CLI"
---

# CLI

The `benchscope` command-line brings the platform's capabilities to your terminal: start the service, run performance testing and accuracy evaluation — all with a single command, producing artifacts fully compatible with the Web UI.

```text
benchscope [--version] {serve,perf,eval} [subcommand options]
```

- **`benchscope`** (or `benchscope serve`): starts the Web service, opening the full platform at `http://127.0.0.1:8080` by default.
- **`benchscope perf`**: runs one performance test (Concurrency / Threshold mode), prints throughput and latency metrics, and saves `run.json`.
- **`benchscope eval`**: runs one accuracy evaluation (Serving / Native / Mock), prints accuracy / pass_rate metrics, and saves to `evals/eval-<time>/`.

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

All CLI task artifacts can be packaged and restored in the Web UI via **Datas → Perfs / Evals → Import backup**, fully compatible with tasks created in the UI.

## Related

- [CLI Reference](/en/docs/cli/reference/) — complete `serve` / `perf` / `eval` option tables
- [Install](/en/docs/install/) — environment requirements and startup
- [Performance Testing](/en/docs/performance/) — Concurrency and Threshold modes
- [Accuracy Testing](/en/docs/accuracy/) — dual-mode evaluation
