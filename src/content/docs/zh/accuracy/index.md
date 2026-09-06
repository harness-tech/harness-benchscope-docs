---
title: "精度测试"
---

# 精度测试

精度测试模块对模型的输出做量化评估，支持**原生（Native）**与**服务（Serving）**双模式，内置多种评测数据集与判分器，并提供 Token 预估与开源基线对标能力。

![BenchScope 精度测试默认界面](/images/benchscope-accuracy_default.png)

<div class="tip">

**tip**：

精度测试专注于「模型输出是否正确」，与[性能测试](/zh/docs/performance/)互补：性能回答「跑得多快」，精度回答「答得多准」。

</div>

## 模式总览

| 模式 | 说明 | 依赖 |
| --- | --- | --- |
| 原生 Native | 直接加载本地模型权重（transformers / HF id）离线评测 | 可选依赖 `accuracy-native`（torch / transformers / peft） |
| 服务 Serving | 通过 OpenAI 兼容链路评测已部署服务 | 无 |
| Mock（联调） | 无真实服务，验证链路正确性 | 无 |

## 内置评测数据集

BenchScope 内置 **9 个专用评测数据集**，覆盖知识 / 数学 / 代码 / 对话 / 中文专项等类别，包括：

- **MMLU**、**GSM8K** 等通用评测集；
- **HumanEval**、**MBPP** 等代码评测集（代码沙箱 `pass@1`）；
- **MT-Bench**（LLM-as-judge 对话评审）等。

数据集可传**内置数据集 id**（`mmlu` / `gsm8k` 等）或**本地 JSONL 路径**，见 [设置（Settings）→ Datasets](/zh/docs/tools/settings/)。

## 判分器与指标

内置多种判分器，覆盖不同任务类型：

| 判分器 | 适用任务 | 指标 |
| --- | --- | --- |
| `choice` | 选择题 | exact_match |
| `math` | 数学题 | math_accuracy |
| `code` | 代码生成 | pass_at_1 / compile_rate |
| `judge` | MT-Bench 评审 | mt_bench_score（需 judge-model） |

**输出指标**：`accuracy` / `pass_rate`、`dataset_metrics`、Token 消耗，以及**基线对标**（`baseline_used` / `diff_pp` / `grade` / `conclusion`）。

## 原生模式（Native）

原生模式加载本地权重或 HF 模型 id 离线评测，支持 LoRA 适配器。需先安装可选依赖：

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

## 服务模式（Serving）

服务模式通过 OpenAI 兼容链路评测已部署服务；被测服务地址缺省使用全局 Provider 配置。

```console
# 例：对已部署服务在 GSM8K 上评测 200 个样本
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

<div class="info">

**info**：

Serving 模式无额外依赖，评测时每一次请求都经过真实的服务链路（含 Token 消耗），能反映线上真实行为。

</div>

## Token 预估

评测开始前可**预估消耗的总 token**，便于成本控制：

- Serving 模式支持**全量 Token 消耗预估算**；
- 预估超过预期时会给出**强提醒**；
- 评测结束提供**实统计**，与实际消耗对标。

<div class="tip">

**tip**：

在数据量大或模型较贵时，先用 `--limit` 抽样（如 100–200 条）做小规模验证，确认链路与判分正常后再跑全量。

</div>

## Mock 联调

无真实服务验证链路正确性（常用于开发 / CI 联调）：

```console
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

可通过 `--mock-correct-rate`（默认 `0.7`）调节 mock 正确率，模拟不同的评测结果。

## 产物

落盘 `evals/eval-<月日时分秒>/`：

- `task.json` — 任务主表，对齐 Web 精度任务结构；
- `result.json` — 精度结果，含指标 / benchmark / conclusion；
- `samples.jsonl` — 单样本溯源。

支持**样本级溯源**，可在 **Datas → Evals** 查看 / 打包导入。

![BenchScope 精度结果统计](/images/benchscope-datas-perfs_statistics.png)

## 常见问题

**问题：Native 模式启动被阻断？**
未检测到 torch / transformers / peft。执行 `pip install benchscope[accuracy-native]` 后重试。

**问题：评测结果中的 conclusion 是什么？**
`conclusion` 是对比基线的结论（合格 / 精度下跌 / 持平 / 优于基线等），由 `diff_pp`、`grade` 等共同判定。

**问题：如何定位个别错误样本？**
打开 `samples.jsonl`，按样本逐条查看输入、输出与判分结果，实现样本级溯源。

## 相关文档

- [CLI 参考](/zh/docs/cli/reference/) — `eval` 命令完整参数
- [教程：精度评测](/zh/docs/accuracy/guide/) — 分步操作
- [数据与统计（Datas）](/zh/docs/data/) — 结果查看与导入
- [设置（Settings）](/zh/docs/tools/settings/) — 配置 Provider、Datasets
