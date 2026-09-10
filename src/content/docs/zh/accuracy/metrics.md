---
title: "精度核心指标"
description: "精度评测的全部核心指标与关键指标：正确率 / 通过率 / 样本统计 / 分学科 / 判分器专项 / Token 消耗 / 基线对标 / 结论，含指标含义与判定规则。"
---

# 精度核心指标

本页是精度评测指标的**完整口径说明**：覆盖核心正确率指标、样本统计、分学科与错因分析、各判分器专项指标、Token 消耗统计、基线对标与最终结论。阅读其他精度文档（[评测模式](/zh/docs/accuracy/modes/)、[判分器与指标](/zh/docs/accuracy/scoring/)）时遇到指标名，可在此页查找含义。

## 核心指标

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |
| 正确率（核心主指标） | `accuracy` | % | 正确样本数 / 总样本数，精度评测的**核心主指标**。 |
| 通过率 | `pass_rate` | % | 有效可解析样本占比 =（总样本 - 无效样本）/ 总样本，衡量回答中可被判分的比例。 |
| 总样本数 | `total_samples` | 个 | 本轮评测实际执行的样本总数。 |
| 正确样本数 | `correct_samples` | 个 | 判分结果为正确的样本数。 |
| 错误样本数 | `wrong_samples` | 个 | 可判分但结果错误的样本数。 |
| 无效样本数 | `invalid_samples` | 个 | 无法解析 / 无法判分的样本数（格式错误、未作答等）。 |

<div class="tip">

**tip**：

`accuracy` 与 `pass_rate` 的分工：**accuracy** 回答「答对了多少」，**pass_rate** 回答「有多少回答可以被判分」。pass_rate 明显低于 100% 时，应优先排查回答格式（如选择题未输出选项字母），而不是模型能力。

</div>

## 分学科与错因分析

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |
| 分学科正确率 | `subjects` | % | 按数据集 `subject` 字段分组的逐学科正确率（`subject` 为空的样本不参与），用于定位薄弱学科。 |
| 错因标签分布 | `error_tag_summary` | 个 | 错误样本的归因标签计数（如「知识错误」），用于定位薄弱能力。 |

分学科正确率是**能力雷达图**的数据来源，雷达维度为：知识 / 数学 / 代码 / 对话（综合类数据集归入「综合」维度）。

## 判分器专项指标

不同数据集绑定不同判分器（`choice` / `math` / `code` / `judge`），判分器专项指标随判分器类型输出：

### math 判分器（数学类：GSM8K / MATH）

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |
| 精确匹配率 | `exact_match` | % | 数学题最终答案与标准答案精确匹配的样本占比。 |
| 数学正确率 | `math_accuracy` | % | 数学类数据集主指标，与 `exact_match` 同口径。 |
| 答案解析率 | `answer_parse_rate` | % | 能从模型回答中提取出可判分答案的样本占比，反映答案格式质量。 |

### code 判分器（代码类：HumanEval / MBPP）

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |
| pass@1 | `pass_at_1` | % | 单次生成即通过全部测试用例的样本占比，代码类数据集主指标。 |
| 编译通过率 | `compile_rate` | % | 生成代码可成功编译 / 执行的样本占比。 |
| 用例通过率 | `case_pass_rate` | % | 全部样本的测试用例总体通过率（通过用例数 / 总用例数），比 pass@1 更细粒度。 |

### judge 判分器（对话类：MT-Bench）

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |
| MT-Bench 总分 | `mt_bench_score` | 0–10 | LLM 评审的两轮对话平均分（首轮均分 × 0.5 + 二轮均分 × 0.5），对话类数据集主指标。 |
| 首轮得分 | `first_turn_score` | 0–10 | 第一轮对话的评审平均分。 |
| 二轮得分 | `second_turn_score` | 0–10 | 第二轮对话的评审平均分（考察对首轮上下文的继承）。 |
| 有用性维度分 | `dim_helpfulness` | 0–10 | 评审的有用性（helpfulness）维度平均分。 |
| 真实性维度分 | `dim_truthfulness` | 0–10 | 评审的真实性（truthfulness）维度平均分。 |
| 无害性维度分 | `dim_harmlessness` | 0–10 | 评审的无害性（harmlessness）维度平均分。 |

> `choice` 判分器（MMLU / CMMLU / C-Eval / GAOKAO-Bench）无额外专项指标，以 `accuracy` + 分学科正确率为主。

## Token 消耗统计（Serving 模式）

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |
| 输入 token 总量 | `prompt_tokens_total` | tokens | 本轮评测全部请求的输入（prompt）token 总量。 |
| 输出 token 总量 | `completion_tokens_total` | tokens | 本轮评测全部响应的输出（completion）token 总量。 |
| token 总量 | `total_tokens` | tokens | 输入 + 输出 token 总量，用于成本核算。 |
| 单样本平均输入 token | `avg_prompt_tokens_per_sample` | tokens | 输入 token 总量 / 总样本数。 |
| 单样本平均输出 token | `avg_completion_tokens_per_sample` | tokens | 输出 token 总量 / 总样本数。 |

> **Native 模式无 Token 统计**（本地离线推理，无线上链路消耗），`tokens` 字段为 null。

## 基线对标

评测结果与**开源基线库**（内置 10 个基线模型，见[评测模式 → 基线库](/zh/docs/accuracy/modes/)）对标，输出以下字段：

| 指标 | 键名 | 单位 | 含义 |
| --- | --- | --- | --- |
| 对标基线 | `baseline_used` | — | 参与对标的开源基线模型名（基线库中同尺寸段最优 / 指定模型）。 |
| 基线差值 | `diff_pp` | pp | 本次主指标得分与基线得分的差值（百分点），正数表示优于基线。 |
| 档位评级 | `grade` | S/A/B/C | 按与同尺寸段最优基线的差值评级：**S** ≥ 0；**A** ≥ -5；**B** ≥ -15；其余为 **C**。 |

### 最终结论（conclusion）

| 结论 | 判定规则 |
| --- | --- |
| 异常 | 总样本 = 0，或无效样本占比 > 20%。 |
| 精度下跌 | 主指标较基线下降 > 5pp（`diff_pp` < -5）。 |
| 合格 | 其余情况。 |

## Token 消耗预估（estimate）

评测前按数据集样本量与平均长度预估消耗，字段如下：

| 字段 | 含义 |
| --- | --- |
| `prompt_tokens` / `completion_tokens` / `total_tokens` | 预估的输入 / 输出 / 总 token 量。 |
| `est_seconds` | 预估耗时（秒）。 |
| `source` | 估算来源：内置样本均值（builtin）或字符估算（chars，自定义数据集）。 |
| `total_samples` | 参与预估的样本数。 |

评测结束后提供**预估 vs 实际**对比（偏差百分比 =（实际 - 预估）/ 预估）。Native 模式预估恒为 0（无线上链路消耗）。

## 产物文件

| 文件 | 内容 |
| --- | --- |
| `task.json` | 任务主表：模式 / 引擎 / 模型 / LoRA / 数据集 / 采样参数 / 进度 / 预估 / 状态。 |
| `result.json` | 精度结果：全部核心指标 + 分学科 + 专项指标 + Token 统计 + 基线对标 + 结论。 |
| `samples.jsonl` | 逐样本记录：输入 / 输出 / 判分状态 / 错因标签 / token 数，用于样本级溯源。 |

## 常见问题

**问题：accuracy 很高但 pass_rate 很低，说明什么？**
说明大量回答无法被判分（格式错误、未输出标准答案形式），优先修复回答格式或提示词，而不是怀疑模型能力。

**问题：grade 是怎么评出来的？**
按本次主指标得分与**同尺寸段最优开源基线**的差值分档：S（不低于最优基线）/ A（差距 ≤ 5pp）/ B（差距 ≤ 15pp）/ C（差距 > 15pp）。

**问题：什么时候会给出「异常」结论？**
总样本为 0（评测未实际执行）或无效样本占比超过 20%（回答大面积无法判分）时，结论为「异常」，应先排查数据与链路。

**问题：Native 模式为什么没有 Token 统计？**
Native 模式是本地离线推理，不经过线上服务链路，无 API Token 消耗，`tokens` 字段为 null。

## 相关文档

- [精度测试概述](/zh/docs/accuracy/) — 模块总览
- [评测模式](/zh/docs/accuracy/modes/) — Native / Serving / Mock 与基线库
- [评测数据集](/zh/docs/accuracy/datasets/) — 数据集与判分器绑定
- [判分器与指标](/zh/docs/accuracy/scoring/) — 判分流程与对标
- [eval 命令](/zh/docs/cli/eval/) — CLI 输出指标对照