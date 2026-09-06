---
title: "教程：精度评测"
---

# 教程：精度评测

本教程演示对模型输出做**精度评测**（服务模式与原生模式），并解读结果指标、对标基线与样本级溯源。

## 前置条件

- 已安装 benchscope（见 [快速入门](/zh/docs/quickstart/)）；
- Serving 模式需要一个已部署的 OpenAI 兼容服务；
- Native 模式需要安装可选依赖 `benchscope[accuracy-native]`。

## 服务模式（Serving）

评测已部署服务链路：

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

无真实服务验证链路：

```bash
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

可通过 `--mock-correct-rate 0.85` 调节正确率，模拟不同的评测结果（联调用）。

## 解读结果

- **`accuracy` / `pass_rate`**：整体正确率与通过率；
- **`dataset_metrics`**：数据集专项指标（`math_accuracy` / `pass_at_1` 等）；
- **`benchmark`**：与基线对标（`diff_pp` / `grade` / `conclusion`）；
- **`samples.jsonl`**：样本级溯源，可定位个别错误样本。

```console
accuracy:            87.5%
pass_rate:           92.0%
total_samples:       200
correct_samples:     175
wrong_samples:       25
dataset_metrics:     { "math_accuracy": 0.875 }
tokens.total_tokens: 51200
conclusion:          合格（优于基线）
```

## Web 操作

在网页 **精度测试** 页创建评测任务（原生 / 服务双模式），选择数据集与判分器，Token 预估后启动；结果在 **Datas → Evals** 查看。

![BenchScope 精度测试默认界面](/images/benchscope-accuracy_default.png)

## 常见问题

**问题：如何快速避免成本超支？**
先用 `--limit 100` 抽样验证链路与判分，正常后再跑全量；Serving 模式会做 Token 预估并强提醒。

**问题：能否对比不同模型？**
可以。分别评测后用 `conclusion` / `diff_pp` 与基线对标，或在 Datas 中对比查看。

## 相关文档

- [精度测试](/zh/docs/accuracy/) — 双模式与判分器详解
- [CLI 参考](/zh/docs/cli/reference/) — `eval` 完整参数
- [数据与统计（Datas）](/zh/docs/data/) — 结果查看与导入
