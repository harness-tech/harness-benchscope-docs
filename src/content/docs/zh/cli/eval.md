---
title: "eval 命令"
---

# eval 命令

执行一次精度评测（Serving / Native / Mock），输出 accuracy / pass_rate 等指标。

```bash
benchscope eval --model MODEL --dataset DATASET [选项]
```

数据集可传内置 id（`mmlu` / `gsm8k` ...）或本地 JSONL 路径。

## 常用示例

```console
# Serving 链路评测：对已部署的 OpenAI 兼容服务评测
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200

# Native 原生评测：本地 transformers 权重 / HF id 离线评测
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100

# Mock 联调：无需真实服务即可验证链路
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

## 主要参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--engine` | str | `benchscope` | 精度引擎 id（`benchscope`=serving / `native-hf`=native / `mock`=联调） |
| `--mode` | str | `serving` | 评测模式：`serving`（链路）/ `native`（本地权重） |
| `--model` | str | **必填** | 被测模型名（Native 可传本地权重路径或 HF id） |
| `--dataset` | str | **必填** | 内置数据集 id（mmlu / gsm8k / ...）或本地 JSONL 路径 |

**服务与模型适配**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--lora-path` | str | 空 | LoRA 微调增量模型（adapter）路径（可选） |
| `--lora-name` | str | 空 | LoRA 增量模型服务端注册名（Serving 请求侧 model，可选） |
| `--base-url` | str | 空 | 被测服务地址（Serving；缺省取全局 Provider 配置） |
| `--api-key` | str | 空 | 被测服务 API Key（可选） |

**采样与生成**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--limit` | int | `0` | 样本抽样上限（0 = 全量） |
| `--seed` | int | `1234` | 全局随机种子（抽样与生成，固定可复现） |
| `--temperature` | float | `0.0` | 采样温度 |
| `--top-p` | float | `1.0` | 核采样概率 |
| `--max-tokens` | int | `512` | 单样本最大输出 token |
| `--concurrency` | int | `4` | 并发推理数 |

**评审 / 联调 / 命名**

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--judge-model` | str | 空 | MT-Bench 评审模型（judge 数据集用） |
| `--mock-correct-rate` | float | `0.7` | mock 引擎正确率（0-1） |
| `--name` | str | 空 | 任务名称（可选） |
| `--use-mock-env` | flag | 关闭 | mock 环境标记（联调用） |

## 输出指标

| 指标 | 含义 |
| --- | --- |
| `accuracy` (%) | 整体正确率 |
| `pass_rate` (%) | 通过率 |
| `total_samples` / `correct_samples` | 总样本数 / 正确数 |
| `wrong_samples` / `invalid_samples` | 错误数 / 无效数 |
| `dataset_metrics` | 数据集专项指标（`exact_match` / `math_accuracy` / `pass_at_1` / `compile_rate` / `mt_bench_score` 等） |
| `tokens.total_tokens` | 消耗总 token |
| `benchmark` | 基线对标（`baseline_used.name` / `diff_pp` / `grade` / `conclusion`） |
| `conclusion` | 结论（合格 / 精度下跌 / 持平 / 优于基线等） |

## 运行示例

```console
# 一次典型的 Serving 评测运行输出示例
$ benchscope eval --mode serving --model Qwen2.5-7B \
    --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
Evaluating Qwen2.5-7B on gsm8k (mode=serving, limit=200) ...
100%|████████████████████████████████████| 200/200 [00:50<00:00]
===================== Accuracy Summary =====================
accuracy:            87.5%
pass_rate:           92.0%
total_samples:       200
correct_samples:     175
wrong_samples:       25
invalid_samples:     0
dataset_metrics:     { "math_accuracy": 0.875 }
tokens.total_tokens: 51200
conclusion:          合格（优于基线）
Saved -> ~/.benchscope/evals/eval-<时间>/ (task.json / result.json / samples.jsonl)
```

## 产物与导入

产物落盘 `evals/eval-<月日时分秒>/`：

- `task.json` — 任务主表，对齐 Web 精度任务结构；
- `result.json` — 精度结果，含指标 / benchmark / conclusion；
- `samples.jsonl` — 单样本溯源。

另写终端日志 `logs/eval_<task_id>_<时间>.log`。所有产物可在网页 **Datas → Evals** 查看 / 打包导入。

## 相关文档

- [CLI 概述](/zh/docs/cli/) — 子命令总览与快速上手
- [serve 命令](/zh/docs/cli/serve/) — 启动 Web 服务
- [perf 命令](/zh/docs/cli/perf/) — 性能压测
- [性能测试](/zh/docs/performance/) — 并发压测与阈值探测
- [概述](/zh/docs/accuracy/) — 双模式评测
