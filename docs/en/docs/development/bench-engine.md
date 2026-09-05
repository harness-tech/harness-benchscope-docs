# Bench Engine

The **engine abstraction** (Bench Engine) unifies how different stress-testing backends are integrated into BenchScope. It supports the **self-developed engine**, upstream **vLLM / SGLang engines**, and **custom engines**, all behind a common contract.

## Engine Types

| Engine | Description |
| --- | --- |
| `benchscope` (self-developed) | Built-in self-developed engine with streaming timeline collection and metric definitions aligned with vLLM |
| `vllm-<ver>` | Official vLLM bench engine (version-pinned, e.g. `vllm-0.23`) |
| `sglang-<ver>` | Official SGLang bench engine (version-pinned, e.g. `sglang-0.5.10`) |
| Custom Engines | Custom engines registered through skills / plugins (`bs-engine-create`) |

The self-developed `benchscope` engine is the default for `benchscope perf` — it needs **no local framework environment** and can stress **remote OpenAI-compatible services** directly.

## Composition

Every engine is composed of the same three parts, which the platform uses to integrate it without special-casing:

- **Environment validation** — validates the engine’s dependencies and runtime environment *before* starting. Native vLLM / SGLang engines require the matching framework version; the self-developed engine needs nothing special.
- **Parameter description** — each engine declares its parameters (cluster / generation / request parameters), surfaced as dropdowns with descriptions in the UI.
- **Metric availability** — *available → value*, *unavailable → N/A*, *missing → gray dash*, under a **fixed 11-metric snapshot contract**.

## Metric Definitions

The throughput / TTFT / TPOT / ITL metric definitions of the self-developed engine are **aligned with vLLM** to guarantee **cross-engine comparability** — a result measured with the self-developed engine and one measured with a vLLM bench mean the same thing.

| Metric | Definition |
| --- | --- |
| Throughput | Output (`output_mean`) / total (`total_mean`) throughput in tok/s |
| TTFT | First-token latency, ms |
| TPOT | Per-output-token latency, ms |
| ITL | Inter-token latency, ms |

## The 11-metric snapshot contract

Every engine reports a fixed set of 11 metrics per snapshot. If a third-party engine cannot provide one of them, it is marked explicitly:

- **Available** → the value is shown (blue).
- **Unavailable** → shown as `N/A` (gray-black).
- **Missing** → shown as a gray dash.

This keeps the real-time panel and the record schema consistent no matter which engine produced the data.

## Custom Engines (Advanced)

Custom engines are **created through the `bs-engine-create` skill** and must follow the implementation contract, which consists of four parts:

- **Input** — how the engine receives a task’s parameters
- **Core** — where the stress-testing workload is executed
- **Output** — how metrics / progress are emitted
- **Mock** — a mock implementation for pipeline integration testing

Once a custom engine passes **import validation**, it can be enabled under **Settings → Bench Engines**. Each engine (including custom ones) has a **Mock switch** for integration testing.

## See Also

- [Architecture](architecture.md) — where engines fit in the platform
- [Settings → Bench Engines](../core/settings.md) — configuring engines in the UI
- [Performance Testing](../core/performance.md) — how engines drive load tests
