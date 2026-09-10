---
title: "Settings"
description: "The Settings page manages global configuration through seven panels: General / Providers / Models / Datasets / Bench Engines / Skills / Plugins, with changes persisted automatically to settings.json."
---

# Settings

The Settings page manages the platform's global configuration across **seven panels**: General / Providers / Models / Datasets / Bench Engines / Skills / Plugins (panelized in 1.0.7, with a new per-engine Mock switch added).

![BenchScope Settings default view](/images/benchscope-settings_default.png)

<div class="tip">

**Tip**:

Every change in Settings is **persisted automatically** to `~/.benchscope/settings.json`; no manual editing of config files is needed. See [Configuration](/en/docs/install/configuration/).

</div>

## General

- **Data root directory and Cache Paths**: the Root Dir takes effect **immediately (no restart needed)**; each subdirectory is displayed read-only by default (managed by the platform).

| Setting | Description |
| --- | --- |
| Root Dir | Data root directory (default `~/.benchscope`); changes take effect immediately |
| perfs / evals / logs / sessions / datasets / models / plugins / ... | Mapping of each subdirectory (read-only display) |

<div class="info">

**Info**:

The Cache Paths view lists every subdirectory under the data root (`perfs`, `evals`, `logs`, `sessions`, `datasets`, `models`, `plugins`, etc.), so you can see clearly where each kind of data is stored and where new data will be written.

</div>

## Providers

- Configure the **Base URL** and **API Key** of inference service providers such as OpenAI-compatible / vLLM / SGLang.
- Each Provider card shows: name, Base URL, API Key, **model availability status**, and **the list of probed models**.
- Service **availability status** is shown in the top bar and on the Dashboard.
- Accuracy Serving mode **defaults to the global Provider configuration** (no need to fill in the address repeatedly each time); session requests are likewise proxied to the active Provider.

A Provider is a single inference service endpoint, for example:

```json
{
  "id": "provider_my-vllm",
  "name": "my-vllm",
  "base_url": "http://127.0.0.1:8000",
  "api_key": ""
}
```

<div class="info">

**Info**:

Providers in legacy configurations that lack an `id` (such as the old "Default") get a **stable id backfilled automatically** at config load time (generated from the name slug, with a numeric suffix appended on collision); no manual completion is needed.

</div>

<div class="tip">

**Tip**:

**Add** a vLLM / SGLang or OpenAI-compatible endpoint **once** here, and it can be used as a target for performance testing, sessions, and accuracy (Serving mode).

</div>

## Models

- Maintains the **built-in model list**;
- Provider models are shown with a **green label**, making it easy to distinguish the "built-in list" from "Provider dynamic models".

## Datasets

- **Built-in dataset** management and the download directory (`datasets_dir`);
- Datasets are defined by `datasets.yaml` (currently **12**: 9 accuracy evaluation datasets + 3 performance stress-test datasets, see [Evaluation Datasets](/en/docs/accuracy/datasets/)); they can be downloaded from **modelscope** or a **url source**, and cached in `datasets/{id}/` under the data root (default `~/.benchscope/datasets/{id}/`).

## Bench Engines

- **Engine registration and configuration**; cards are **color-coded by source** (built-in blue / user-uploaded purple), and each engine can turn on its **Mock switch**.
- Built-in self-developed engine **`benchscope`**, plus support for vLLM / SGLang upstream engines and custom engines.

| Engine | Description |
| --- | --- |
| `benchscope` (self-developed) | Built-in self-developed engine; no local framework environment required; also supports Serving-chain accuracy evaluation |
| `vllm-0.23` | Official vLLM bench engine (requires torch >= 2.0 + vllm >= 0.23, < 0.24) |
| `sglang-0.5.10` | Official SGLang bench engine (requires torch + sglang >= 0.5.10, < 0.6) |
| `native-hf` | Local-weights accuracy evaluation engine (requires torch + transformers, optional LoRA) |
| `mock` | Mock accuracy evaluation engine (controllable correctness rate, for integration debugging) |
| Custom engine | Registered via Upload Engine / import (creation can be assisted by the `bs-engine-create` skill) |

<div class="info">

**Info**:

See [Bench Engine](/en/docs/tools/bench-engine/) for the full engine design. Environment validation convention: native engines (vllm / sglang) must validate torch and the corresponding framework version; if not satisfied, they are blocked from proceeding to the next step.

</div>

## Skills / Plugins

- **Installation and loading directory** for **skill packages** and **plugins** (`plugins_dir`);
- The Skills panel shows the **3 built-in skills** (`bs-perfs-concurrency` / `bs-perfs-threshold` / `bs-engine-create`), with packaged downloads supported; see [Built-in Skills](/en/docs/tools/skills/) for details;
- For example, create a custom engine via the `bs-engine-create` skill.

## Related docs

- [Configuration](/en/docs/install/configuration/) — data directories and settings.json
- [Dashboard Overview](/en/docs/tools/dashboard/) — resource counts and Provider model counts
- [Built-in Skills](/en/docs/tools/skills/) — viewing and downloading the 3 built-in skills
- [Bench Engine](/en/docs/tools/bench-engine/) — engine architecture and customization
- [Performance Testing](/en/docs/performance/) — stress testing with Bench Engines
- [Accuracy Testing](/en/docs/accuracy/) — use of datasets / baselines in evaluations