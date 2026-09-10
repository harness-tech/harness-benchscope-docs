---
title: "精度评测"
description: "精度评测操作指南：Serving / Native / Mock 模式的运行命令与参数、结果指标解读、基线对标与样本级溯源，以及 Web 三步表单操作。"
---

# 精度评测

本节演示如何对模型输出做**精度评测**（服务模式与原生模式），并解读结果指标、基线对标与样本级溯源。

## 前置条件

- 已安装 benchscope（见 [快速入门](/zh/docs/quickstart/)）；
- Serving 模式需要一个已部署的 OpenAI 兼容服务；
- Native 模式需要安装可选依赖 `benchscope[accuracy-native]`。

## 服务模式（Serving）

评测已部署服务链路——反映用户线上真实拿到的行为，**含服务栈**：

```bash
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

| 参数 | 说明 |
| --- | --- |
| `--mode serving` | 走 OpenAI 兼容链路评测（默认） |
| `--model` | 被测模型名 |
| `--base-url` | 服务地址（缺省用全局 Provider 配置） |
| `--dataset gsm8k` | 内置数据集 id |
| `--limit 200` | 抽样 200 条 |

## 原生模式（Native）

加载本地权重离线评测（需安装可选依赖）：

```bash
pip install benchscope[accuracy-native]
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100
```

<div class="warning">

**warning**：

Native 模式会检测本地 torch / transformers 依赖，不满足则直接阻断并提示安装，而非带病运行。

</div>

### 使用 LoRA 适配器（可选）

```bash
benchscope eval --mode native --model Qwen/Qwen2.5-7B \
  --lora-path /path/to/adapter --dataset gsm8k --limit 100
```

## Mock 联调

无需真实服务即可验证链路：

```bash
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

可通过 `--mock-correct-rate 0.85` 调节正确率，模拟不同的评测结果（联调用）。

## 解读结果

全部指标口径见[精度核心指标](/zh/docs/accuracy/metrics/)，常用指标如下：

- **`accuracy` / `pass_rate`**：核心主指标——整体正确率与通过率；
- **`subjects` / `error_tag_summary`**：分学科正确率（能力雷达）与错因标签分布；
- **`dataset_metrics`**：判分器专项指标（`exact_match` / `math_accuracy` / `pass_at_1` / `compile_rate` / `mt_bench_score` 等）；
- **`tokens`**（Serving 模式）：输入 / 输出 / 总 token 量与单样本均值；
- **`benchmark`**：与基线对标（`baseline_used` / `diff_pp` / `grade`）；
- **`conclusion`**：最终结论（合格 / 精度下跌 / 异常）；
- **`samples.jsonl`**：样本级溯源，可定位个别错误样本。

```console
accuracy:            87.5%
pass_rate:           92.0%
total_samples:       200
correct_samples:     175
wrong_samples:       25
dataset_metrics:     { "math_accuracy": 87.5 }
tokens.total_tokens: 51200
conclusion:          合格
```

## Web 操作

在网页 **精度测试** 页创建评测任务（三步表单）：

1. **Step1 数据集**：选择内置评测数据集（或本地 JSONL）与抽样上限（limit）；
2. **Step2 模式与引擎**：选择 Native / Serving 模式与精度引擎（benchscope / native-hf / mock）；
3. **Step3 预览与确认**：核对任务参数与 **Token 消耗预估**（超阈值强提醒），确认后启动；
4. 在 **Accuracy 页面**查看任务进度、结果指标、分学科与基线对标。

![BenchScope 精度测试默认界面](/images/benchscope-accuracy_default.png)

## 常见问题

**问题：如何快速避免成本超支？**
先用 `--limit 100` 抽样验证链路与判分，正常后再跑全量；Serving 模式会做 Token 预估并强提醒。

**问题：能否对比不同模型？**
可以。分别评测后用 `diff_pp` / `grade` 与基线对标，或在 Accuracy 页面对多个任务的结果横向对比。

**问题：评测中途被阻断？**
Serving 检查服务可达性、Native 检查本地依赖；缺依赖时按提示安装 `benchscope[accuracy-native]` 后重试。

## 相关文档

- [概述](/zh/docs/accuracy/) — 三模式与判分器详解
- [精度核心指标](/zh/docs/accuracy/metrics/) — 全部指标完整口径
- [eval 命令](/zh/docs/cli/eval/) — `eval` 完整参数
- [评测模式](/zh/docs/accuracy/modes/) — Native / Serving / Mock 与基线库
