---
title: "判分器与指标"
description: "精度评测判分器详解：choice / math / code / judge 四类判分器的适用任务与指标，输出指标概览、开源基线对标字段与最终结论判定规则。"
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

全部指标口径见[精度核心指标](/zh/docs/accuracy/metrics/)，此处为概览：

- `accuracy` / `pass_rate` — 核心主指标：整体正确率与通过率；
- `total_samples` / `correct_samples` / `wrong_samples` / `invalid_samples` — 样本统计；
- `subjects` — 分学科正确率（能力雷达图数据来源，维度：知识 / 数学 / 代码 / 对话 / 综合）；
- `error_tag_summary` — 错因标签分布（错误样本归因）；
- `dataset_metrics` — 判分器专项指标：math 类（`exact_match` / `math_accuracy` / `answer_parse_rate`）、code 类（`pass_at_1` / `compile_rate` / `case_pass_rate`）、judge 类（`mt_bench_score` / `first_turn_score` / `second_turn_score` / `dim_helpfulness` / `dim_truthfulness` / `dim_harmlessness`）；
- **Token 消耗**（Serving 模式） — `prompt_tokens_total` / `completion_tokens_total` / `total_tokens` / 单样本均值；
- **基线对标** — `baseline_used` / `diff_pp` / `grade` / `conclusion`，与开源基线库对比并给出档位评级。

### 基线对标（Baseline）

评测结果与**开源基线库**（内置 10 个基线模型，见[评测模式 → 开源基线库](/zh/docs/accuracy/modes/)）对标，输出档位评级与能力对比：

| 字段 | 含义 |
| --- | --- |
| `baseline_used` | 所用基线模型名（同尺寸段最优 / 指定模型） |
| `diff_pp` | 与基线得分的差值（百分点），正数表示优于基线 |
| `grade` | 档位评级：S（≥ 0）/ A（≥ -5）/ B（≥ -15）/ C（其余），按与同尺寸段最优基线的差值 |
| `conclusion` | 最终结论：**合格 / 精度下跌 / 异常** 三选一（规则见下表） |

### 最终结论判定规则

| 结论 | 判定规则 |
| --- | --- |
| 异常 | 总样本 = 0，或无效样本占比 > 20% |
| 精度下跌 | 主指标较基线下降 > 5pp（`diff_pp` < -5） |
| 合格 | 其余情况 |

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

- `task.json` — 任务主表，对齐 Web 精度任务结构（模式 / 引擎 / 模型 / LoRA / 数据集 / 采样参数 / 进度 / 预估 / 状态）；
- `result.json` — 精度结果，含全部核心指标 / 分学科 / 专项指标 / Token 统计 / benchmark / conclusion；
- `samples.jsonl` — 单样本溯源（输入 / 输出 / 判分状态 / 错因标签 / token 数）。

精度评测产物在 **Accuracy 页面**管理（任务列表 + 详情 + 样本查看）。

![BenchScope 精度结果统计](/images/benchscope-datas-perfs_statistics.png)

## 常见问题

**问题：评测结果中的 conclusion 是什么？**
`conclusion` 是最终评测结论，取值为**合格 / 精度下跌 / 异常**三选一：总样本为 0 或无效占比 > 20% → 异常；主指标较基线下降 > 5pp（`diff_pp` < -5）→ 精度下跌；其余 → 合格。

**问题：如何定位个别错误样本？**
打开 `samples.jsonl`，按样本逐条查看输入、输出、判分状态与错因标签，实现样本级溯源；`error_tag_summary` 提供错因分布汇总。

**问题：能否对比不同模型？**
可以。分别评测后用 `diff_pp` / `grade` 与基线对标，或在 Accuracy 页面对两个任务的结果横向对比。

## 相关文档

- [概述](/zh/docs/accuracy/) — 模块总览
- [精度核心指标](/zh/docs/accuracy/metrics/) — 全部指标完整口径
- [评测模式](/zh/docs/accuracy/modes/) — Native / Serving / Mock 与基线库
- [评测数据集](/zh/docs/accuracy/datasets/) — 选取评测集
- [eval 命令](/zh/docs/cli/eval/) — `eval` 完整参数
