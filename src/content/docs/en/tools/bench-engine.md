---
title: "Bench Engine"
description: "The Bench Engine abstraction: one integration contract for the self-developed, vLLM / SGLang, and custom engines, covering environment validation, parameter descriptions, and metric availability."
---

# Bench Engine

The engine abstraction (Bench Engine) unifies how different stress-test backends are integrated, supporting **self-developed engines, vLLM / SGLang upstream engines**, and **custom engines**, all of which follow the same contract.

## Engine Types

**Performance engines** (available to `benchscope perf`):

| Engine | Description |
| --- | --- |
| `benchscope` (self-developed) | Built-in self-developed engine; streaming timeline collection; metric definitions aligned with vLLM |
| `vllm-0.23` | Official vLLM bench engine (requires torch >= 2.0 + vllm >= 0.23, < 0.24) |
| `sglang-0.5.10` | Official SGLang bench engine (requires torch + sglang >= 0.5.10, < 0.6) |
| Custom engine | Custom engine registered via Upload Engine / import (creation assisted by the `bs-engine-create` skill) |

**Accuracy engines** (available to `benchscope eval`):

| Engine | Description |
| --- | --- |
| `benchscope` (serving) | Serving-chain evaluation via an OpenAI-compatible endpoint (default) |
| `native-hf` | Offline evaluation with local weights (requires torch + transformers, optional LoRA mounting) |
| `mock` | Mock evaluation engine (controllable correctness rate, for integration debugging / demos) |

The self-developed `benchscope` engine is the default engine of `benchscope perf` — **no local framework environment required**, and it can stress-test **remote OpenAI-compatible services** directly; it is also the default serving chain for accuracy evaluation.

## Composition

Each engine has the three parts below, which let the platform integrate engines uniformly without special-casing:

### Environment Validation

- **Validates the engine's dependencies and runtime environment** before startup;
- Native engines (vllm / sglang) strictly validate torch and the framework version; if not satisfied, they are blocked.

### Parameter Description

- Each engine declares its parameters (**cluster / generation / request parameters**);
- Parameters can be **selected from a dropdown with descriptions** in Settings → Bench Engines.

### Metric Availability

- Available → value (blue); unavailable → N/A (gray-black); missing → gray dash;
- A **fixed 11-metric snapshot contract** ensures structural consistency across engines.

## Metric Definitions

The throughput / TTFT / TPOT / ITL metric definitions of the self-developed engine are **aligned with vLLM**, guaranteeing cross-engine comparability — a result measured with the self-developed engine has the same meaning as one measured with a vLLM bench. For the full definitions, see [Performance Core Metrics](/en/docs/performance/metrics/):

| Metric | Definition |
| --- | --- |
| Throughput (output_mean / peakoutput_mean / total_mean) | Output / peak output / total throughput (tok/s) |
| Request throughput (req_per_s) | Completed requests per second (req/s) |
| Single-user throughput (single_user) | Derived from `1000 / TPOT(mean)` (tok/s) |
| TTFT (ttft_mean / ttft_median / ttft_p99) | First-token latency (ms) |
| TPOT (tpot_mean / tpot_median / tpot_p99) | Per-output-token latency (ms) |
| ITL (itl_mean / itl_median / itl_p99) | Inter-token latency (ms) |

## Custom Engines (Advanced)

Create a custom engine via the **`bs-engine-create`** skill. It must follow the implementation contract, which consists of four parts:

- **Input** — how the engine receives a task's parameters;
- **Core** — where the stress-test workload is executed;
- **Output** — how metrics / progress are emitted;
- **Mock** — a Mock implementation for pipeline integration testing.

Once it passes **import validation**, it can be enabled in Settings → Bench Engines. Every engine (including custom engines) has a **Mock switch** for integration testing.

<div class="tip">

**Tip**:

If you need to integrate a stress-test backend that is not yet officially supported (for example, a self-developed inference framework or a gateway proxy), a custom engine is the most flexible path. First refer to the skill template and [Contributing](/en/docs/help/contributing/) to understand the implementation conventions.

</div>

## FAQ

**Question: Why can't I proceed to the next step after selecting an engine?**

Native engines run environment validation; if a matching torch / framework version is not installed on this machine, they are blocked. Switching to the self-developed `benchscope` engine lets you test a remote API directly from this machine.

**Question: Some metrics of a third-party engine show N/A?**

The engine does not support the corresponding metric; metric availability has been made explicit (N/A / gray dash). If you need the full metric set, use the self-developed engine.

## Related docs

- [Settings → Bench Engines](/en/docs/tools/settings/) — configure engines in the UI
- [Performance Core Metrics](/en/docs/performance/metrics/) — full metric definitions of engines
- [Accuracy Core Metrics](/en/docs/accuracy/metrics/) — metric definitions of accuracy engines
- [Built-in Skills](/en/docs/tools/skills/) — the bs-engine-create custom engine skill
- [Architecture](/en/docs/tools/architecture/) — module division
- [v1.0.7 Release Notes](/en/docs/releases/v1-0-7/) — background of the engine rework