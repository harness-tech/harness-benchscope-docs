---
title: "结果查看与导出"
description: "BenchScope 性能测试结果查看：Realtime Data 结果表格（24 列/默认 13 列）、Best/BestPerf 标记、12 张统计图、Excel 与日志导出、后台产物清单。"
---

# 结果查看与导出

任务执行中（或执行结束后）均可在性能页第三行（Realtime Data）与第四行（Statistics）查看结果，并导出 Excel / 日志文件。

## 1. 页面结构

```
┌──────────────────────────────────────────────────────────────────┐
│ 第三行  Realtime Data   [TPOT: 100ms] [Output: 0 tok/s] 本地阈值 │
│        分组表格（组标题行 + 数据行）                             │
│        表尾: [n 行] [列设置 ▾] [下载]                            │
├──────────────────────────────────────────────────────────────────┤
│ 第四行  Statistics  [联动开关]   12 张统计图（4 组 × 3 统计量）   │
└──────────────────────────────────────────────────────────────────┘
```

## 2. 结果表格（Realtime Data）

表格按条件组（`case_id`）分组：每组一行**组标题行**（组名 + 行数；阈值模式附阈值条件文本），其下每个请求数点位一行。全表**共 24 列**，其中**默认显示 13 列**，其余可在「列设置」中开启：

| 列分组 | 列（i18n 标题） | 默认可见 |
| --- | --- | --- |
| 任务相关 | Case（`label`）、Requests、Concurrency、Successful（成功率 %） | ✅ |
| 任务相关（可选） | Successful requests、Failed requests、Benchmark duration (s)、Total input tokens、Total generated tokens | ❌ |
| 吞吐 | Output token throughput (tok/s)、Total token throughput (tok/s) | ✅ |
| 吞吐（可选） | Request throughput (req/s)、Peak output token throughput (tok/s)、Peak concurrent requests | ❌ |
| TTFT | Mean / Median / P99 TTFT (ms) | ✅ |
| TPOT | Mean / Median / P99 TPOT (ms) | ✅ |
| ITL | Mean / Median / P99 ITL (ms) | ❌ |
| 状态 | Status | ✅ |

- **状态列**：`Failed`（红，该档执行失败）/ `Success`（绿）+ 可选 `BestPerf` / `Best` 金色标签；
- **行高亮**：`BestPerf` 行金色底、`Best` 行绿色底；
- **Concurrency 列**：`request-rate` 为 `inf` 时显示 `Inf`，为 `follow` 时显示实际并发值；
- **列设置**：下拉菜单按任务相关 / 吞吐 / TTFT / TPOT / ITL 分组，复选框控制每列显示与隐藏。

## 3. Best / BestPerf 标记

| 标记 | 适用模式 | 阈值来源 | 规则 |
| --- | --- | --- | --- |
| `Best`（绿行） | 两种模式 | 本地面板阈值（第三行右上，点击数字编辑） | 组内满足**全部**条件（`TPOT-Mean ≤ TPOT 阈值`；Output 阈值非 0 时还需 `output ≤ 阈值`）的行中，标记并发最大的一行 |
| `BestPerf`（金行） | 仅阈值模式 | 每组阈值（Step 1 配置，按 `case_id` 独立） | 组内满足全部已配置条件（`TTFT-统计量 ≤`、`TPOT-统计量 ≤`、`output ≤`）的行中，标记并发最大的一行 |

本地面板阈值：**TPOT** 默认 `100` ms、**Output Token Threshold** 默认 `0` tok/s（整数 ≥0，点击数字进入编辑，回车/失焦保存）。它**只影响表格标记，不写回任务**；全部为 0 时不做任何标记。

<div class="tip">
**输出吞吐阈值的方向**：`Best` / `BestPerf` 是**前端可视化标记**，其判定统一按「值 ≤ 阈值」比较（与创建页 `≤ X tok/s` 的展示一致）。而**阈值模式的实际压测判定**（后台）对输出吞吐按**下限**判定（`output_mean ≥ 阈值` 才算达标，详见 [并发模式与阈值模式](/zh/docs/manual/performance/modes/)）。两者对输出吞吐的比较方向不同，属当前版本的前后端不一致，标记仅供参考，最终达标判定以后台阈值模式结果为准。
</div>

## 4. 统计图

Statistics 面板的 12 张图（明细见 [实时监控与曲线](/zh/docs/manual/performance/live-metrics/)）。任务完成后曲线完整，可用于：

- **吞吐组**：观察各组吞吐的爬升与平台期；
- **TTFT / TPOT / ITL 组**：定位延迟拐点（服务容量拐点）；
- **多组对比**：同组内相同 case 同色，一张图内比较多个长度组合。

## 5. 导出与下载

| 操作 | 入口 | 行为 |
| --- | --- | --- |
| Excel 导出 | 第三行表尾 **下载** 按钮 | 前端把当前显示列（含组标题行）的 `headers + rows` 提交 `POST /api/tasks/{task_id}/export`；后台用 openpyxl 生成 `realtime_{task_id}.xlsx`（表头加粗、组标题行加粗 + 浅蓝底）并写入 `run_dir`，浏览器下载（文件名 `realtime_{task_id}_{hhmmss}.xlsx`） |
| 日志下载 | Logs 面板右上 **下载** 按钮 | 纯前端：把当前日志缓冲拼为 `{task_id}_{hhmmss}.txt` 下载（无 API 调用） |
| 历史记录备份 | Datas → Perfs → **备份** | `GET /api/logs/runs/{run_id}/backup` 将整个 run 目录 + 终端日志打包 zip 下载（可再导入恢复） |

<div class="tip">
Excel 导出的是「所见即所得」：列顺序 = 当前显示列，含组标题行；`Best` / `BestPerf` 标记以文字形式写入状态列。
</div>

## 6. 后台执行逻辑与产物

| 产物 | 路径 | 说明 |
| --- | --- | --- |
| 任务状态 | `~/.benchscope/perfs/tasks/{task_id}.json` | 任务快照持久化（删除任务时移除） |
| 运行元数据 | `run_dir/run.json` | 完整快照（含 `rows`），每档完成即刷新 |
| mean 汇总 CSV | `run_dir/{model}_X{gpu}.log` | CSV（含用例块头），**每档增量写入** |
| p99 汇总 CSV | `run_dir/{model}_X{gpu}_p99.log` | 同上，p99 口径 |
| 用例明细日志 | `run_dir/{model}_{case}_X{gpu}.log` | 每个 case 的引擎原始输出 |
| 汇总 Excel | `run_dir/benchmark-{DDMMYY}.xlsx` | 任务结束自动生成，按每组 TPOT 阈值标注 `best` |
| 按请求快照 | `run_dir/live/*.json` | 每请求最终实时帧（回看 / Datas 详情用） |
| 手工导出 | `run_dir/realtime_{task_id}.xlsx` | 导出 API 生成 |
| 终端日志 | `logs/perf_{run_id}_{MMDDHHMMSS}.log` | 全部终端输出；`GET /api/tasks/{id}/logs` 可读取（默认末尾 8000 行） |

执行流程（每请求数点位）：`_run_one()` 执行压测 → `_record_row()` 追加 `rows` + 增量写两份 CSV + `persist()` + 广播 `task_result`；任务结束后生成 `benchmark-*.xlsx` 与 `run.json`，广播 `task_done`。

## 7. 常见问题

**问题：结果表格的行数为什么在执行中不断增长？**
每完成一个请求数点位就追加一行（`task_result` 广播）。阈值模式的点位数量是动态的（由扫描策略决定），总行数要等结束才知道。

**问题：刷新页面后 Best 标记还在吗？**
在。标记由前端基于持久化的 `rows` 与阈值实时计算；刷新后本地面板阈值恢复默认（TPOT=100 / Output=0），Best 可能随之变化，`BestPerf` 不受影响（每组阈值随任务持久化）。

**问题：能直接导出 CSV 吗？**
没有独立 CSV 导出按钮，但 `run_dir` 下的两份汇总 CSV（mean / p99）实时增量写入，可在 Datas → Perfs 文件列表中预览或下载；Excel 导出对应表格当前视图。

## 8. 相关文档

- [实时监控与曲线](/zh/docs/manual/performance/live-metrics/) — 执行中的 12 条实时曲线
- [并发模式与阈值模式](/zh/docs/manual/performance/modes/) — 两种模式的扫描逻辑
- [性能核心指标](/zh/docs/performance/metrics/) — 列口径说明
- [数据管理手册](/zh/docs/manual/datas/) — 历史记录与备份/导入