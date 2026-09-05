# Configuration

BenchScope uses a simple, file-based configuration model. All runtime data lives under a single **data root directory**, and user-editable settings are persisted to a single JSON file. This page explains the directory layout, how to override it, and the built-in configuration files.

## Data Root Directory

The default data root directory is `~/.benchscope`. Every task artifact — performance runs, accuracy evaluations, logs, datasets, models, sessions and plugins — is written beneath it.

You can override the root via the environment variable `BENCHSCOPE_DATA_DIR`:

```bash
export BENCHSCOPE_DATA_DIR=/path/to/my/bench-data
benchscope
```

::: tip
Overriding the data root is commonly used for **test isolation**: run multiple BenchScope instances side by side, or point the platform at a dedicated volume, without interfering with your main data.
:::

Settings are persisted to `~/.benchscope/settings.json`. If you upgrade from an older version that used the legacy `config.json`, the file is **migrated to `settings.json` automatically** on startup — no manual step is needed.

::: warning
`~/.benchscope` holds all of your performance artifacts, accuracy evaluations, logs, downloaded datasets, and cached models. Back it up before uninstalling or wiping it — see [Update & Uninstall](update-uninstall.md).
:::

## Default Subdirectories

The following table maps each configuration key to the corresponding subdirectory under the data root:

| Config key | Subdirectory | Description |
| --- | --- | --- |
| `perfs_dir` | `perfs` | Performance testing task artifacts |
| `evals_dir` | `evals` | Accuracy evaluation task artifacts |
| `analysis_dir` | `analysys` | Data analysis (linked to **Datas**) |
| `logs_dir` | `logs` | Runtime logs + task terminal output |
| `sessions_dir` | `sessions` | Session cache |
| `datasets_dir` | `datasets` | Dataset download directory |
| `models_dir` | `models` | Model download cache |
| `plugins_dir` | `plugins` | Plugin installation / loading directory |

For example, a performance run will write its `run.json` into `~/.benchscope/perfs/` and its terminal log into `~/.benchscope/logs/`, while an accuracy run writes its artifact directory under `~/.benchscope/evals/`.

## Web UI Settings

The **Settings** page in the Web UI is the primary way to change platform configuration. It centralizes the global configuration across multiple panels:

- **General** — data root directory, cache paths, and runtime parameters
- **Providers** — inference service providers (Base URL / API key)
- **Models** — built-in model list management
- **Datasets** — built-in dataset management and download
- **Bench Engines** — engine registration and configuration
- **Skills / Plugins** — skill packages and plugin installation

Any change you make in the UI is **persisted automatically to `settings.json`**. See [Settings](../core/settings.md) for a full walkthrough of each panel.

## List of Built-in Configs

The package ships a set of declared configuration files used to define defaults. These are not usually edited by end users, but understanding them helps you know where behaviour comes from:

| File | Purpose |
| --- | --- |
| `benchscope/configs/benchscope-default.yaml` | Default parameters for the self-developed engine |
| `benchscope/configs/bench-params.yaml` | Stress-test parameter description |
| `benchscope/configs/benchs.yaml` | Engine registration |
| `benchscope/configs/datasets.yaml` | Built-in datasets |
| `benchscope/configs/models.yaml` | Built-in models |
| `benchscope/configs/baselines.yaml` | Accuracy baselines |
| `benchscope/configs/token_estimates.yaml` | Token estimation |

::: info
The engine registry (`benchs.yaml`) is what makes the **Bench Engines** panel in Settings aware of the self-developed `benchscope` engine and the upstream `vllm-*` / `sglang-*` engines. Custom engines registered through skills / plugins extend this registry.
:::

## Related

- [Quick Start](quickstart.md) — installing and launching
- [CLI Reference](cli.md) — `serve` / `perf` / `eval` subcommands
- [Settings](../core/settings.md) — the 7 Settings panels
- [Update & Uninstall](update-uninstall.md) — migration and cleanup of `~/.benchscope`
