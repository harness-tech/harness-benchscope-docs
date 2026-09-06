---
title: "Configuration"
description: "Data root directory, default subdirectories, settings.json, and built-in config lists."
---

# Configuration

BenchScope uses a simple, file-based configuration model. All runtime data lives under a single **data root directory**, and user-editable settings are persisted to a single JSON file. Most configuration can be done visually in the **Settings** page of the web UI, and every change is automatically persisted to `settings.json`.

This page explains the data root directory, the configuration file, the default subdirectory mapping, and the built-in configuration files.

## Data Root Directory

All runtime data defaults to a single data root at `~/.benchscope`. Every task artifact — performance runs, accuracy evaluations, logs, datasets, models, sessions and plugins — is written beneath it.

You can override the root via the environment variable `BENCHSCOPE_DATA_DIR`:

```bash
export BENCHSCOPE_DATA_DIR=/path/to/custom/data
benchscope
```

<div class="warning">

**warning**：

`BENCHSCOPE_DATA_DIR` is often used for **test isolation** (e.g. a fresh data directory per run in CI). After switching the data root, earlier performance / accuracy artifacts do **not** appear in the new directory. The root holds all of your historical artifacts — back it up before uninstalling or wiping it.

</div>

Settings are persisted to `~/.benchscope/settings.json`. If you upgrade from an older version that used the legacy `config.json`, the file is **migrated to `settings.json` automatically** on startup — no manual step is needed.

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

The following table maps each configuration key to the corresponding subdirectory under the data root:

| Config key | Subdirectory | Description |
| --- | --- | --- |
| `perfs_dir` | `perfs` | Performance testing task artifacts (`run.json`, logs, ...) |
| `evals_dir` | `evals` | Accuracy evaluation task artifacts (`eval-<time>/` dirs) |
| `analysis_dir` | `analysys` | Data analysis (linked to the Datas Analysis panel) |
| `logs_dir` | `logs` | Runtime logs + task terminal output |
| `sessions_dir` | `sessions` | Session cache |
| `datasets_dir` | `datasets` | Dataset download directory |
| `models_dir` | `models` | Model download cache |
| `plugins_dir` | `plugins` | Plugin installation / loading directory |

<div class="info">

**info**：

These subdirectory settings can be viewed and adjusted in **Settings → General → Cache Paths**. The Root Dir takes effect **immediately (no restart needed)**, while the individual subdirectory paths are normally shown read-only during normal operation.

</div>

## Web UI Settings

The **Settings** page in the Web UI is the primary way to change platform configuration. It centralizes the global configuration across seven panels (see [Settings](/en/docs/tools/settings/)):

- **General** — data root directory, cache paths, and runtime parameters
- **Providers** — inference service providers (OpenAI-compatible / vLLM / SGLang Base URL & API key)
- **Models** — built-in model list management
- **Datasets** — built-in dataset management and download
- **Bench Engines** — engine registration and configuration
- **Skills** — skill package management
- **Plugins** — plugin installation and loading

Any change you make in the UI is **persisted automatically to `settings.json`**:

```json
{
  "perfs_dir": "perfs",
  "evals_dir": "evals",
  "analysis_dir": "analysys",
  "logs_dir": "logs",
  "sessions_dir": "sessions",
  "datasets_dir": "datasets",
  "models_dir": "models",
  "plugins_dir": "plugins",
  "providers": [],
  "models": [],
  "datasets": [],
  "bench_engines": []
}
```

<div class="tip">

**tip**：

In most cases you do **not** need to hand-edit `settings.json` — use the Settings page instead. Only edit the file directly for scripting or bulk configuration, and back it up first.

</div>

## Built-in Configuration Files

The package ships a set of YAML configuration files used to define defaults (engines, parameters, datasets, and so on). These are not usually edited by end users, but understanding them helps you know where behaviour comes from:

| File | Purpose |
| --- | --- |
| `benchscope/configs/benchscope-default.yaml` | Default parameters for the self-developed engine |
| `benchscope/configs/bench-params.yaml` | Stress-test parameter description |
| `benchscope/configs/benchs.yaml` | Engine registration |
| `benchscope/configs/datasets.yaml` | Built-in datasets |
| `benchscope/configs/models.yaml` | Built-in models |
| `benchscope/configs/baselines.yaml` | Accuracy baselines |
| `benchscope/configs/token_estimates.yaml` | Token estimation |

These lists are linked to the Settings panels — for example, the datasets shown in Settings → Datasets come from `datasets.yaml`, and the engine registry in `benchs.yaml` is what makes Settings → Bench Engines aware of the self-developed `benchscope` engine and the upstream `vllm-*` / `sglang-*` engines.

## FAQ

**Q: Do I need to restart after changing a setting?**
The Root Dir in the General panel takes effect immediately with no restart. Other panel changes usually take effect right after saving; if something seems off, restart the service.

**Q: Is the legacy `config.json` still used?**
It is migrated to `settings.json` automatically on startup, and the old file can be safely deleted.

**Q: My runtime data is taking a lot of space — how do I clean it up?**
Clean up unwanted historical artifacts under subdirectories such as `perfs` / `evals` / `logs` / `datasets`. See the data-cleanup notes in [Update & Uninstall](/en/docs/install/update-uninstall/).

## Related

- [Install](/en/docs/install/) — requirements and launching
- [Settings](/en/docs/tools/settings/) — the 7 Settings panels
- [Data & Statistics (Datas)](/en/docs/data/) — artifact persistence and import
- [Update & Uninstall](/en/docs/install/update-uninstall/) — data cleanup and backup
