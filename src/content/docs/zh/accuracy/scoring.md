---
title: "判分器与指标"
---

# 判分器与指标

精度评测内置多种判分器，覆盖不同任务类型，并输出标准精度指标、Token 消耗与**开源基线对标**结果。

## 判分器

| 判分器 | 适用任务 | 指标 |
| --- | --- | --- |
| `choice` | 选择题 | exact_match |
| `math` | 数学题 | math_accuracy |
| `code` | 代码生成 | pass_at_1 / compile_rate |
| `judge` | MT-Bench 评审 | mt_bench_score（需 judge-model） |

## 输出指标

- `accuracy` / `pass_rate` — 整体正确率与通过率；
- `dataset_metrics` — 数据集专项指标（`math_accuracy` / `pass_at_1` 等）；
- **Token 消耗** — 本次评测使用的总 token；
- **基线对标** — `baseline_used` / `diff_pp` / `grade` / `conclusion`，与开源基线库对比并给出档位评级。

### 基线对标（Baseline）

评测结果与**开源基线库**对标，输出档位评级与能力对比：

| 字段 | 含义 |
| --- | --- |
| `baseline_used` | 所用基线（名称 / 权重） |
| `diff_pp` | 与基线的百分比差值 |
| `grade` | 档位评级 |
| `conclusion` | 结论（合格 / 精度下跌 / 持平 / 优于基线等） |

### 结果示例

```console
accuracy:            87.5%
pass_rate:           92.0%
dataset_metrics:     { "math_accuracy": 0.875 }
tokens.total_tokens: 51200
benchmark.conclusion: 合格（优于基线）
```

## 产物

落盘 `evals/eval-<月日时分秒>/`：

- `task.json` — 任务主表，对齐 Web 精度任务结构；
- `result.json` — 精度结果，含指标 / benchmark / conclusion；
- `samples.jsonl` — 单样本溯源。

支持**样本级溯源**，可在 **Datas → Evals** 查看 / 打包导入。

![BenchScope 精度结果统计](/images/benchscope-datas-perfs_statistics.png)

## 常见问题

**问题：评测结果中的 conclusion 是什么？**
`conclusion` 是对比基线的结论（合格 / 精度下跌 / 持平 / 优于基线等），由 `diff_pp`、`grade` 等共同判定。

**问题：如何定位个别错误样本？**
打开 `samples.jsonl`，按样本逐条查看输入、输出与判分结果，实现样本级溯源。

**问题：能否对比不同模型？**
可以。分别评测后用 `conclusion` / `diff_pp` 与基线对标，或在 Datas 中对比查看。

## 相关文档

- [概述](/zh/docs/accuracy/) — 模块总览
- [评测模式](/zh/docs/accuracy/modes/) — Native / Serving / Mock
- [评测数据集](/zh/docs/accuracy/datasets/) — 选取评测集
- [eval 命令](/zh/docs/cli/eval/) — `eval` 完整参数
