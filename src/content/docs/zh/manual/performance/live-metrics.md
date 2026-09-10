---
title: "实时监控与曲线"
description: "BenchScope 性能测试实时监控：Profile Progress 进度面板、Real-Time Metrics 11 指标表、12 条实时曲线，以及 WebSocket 数据流。"
---

# 实时监控与曲线

任务执行期间，性能页第二行（Profile Progress + Real-Time Metrics）与第四行（Statistics 12 图）实时刷新。数据经 WebSocket（`/ws`）推送，前端无需轮询。

## 1. 页面结构

```
┌─────────────────────────────────────────────────────────────┐
│ 第二行  Profile Progress (左 36%) │ Real-Time Metrics (右 64%) │
├─────────────────────────────────────────────────────────────┤
│ 第四行  Statistics：4 指标组 × 3 统计量 = 12 张图（联动开关）  │
└─────────────────────────────────────────────────────────────┘
```

**快照来源**（第二行按「当前活跃请求」渲染，优先级从高到低）：

1. 在 Cases 面板点击选中的请求数标签（历史请求回看，状态显示 `Completed`）；
2. 正在执行的请求（状态显示 `Profiling`）；
3. 默认：最后一个已完成的请求。

## 2. Profile Progress

展示当前请求（单请求口径）的状态与进度：

| 项 | 内容 | 数据来源 |
| --- | --- | --- |
| 当前状态 | `Profiling`（执行中）/ `Completed`（已完成或回看） | 任务状态 + 是否选中回看 |
| 标题右侧 | `case#g{case_id} · {concurrency} req` | 当前执行位置 |
| Profiling 进度条 | 当前请求 `completed/total` % | `task_live.stats` |
| Records 进度条 | 与上相同（当前请求口径） | `task_live.stats` |
| Progress | `已完成 / 总数 requests (pct%)` | 当前请求实时快照（无快照时 `-`） |
| Errors | `错误数 / 已完成数 (pct%)`，>0 时红色高亮 | 同上 |
| Request Rate | `req_per_s requests/s` | 同上 |
| Processing Rate | `completed/t records/s` | 同上 |
| Elapsed | `m ss`（≥1h 显示 `h mm`） | 快照 `t`（已运行秒数） |
| ETA | `(t/已完成) × (总数-已完成)`，<120s 显示 `x.x s` | 按完成进度推算；请求完成显示 `0s`，无快照显示 `-` |

## 3. Real-Time Metrics

**11 项指标 × 7 统计量**（列：`avg/min/max/p99/p90/p50/std`）表格，运行中随 `task_live` 流逐秒刷新：

| 分组 | 指标 | 单位 | 含义 |
| --- | --- | --- | --- |
| 延迟 | `TTFT` | ms | 首 token 延迟 |
| 延迟 | `TTST` | ms | 前 2 token 延迟（首次累计达 2 个输出 token） |
| 延迟 | `TPOT` | ms | 每输出 token 延迟 |
| 延迟 | `Req Latency` | ms | 请求端到端延迟 |
| 延迟 | `ITL` | ms | token 间延迟 |
| 吞吐 | `Output TPS/User` | tok/s | 单用户生成速率 |
| 吞吐 | `Output TPS` | tok/s | 总输出吞吐 |
| 吞吐 | `Req/sec` | req/s | 请求完成速率 |
| 吞吐 | `Requests` | 个 | 已完成请求数（仅 `avg` 列可计算） |
| 长度 | `OSL` | tokens | 输出序列长度 |
| 长度 | `ISL` | tokens | 输入序列长度 |

单元格有三种状态：**蓝色数字** = 已计算出值；**灰色短横线 `-`** = 可计算但暂无值；**灰黑色 `N/A`** = 不可计算。

<div class="info">
**原生引擎可得性**：vLLM/SGLang 原生引擎无逐请求实时流，快照由每档结束聚合构造——仅 `avg/p50/p99` 可得（其余统计量为 `N/A`）；`TTST`、`Output TPS/User` 全程不可得（整行 `N/A`）。自研 Bench CLI 引擎逐秒提供全部分布统计。
</div>

<div class="info">
i18n 另保留了 **单位换算（ms/tok ↔ s/k）**、**Trend 列**、**分组表头（延迟/吞吐/长度）** 与 **复制当前快照** 等键，当前界面未启用这些键，表格按原始 ms/tok 单位显示。
</div>

## 4. 12 条实时曲线

Statistics 面板（第四行）共 **12 张折线图**：4 指标组 × `Mean/Median/P99`，横轴为请求数（升序），每个条件组（case）一条曲线：

| 分组 | 三张图（键名） | 单位 |
| --- | --- | --- |
| 吞吐 Throughput | `output_mean` / `peakoutput_mean` / `total_mean` | tok/s |
| TTFT | `ttft_mean` / `ttft_median` / `ttft_p99` | ms |
| TPOT | `tpot_mean` / `tpot_median` / `tpot_p99` | ms |
| ITL | `itl_mean` / `itl_median` / `itl_p99` | ms |

- **实时生长**：每完成一个请求数点位，`rows` 追加一行，各图自动补一个数据点，曲线在执行中逐渐「长出来」；
- **分组成色**：每组 8 色调色板，同组内相同 case 颜色一致，便于多组对比；
- **联动开关**：面板右上 `linkage` 开关（默认开启），开启后 hover 任一图，12 张图同步显示相同横轴的 tooltip。

## 5. 按钮操作

1. **回看任意请求**：点击 Cases 面板中任一请求数标签（选中后蓝色描边），第二行切换为该请求的快照；再次点击取消选中，恢复执行中视图。
2. **联动开关**：切换 Statistics 面板右上 `linkage` 开关，开启/关闭 12 图 tooltip 联动。
3. **日志跟随**：Logs 面板与 Cases 面板在执行中自动滚动到底部；手动上滚后日志停止跟随（新内容到达再回底）。

## 6. 后台执行逻辑

| 环节 | 机制 |
| --- | --- |
| WS 连接 | `/ws` 连接后先推 `status` 与全部 `task_snapshot`；断线 3 秒后自动重连 |
| 自研引擎实时流 | `run_builtin_bench` 每秒回调 `live_cb`：基于已完成记录计算 10 项指标分布统计，广播 `task_live`（含 `t/completed/total/errors/req_per_s/output_tps/metrics`） |
| 原生引擎实时流 | 每档一个 1 秒 ticker 线程广播 `task_live`；进度解析日志 `benchscope-live-done k/N` 行（仅 Mock 输出含该行，真实 vLLM/SGLang 时仅 Elapsed 滚动） |
| 按请求缓存 | 前端按 `case_id + concurrency` 缓存最新快照（`liveReq`），任务结束后可点击回看 |
| 快照持久化 | 每档完成时最终帧写入 `run_dir/live/<label#gid__c<conc>>.json`；任务结束（`done`/`stopped`/`error`）后前端调 `GET /api/logs/runs/{run_id}/live` 补载 |
| 日志流 | 引擎输出每行广播 `task_log`，前端保留最近 8000 行 |

## 7. 常见问题

**问题：Real-Time Metrics 表为什么很多 N/A？**
原生引擎（vLLM/SGLang）无逐请求实时流，快照由每档结束聚合反推：仅 `avg/p50/p99` 可得，且 `TTST`、`Output TPS/User` 引擎不提供。换用自研 Bench CLI 引擎可得全部分布统计。

**问题：任务结束后曲线还在吗？**
在。每个请求数的结果持久化在 `rows`（随 `run.json` 落盘）；任务结束后前端补载按请求持久化快照（`/api/logs/runs/{run_id}/live`），第二行可回看历史请求。

**问题：ETA 与 Elapsed 有什么区别？**
Elapsed 是自开始到当前的实际耗时；ETA 按「已耗时 ÷ 完成比例」推算剩余时间，非运行中或完成度为 0 时显示 `-`。

## 8. 相关文档

- [Performance 手册概览](/zh/docs/manual/performance/) — 页面结构与任务状态机
- [结果查看与导出](/zh/docs/manual/performance/results/) — 最终结果表格与导出
- [性能核心指标](/zh/docs/performance/metrics/) — 指标口径