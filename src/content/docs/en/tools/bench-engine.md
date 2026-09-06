---
title: "Bench Engine"
---

# Bench Engine

The **engine abstraction** (Bench Engine) unifies how different stress-testing backends are integrated into BenchScope. It supports the **self-developed engine**, upstream **vLLM / SGLang engines**, and **custom engines**, all behind a common contract.

## Engine Types

| Engine | Description |
| --- | --- |
| `benchscope` (self-developed) | Built-in self-developed engine with streaming timeline collection and metric definitions aligned with vLLM |
| `vllm-<ver>` | Official vLLM bench engine (version-pinned, e.g. `vllm-0.23`) |
| `sglang-<ver>` | Official SGLang bench engine (version-pinned, e.g. `sglang-0.5.10`) |
| Custom | Custom engines registered through skills / plugins (`bs-engine-create`) |

The self-developed `benchscope` engine is the default for `benchscope perf` — it needs **no local framework environment** and can stress **remote OpenAI-compatible services** directly.

## Composition

Every engine is composed of the same three parts, which the platform uses to integrate it without special-casing:

### Environment validation

- Validates the engine’s dependencies and runtime environment **before** starting.
- Native vLLM / SGLang engines require a validated `torch` and matching framework version, or the task is blocked. The self-developed engine needs nothing special.

### Parameter description

- Each engine declares its parameters (**cluster / generation / request parameters**).
- Parameters are surfaced in the UI as **dropdowns with descriptions** under Settings → Bench Engines.

### Metric availability

- **Available → value (blue)** · **Unavailable → N/A (gray-black)** · **Missing → gray dash**.
- A **fixed 11-metric snapshot contract** keeps the structure consistent across engines.

## Metric Definitions

The throughput / TTFT / TPOT / ITL metric definitions of the self-developed engine are **aligned with vLLM** to guarantee **cross-engine comparability** — a result measured with the self-developed engine and one measured with a vLLM bench mean the same thing.

| Metric | Definition |
| --- | --- |
| Throughput | Output (`output_mean`) / total (`total_mean`) throughput, in tok/s |
| TTFT | First-token latency, ms |
| TPOT | Per-output-token latency, ms |
| ITL | Inter-token latency, ms |

## Custom Engines (Advanced)

Custom engines are **created through the `bs-engine-create` skill** and must follow the implementation contract, which consists of four parts:

- **Input** — how the engine receives a task’s parameters
- **Core** — where the stress-testing workload is executed
- **Output** — how metrics / progress are emitted
- **Mock** — a mock implementation for pipeline integration testing

Once a custom engine passes **import validation**, it can be enabled under **Settings → Bench Engines**. Each engine (including custom ones) has a **Mock switch** for integration testing.

<div class="tip">

**tip**：

For stress-testing backends that are not yet officially supported (for example a custom inference framework or a gateway proxy), a custom engine is the most flexible path. Start from the skill template and see [Contributing](/en/docs/help/contributing/) for the implementation conventions.

</div>

## FAQ

**Q: Why can I not proceed after selecting an engine?**

Native vLLM / SGLang engines run environment validation — if `torch` and the matching framework version are not installed, the step is blocked. Switch to the self-developed `benchscope` engine to stress a remote API directly from your machine.

**Q: Why do some metrics show N/A for a third-party engine?**

That engine does not support the metric; availability is made explicit (N/A / gray dash). Use the self-developed engine if you need the full metric set.

## See Also

- [Settings → Bench Engines](/en/docs/tools/settings/) — configuring engines in the UI
- [Architecture](/en/docs/tools/architecture/) — where engines fit in the platform
- [Performance Testing](/en/docs/performance/) — how engines drive load tests
- [v1.0.7 release](/en/docs/releases/v1-0-7/) — the engine-rework background
