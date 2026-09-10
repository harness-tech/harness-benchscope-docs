---
title: "架构介绍"
description: "BenchScope 单体 Web 平台的整体架构：核心模块、API 面、性能与精度模块解耦设计及数据流。"
---

# 架构介绍

BenchScope 是一个「后端 Python（FastAPI）+ 前端 Vue」的**单体 Web 平台**，前后端由同一个 `benchscope` 命令统一启动。

## 整体架构

```text
┌──────────────────────────────────────────────────────┐
│                     Web 前端 (Vue3 + antd)            │
│   Dashboard · 性能测试 · 精度测试 · 会话 · 数据 · 设置  │
└───────────────────────────┬──────────────────────────┘
                            │ HTTP / SSE / WS
┌───────────────────────────┴──────────────────────────┐
│               backend (FastAPI — benchscope/server)   │
│   api_benchs · api_accuracy · api_dashboard ·         │
│   api_config · api_logs · api_sessions · api_tasks ·  │
│   api_skills · api_test（legacy）· /api/version · /ws  │
└───────┬──────────────────────┬───────────────────────┘
        │ 任务执行               │ 配置持久化
┌───────┴────────┐     ┌────────┴─────────┐
│  benches/      │     │  config.py       │
│  runner ·      │     │  ~/.benchscope/  │
│  builtin_bench │     │  settings.json   │
│  vllm · sglang │     └──────────────────┘
├───────────────┤
│  accuracy/     │  executor · metrics · baselines ·
│  native_runner │  scorers · datasets · estimator
└───────┬────────┘
        ▼
 推理服务 (vLLM / SGLang / 任意 OpenAI 兼容 API)
```

前端通过 **HTTP / SSE / WebSocket** 与后端交互；后端执行性能压测与精度评测，并把配置与产物持久化到数据根目录下。

## 核心模块

| 模块 | 职责 |
| --- | --- |
| `benchscope/server` | FastAPI 应用与各 REST / SSE API |
| `benchscope/benches` | 性能压测引擎：自研引擎、vLLM、SGLang 及 runner |
| `benchscope/accuracy` | 精度评测：executor / metrics / baselines / scorers / estimator / datasets |
| `benchscope/config.py` | 配置持久化（settings.json）与运行时单例 |
| `benchscope/task_manager.py` / `session_manager.py` | 任务调度与会话管理 |
| `benchscope/cli.py` | 命令行入口（serve / perf / eval） |

### API 面

后端对外暴露一组 API 分组，供前端消费（完整清单见 [API 概述](/zh/docs/api/)）：

- `api_config` — 配置读写（含 Providers / Models / Datasets / 目录 / 重启）
- `api_tasks` — 性能测试任务管理（创建 / 启动 / 停止 / 日志 / 导出）
- `api_logs` — 日志与历史运行（列表 / 详情 / 实时 / 备份 / 导入 / 汇总）
- `api_dashboard` — 概览统计 / 环境信息
- `api_sessions` — 会话对话（SSE 流式）
- `api_accuracy` — 精度评测任务（任务 / 样本 / 对标 / 引擎 / 数据集 / 预估 / 基线）
- `api_benchs` — 内置引擎（清单 / 详情 / 环境校验 / 上传 / 导入 / 参数）
- `api_skills` — 内置技能（清单 / 下载）
- `api_test` — 精度测试 legacy 接口（start / preview / stop / status）
- `/api/version` · `/ws` — 版本查询与 WebSocket 实时推送

### 性能模块（benches）

- `runner`：任务运行器，负责拉起压测、收集与汇总指标；
- `builtin_bench`：自研引擎实现（流式时间线采集，指标口径对齐 vLLM）；
- `vllm` / `sglang`：上游官方 bench 引擎的封装与版本化。

### 精度模块（accuracy）

- `executor`：评测执行器；
- `metrics`：指标统计（accuracy / pass_rate / 专项指标）；
- `baselines`：开源基线库与档位评级；
- `scorers`：判分器（choice / math / code / judge）；
- `datasets`：内置数据集定义与加载；
- `estimator`：Token 预估算。

### 配置与调度

- 配置统一持久化到数据根目录下的 `settings.json`（默认 `~/.benchscope/settings.json`），数据根目录可通过环境变量 `BENCHSCOPE_DATA_DIR` 覆盖，见 [配置说明](/zh/docs/install/configuration/)；
- `task_manager` 负责任务调度，`session_manager` 负责会话管理。

<div class="info">

**info**：

架构遵循「性能与精度模块解耦」的原则：两者拥有独立的任务、结果与调度，互不依赖，便于独立扩展与维护。

</div>

## Bench 引擎抽象

引擎抽象支持自研 `benchscope` 引擎、vLLM / SGLang 上游引擎与自定义引擎，提供**环境校验**与**参数描述**，并将第三方引擎的**指标可得性显式化**。详见 [Bench 引擎](/zh/docs/tools/bench-engine/)。

## 技术栈总览

| 层 | 技术 |
| --- | --- |
| 前端 | Vue 3 + antd |
| 后端 | Python + FastAPI |
| 实时通信 | HTTP / SSE / WebSocket |
| 配置 | settings.json（YAML 内置清单） |
| 推理服务 | vLLM / SGLang / 任意 OpenAI 兼容 API |

## 相关文档

- [Bench 引擎](/zh/docs/tools/bench-engine/) — 引擎抽象与自定义
- [配置说明](/zh/docs/install/configuration/) — 数据目录与持久化
- [参与贡献](/zh/docs/help/contributing/) — 本地开发与贡献流程