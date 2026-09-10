---
title: "Performance 手册概览"
description: "BenchScope 性能测试（Performance）手册总览：页面结构、任务列表、任务状态机，以及本手册五篇文档的导航索引。"
---

# Performance 手册概览

本手册面向 **性能测试（Performance）** 模块，讲解「怎么点、怎么填、后台怎么跑」。性能测试对已部署的推理服务（OpenAI 兼容接口）进行压测，支持 **并发模式** 与 **阈值模式**，提供实时监控、统计图表与 Excel 导出。

<div class="info">
**导航位置**：左侧导航「性能测试（performance）」，路由 `/performance`；无任务时展示介绍页，点击「并发模式 / 阈值模式」进入创建向导（`/performance/create?mode=concurrency|threshold`）。
</div>

## 1. 页面结构

性能页面（`PerformanceView.vue`）按「有无任务」切换两种布局：

- **无任务 — 介绍页**：顶部 `a-result`（标题 + 副标题「一键发起 vLLM / SGLang 服务性能基准测试」）+ 两个模式按钮 + 3 张特性卡片（⚡ 并发测试 / 🎯 阈值搜索 / 📈 实时性能图表）。
- **有任务 — 四行布局**：
  - **第一行，三个等宽面板**：Perf 面板（任务信息 + 开始测试/停止测试/关闭）｜Cases 面板（条件组与请求数标签）｜Logs 面板（终端式日志 + 下载）。
  - **第二行，实时监控**：Profile Progress（左 1/3）+ Real-Time Metrics（右 2/3），按「当前请求」快照渲染。
  - **第三行，Realtime Data**：按条件组分组的结果表格（本地面板阈值 + 列设置 + Excel 导出）。
  - **第四行，Statistics**：12 张统计图（4 指标组 × Mean/Median/P99），支持 tooltip 联动。

```
┌───────────────────────────────────────────────────────────┐
│ 第一行: Perf 面板 │ Cases 面板 │ Logs 面板 (各占 1/3)     │
│ 第二行: Profile Progress (1/3) │ Real-Time Metrics (2/3)  │
│ 第三行: Realtime Data 分组结果表    │ 第四行: Statistics  │
└───────────────────────────────────────────────────────────┘
```

## 2. 任务列表

性能页面采用**单任务语义**：始终展示最近创建的任务，后端 `TaskManager` 维护完整任务列表（`GET /api/tasks` 按 `created_at` 倒序，不含 `rows`），持久化于 `~/.benchscope/perfs/tasks/<task_id>.json`。i18n 保留了 `newTask` / `taskList` 等键（旧多任务列表版），当前界面不再渲染独立任务列表；历史记录可在 **Datas → Perfs** 查看。

| 字段 | 说明 |
| --- | --- |
| `task_id` | 格式 `task-MMDD-HHMMSS` |
| `model` / `framework` | 被测模型与框架（Bench CLI / vLLM / SGLang） |
| `mode` | `concurrency`（并发模式）/ `threshold`（阈值模式） |
| `cases` | 条件组列表（含 `case_id`、输入/输出长度、每组阈值） |
| `status` | 任务状态，见下文状态机 |
| `rows` | 已完成结果行（每个请求数一行；列表接口不含，需 `GET /api/tasks/{task_id}` 单独获取） |
| `run_dir` / `log_path` | 运行记录目录 `~/.benchscope/perfs/<run_id>/` 与终端日志路径 |

## 3. 任务状态机

后端 `TaskManager`（`benchscope/task_manager.py`）维护任务状态机：

| 状态 | 值 | 触发条件 |
| --- | --- | --- |
| 待开始 | `pending` | 任务创建后（`POST /api/tasks`）、启动前的初始态 |
| 运行中 | `running` | `POST /api/tasks/{task_id}/start` 启动执行线程 |
| 已完成 | `done` | 全部点位执行完毕；阈值模式因超 `max_requests` 强制结束时页面显示 `Finish` |
| 已停止 | `stopped` | 点击「停止测试」，或服务重启时 `running` 任务被中断 |
| 出错 | `error` | 执行过程抛出异常（服务不可达、引擎报错等） |

转移关系：`pending` →（start）→ `running` →（结束）→ `done` / `stopped` / `error`；`pending` / `error` 时可再次点击「开始测试」重试；非运行中可「关闭」（删除任务）。

<div class="warning">
**停止后任务自动删除**：任务以 `stopped` 状态结束时，前端自动将其从本地列表移除并调用 `DELETE /api/tasks/{task_id}`（页面回到介绍页）；运行记录目录保留，仍可在 Datas → Perfs 查看。
</div>

## 4. 本手册导航

| 篇 | 文档 | 内容 |
| --- | --- | --- |
| 2.1 | [Performance 手册概览](/zh/docs/manual/performance/) | 页面结构、任务列表、任务状态机 |
| 2.2 | [创建压测任务](/zh/docs/manual/performance/create-task/) | 三步向导：性能条件 → 性能参数 → 启动测试 |
| 2.3 | [并发模式与阈值模式](/zh/docs/manual/performance/modes/) | 两种模式的参数、限制与扫描逻辑 |
| 2.4 | [实时监控与曲线](/zh/docs/manual/performance/live-metrics/) | Profile Progress、Real-Time Metrics、12 条实时曲线 |
| 2.5 | [结果查看与导出](/zh/docs/manual/performance/results/) | 统计图、结果表格、Excel/日志导出 |

## 5. 相关文档

- [性能测试参考文档](/zh/docs/performance/) — 概念与指标口径
- [数据管理手册](/zh/docs/manual/datas/) — 历史运行记录查看与备份/导入