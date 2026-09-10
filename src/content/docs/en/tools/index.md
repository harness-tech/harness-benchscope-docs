---
title: "Overview"
description: "The BenchScope Tools section at a glance: session-based interaction, global settings, the mock debug environment, and developer-facing architecture and engine abstractions."
---

# Overview

The Tools section covers BenchScope's **advanced usage and platform-level capabilities**: session-based interaction, global settings, and — for developers — the architecture and engine abstraction. Its seven sub-pages cover the complete chain from "chatting with a model in the browser" to "extending the platform itself".

## Sub-pages at a glance

- **[Dashboard Overview](/en/docs/tools/dashboard/)** — the platform home page: statistics overview (performance / accuracy / sessions / built-in skills / models / datasets / Provider counts), environment info (hardware / operating system / network / framework versions), and the latest performance records.
- **[Sessions](/en/docs/tools/sessions/)** — SSE-streaming interactive chat: configure sampling parameters such as `temperature` / `top_p`, send messages and watch streaming output in real time, with Markdown rendering + code highlighting, reasoning parsing, and a performance bar.
- **[Settings](/en/docs/tools/settings/)** — seven panels managing global configuration: General / Providers / Models / Datasets / Bench Engines / Skills / Plugins; every change is persisted to `settings.json` automatically.
- **[Built-in Skills](/en/docs/tools/skills/)** — three Agent skills shipped with the package: `bs-perfs-concurrency` / `bs-perfs-threshold` / `bs-engine-create`, including how to view and download them.
- **[Mock Debug Environment](/en/docs/tools/mock/)** — a complete integration-debugging environment without a real vLLM / SGLang / GPU: mock OpenAI service, FAKE bench backend, and how to run the full feature test cases in simulation.
- **[Architecture](/en/docs/tools/architecture/)** — a monolithic architecture with a Python (FastAPI) backend + Vue frontend: core modules, the API surface, the decoupled performance / accuracy modules, and data flow.
- **[Bench Engine](/en/docs/tools/bench-engine/)** — engine abstraction and customization: a unified integration contract for the self-developed `benchscope` / vLLM / SGLang / custom engines (environment validation / parameter descriptions / metric availability).

## Where should I start

| Your goal | Go to |
| --- | --- |
| View platform status and resource counts | [Dashboard Overview](/en/docs/tools/dashboard/) |
| **Chat interactively** with a model in the browser | [Sessions](/en/docs/tools/sessions/) |
| Configure inference services, model lists, datasets, and engines | [Settings](/en/docs/tools/settings/) |
| Debug all features without a real service / GPU | [Mock Debug Environment](/en/docs/tools/mock/) |
| Understand how BenchScope works internally | [Architecture](/en/docs/tools/architecture/) |
| Integrate a new stress-testing backend / self-developed engine | [Bench Engine](/en/docs/tools/bench-engine/) |
| Run a model for a stress test or evaluation | [Quick Start](/en/docs/quickstart/) and [CLI](/en/docs/cli/) |

<div class="tip">

**Tip**:

The Tools section focuses on **in-platform interaction and global configuration**, as well as **secondary development**. If you just want to run a model for a stress test or evaluation, start with [Quick Start](/en/docs/quickstart/) and the [CLI](/en/docs/cli/).

</div>

## FAQ

**Question: What is the relationship between the Tools section and the command line / API?**

The Tools section is the interaction, configuration, and platform capabilities in the Web UI; the [CLI](/en/docs/cli/) and [API](/en/docs/api/) provide equivalent or scriptable entry points, with fully consistent artifacts and data.

**Question: Do I need to restart after changing Settings?**

The data root directory (Root Dir) takes effect **immediately**, no restart needed; all other changes are persisted automatically to `~/.benchscope/settings.json`. See [Configuration](/en/docs/install/configuration/).

**Question: What is the difference between Sessions and stress / evaluation runs?**

Sessions is **interactive conversation**, used to quickly verify answer quality; stress / evaluation runs are **batch load / batch evaluation**, used to obtain reproducible metrics. Both also use consistent sampling parameters in the [CLI](/en/docs/cli/).

## Related docs

- [CLI](/en/docs/cli/) — equivalent command-line capabilities
- [API](/en/docs/api/) — HTTP interface
- [Configuration](/en/docs/install/configuration/) — data directories and settings.json
- [Contributing](/en/docs/help/contributing/) — local development and submitting PRs