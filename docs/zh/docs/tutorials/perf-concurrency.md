# 教程：并发压测

本教程演示如何对已部署的 OpenAI 兼容推理服务做**并发压测**，观察系统在不同并发负载下的吞吐与延迟变化曲线。

## 前置条件

- 已安装 benchscope（见 [快速入门](../get-started/quickstart.md)）
- 已有一个可用的推理服务（如 vLLM / SGLang，地址 `http://127.0.0.1:8000`）

::: tip
先用 curl 快速确认服务可用：

```bash
curl http://127.0.0.1:8000/v1/models
```
返回模型列表即表示服务可用。
:::

## 方式一：网页操作

1. 进入 **性能测试** → **创建任务**；
2. 配置**被测模型**与**服务地址**（Provider）；
3. 选择 **并发压测（Concurrency）**，填入并发级别与请求参数；
4. 三步表单完成后**预览命令**并**启动**；
5. 运行中查看**表格 / 曲线 / 进度**，结束后**导出产物**。

![BenchScope 性能测试创建任务](/images/benchscope-performance_create.png)

## 方式二：CLI

```bash
benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
  --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024
```

| 参数 | 说明 |
| --- | --- |
| `--model` | 被测模型名 |
| `--base-url` | 服务地址（默认 `http://127.0.0.1:8000`） |
| `--concurrency` | 并发数（本教程为 8） |
| `--num-prompts` | 请求总数（100） |
| `--input-len` / `--output-len` | 输入 / 输出 token 数（各 1024） |

### 多档并发对比

要观察负载变化曲线，建议跑多组不同并发（如 1 / 2 / 4 / 8 / 16），逐档记录指标并绘制对比：

```bash
for c in 1 2 4 8 16; do
  benchscope perf --model Qwen2.5-7B --concurrency $c \
    --num-prompts 100 --input-len 1024 --output-len 1024 \
    --name "concurrency-$c"
done
```

## 解读结果

观察输出指标：

- **吞吐**（`output_mean` / `total_mean`）：**越高越好**；
- **TTFT / TPOT / ITL**：**越低越好**；
- 关注实测值与**预期 SLA** 的差距，据此调整并发或服务配置。

```console
Successful requests: 100
Failed requests:     0
Benchmark duration:  45.23s
Output throughput:   112.4 tokens/s (output_mean)
Total throughput:    335.6 tokens/s (total_mean)
TTFT (mean):         92.5 ms
TPOT (mean):         34.2 ms
ITL  (mean):         33.9 ms
```

一个典型的并发增长规律：并发较低时吞吐随并发提升而上升，达到一定并发后进入饱和，随后因排队与争用，TTFT / TPOT 开始恶化——据此可找到系统的**最佳工作区间**。

## 常见问题

**问题：并发越高吞吐越高吗？**
不一定。并发提升会先抬升吞吐，但超过服务承载后会因排队、显存 / 算力争用而下降或延迟恶化。

**问题：如何在网页里看实时曲线？**
并发压测运行中会自动刷新表格与曲线；单并发点内支持连续滚动观察波动。

## 相关文档

- [性能测试](../core/performance.md) — 双模式详解
- [CLI 参考](../get-started/cli.md) — `perf` 完整参数
- [教程：阈值压测](./perf-threshold.md) — 自动求最优并发
