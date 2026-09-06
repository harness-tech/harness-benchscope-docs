---
title: "性能测试"
---

# 性能测试

性能测试页用于对已部署的推理服务进行压测，支持**并发压测（Concurrency Mode）**与**阈值探测（Threshold Mode）**双模式，实时可视化吞吐、延迟与进度。

![BenchScope 性能测试主界面（运行中）](/images/benchscope-performance_perf_running.png)

<div class="tip">

**tip**：

性能测试针对的是**服务链路**——无论目标服务由 vLLM、SGLang 还是其他兼容 OpenAI 协议的后端提供，都可以用统一的界面进行压测与结果对比。

</div>

## 模式总览

| 模式 | 说明 | 适用场景 |
| --- | --- | --- |
| 并发压测 Concurrency | 固定多个并发级别逐级施压，实时记录每个并发的指标 | 观察系统随负载的变化曲线 |
| 阈值探测 Threshold | 从 1 并发起以 2 的次方递增 + 二分，自动寻找满足阈值条件的最大并发 | 已知业务 SLA，求最优承载并发 |

## 创建任务

进入**性能测试**页，点击**创建任务**，通过三步表单（Step1 条件 / Step2 参数 / Step3 命令预览）即可启动一次压测：

![BenchScope 创建性能任务](/images/benchscope-performance_create.png)

1. **Step1 条件**：选择被测模型与服务地址（Provider）、引擎、模式（并发 / 阈值）。
2. **Step2 参数**：填写并发、输入输出 token、请求数等参数。
3. **Step3 命令预览**：核对等价的 CLI 命令，确认后启动。

<div class="tip">

**tip**：

若使用带 Token 预估的能力，可在创建页看到消耗预估（见下图的 Token 展示）：

![BenchScope 创建任务 Token 展示](/images/benchscope-performance_create_token.png)

</div>

## 并发压测（Concurrency Mode）

按并发级别逐层施压，每个并发实时反馈到：

- **表格**：每个并发的吞吐 / TTFT / TPOT / ITL；
- **曲线**：多维度实时统计图；
- **进度**：运行进度实时更新。

随机并发面板提供运行中实时更新；单并发点内支持「连续滚动」，便于观察长时间运行下的波动。

运行中的主界面：

![BenchScope 性能测试运行统计](/images/benchscope-performance_perf_running_statistics.png)

### 使用步骤

1. 选择被测模型与服务地址（Provider）；
2. 选择 **并发压测（Concurrency）**；
3. 填入并发级别、输入输出 token、请求总数等参数；
4. 提交后实时查看表格 / 曲线 / 进度；
5. 完成后导出或查看历史记录。

## 阈值探测（Threshold Mode）

在已知业务 SLA（服务水平目标）时，用阈值探测自动寻找满足全部阈值条件的**最大并发**（`best_concurrency`）。

**判定条件**：

- TTFT ≤ 阈值（`mean` / `median` / `p99`）；
- TPOT ≤ 阈值（`mean` / `median` / `p99`）；
- 输出吞吐 ≥ 阈值。

**探测策略**：

1. 从 **1 并发** 开始，以 **2 的次方递增**（1, 2, 4, 8, …）逐步压测；
2. 若 1 并发已不满足阈值 → 最佳并发为 1，结束；
3. 若执行到 `hi = 2^k` 不满足（`lo = 2^(k-1)` 满足）→ 在 `(lo, hi]` 内二分，直到相邻两个值，`lo` 即满足阈值的最大并发；
4. 达到搜索上限仍满足 → 上限并发为最佳（正常结束）。

<div class="info">

**info**：

阈值判定所使用的统计量可通过参数调整（如 `--ttft-statistic p99`），以适配不同的业务口径。详见 [CLI 参考](/zh/docs/cli/reference/)。

</div>

## 指标口径

| 指标 | 含义 |
| --- | --- |
| 吞吐（output_mean / total_mean） | 输出 / 总吞吐（tok/s） |
| TTFT（ttft_mean） | 首 token 延迟（ms） |
| TPOT（tpot_mean） | 每输出 token 延迟（ms） |
| ITL（itl_mean） | 令牌间隔延迟（ms） |

### 第三方引擎指标可得性

针对第三方引擎，指标可得性会**显式化**展示：

| 状态 | 展示 | 说明 |
| --- | --- | --- |
| 可得 | 蓝色数值 | 指标正常采集到 |
| 不可得 | N/A（灰黑） | 该引擎不支持 / 无法采集该指标 |
| 缺失 | 灰色横线 | 指标采集缺失 |

固定的 **11 指标快照契约**保证了不同引擎间指标结构的一致性，便于跨引擎对比。

## 产物与导入

- 落盘 `run.json` + 日志 `perf_<run_id>_*.log`；
- 打包为**扁平 zip**，可在 **Datas → Perfs → 导入备份** 导入，跨环境恢复历史压测记录。

<div class="warning">

**warning**：

压测过程中如果被测服务地址错误、请求超时或引擎不可用，任务可能失败或部分请求计为 failed。请先在浏览器 / curl 确认服务可访问后再开始压测。

</div>

## 常见问题

**问题：为什么某个指标显示 N/A 或灰横线？**
该引擎可能不支持该指标，或指标采集缺失。可切换自研引擎 `benchscope` 获取最完整的指标。

**问题：压测请求大量失败？**
检查 `--base-url`、API Key、`--timeout` 与并发设置；确认服务负载是否已接近上限。

## 相关文档

- [CLI 参考](/zh/docs/cli/reference/) — `perf` 命令完整参数
- [教程：并发压测](/zh/docs/performance/concurrency/) — 分步操作
- [教程：阈值压测](/zh/docs/performance/threshold/) — 求最优并发
- [设置（Settings）](/zh/docs/tools/settings/) — 配置 Provider 与 Bench Engines
- [数据与统计（Datas）](/zh/docs/data/) — 历史记录与导入
