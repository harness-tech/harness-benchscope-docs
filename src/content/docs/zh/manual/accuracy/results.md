---
title: "结果查看与溯源"
description: "Accuracy 结果详情面板详解：核心指标、Token 统计、开源基线对标、分学科准确率与单样本溯源、错题集导出，含输入参数、按钮操作与后台数据流。"
---

# 结果查看与溯源

精度任务运行结束后，点击左侧任务列表中的任意任务，右侧**详情面板**自上而下展示：任务头 → 核心指标（accMetrics）→ Token 统计（Serving 专属）→ 开源基线对标（accBenchmark）→ 分学科准确率（accSubjects）→ 评测日志（accConsole）→ 单样本溯源（accSamples）。

<div class="info">
**加载时机**：任务运行中只显示进度条与实时日志；全部样本判分完成后，核心指标 / Token 统计 / 基线对标 / 分学科 / 样本溯源才出现。
</div>

## 1. 页面结构

```
┌──────────────────────────────────────────────────────────┐
│ 详情面板（垂直堆叠卡片）                                    │
│  ① 任务头：模型/数据集/种子/温度 + 进度条 + [停止]           │
│  ② 核心指标 accMetrics：6 个指标卡 + 数据集专属指标 + 结论   │
│  ③ Token 统计 accTokenReport（Serving）：5 项 + 预估vs实际  │
│  ④ 开源基线对标 accBenchmark：档位/基线/差值/排名/雷达图     │
│  ⑤ 分学科准确率 accSubjects：学科/正确/总/准确率 表格        │
│  ⑥ 评测日志 accConsole：实时滚动日志                        │
│  ⑦ 单样本溯源 accSamples：筛选 + 表格 + 导出错题集          │
└──────────────────────────────────────────────────────────┘
```

## 2. 输入参数

结果详情面板以只读展示为主，可交互的输入参数集中在**单样本溯源**的筛选与导出：

| 字段 | 标识 | 类型 | 默认 | 说明 |
| --- | --- | --- | --- | --- |
| 样本筛选 | `sampleFilter` | 单选 `all`/`wrong`/`invalid` | `all` | 全部（accSampleAll）/ 答错（accSampleWrong）/ 无效（accSampleInvalid） |
| 导出筛选 | `filter` | 固定 `wrong` | `wrong` | 导出错题集（accExportWrong），后端另支持 `invalid` |
| 样本分页 | — | 分页 | 10 条/页 | 初次加载 `limit=200, offset=0`，前端分页 10 条 |

## 3. 字段限制

| 字段 | 必填 | 约束 / 枚举 |
| --- | --- | --- |
| `sampleFilter` | 可选（默认 all） | 枚举 `all` / `wrong` / `invalid`（UI 三项）；后端 `filter` 另支持 `correct` |
| `filter`（导出） | 可选 | 枚举 `wrong` / `invalid`（默认 `wrong`）；无对应样本时返回 404 |
| 样本分页 | — | `limit` / `offset` 为非负整数，页大小固定 10 |

## 4. 核心指标（accMetrics）

| 指标 | 键 | 口径 / 公式 |
| --- | --- | --- |
| 准确率 | `accuracy` | `correct_samples / total_samples`（核心主指标） |
| 有效通过率 | `pass_rate` | `(total - invalid) / total`（有效可解析样本占比） |
| 总样本 | `total_samples` | 实际参与评测的样本数 |
| 正确 | `correct_samples` | `status = correct` 计数 |
| 错误 | `wrong_samples` | `status = wrong` 计数 |
| 无效 | `invalid_samples` | `status = invalid` 计数 |
| 评测结论 | `conclusion` | 见下方结论规则 |

**评测结论（`conclusion`）规则**（最终结论枚举为 **合格 / 精度下跌 / 异常**）：

| 结论 | 触发条件 |
| --- | --- |
| 异常 | `total_samples = 0` 或 `invalid / total > 0.2` |
| 精度下跌 | 基线主指标差值 `diff_pp < -5.0` |
| 合格 | 其余情况 |

<div class="warning">
**注意区分**：`result.conclusion`（评测结论）是最终枚举 **合格/精度下跌/异常**；`benchmark.conclusion`（基线对标结论）是相对开源基线的对比文案（优于/持平/明显劣于），二者相互独立。
</div>

## 5. Token 消耗统计（Serving，accTokenReport）

| 指标 | 键 | 说明 |
| --- | --- | --- |
| 输入 Token | `prompt_tokens_total` | 全部样本输入 token 之和 |
| 输出 Token | `completion_tokens_total` | 全部样本输出 token 之和 |
| 总消耗 | `total_tokens` | 输入 + 输出 |
| 单样本输入均值 | `avg_prompt_tokens_per_sample` | 输入总 / 样本数 |
| 单样本输出均值 | `avg_completion_tokens_per_sample` | 输出总 / 样本数 |
| 预估 vs 实际 | `estimate_vs_actual` | `estimate_total → actual_total`（`deviation_pct` 偏差百分比） |

<div class="info">
**Native 模式无 Token 统计**：`result.tokens` 为 `null`，该卡片自动隐藏（Native 模式的能力边界）。
</div>

## 6. 开源基线对标（accBenchmark）

| 字段 | 键 | 说明 |
| --- | --- | --- |
| 档位 | `grade` | 相对最优基线：S（≥0）/ A（≥-5pp）/ B（≥-15pp）/ C |
| 所用基线 | `baseline_used` | 尺寸最接近基线的 `name` / `score` |
| 差值 | `diff_pp` | 当前得分 − 基线得分（百分点） |
| 同尺寸排名 | `rank_pct` | 同尺寸段基线中被当前模型超越的比例（%） |
| 对标结论 | `conclusion` | 优于同尺寸开源基线 / 持平基线 / 明显劣于基线（风险预警） |
| 能力雷达 | `radar` | 知识 / 数学 / 代码 / 对话 四维度（单数据集仅该维度有值） |

## 7. 分学科准确率（accSubjects）

| 列 | 字段 | 说明 |
| --- | --- | --- |
| 学科 | `subject` | 样本学科标签（空值样本不参与） |
| 正确 | `correct` | 该学科正确数 |
| 总 | `total` | 该学科样本数 |
| 准确率 | `accuracy` | 该学科 `correct / total` |

## 8. 单样本溯源（accSamples）

列字段：`#`（index）、学科（`subject`）、Prompt（`prompt`）、模型输出（`output`）、标准答案（`answer`）、Token(入/出)（`tokens`）、判定（`status`）。

- **筛选**：全部（accSampleAll）/ 答错（accSampleWrong）/ 无效（accSampleInvalid）；后端 `filter` 另支持 `correct`。
- **导出错题集（accExportWrong）**：下载 `wrong` 样本为 `wrong_samples.jsonl`（含 prompt/output/answer/判定），用于错误分析与回灌训练。

## 9. 按钮操作与执行步骤

1. 在左侧任务列表**点击任务行** → 加载完整详情与样本列表。
2. 自上而下查看：核心指标 → Token 统计（Serving）→ 基线对标 → 分学科 → 评测日志。
3. 在「单样本溯源」用「全部 / 答错 / 无效」切换筛选，定位具体问题样本。
4. 点「导出错题集」下载 `wrong_samples.jsonl`。
5. （`running`）点任务头或列表行的「停止」发送停止请求。
6. 点「删除」移除任务（同时删除落盘目录）。

## 10. 后台执行逻辑

| 动作 | API / 数据流 |
| --- | --- |
| 选中任务 | `store.loadTask()` → `GET /api/accuracy/tasks/{task_id}`（列表快照不含 result，拉完整详情） |
| 加载样本 | `GET /api/accuracy/tasks/{task_id}/samples?filter=all&limit=200&offset=0` |
| 切换筛选 | `watch(sampleFilter)` 重新请求 `samples`（新 `filter`） |
| 导出错题集 | `window.open` → `GET /api/accuracy/tasks/{task_id}/export-samples?filter=wrong`（返回 `FileResponse`） |
| 基线对标 | `run_eval` 结束时 `compute_benchmark()` 计算，存入 `result.benchmark` 随详情下发 |
| 实时推送 | WebSocket `eval_task_log` / `eval_task_progress` / `eval_task_result`（逐样本，前端累加上限 500），`done` 后以 API 分页为准 |

落盘文件：`evals/<task_id>/result.json`（结果）、`samples.jsonl`（逐样本溯源）、`task.json` / `run.json`（主表 / 记录）。

## 11. 常见问题

**问题：点击任务后为什么看不到结果？**
列表快照不含 `result`，点击后前端才发 `GET /tasks/{id}` 拉完整详情；任务运行中仅显示进度与日志，完成后结果卡片才出现。

**问题：评测结论的判定依据是什么？**
优先「异常」（`total=0` 或无效占比 > 0.2）→ 再看「精度下跌」（基线 `diff_pp < -5pp`）→ 否则「合格」。

**问题：「评测结论」和「基线对标结论」有什么区别？**
`result.conclusion` 是最终枚举 **合格/精度下跌/异常**；`benchmark.conclusion` 是相对开源基线的对比文案（优于/持平/明显劣于），二者独立，不要混用。

**问题：Token 统计卡片为什么没显示？**
仅 Serving 模式采集 `usage`；Native 模式 `result.tokens` 为 `null`，卡片自动隐藏。

**问题：错题集怎么用？**
错题集是含 `prompt`/`output`/`answer`/判定 的 JSONL，可直接用于错误分析、坏例复盘或回灌微调训练。