---
title: "评测模式"
description: "精度评测的三种模式：原生（Native）、服务（Serving）与 Mock 联调，含运行命令、内置开源基线库（10 个基线模型）与 Token 预估说明。"
---

# 评测模式

精度评测支持**原生（Native）**、**服务（Serving）**与 **Mock（联调）**三种模式，并可在评测前**预估 Token 消耗**以控制成本。选择模式的关键在于：是否已有真实服务、是否需要离线评测本地权重。

## 原生模式（Native）

原生模式加载本地权重或 HF 模型 id 离线评测，支持 LoRA 适配器，需先安装可选依赖：

```bash
pip install benchscope[accuracy-native]
```

```console
# 例：对本地 / HF 模型在 MMLU 上评测 100 个样本
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100
```

<div class="warning">

**warning**：

Native 模式**不强制安装** torch / transformers——仅检测已有依赖，**不满足则直接阻断**并提示安装，而不是带病运行。请确保已安装所需依赖后再发起评测。

</div>

### 使用 LoRA 适配器（可选）

```bash
benchscope eval --mode native --model Qwen/Qwen2.5-7B \
  --lora-path /path/to/adapter --dataset gsm8k --limit 100
```

## 服务模式（Serving）

服务模式通过 OpenAI 兼容链路评测已部署服务；被测服务地址缺省时使用全局 Provider 配置。

```console
# 例：对已部署服务在 GSM8K 上评测 200 个样本
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

<div class="info">

**info**：

Serving 模式无额外依赖，评测时每一次请求都经过真实的服务链路（含 Token 消耗），能反映线上真实行为。

</div>

## Mock 联调

无真实服务也可验证链路正确性（常用于开发 / CI 联调）：

```console
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

可通过 `--mock-correct-rate`（默认 `0.7`）调节 mock 正确率，模拟不同的评测结果。

## 开源基线库

评测结果与**内置开源基线库**对标（当前 10 个基线模型），用于横向对比与档位评级：

| 基线模型 | 参数量 | 分组 | 覆盖数据集 |
| --- | --- | --- | --- |
| Llama-3-8B | 8B | 通用 | MMLU / GSM8K / MATH / HumanEval / MBPP / CMMLU / C-Eval / MT-Bench |
| Llama-3-70B | 70B | 通用 | 同上 |
| Qwen2-7B | 7B | 通用 | 同上 |
| Qwen2-14B | 14B | 通用 | 同上 |
| Qwen2-72B | 72B | 通用 | 同上 |
| InternLM2-7B | 7B | 通用 | 同上 |
| Mistral-7B | 7B | 通用 | 同上 |
| Qwen2-Chinese | 7B | 中文专项 | MMLU / CMMLU / C-Eval / GSM8K / MT-Bench |
| Llama3-CN | 8B | 中文专项 | 同上 |
| Zephyr-7B | 7B | 中文专项 | MMLU / GSM8K / MATH / HumanEval / MBPP / MT-Bench |

基线分数为公开技术报告 / 榜单的**近似参考值**（多为 instruct / chat 口径），用于横向对标，不作为官方口径引用；管理员可经 `PUT /api/accuracy/baselines` 更新基线库。评级规则（S / A / B / C 与 `diff_pp`）见[精度核心指标 → 基线对标](/zh/docs/accuracy/metrics/)。

## Token 预估

评测开始前可**预估消耗的总 token**，便于成本控制：

- Serving 模式支持**全量 Token 消耗预估**（字段：`prompt_tokens` / `completion_tokens` / `total_tokens` / `est_seconds` / `source`）；
- 创建页（Web）与 `benchscope eval`（CLI）均会在启动前展示预估，超过预期时给出**强提醒**；
- 评测结束提供**预估 vs 实际对比**（偏差百分比 =（实际 - 预估）/ 预估）；
- Native 模式预估恒为 0（本地离线推理，无线上链路消耗）。

详见[精度核心指标 → Token 消耗预估](/zh/docs/accuracy/metrics/)。

<div class="tip">

**tip**：

在数据量大或模型较贵时，先用 `--limit` 抽样（如 100–200 条）做小规模验证，确认链路与判分正常后再跑全量。

</div>

## 常见问题

**问题：如何快速避免成本超支？**
先用 `--limit 100` 抽样验证链路与判分，正常后再跑全量；Serving 模式会做 Token 预估并强提醒。

**问题：评测中途被阻断？**
Serving 检查服务可达性、Native 检查本地依赖；缺依赖时按提示安装 `benchscope[accuracy-native]` 后重试。

## 相关文档

- [概述](/zh/docs/accuracy/) — 模块总览
- [精度核心指标](/zh/docs/accuracy/metrics/) — 全部指标完整口径
- [评测数据集](/zh/docs/accuracy/datasets/) — 选择评测集
- [判分器与指标](/zh/docs/accuracy/scoring/) — 解读结果
- [eval 命令](/zh/docs/cli/eval/) — `eval` 完整参数
