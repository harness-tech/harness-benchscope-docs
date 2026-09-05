# Settings

The **Settings** page centrally manages the platform’s global configuration across **seven panels**: General / Providers / Models / Datasets / Bench Engines / Skills / Plugins. The page was panelized since **1.0.7**, which also added a per-engine **Mock** switch. Any change is persisted automatically to `settings.json`.

![Settings page](/images/benchscope-settings_default.png)

## General

- **Data root directory and Cache Paths** — the Root Dir takes effect **immediately (no restart needed)**, and the subdirectories are read-only (they are managed by the platform).
- **Global configuration items** such as runtime parameters.

The Cache Paths view shows every subdirectory of your data root — `perfs`, `evals`, `analysys`, `logs`, `sessions`, `datasets`, `models`, `plugins` — so you always know where each kind of data lives, and where new data will be written.

::: info
Because the Root Dir takes effect immediately and subdirectories are read-only, moving your data root is as simple as changing it here — no restart required. See [Configuration](../get-started/configuration.md) for the full directory map.
:::

## Providers

- Configures the **Base URL** and **API Key** of inference service providers such as **OpenAI-compatible** / **vLLM** / **SGLang**.
- Service **availability** is shown in the **top bar** and on the **Dashboard**.
- Accuracy **Serving mode** defaults to the global Provider configuration when no explicit service is given.

::: tip
Add your vLLM / SGLang or OpenAI-compatible endpoint here once; it will then be available as a target across Performance, Sessions, and Accuracy (Serving mode).
:::

## Models

- Maintains the **built-in model list**.
- **Provider models** are shown with a **green label** to distinguish them from the built-in model entries.

## Datasets

- **Built-in dataset management** and the **download directory** (`datasets_dir`).
- Datasets are declared in `datasets.yaml` and downloaded from **modelscope** or a **url source**, cached to `data_dir/datasets/{id}/`.

## Bench Engines

- **Engine registration and configuration**; cards are **color-coded by source**, and each engine has a **Mock switch** (added in 1.0.7).
- Ships with the self-developed engine **`benchscope`**, and also supports upstream **vLLM / SGLang engines** and **custom engines**.

| Engine | Notes |
| --- | --- |
| `benchscope` | Self-developed engine; no local framework required |
| `vllm-<ver>` | Official vLLM bench engine (for a specific version) |
| `sglang-<ver>` | Official SGLang bench engine (for a specific version) |
| Custom | Registered through skills / plugins (`bs-engine-create`) |

See [Bench Engine](../development/bench-engine.md) for the engine abstraction.

## Skills / Plugins

- **Installation and loading directory** for skill packages and plugins (`plugins_dir`).
- Skills / plugins extend the platform with, for example, custom bench engines and automation.

## Related

- [Configuration](../get-started/configuration.md) — data directories and config files
- [Bench Engine](../development/bench-engine.md) — engine architecture
- [Performance Testing](performance.md) — how providers / engines are used in tests
- [Accuracy Testing](accuracy.md) — how datasets / baselines are used in evaluations
