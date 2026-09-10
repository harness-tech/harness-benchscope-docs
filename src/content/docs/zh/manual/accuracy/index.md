---
title: "Accuracy 手册概览"
description: "BenchScope 精度测试（Accuracy）手册总览：页面结构、任务列表、评测状态机，以及本手册四篇文档的导航索引。"
---

# Accuracy 手册概览

本手册介绍 **精度测试（Accuracy）** 模块的页面操作：怎么点、怎么填、后台怎么跑。精度测试对模型输出做量化评估，支持 **Serving 链路** 与 **Native 原生** 双模式，内置 **9 个评测数据集** 与专用判分器，并提供 Token 预估与开源基线对标能力。

<div class="info">
**导航位置**：左侧导航「精度测试（accuracy）」。无任务时展示介绍页，点击「创建精度任务（accCreateTask）」进入三步向导。
</div>

## 1. 页面结构

精度页面（`AccuracyView.vue`）按「有无任务」切换两种布局：

- **无任务 — 介绍页**：顶部 `a-result`（标题 + 「创建精度任务」按钮），下方 3 张特性卡片（🎯 模型链路精度测评 / ⚖️ 离线模型精度测评 / 🚨 模型精度基准对比）。
- **有任务 — 两栏布局**：
  - **左栏 任务列表卡片**（`accTasks`）：右上「刷新 / 创建」按钮 + 任务表格（ID / 模型 / 模式 / 数据集 / 状态 / 准确率 / 操作）。
  - **右栏 详情面板**（垂直堆叠卡片）：① 任务头（模型/数据集/种子/温度/进度条）→ ② 核心指标 `accMetrics` → ③ Token 统计（Serving 专属）→ ④ 开源基线对标 `accBenchmark` → ⑤ 分学科准确率 `accSubjects` → ⑥ 评测日志 `accConsole` → ⑦ 单样本溯源 `accSamples`。

```
┌──────────────┐  ┌──────────────────────────────────────┐
│ 任务列表卡片    │  │ 详情面板（垂直堆叠卡片）                 │
│ [刷新][创建]   │  │  ① 任务头  ② 核心指标  ③ Token 统计      │
│ 任务表格        │  │  ④ 基线对标  ⑤ 分学科  ⑥ 日志  ⑦ 样本溯源 │
│ ID/模型/模式/  │  └──────────────────────────────────────┘
│ 数据集/状态/准确率│
└──────────────┘
```

## 2. 任务列表

任务列表（`accTasks`）列字段如下，点击行选中任务并加载详情：

| 列 | 字段 | 说明 |
| --- | --- | --- |
| 任务 ID | `task_id` | 格式 `eval-MMDD-HHMMSS`（冲突时追加 `-N` 后缀） |
| 模型 | `model` | 被测模型名，配置 LoRA 时追加 `LoRA` 标签 |
| 模式 | `mode` | `Native`（绿）/ `Serving`（蓝） |
| 数据集 | `dataset_name` | 数据集名称或本地路径 |
| 状态 | `status` | 见下文状态机 |
| 准确率 | `accuracy` | 完成后显示 `xx%`；运行中显示进度条 |
| 操作 | — | `running` 时显示「停止」，恒显示「删除」 |

## 3. 评测状态机

后端 `EvalTaskManager` 维护独立状态机，任务持久化于 `evals/<task_id>/`：

| 状态 | 值 | 触发条件 |
| --- | --- | --- |
| 等待中 | `pending` | 任务创建后、启动前的初始态 |
| 运行中 | `running` | `start_task()` 启动执行线程 |
| 已完成 | `done` | 全部样本推理并判分成功 |
| 已停止 | `stopped` | 手动点击「停止」，或服务重启时 `running` 任务被中断 |
| 错误 | `error` | 执行过程抛出异常（如数据集加载失败、依赖缺失） |

转移关系：`pending` →（`start_task()`）→ `running` →（结束）→ `done` / `stopped` / `error`。

<div class="warning">
**服务重启**：若服务在任务运行期间重启，所有 `running` 任务会被置为 `stopped`，`error` 字段记录「服务重启，任务中断」。
</div>

## 4. 本手册导航

| 篇 | 文档 | 内容 |
| --- | --- | --- |
| 3.1 | [Accuracy 手册概览](/zh/docs/manual/accuracy/) | 页面结构、任务列表、评测状态机 |
| 3.2 | [创建评测任务](/zh/docs/manual/accuracy/create-task/) | 三步向导：选择数据集 → 模式与模型 → 预览与启动 |
| 3.3 | [数据集与模式](/zh/docs/manual/accuracy/datasets-modes/) | 9 个内置数据集、Serving/Native 双模式、判分器 |
| 3.4 | [结果查看与溯源](/zh/docs/manual/accuracy/results/) | 核心指标、基线对标、分学科准确率、单样本溯源 |

## 5. 相关文档

- [精度测试参考文档](/zh/docs/accuracy/) — 概念与指标口径
- [性能测试手册](/zh/docs/manual/performance/) — 压测操作指南
- [CLI 参考](/zh/docs/cli/) — `benchscope eval` 命令行参数
- [API 参考](/zh/docs/api/) — `/api/accuracy` 完整路由