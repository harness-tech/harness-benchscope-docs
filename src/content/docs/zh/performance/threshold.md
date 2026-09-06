---
title: "阈值压测"
---

# 阈值压测

在**已知业务 SLA** 时，用阈值探测自动找到满足条件的**最大并发**（`best_concurrency`），回答「这套配置最多能扛住多少并发且不超 SLA」。相比手动猜测固定并发档位，阈值模式会自动搜索。

## 定义 SLA

首先把 SLA 落成具体数值。例如交互类业务的典型要求：

- **TTFT ≤ 200ms**（首 token 及时响应）；
- **TPOT ≤ 100ms**（流式输出保持流畅）。

这两项即你的阈值条件。

<div class="tip">

**tip**：

阈值条件还可加**输出吞吐下限**（`--output-threshold`），要求吞吐不低于某值才算达标，详见 [perf 命令](/zh/docs/cli/perf/)。

</div>

## CLI 命令与参数

在阈值模式下，指定阈值与搜索上限启动：

```bash
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --mode threshold \
  --ttft-threshold-ms 200 --tpot-threshold-ms 100 \
  --max-concurrency-search 1024
```

| 参数 | 含义 |
| --- | --- |
| `--mode threshold` | 启用阈值探测 |
| `--ttft-threshold-ms 200` | TTFT 均值超过 200ms 即判定该档不达标 |
| `--tpot-threshold-ms 100` | TPOT 均值超过 100ms 即判定该档不达标 |
| `--max-concurrency-search 1024` | 搜索上限（并发天花板） |

## 探测策略

1. 从 **1 并发** 起以 **2 的次方递增**（1, 2, 4, 8, …）压测；
2. 找到**首个不满足阈值**的点后，在相邻区间内**二分**；
3. 输出**每个已测并发**的指标与 `best_concurrency`。

```console
# 探测过程示意
Concurrency  1  : TTFT 45ms / TPOT 18ms  -> OK
Concurrency  2  : TTFT 58ms / TPOT 22ms  -> OK
Concurrency  4  : TTFT 90ms / TPOT 41ms  -> OK
Concurrency  8  : TTFT 155ms/ TPOT 78ms  -> OK
Concurrency 16  : TTFT 312ms/ TPOT 160ms -> FAIL
-> 二分区间 (8, 16] ...
Concurrency 12  : TTFT 210ms/ TPOT 105ms -> FAIL
Concurrency 10  : TTFT 198ms/ TPOT 96ms  -> OK
best_concurrency = 10
```

本例中，10 是同时满足两项阈值的最大并发。

## 解读结果

- **`best_concurrency`** 即满足**全部阈值条件**的最大并发；
- 若取到**搜索上限**仍满足，说明系统在该上限下仍达标（可放大搜索上限进一步探测）；
- 可调整判定统计量（`--ttft-statistic p99` 等）以适配**不同的业务口径**——例如严格 SLA 可改用 `p99` 而非 `mean`。

| 判定统计量 | 含义 | 适用 |
| --- | --- | --- |
| `mean` | 均值 | 一般业务口径 |
| `median` | 中位数 | 减弱极端值影响 |
| `p99` | 99 分位 | 对长尾延迟敏感的业务（更严格） |

## 网页操作

在 **性能测试** 页创建阈值为模式的压测任务：选择 Threshold 模式，填入 TTFT / TPOT 阈值、判定统计量与搜索上限，预览命令后启动；运行结果自动给出 `best_concurrency`。

<div class="tip">

**tip**：

阈值模式很高效——先翻倍探测到首个失败点，再二分收敛，即使搜索上限很大，实际压测轮次也保持很少。

</div>

## 常见问题

**问题：搜索上限设多大合适？**
从业务可接受的规模估计，如未知可先设 512–1024；上限越大探测时间通常越长。

**问题：为什么 `best_concurrency` 是 1？**
说明 1 并发时已不满足阈值（例如单次请求本身就超 TTFT/TPOT），需先排查服务性能。

## 相关文档

- [性能测试](/zh/docs/performance/) — 阈值模式原理与判定条件
- [perf 命令](/zh/docs/cli/perf/) — 阈值模式专属参数
- [并发压测](/zh/docs/performance/concurrency/) — 手动逐档压测
