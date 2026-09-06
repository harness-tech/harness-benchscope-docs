---
title: "Settings"
---

# Settings

The **Settings** page centrally manages the platform’s global configuration across **seven panels**: General / Providers / Models / Datasets / Bench Engines / Skills / Plugins. The page was panelized in **1.0.7**, which also added a per-engine **Mock** switch. Any change is persisted automatically to `settings.json`.

![Settings page](/images/benchscope-settings_default.png)

<div class="tip">

**tip**：

Every change you make in Settings is **persisted automatically** to `~/.benchscope/settings.json` — no manual config-file editing. See [Configuration](/en/docs/install/configuration/).

</div>

## General

- **Data root directory and Cache Paths** — the Root Dir takes effect **immediately (no restart needed)**; subdirectories are read-only (managed by the platform).
- **Global configuration items** such as runtime parameters.

The Cache Paths view lists every subdirectory of your data root — `perfs`, `evals`, `logs`, `sessions`, `datasets`, `models`, `plugins` — so you always know where each kind of data lives and where new data will be written.

<div class="info">

**info**：

Because the Root Dir takes effect immediately and subdirectories are read-only, moving your data root is as simple as changing it here — no restart required. See [Configuration](/en/docs/install/configuration/) for the full directory map.

</div>

## Providers

- Configures the **Base URL** and **API Key** of inference service providers such as **OpenAI-compatible** / **vLLM** / **SGLang**.
- Service **availability** is shown in the **top bar** and on the **Dashboard**.
- Accuracy **Serving mode** defaults to the global Provider configuration when no explicit service is given.

A Provider is a single inference endpoint. For example:

```json
{
  "name": "my-vllm",
  "type": "vllm",
  "base_url": "http://127.0.0.1:8000",
  "api_key": ""
}
```

<div class="tip">

**tip**：

Add your vLLM / SGLang or OpenAI-compatible endpoint **once** here; it then becomes available as a target across Performance, Sessions, and Accuracy (Serving mode).

</div>

## Models

- Maintains the **built-in model list**.
- **Provider models** are shown with a **green label** to distinguish them from the built-in model entries.

## Datasets

- **Built-in dataset management** and the **download directory** (`datasets_dir`).
- Datasets are declared in `datasets.yaml` and downloaded from **modelscope** or a **url source**, cached under the data root at `datasets/{id}/` (default `~/.benchscope/datasets/{id}/`).

## Bench Engines

- **Engine registration and configuration**; cards are **color-coded by source**, and each engine has a **Mock switch** (added in 1.0.7).
- Ships with the self-developed engine **`benchscope`**, and also supports upstream **vLLM / SGLang engines** and **custom engines**.

| Engine | Notes |
| --- | --- |
| `benchscope` (self-developed) | Self-developed engine; no local framework required |
| `vllm-<ver>` | Official vLLM bench engine (for a specific version) |
| `sglang-<ver>` | Official SGLang bench engine (for a specific version) |
| Custom | Registered through skills / plugins |

<div class="info">

**info**：

See [Bench Engine](/en/docs/tools/bench-engine/) for the full engine abstraction. Environment-validation convention: native vLLM / SGLang engines must validate `torch` and the matching framework version, or the next step is blocked.

</div>

## Skills / Plugins

- **Installation and loading directory** for skill packages and plugins (`plugins_dir`).
- Extend the platform with, for example, custom bench engines (created via the `bs-engine-create` skill) and automation.

## Related

- [Configuration](/en/docs/install/configuration/) — data directories and config files
- [Bench Engine](/en/docs/tools/bench-engine/) — engine architecture
- [Performance Testing](/en/docs/performance/) — how providers / engines are used in tests
- [Accuracy Testing](/en/docs/accuracy/) — how datasets / baselines are used in evaluations
