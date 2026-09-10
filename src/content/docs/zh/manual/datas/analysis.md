---
title: 数据分析
description: Datas 数据分析手册：Analysis 标签页现状（敬请期待）、Perfs 详情内的统计口径（均值/中位数/P99）、统计图联动与行/组过滤的按钮操作与后台执行逻辑。
---

# 数据分析

数据分析用于**从性能指标中提炼统计结论**：按不同统计口径（均值 / 中位数 / P99）查看指标，并通过**联动**在多张统计图之间同步悬浮提示，快速定位性能拐点。

## 1. 功能说明

Datas 的「数据分析」分两部分：

- **Analysis 标签页**（`/datas/analysis`）：当前为**敬请期待**占位页（「数据分析功能规划中」），预留跨记录的**记录对比分析**（选择要对比的记录）能力。
- **Perfs 详情内的分析能力**（已可用）：
  - 第 3 行 **Perf Datas 数据面板**：按 **默认 / Mean / Median / P99** 口径查看指标表。
  - 第 4 行 **统计图**：**联动**开关、按 TTFT / TPOT / ITL 过滤指标行、按 case 分组过滤。

<div class="warning">

**warning**：

跨多条记录的「记录对比分析」（选择要对比的记录后并排比较）属于 **Analysis 标签页规划中**的功能，当前版本尚未上线。当前可用的分析均在单条记录的 Perfs 详情内完成。

</div>

## 2. 页面结构

```
Analysis 标签页：
┌────────────────────────────────────┐
│            敬请期待                  │
│        数据分析功能规划中             │
└────────────────────────────────────┘

Perfs 详情 第 3 行（数据面板）：
┌──────────────────────────────────────────────────┐
│  Perf Datas        [默认][Mean][Median][P99]      │
│   [ case 分组 tab ]                               │
│   ┌ 指标数据表（列随口径切换）…… [详情] ┐           │
└──────────────────────────────────────────────────┘

Perfs 详情 第 4 行（统计图）：
┌──────────────────────────────────────────────────┐
│  统计图   [联动 ●]  [默认] [TTFT] [TPOT] [ITL]      │
│   吞吐： Output  Peak  Total  （tok/s）            │
│   TTFT： mean  median  p99  （ms）                │
│   TPOT： mean  median  p99  （ms）                │
│   ITL：  mean  median  p99  （ms）                │
└──────────────────────────────────────────────────┘
```

![BenchScope Datas 性能记录统计](/images/benchscope-datas-perfs_statistics.png)

## 3. 输入参数与字段限制

| 字段 | 类型 | 限制 / 约束 | 默认值 | 说明 |
| --- | --- | --- | --- | --- |
| 数据口径 `mode` | enum | `default` / `mean` / `median` / `p99` | `default` | 数据面板显示的统计列口径 |
| 联动 `linkage` | boolean | 开 / 关 | 关 | 统计图 tooltip 是否跨图联动 |
| 指标行 `visible` | object | `throughput` / `ttft` / `tpot` / `itl` 各自开 / 关 | 全开 | 控制显示哪些指标行（吞吐行恒显） |
| case 分组 `groups` | array | 可整体启停（默认 / 逐组） | 全启用 | 控制哪些 case 分组参与统计图 |

### 3.1 各统计口径对应的数据列

| 口径 | 数据表列（Datas 内默认隐藏 用例 / 并发 / 成功 / 状态 列后） |
| --- | --- |
| `default` | Requests、Output、Total、TTFT mean/median/p99、TPOT mean/median/p99 |
| `mean`（均值） | Requests、Output、Peak、Total、TTFT mean、TPOT mean、ITL mean |
| `median`（中位数） | Requests、Output、Peak、Total、TTFT median、TPOT median、ITL median |
| `p99` | Requests、Output、Peak、Total、TTFT p99、TPOT p99、ITL p99 |

## 4. 按钮操作
1. **数据面板口径**：点击 **默认 / Mean / Median / P99**，切换指标表统计列。
2. **联动开关**：在统计图标题区打开 / 关闭**联动**；开启后鼠标进入任意图，同组所有图的 tooltip 同步显示。
3. **指标行过滤**：点击 **TTFT / TPOT / ITL** 显示 / 隐藏对应指标行；**默认**一键全显。
4. **case 分组过滤**（多组时）：统计图顶部出现分组行，点击某组隐藏 / 恢复该组曲线，**默认**全部恢复。
5. **详情**：数据表行尾点击，弹窗查看该请求 Profile Progress / Real-Time Metrics。

## 5. 操作步骤（看一条记录的统计结论）
1. 在 Perfs 页选中一条记录。
2. 第 3 行选择口径（如 **Median** 看稳健统计，或 **P99** 看尾部延迟）。
3. 第 4 行打开**联动**，将鼠标移到某并发点，观察吞吐 / TTFT / TPOT / ITL 同步变化。
4. 仅关注延迟时，关掉 **TTFT** 或只保留 **TPOT / ITL**。
5. 多 case 分组时，用分组行只保留目标分组，减少曲线干扰。

## 6. 后台执行逻辑

- **数据来源**：数据表与统计图都读自 `run.json` 的 `rows[].metrics`。每个 case × 并发组合作为一行，`metrics` 含全部指标键：`output_mean`、`peakoutput_mean`、`total_mean`、`ttft_{mean,median,p99}`、`tpot_{mean,median,p99}`、`itl_{mean,median,p99}` 等。
- **口径切换**：纯前端——按 `mode` 选取对应指标键作为列，无额外 API 调用。
- **联动**：纯前端 `echarts.connect('run-charts')` / `disconnect`，将同组 ECharts 实例绑定，实现 tooltip 联动；关闭即解绑。
- **行 / 组过滤**：纯前端，按 `visible` 与启用的分组过滤 `rows` 后重绘曲线。
- **（可选）汇总接口**：`GET /api/logs/runs/{run_id}/summary?threshold=` 可返回 `records_mean` / `records_p99` 与按 `tpot_threshold_ms` 计算的 best（供需要时后端再聚合）。

<div class="tip">

**tip**：

「联动」只影响**悬浮提示（tooltip）联动**，不会改变曲线数据；曲线始终由 `rows[].metrics` 决定。

</div>

## 7. 常见问题

**问题：Analysis 标签页是空的？**
是占位页（敬请期待），跨记录对比分析仍在规划中。目前请在 Perfs 详情内做单记录分析。

**问题：联动没反应？**
确认联动开关已打开，且至少存在一张可见图。联动在纯前端建立 ECharts 连接，无需刷新。

**问题：某口径下列为空？**
对应指标键在该记录 `metrics` 中缺失（如引擎未产出 ITL），前端以 `-` 显示。

## 8. 相关文档

- [性能记录管理](/zh/docs/manual/datas/perfs/) — 数据面板所在页面
- [Datas 手册概览](/zh/docs/manual/datas/) — 模块入口
- [性能核心指标（参考）](/zh/docs/performance/metrics/) — 指标键与口径
- [API 参考](/zh/docs/api/) — `/api/logs/runs/{id}/summary`
