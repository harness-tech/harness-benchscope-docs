---
title: "Configuration"
description: "Data root directory, default subdirectories, settings.json, and built-in config lists."
---

# Configuration

BenchScope follows the configuration principles of "unified on-disk data, visual editing in the web UI, and automatic persistence of settings". Most configuration can be completed on the web **Settings** page, and changes are automatically persisted to the local `settings.json` file.

This page covers the data root directory, the configuration file, the default subdirectory mapping, and the built-in configuration lists.

## Data Root Directory

By default, all runtime data is stored centrally under the `~/.benchscope` data root directory, including performance test artifacts, accuracy evaluation results, logs, dataset caches, model caches, session caches, and the plugins directory.

The data root directory can be overridden with the environment variable **`BENCHSCOPE_DATA_DIR`**:

```bash
export BENCHSCOPE_DATA_DIR=/path/to/custom/data
benchscope
```

<div class="warning">

**Warning**:

`BENCHSCOPE_DATA_DIR` is commonly used for **test isolation** (for example, creating a separate data directory per run in CI). After switching data directories, previous performance / accuracy artifacts will not automatically appear in the new directory. The directory holds all historical artifacts — please confirm whether a backup is needed before uninstalling or wiping it.

</div>

The settings persistence file is `~/.benchscope/settings.json` (the legacy `config.json` is automatically migrated to `settings.json` on startup; no manual handling is needed).

```text
~/.benchscope/
├── settings.json       # global settings persistence file
├── perfs/              # performance testing task artifacts
├── evals/              # accuracy evaluation task artifacts
├── analysys/           # data analysis (linked to Datas)
├── logs/               # runtime logs + task terminal output
├── sessions/           # session cache
├── datasets/           # dataset download directory
├── models/             # model download cache
└── plugins/            # plugin installation / loading directory
```

## Default Subdirectories

The default subdirectory mapping under the data root directory is as follows:

| Config key | Subdirectory | Description |
| --- | --- | --- |
| `perfs_dir` | `perfs` | Performance testing task artifacts (`run.json`, logs, etc.) |
| `evals_dir` | `evals` | Accuracy evaluation task artifacts (`eval-<time>/` directories) |
| `analysis_dir` | `analysys` | Data analysis (linked to the Datas Analysis panel; the built-in default directory name is `analysys`) |
| `logs_dir` | `logs` | Runtime logs + task terminal output |
| `sessions_dir` | `sessions` | Session cache |
| `datasets_dir` | `datasets` | Dataset download directory |
| `models_dir` | `models` | Model download cache |
| `plugins_dir` | `plugins` | Plugin installation / loading directory |

<div class="info">

**Info**:

All of these subdirectory settings can be viewed and adjusted in the Cache Paths panel of **Settings → General**. Changes to the Root Dir take effect **immediately (no restart needed)**, while the individual subdirectory paths are usually shown read-only during normal operation.

</div>

## Web Interface Settings

The web **Settings** page lets you configure the following seven panels (see [Settings](/en/docs/tools/settings/) for details):

- **General**: global configuration such as the data root directory, Cache Paths, and runtime parameters.
- **Providers**: Base URL and API Key for inference service providers (OpenAI-compatible, vLLM, SGLang, etc.).
- **Models**: maintenance of the built-in model list.
- **Datasets**: built-in dataset management and download directory.
- **Bench Engines**: registration and configuration of performance stress-test engines.
- **Skills**: skill package management.
- **Plugins**: plugin installation and loading.

All changes are automatically persisted to `~/.benchscope/settings.json`:

```json
{
  "framework": "vllm",
  "api": {
    "base_url": "http://127.0.0.1:8000",
    "endpoint": "/v1/chat/completions",
    "api_key": "",
    "extra_headers": {}
  },
  "providers": [],
  "active_provider": "",
  "gpu": { "auto": true, "name": "", "count": 8 },
  "data_dir": "~/.benchscope",
  "perfs_dir": "~/.benchscope/perfs",
  "evals_dir": "~/.benchscope/evals",
  "analysis_dir": "~/.benchscope/analysys",
  "logs_dir": "~/.benchscope/logs",
  "sessions_dir": "~/.benchscope/sessions",
  "models_dir": "~/.benchscope/models",
  "datasets_dir": "~/.benchscope/datasets",
  "plugins_dir": "~/.benchscope/plugins",
  "tpot_threshold_ms": 100,
  "request_rate": "inf",
  "bench_commands": {
    "vllm": "vllm bench serve",
    "sglang": "python -m sglang.bench_serving"
  },
  "engine_mocks": {}
}
```

<div class="tip">

**Tip**:

In most cases you do **not** need to hand-edit `settings.json` — the web Settings page is enough. Edit the file directly only when scripting or applying configuration in bulk, and back up the original file first.

</div>

## Built-in Configuration Lists

BenchScope ships multiple built-in YAML configuration files as the base lists for engines, parameters, datasets, and so on:

| Config file | Description |
| --- | --- |
| `benchscope/configs/benchscope-default.yaml` | Default parameters of the built-in engine |
| `benchscope/configs/vllm-default.yaml` | Default parameters of the vLLM engine |
| `benchscope/configs/sglang-default.yaml` | Default parameters of the SGLang engine |
| `benchscope/configs/bench-params.yaml` | Stress-test parameter descriptions (including option-level help text, driving the creation-page parameter panel) |
| `benchscope/configs/benchs.yaml` | Engine registration list + engine comparison table |
| `benchscope/configs/datasets.yaml` | Built-in dataset definitions (including accuracy evaluation metadata) |
| `benchscope/configs/models.yaml` | Built-in model list |
| `benchscope/configs/baselines.yaml` | Accuracy baseline library (10 open-source model baselines) |
| `benchscope/configs/token_estimates.yaml` | Token estimation parameters (dataset sample counts and average lengths) |

These lists are linked to the web Settings panels: for example, the datasets shown in Settings → Datasets come from `datasets.yaml`; the engine registration list in `benchs.yaml` is what lets the Settings → Bench Engines panel recognize the built-in `benchscope` engine and the upstream `vllm-*` / `sglang-*` engines.

## FAQ

**Question: Do I need to restart after changing a setting?**
The Root Dir in the General panel takes effect immediately with no restart; changes in other panels are normally also reflected immediately after saving. If you run into an issue, restarting the service applies the changes.

**Question: Is the legacy `config.json` still there?**
It is automatically migrated to `settings.json` on startup; the old file can be safely deleted.

**Question: Runtime data takes up a lot of space — how do I clean it up?**
You can clean up unneeded historical artifacts under subdirectories such as `perfs` / `evals` / `logs` / `datasets`; see the data-cleanup notes in [Update & Uninstall](/en/docs/install/update-uninstall/) for details.

## Related Docs

- [Install](/en/docs/install/) — environment requirements and startup
- [Settings](/en/docs/tools/settings/) — detailed configuration of the seven panels
- [Data & Statistics (Datas)](/en/docs/data/) — artifact persistence and import
- [Update & Uninstall](/en/docs/install/update-uninstall/) — data cleanup and backup