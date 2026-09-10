---
title: "配置说明"
description: "数据根目录、默认子目录、settings.json 与内置配置清单。"
---

# 配置说明

BenchScope 的配置遵循「数据落盘统一、网页可视化编辑、配置自动持久化」的原则。绝大部分配置都可以在网页的 **Settings** 页完成，修改会自动持久化到本地的 `settings.json` 文件。

本文介绍数据根目录、配置文件、默认子目录映射以及内置配置清单。

## 数据根目录

所有运行时数据默认集中存放在 `~/.benchscope` 数据根目录下，包括性能测试产物、精度评测结果、日志、数据集缓存、模型缓存、会话缓存与插件目录等。

数据根目录可以通过环境变量 **`BENCHSCOPE_DATA_DIR`** 覆盖：

```bash
export BENCHSCOPE_DATA_DIR=/path/to/custom/data
benchscope
```

<div class="warning">

**warning**：

`BENCHSCOPE_DATA_DIR` 常用于**测试隔离**（例如 CI 中为每次运行创建独立数据目录）。切换数据目录后，之前的性能 / 精度产物不会自动出现在新目录中。该目录存放所有历史产物，请在卸载或清空前确认是否需要备份。

</div>

设置持久化文件为 `~/.benchscope/settings.json`（旧版 `config.json` 会在启动时自动迁移为 `settings.json`，无需手动处理）。

```text
~/.benchscope/
├── settings.json       # 全局设置持久化文件
├── perfs/              # 性能测试任务产物
├── evals/              # 精度评测任务产物
├── analysys/           # 数据分析（联动 Datas）
├── logs/               # 运行日志 + 任务终端输出
├── sessions/           # 会话缓存
├── datasets/           # 数据集下载目录
├── models/             # 模型下载缓存
└── plugins/            # 插件安装加载目录
```

## 默认子目录

数据根目录下的默认子目录映射如下：

| 配置 key | 子目录 | 说明 |
| --- | --- | --- |
| `perfs_dir` | `perfs` | 性能测试任务产物（`run.json`、日志等） |
| `evals_dir` | `evals` | 精度评测任务产物（`eval-<时间>/` 目录） |
| `analysis_dir` | `analysys` | 数据分析（联动 Datas 的 Analysis 面板；内置默认目录名为 `analysys`） |
| `logs_dir` | `logs` | 运行日志 + 任务终端输出 |
| `sessions_dir` | `sessions` | 会话缓存 |
| `datasets_dir` | `datasets` | 数据集下载目录 |
| `models_dir` | `models` | 模型下载缓存 |
| `plugins_dir` | `plugins` | 插件安装加载目录 |

<div class="info">

**info**：

这些子目录配置都可以在 **Settings → General** 的 Cache Paths 面板查看和调整。Root Dir 修改后**即时生效（无需重启）**，而各子目录路径在正常运行中通常为只读展示。

</div>

## Web 界面设置

在网页 **Settings** 页可配置以下七个面板（详见 [设置（Settings）](/zh/docs/tools/settings/)）：

- **General**：数据根目录、Cache Paths 与运行参数等全局配置。
- **Providers**：配置 OpenAI 兼容 / vLLM / SGLang 等推理服务提供方的 Base URL 与 API Key。
- **Models**：维护内置模型清单。
- **Datasets**：内置数据集管理与下载目录。
- **Bench Engines**：性能压测引擎注册与配置。
- **Skills**：技能包管理。
- **Plugins**：插件安装与加载。

所有修改都会自动持久化到 `~/.benchscope/settings.json`：

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

**tip**：

绝大多数场景下**不需要手工编辑 `settings.json`**，直接使用网页 Settings 页即可。只有需要脚本化或批量配置时才建议直接编辑该文件——请先备份原文件。

</div>

## 内置配置清单

BenchScope 内置了多份 YAML 配置文件，作为引擎、参数、数据集等的基础清单：

| 配置文件 | 说明 |
| --- | --- |
| `benchscope/configs/benchscope-default.yaml` | 自研引擎默认参数 |
| `benchscope/configs/vllm-default.yaml` | vLLM 引擎默认参数 |
| `benchscope/configs/sglang-default.yaml` | SGLang 引擎默认参数 |
| `benchscope/configs/bench-params.yaml` | 压测参数描述（含选项级说明文案，驱动创建页参数面板） |
| `benchscope/configs/benchs.yaml` | 引擎注册清单 + 引擎对比表 |
| `benchscope/configs/datasets.yaml` | 内置数据集定义（含精度评测元数据） |
| `benchscope/configs/models.yaml` | 内置模型清单 |
| `benchscope/configs/baselines.yaml` | 精度基线库（10 个开源模型基线） |
| `benchscope/configs/token_estimates.yaml` | Token 预估参数（数据集样本量与平均长度） |

这些清单与网页 Settings 面板联动：例如 Settings → Datasets 展示的数据集来自 `datasets.yaml`；`benchs.yaml` 中的引擎注册清单，是 Settings → Bench Engines 面板能识别自研 `benchscope` 引擎及上游 `vllm-*` / `sglang-*` 引擎的来源。

## 常见问题

**问题：修改配置后需要重启吗？**
General 面板的 Root Dir 即时生效、无需重启；其他面板的配置修改通常也会在保存后即时反映。若遇到异常，重启服务即可生效。

**问题：旧版 `config.json` 还在吗？**
启动时会自动迁移为 `settings.json`，旧文件可安全删除。

**问题：运行数据占空间很大，如何清理？**
可清理 `perfs` / `evals` / `logs` / `datasets` 等子目录中不需要的历史产物，详见 [更新与卸载](/zh/docs/install/update-uninstall/) 的数据清理说明。

## 相关文档

- [安装](/zh/docs/install/) — 环境要求与启动
- [设置（Settings）](/zh/docs/tools/settings/) — 七个面板配置详解
- [数据与统计（Datas）](/zh/docs/data/) — 产物落盘与导入
- [更新与卸载](/zh/docs/install/update-uninstall/) — 数据清理与备份
