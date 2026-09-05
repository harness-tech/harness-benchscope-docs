# CLI 参考

`benchscope` 命令行提供三个子命令：**`serve`**（Web 服务）、**`perf`**（性能压测）与 **`eval`**（精度评测）。

```text
benchscope [--version] {serve,perf,eval} [子命令选项]
```

::: info
**向后兼容行为**：当 `benchscope` 无参数、或首个参数是选项（如 `--port 8080`）时，会走向兼容的「启动服务」行为，等价于 `benchscope serve`。
:::

## 启动服务（serve）

```bash
benchscope serve [--host HOST] [--port PORT] [--no-browser] [--debug]
```

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `--host` | `0.0.0.0` | 监听地址 |
| `--port` | `8080` | 监听端口 |
| `--no-browser` | 关闭 | 启动时不自动打开浏览器 |
| `--debug` | 关闭 | 开启调试日志（输出更详细的运行日志便于排障） |

::: tip
`--debug` 在排查任务启动、接口调用等问题时非常有用，会输出详细的 debug 级别日志。
:::

## 性能压测（perf）

对 OpenAI 兼容推理服务执行一次自研引擎压测，输出吞吐与延迟指标。

```bash
benchscope perf --model MODEL [选项]
```

**模式（`--mode`）**：

- `concurrency`（默认）：单并发压测一次；
- `threshold`：从 1 并发起以 2 的次方递增 + 二分，找到满足阈值的最大并发（`best_concurrency`）。

### 常用示例

```console
# 并发模式：固定并发 8，每个并发 100 个请求，输入/输出各 1024 token
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024

# 阈值模式：TTFT ≤ 200ms 且 TPOT ≤ 100ms，搜索最大并发（上限 1024）
benchscope perf --model Qwen2.5-7B --mode threshold \
  --ttft-threshold-ms 200 --tpot-threshold-ms 100 --max-concurrency-search 1024
```

### 主要参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--engine` | str | `benchscope` | 引擎 id（默认自研引擎 benchscope） |
| `--model` | str | **必填** | 被测模型名 |
| `--base-url` | str | `http://127.0.0.1:8000` | 被测推理服务地址 |
| `--api-key` | str | 空 | 被测服务 API Key（可选） |
| `--backend` | str | `openai-chat` | 接口协议：`openai-chat` / `openai` |
| `--endpoint` | str | `/v1/chat/completions` | 请求的接口路径 |
| `--mode` | str | `concurrency` | 压测模式：`concurrency` / `threshold` |
| `--concurrency` | int | `1` | 并发数（concurrency 模式） |
| `--num-prompts` | int | `0` | 请求总数（0 = 跟随并发数，每个 worker 一个请求） |
| `--input-len` | int | `1024` | 输入 token 数 |
| `--output-len` | int | `1024` | 输出 token 数 |
| `--request-rate` | str | `inf` | 请求速率（req/s，`inf` 表示不限速） |
| `--num-warmups` | int | `0` | 预热请求数（不计入指标） |
| `--chars-per-token` | float | `4.0` | 字符 / token 近似比（构造输入长度用） |
| `--timeout` | float | `600.0` | 单请求超时（秒），超时计为失败 |
| `--temperature` | float | `0.0` | 采样温度（压测建议固定为 0） |
| `--seed` | int | `0` | 随机种子（0 = 不固定） |

### 阈值模式专属参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--ttft-threshold-ms` | float | `0.0` | TTFT 阈值（ms），`0` = 不判定 |
| `--tpot-threshold-ms` | float | `100.0` | TPOT 阈值（ms），`0` = 不判定 |
| `--output-threshold` | float | `0.0` | 输出吞吐阈值（tok/s），**低于**该值判为不满足，`0` = 不判定 |
| `--ttft-statistic` | str | `mean` | TTFT 阈值判定的统计量：`mean` / `median` / `p99` |
| `--tpot-statistic` | str | `mean` | TPOT 阈值判定的统计量：`mean` / `median` / `p99` |
| `--max-concurrency-search` | int | `4096` | 阈值搜索上限：达到仍满足阈值则取上限为最佳并发 |
| `--max-requests` | int | `4096` | 阈值探测中并发数超过该上限则强制结束（Finish） |

### 阈值探测策略

1. 从 **1 并发** 开始，以 **2 的次方递增**（1, 2, 4, 8, …）逐步压测；
2. 若 1 并发已不满足阈值 → 最佳并发为 1，结束；
3. 若执行到 `hi = 2^k` 不满足（`lo = 2^(k-1)` 满足）→ 在 `(lo, hi]` 内**二分**，直到相邻两个值，`lo` 即满足阈值的最大并发；
4. 达到搜索上限仍满足 → 上限并发为最佳（正常结束）。

输出每个已测并发的指标（吞吐 / TTFT / TPOT / ITL）与 `best_concurrency`。

### 输出指标

| 指标 | 含义 |
| --- | --- |
| `successful_requests` | 成功请求数 |
| `failed_requests` | 失败请求数 |
| `benchmark_duration` | 压测墙钟时长 |
| `output_mean` (tok/s) | 输出吞吐（均值） |
| `total_mean` (tok/s) | 总吞吐（均值） |
| `ttft_mean` (ms) | 首 token 延迟（均值） |
| `tpot_mean` (ms) | 每输出 token 延迟（均值） |
| `itl_mean` (ms) | 令牌间隔延迟（均值） |

### 产物与导入

- 落盘 `run.json`（含 `task_id` / `kind: perf` / `summary`）+ 日志 `perf_<run_id>_*.log`（写入 `perfs_dir` / `logs_dir`）。
- 打包为**扁平 zip**（含 `run.json` + 日志 + 可选 `metrics.json`），可在网页 **Datas → Perfs → 导入备份** 导入。

```console
# 一次典型的并发压测运行输出示例
$ benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
    --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024
Benchmarking Qwen2.5-7B @ http://127.0.0.1:8000 (mode=concurrency, concurrency=8) ...
100%|████████████████████████████████████| 100/100 [00:45<00:00]
============================ Summary ============================
Successful requests: 100
Failed requests:     0
Benchmark duration:  45.23s
Output throughput:   112.4 tokens/s (output_mean)
Total throughput:    335.6 tokens/s (total_mean)
TTFT (mean):         92.5 ms
TPOT (mean):         34.2 ms
ITL  (mean):         33.9 ms
Saved run.json -> ~/.benchscope/perfs/run_<id>.json
```

::: tip
CLI 生成的 `run.json`（含完整 summary）可直接打包后在网页 **Datas → Perfs** 中导入，与网页创建的性能任务产物完全兼容。
:::

## 精度评测（eval）

执行一次精度评测（Serving / Native / Mock），输出 accuracy / pass_rate 等指标。

```bash
benchscope eval --model MODEL --dataset DATASET [选项]
```

数据集可传内置 id（`mmlu` / `gsm8k` ...）或本地 JSONL 路径。

### 常用示例

```console
# Serving 链路评测
benchscope eval --mode serving --model Qwen2.5-7B \
  --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200

# Native 原生评测
benchscope eval --mode native --model Qwen/Qwen2.5-7B --dataset mmlu --limit 100

# Mock 联调
benchscope eval --mode serving --engine mock --model mock-model --dataset gsm8k --use-mock-env
```

### 主要参数

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `--engine` | str | `benchscope` | 精度引擎 id（`benchscope`=serving / `native-hf`=native / `mock`=联调） |
| `--mode` | str | `serving` | 评测模式：`serving`（链路）/ `native`（本地权重） |
| `--model` | str | **必填** | 被测模型名（Native 可传本地权重路径或 HF id） |
| `--lora-path` | str | 空 | LoRA 微调增量模型（adapter）路径（可选） |
| `--lora-name` | str | 空 | LoRA 增量模型服务端注册名（Serving 请求侧 model，可选） |
| `--dataset` | str | **必填** | 内置数据集 id（mmlu / gsm8k / ...）或本地 JSONL 路径 |
| `--base-url` | str | 空 | 被测服务地址（Serving；缺省取全局 Provider 配置） |
| `--api-key` | str | 空 | 被测服务 API Key（可选） |
| `--limit` | int | `0` | 样本抽样上限（0 = 全量） |
| `--seed` | int | `1234` | 全局随机种子（抽样与生成，固定可复现） |
| `--temperature` | float | `0.0` | 采样温度 |
| `--top-p` | float | `1.0` | 核采样概率 |
| `--max-tokens` | int | `512` | 单样本最大输出 token |
| `--concurrency` | int | `4` | 并发推理数 |
| `--judge-model` | str | 空 | MT-Bench 评审模型（judge 数据集用） |
| `--mock-correct-rate` | float | `0.7` | mock 引擎正确率（0-1） |
| `--name` | str | 空 | 任务名称（可选） |
| `--use-mock-env` | flag | 关闭 | mock 环境标记（联调用） |

### 输出指标

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

### 产物与导入

产物落盘 `evals/eval-<月日时分秒>/`：

- `task.json` — 任务主表，对齐 Web 精度任务结构；
- `result.json` — 精度结果，含指标 / benchmark / conclusion；
- `samples.jsonl` — 单样本溯源。

另写终端日志 `logs/eval_<task_id>_<时间>.log`。所有产物可在网页 **Datas → Evals** 查看 / 打包导入。

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

## 相关文档

- [快速入门](./quickstart.md) — 安装与启动
- [性能测试](../core/performance.md) — 并发压测与阈值探测
- [精度测试](../core/accuracy.md) — 双模式评测
- [教程：并发压测](../tutorials/perf-concurrency.md)
- [教程：阈值压测](../tutorials/perf-threshold.md)
- [教程：精度评测](../tutorials/accuracy-guide.md)
