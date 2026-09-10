---
title: "概述"
description: "概述 BenchScope 性能测试的两种模式——并发压测与阈值探测，以及如何创建压测任务、查看实时指标并解读结果。"
---

# 概述

性能测试用于对已部署的推理服务进行压测，提供**并发压测（Concurrency Mode）**与**阈值探测（Threshold Mode）**两种模式，实时可视化吞吐、延迟与运行进度。

- **并发压测**：用于回答「随着并发升高，吞吐与延迟如何变化」；
- **阈值探测**：用于回答「给定业务 SLA，这套配置最多能扛住多少并发」。

![BenchScope 性能测试主界面（运行中）](/images/benchscope-performance_perf_running.png)

<div class="tip">

**tip**：

性能测试针对的是**服务链路**——无论目标服务由 vLLM、SGLang 还是其他兼容 OpenAI 协议的后端提供，都可以用统一的界面进行压测与结果对比。

</div>

## 本页内容

- [性能核心指标](/zh/docs/performance/metrics/) — 全部指标的完整口径（TTFT / TPOT / ITL / 吞吐 / 请求统计 / 导出列）
- [并发压测](/zh/docs/performance/concurrency/) — 按并发级别逐档施压、解读结果，找到最佳工作区间
- [阈值压测](/zh/docs/performance/threshold/) — 给定业务 SLA，自动搜索可承载的最大并发

## 模式总览

| 模式 | 说明 | 适用场景 |
| --- | --- | --- |
| 并发压测 Concurrency | 固定多个并发级别逐级施压，实时记录每个并发的指标 | 观察系统随负载的变化曲线 |
| 阈值探测 Threshold | 从 1 并发起以 2 的次方递增 + 二分，自动寻找满足阈值条件的最大并发 | 已知业务 SLA，求最优承载并发 |

## 创建任务

进入**性能测试**页，点击**创建任务**，通过三步表单（Step1 条件 / Step2 参数 / Step3 命令预览）即可启动一次压测：

![BenchScope 创建性能任务](/images/benchscope-performance_create.png)

1. **Step1 条件**：选择被测模型与服务地址（Provider）、引擎、模式（并发 / 阈值）。
2. **Step2 参数**：填写并发、输入输出 token、请求数等参数（阈值模式还需填写 SLA 阈值与搜索上限）。
3. **Step3 命令预览**：核对等价的 CLI 命令，确认后启动。

<div class="tip">

**tip**：

若使用 Token 预估能力，创建页会显示消耗预估（见下图的 Token 展示）：

![BenchScope 创建任务 Token 展示](/images/benchscope-performance_create_token.png)

</div>

## 并发压测（Concurrency Mode）

按并发级别逐档施压，各档指标实时反映在表格、曲线与进度中，便于观察服务在负载下的表现，找到**最佳工作区间**。分步操作见 [并发压测](/zh/docs/performance/concurrency/)。

运行中的主界面：

![BenchScope 性能测试运行统计](/images/benchscope-performance_perf_running_statistics.png)

## 阈值探测（Threshold Mode）

在已知业务 SLA 时，用阈值探测自动寻找满足全部阈值条件的**最大并发**（`best_concurrency`）。

**判定条件**（全部满足才算达标）：

- TTFT ≤ 阈值（`mean` / `median` / `p99`）；
- TPOT ≤ 阈值（`mean` / `median` / `p99`）；
- 输出吞吐 ≥ 阈值。

探测策略为**从 1 并发起以 2 的次方递增**，找到首个不满足的点后在相邻区间**二分**收敛。分步操作见 [阈值压测](/zh/docs/performance/threshold/)。

<div class="info">

**info**：

阈值判定所使用的统计量可通过参数调整（如 `--ttft-statistic p99`），以适配不同的业务口径。详见 [perf 命令](/zh/docs/cli/perf/)。

</div>

## 产物与导入

- 落盘 `run.json` + 日志 `perf_<run_id>_*.log`；
- 打包为**扁平 zip**，可在 **Datas → Perfs → 导入备份** 导入，跨环境恢复历史压测记录。

<div class="warning">

**warning**：

压测过程中如果被测服务地址错误、请求超时或引擎不可用，任务可能失败或部分请求计为 failed。请先在浏览器 / curl 确认服务可访问后再开始压测。

</div>

## 相关文档

- [性能核心指标](/zh/docs/performance/metrics/) — 指标完整口径与导出列
- [并发压测](/zh/docs/performance/concurrency/) — 分步操作
- [阈值压测](/zh/docs/performance/threshold/) — 求最优并发
- [perf 命令](/zh/docs/cli/perf/) — `perf` 命令完整参数
- [设置（Settings）](/zh/docs/tools/settings/) — 配置 Provider 与 Bench Engines
- [数据与统计（Datas）](/zh/docs/data/) — 历史记录与导入
