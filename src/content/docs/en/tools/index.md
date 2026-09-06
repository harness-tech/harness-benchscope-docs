---
title: "Overview"
---

# Overview

The Tools section covers BenchScope's **advanced usage and platform-level capabilities**: session-based interaction, global settings, and, for developers, the architecture and engine abstraction. It spans four sub-pages covering everything from chatting with a model in the browser to extending the platform itself.

## Sub-pages at a glance

- **[Sessions](/en/docs/tools/sessions/)** — SSE-streaming interactive chat: tune sampling parameters like `temperature` / `top_p`, send messages and watch output stream in real time, with Markdown rendering, code highlighting, reasoning parsing, and a performance bar.
- **[Settings](/en/docs/tools/settings/)** — seven panels for global configuration: General / Providers / Models / Datasets / Bench Engines / Skills / Plugins; every change is persisted to `settings.json` automatically.
- **[Architecture](/en/docs/tools/architecture/)** — the single-process Python (FastAPI) + Vue architecture: core modules, the API facade, the decoupled performance / accuracy modules, and data flow.
- **[Bench Engine](/en/docs/tools/bench-engine/)** — the engine abstraction: unified integration of the self-developed `benchscope` / vLLM / SGLang / custom engines (environment validation / parameter descriptions / metric availability).

## Where to start

| Goal | Go to |
| --- | --- |
| **Chat interactively** with a model in the browser | [Sessions](/en/docs/tools/sessions/) |
| Configure inference providers, model lists, datasets, and engines | [Settings](/en/docs/tools/settings/) |
| Understand how BenchScope works internally | [Architecture](/en/docs/tools/architecture/) |
| Integrate a new stress-testing backend / custom engine | [Bench Engine](/en/docs/tools/bench-engine/) |
| Load a model and run a quick performance or accuracy test | [Quick Start](/en/docs/quickstart/) and [CLI](/en/docs/cli/) |

<div class="tip">

**tip**：

Tools is for **in-platform interaction and global configuration**, plus **extending or contributing to** the platform. If you just want to run a quick test, start with [Quick Start](/en/docs/quickstart/) and the [CLI](/en/docs/cli/).

</div>

## FAQ

**Q: How do the Tools section and the CLI / API relate?**

Tools is the in-browser UI for interaction, configuration, and platform abilities. The [CLI](/en/docs/cli/) and [API](/en/docs/api/) provide equivalent or scriptable entry points that produce the same artifacts and data.

**Q: Do I need to restart after changing Settings?**

The data root (Root Dir) takes effect **immediately**; all other changes are persisted automatically to `~/.benchscope/settings.json`. See [Configuration](/en/docs/install/configuration/).

**Q: What is the difference between Sessions and load / accuracy tests?**

Sessions is **interactive conversation**, for quickly validating answer quality; performance and accuracy tests are **batch stress / evaluation** runs that produce repeatable metrics. Both reuse the same sampling parameters in the [CLI](/en/docs/cli/).

## Related

- [CLI](/en/docs/cli/) — equivalent command-line capabilities
- [API](/en/docs/api/) — HTTP interface
- [Configuration](/en/docs/install/configuration/) — data directories and settings.json
- [Contributing](/en/docs/help/contributing/) — local development and opening a PR
