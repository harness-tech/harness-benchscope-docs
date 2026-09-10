---
title: "性能核心指标"
description: "性能测试的全部核心指标与关键指标：TTFT / TPOT / ITL / 吞吐 / 请求统计 / 阈值结果，含指标含义、单位与统计口径。"
---

# 性能核心指标

本页是性能测试指标的**完整口径说明**：覆盖每个并发点输出的核心指标、每次运行的请求统计、阈值模式的判定结果，以及导出文件中的列定义。阅读其他性能文档（[并发压测](/zh/docs/performance/concurrency/)、[阈值压测](/zh/docs/performance/threshold/)）时遇到指标名，可在此页查找含义。

## 核心指标（每个并发点一组）

压测以**并发数**为横轴，每个并发点输出一组指标。延迟类指标提供 `mean`（均值）/ `median`（中位数）/ `p99`（99 分位）三种统计量，吞吐类指标提供 `mean`。

| 指标 | 键名 | 单位 | 统计量 | 含义 |
| --- | --- | --- | --- | --- |
| 首 token 延迟 TTFT | `ttft_mean` / `ttft_median` / `ttft_p99` | ms | mean / median / p99 | 从请求发出到收到第一个生成 token 的耗时，反映用户感知的首字响应速度，**越低越好**。 |
| 每输出 token 延迟 TPOT | `tpot_mean` / `tpot_median` / `tpot_p99` | ms | mean / median / p99 | 生成每个输出 token 的平均耗时，决定流式输出的持续流畅度，**越低越好**。 |
| token 间隔延迟 ITL | `itl_mean` / `itl_median` / `itl_p99` | ms | mean / median / p99 | 相邻两个输出 token 之间的间隔耗时，刻画流式输出的抖动与卡顿，**越低越好**。 |
| 输出吞吐 | `output_mean` | tok/s | mean | 服务端生成的输出 token 速率（总输出 token 数 / 压测时长），**越高越好**。 |
| 峰值输出吞吐 | `peakoutput_mean` | tok/s | mean | 压测窗口内观察到的输出 token 速率峰值（仅 vLLM 提供；引擎不支持时记为 N/A）。 |
| 总 token 吞吐 | `total_mean` | tok/s | mean | 输入 + 输出 token 的总处理速率（总 token 数 / 压测时长），衡量服务整体处理容量，**越高越好**。 |
| 请求吞吐 | `req_per_s` | req/s | mean | 每秒完成的请求数（成功请求数 / 压测时长），衡量服务承载的请求速率，**越高越好**。 |
| 单用户吞吐 | `single_user` | tok/s | 推导值 | 单个用户可获得的生成速率，按 `1000 / TPOT(mean)` 推导，近似单人连续生成的速度。 |

### 统计量说明

| 统计量 | 含义 | 使用建议 |
| --- | --- | --- |
| `mean` | 均值 | 反映整体水平，常规对比使用。 |
| `median` | 中位数 | 对极端值不敏感，分布偏斜时更能代表典型体验。 |
| `p99` | 99 分位 | 刻画长尾延迟，严格 SLA 场景（如在线对话）建议以 p99 为准。 |

<div class="info">

**info**：

第三方引擎（vLLM / SGLang 原生输出）的指标可得性口径：**可得 → 数值（蓝色）；不可得 → N/A（灰黑）；缺失 → 灰横线**。例如 SGLang 原生输出不含峰值输出吞吐，该列显示 N/A，属正常现象。

</div>

## 请求统计（每次运行一组）

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |
| 成功请求数 | `successful_requests` | 个 | 压测中成功完成（收到完整响应）的请求数。 |
| 失败请求数 | `failed_requests` | 个 | 压测中失败（超时 / 错误 / 未完成）的请求数，健康压测中应为 0。 |
| 压测时长 | `benchmark_duration` | s | 整轮压测的墙钟时长（从首个请求发出到全部请求结束）。 |
| 总输入 token 数 | `total_input_tokens` | tokens | 本轮压测发送的全部输入 token 总量。 |
| 总输出 token 数 | `total_generated_tokens` | tokens | 本轮压测服务端生成的全部输出 token 总量。 |
| 峰值并发 | `peak_concurrent` | 个 | 压测过程中同时在途的请求数峰值。 |

## 阈值模式结果

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |
| 最佳并发 | `best_concurrency` | 个 | 阈值模式下满足**全部**阈值条件（TTFT / TPOT / 输出吞吐）的最大并发；达到搜索上限仍满足时取上限。 |

阈值条件与判定统计量（`mean` / `median` / `p99`）的说明见 [阈值压测](/zh/docs/performance/threshold/)。

## 单次运行快照契约

每个并发点（含单请求快照）统一输出以下 **11 项指标**，保证跨引擎、跨运行结构一致：

`output_mean` · `peakoutput_mean` · `total_mean` · `ttft_mean` · `tpot_mean` · `itl_mean` · `ttft_p99` · `tpot_p99` · `itl_p99` · `req_per_s` · `single_user`

引擎不支持某项指标时以 N/A 占位，键位保持不变。

## 图表与导出

### 实时曲线（性能页 4 组 12 图）

| 组 | 指标 | 单位 |
| --- | --- | --- |
| 吞吐 Throughput | `output_mean` / `peakoutput_mean` / `total_mean` | tok/s |
| TTFT | `ttft_mean` / `ttft_median` / `ttft_p99` | ms |
| TPOT | `tpot_mean` / `tpot_median` / `tpot_p99` | ms |
| ITL | `itl_mean` / `itl_median` / `itl_p99` | ms |

### Excel 导出（benchmark-*.xlsx）

含 **均值 Mean** 与 **P99** 两个工作表，列定义如下：

| 列 | 含义 |
| --- | --- |
| GPU | 部署 GPU 信息。 |
| 模型 | 被测模型名。 |
| 精度 | 模型精度（如 FP16 / INT8）。 |
| 推理框架 | 被测服务使用的推理框架。 |
| 输入长度 / 输出长度 | 用例的输入 / 输出 token 长度。 |
| 并发数 | 该行的并发点。 |
| Output | 输出吞吐（tok/s）。 |
| Peak Output | 峰值输出吞吐（tok/s）。 |
| Total | 总 token 吞吐（tok/s）。 |
| TTFT / ITL / TPOT | 延迟指标（ms），P99 表为对应分位值。 |
| 单用户 | 单用户吞吐（tok/s）。 |

最佳行（TPOT 最接近且低于阈值）在表中高亮显示。

### CSV 汇总

汇总 CSV 按**用例**分组，每组含「测试条件」标题行（用例标签 / 输入 / 输出 / 部署 GPU）与数据行：并发数、Output、Peak Output、Total、TTFT、TPOT、ITL；分 mean 与 P99 两套文件。

## 常见问题

**问题：为什么峰值输出吞吐显示 N/A？**
该指标仅部分引擎（vLLM）提供；SGLang 原生输出不含该项，记为 N/A，不影响其他指标。

**问题：TPOT 和 ITL 有什么区别？**
TPOT 是「生成每个输出 token 的平均耗时」，含首 token 后的整体节奏；ITL 是「相邻两个 token 的实际间隔」，更贴近逐 token 的抖动。二者接近时输出平稳，ITL 明显大于 TPOT 时存在卡顿。

**问题：单用户吞吐是怎么算出来的？**
按 `1000 / TPOT(mean)` 推导，近似单个用户连续生成时的 token 速率，便于从吞吐视角理解单人体验。

## 相关文档

- [性能测试概述](/zh/docs/performance/) — 双模式总览
- [并发压测](/zh/docs/performance/concurrency/) — 多档并发对比
- [阈值压测](/zh/docs/performance/threshold/) — best_concurrency 判定
- [perf 命令](/zh/docs/cli/perf/) — CLI 输出指标对照
- [精度核心指标](/zh/docs/accuracy/metrics/) — 精度侧指标口径