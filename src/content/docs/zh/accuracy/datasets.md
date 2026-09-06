---
title: "评测数据集"
---

# 评测数据集

BenchScope 内置 **9 个专用评测数据集**，覆盖知识 / 数学 / 代码 / 对话 / 中文专项等类别。选择数据集时，可直接传**内置数据集 id**（`mmlu` / `gsm8k` 等）或**本地 JSONL 路径**。

| 类别 | 示例 |
| --- | --- |
| 知识 | MMLU |
| 数学 | GSM8K |
| 代码 | HumanEval / MBPP（代码沙箱 `pass@1`） |
| 对话 / 评审 | MT-Bench（LLM-as-judge） |
| 中文专项 | 内置数据集内的中文专项集 |

完整清单见 [设置（Settings）→ Datasets](/zh/docs/tools/settings/)。

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
- [设置（Settings）](/zh/docs/tools/settings/) — 配置 Datasets
