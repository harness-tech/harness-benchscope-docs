---
title: "评测数据集"
description: "BenchScope 内置的 12 个数据集：9 个精度评测数据集（绑定判分器与主指标）与 3 个性能压测数据集，含类别、样本量与用法示例。"
---

# 评测数据集

BenchScope 内置 **12 个数据集**，其中 **9 个精度评测数据集**（绑定判分器与样本量声明，可用于精度评测）与 **3 个性能压测数据集**（提供压测用真实对话数据），覆盖知识 / 数学 / 代码 / 对话 / 综合 / 指令等类别。选择数据集时，可直接传**内置数据集 id**（`mmlu` / `gsm8k` 等）或**本地 JSONL 路径**。

## 精度评测数据集（9 个）

每个评测数据集绑定专用判分器（`choice` / `math` / `code` / `judge`）与主指标，专项指标口径见[精度核心指标](/zh/docs/accuracy/metrics/)：

| 数据集 id | 名称 | 类别 | 判分器 | 主指标 | 样本量 |
| --- | --- | --- | --- | --- | --- |
| `mmlu` | MMLU | 知识 | `choice` | accuracy | 14,079（57 学科） |
| `cmmlu` | CMMLU | 知识 | `choice` | accuracy | 11,960（67 学科） |
| `c-eval` | C-Eval | 知识 | `choice` | accuracy | 13,480（52 学科） |
| `gsm8k` | GSM8K | 数学 | `math` | exact_match | 7,473 |
| `math` | MATH | 数学 | `math` | exact_match | 5,000 |
| `humaneval` | HumanEval | 代码 | `code` | pass@1 | 164 |
| `mbpp` | MBPP | 代码 | `code` | pass@1 | 974 |
| `mt-bench` | MT-Bench | 对话 | `judge` | mt_bench | 80 题（160 轮） |
| `gaokao-bench` | GAOKAO-Bench | 综合 | `choice` | accuracy | 2,000（客观题子集） |

## 性能压测数据集（3 个）

为性能压测提供真实对话数据（ShareGPT 模式），不绑定判分器：

| 数据集 id | 名称 | 类别 | 说明 |
| --- | --- | --- | --- |
| `sharegpt` | ShareGPT | 对话 | ShareGPT 对话数据集（ModelScope 自动下载），用于 ShareGPT 模式基准测试。 |
| `alpaca` | Alpaca | 指令微调 | Stanford Alpaca 指令微调数据集（52K 对话样本），对话格式基准测试。 |
| `dolly` | Dolly | 指令微调 | Databricks Dolly-15k 指令微调数据集（15K 样本），对话格式基准测试。 |

完整清单（含下载源与分类）见 [设置（Settings）→ Datasets](/zh/docs/tools/settings/)。

## 使用内置数据集

传入内置数据集 id 即可：

```console
# 例：在 GSM8K 上评测 200 个样本
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

## 使用本地 JSONL

传本地 JSONL 路径，按你自己的数据评测：

```console
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset /path/to/my-data.jsonl --limit 100
```

## 常见问题

**问题：数据集与判分器如何对应？**
不同数据集适用不同判分器（如选择题用 `choice`、数学用 `math`、代码用 `code`）。详见 [判分器与指标](/zh/docs/accuracy/scoring/)。

**问题：找不到我需要的评测集？**
可以用本地 JSONL 导入自己的数据参与评测。

## 相关文档

- [概述](/zh/docs/accuracy/) — 模块总览
- [判分器与指标](/zh/docs/accuracy/scoring/) — 结果怎样判定
- [精度核心指标](/zh/docs/accuracy/metrics/) — 各判分器专项指标口径
- [设置（Settings）](/zh/docs/tools/settings/) — 配置 Datasets
