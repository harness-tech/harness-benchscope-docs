---
title: "CLI"
---

# CLI

`benchscope` 命令行把 Web 平台的能力带到终端：启动服务、并发压测、精度评测，全部可通过一条命令完成，并产出与 Web 完全兼容的任务产物。

```text
benchscope [--version] {serve,perf,eval} [子命令选项]
```

- **`benchscope`**（或 `benchscope serve`）：启动 Web 服务，默认在 `http://127.0.0.1:8080` 打开完整平台。
- **`benchscope perf`**：执行一次性能压测（并发 / 阈值双模式），输出吞吐与延迟指标，落盘 `run.json`。
- **`benchscope eval`**：执行一次精度评测（Serving / Native / Mock），输出 accuracy / pass_rate 等指标，落盘 `evals/eval-<时间>/`。

```console
$ benchscope --version
benchscope 1.1.0

# 并发压测：并发 8、输入/输出各 1024 token
$ benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
    --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024

# 精度评测：对已部署服务在 GSM8K 上评测 200 个样本
$ benchscope eval --mode serving --model Qwen2.5-7B \
    --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200
```

所有 CLI 任务产物可打包后在网页 **Datas → Perfs / Evals → 导入备份** 恢复，与 Web 创建的任务完全兼容。

## 相关文档

- [CLI 参考](/zh/docs/cli/reference/) — `serve` / `perf` / `eval` 完整参数表
- [安装](/zh/docs/install/) — 环境要求与启动
- [性能测试](/zh/docs/performance/) — 并发压测与阈值探测
- [精度测试](/zh/docs/accuracy/) — 双模式评测
