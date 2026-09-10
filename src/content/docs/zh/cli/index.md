---
title: "概述"
description: "benchscope 命令行工具总览：serve / perf / eval 子命令说明、快速上手与常见问题。"
---

# 概述

`benchscope` 命令行把 Web 平台的能力带到终端：启动服务、并发压测、精度评测均可通过一条命令完成，并产出与 Web 完全兼容的任务产物。

```text
benchscope {serve,perf,eval} [子命令选项]
```

> CLI 未提供 `--version` 选项；查看版本请使用 `pip show benchscope`，或在 Web 界面访问 `/api/version`。

<div class="info">

**info**：

**向后兼容行为**：当 `benchscope` 无参数、或首个参数是选项（如 `--port 8080`）时，会按「启动服务」的兼容行为执行，等价于 `benchscope serve`。

</div>

## 命令总览

| 命令 | 作用 | 主要产物 |
| --- | --- | --- |
| [`benchscope serve`](/zh/docs/cli/serve/) | 启动 Web 服务，默认在 `http://127.0.0.1:8080` 打开完整平台 | — |
| [`benchscope perf`](/zh/docs/cli/perf/) | 一次性能压测（并发 / 阈值两种模式），输出吞吐与延迟指标 | `run.json` |
| [`benchscope eval`](/zh/docs/cli/eval/) | 一次精度评测（Serving / Native / Mock），输出 accuracy / pass_rate 等指标 | `evals/eval-<时间>/` |

## 快速上手

```console
# 并发压测：并发 8、输入/输出各 1024 token
$ benchscope perf --model Qwen2.5-7B --base-url http://127.0.0.1:8000 \
    --concurrency 8 --num-prompts 100 --input-len 1024 --output-len 1024

# 精度评测：对已部署服务在 GSM8K 上评测 200 个样本
$ benchscope eval --mode serving --model Qwen2.5-7B \
    --base-url http://127.0.0.1:8000 --dataset gsm8k --limit 200

# 查看已安装版本（CLI 未提供 --version 选项）
$ pip show benchscope
```

<div class="tip">

**tip**：

CLI 与 Web 任务产物完全兼容：所有 CLI 产物可打包后在网页 **Datas → Perfs → 导入备份** 恢复，与在网页创建的任务一致。

</div>

## 常见问题

**问题：`benchscope` 不带参数执行会怎样？**
等价于 `benchscope serve`，直接启动 Web 平台。

**问题：产出的任务能在网页里管理吗？**
可以。CLI 产物与网页任务完全兼容：性能产物可在 **Datas → Perfs** 查看、打包导入；精度产物在 **Accuracy 页面**管理。

**问题：如何按需选择命令？**
启动服务用 [`serve`](/zh/docs/cli/serve/)；压测吞吐 / 延迟（含阈值探测）用 [`perf`](/zh/docs/cli/perf/)；评测精度用 [`eval`](/zh/docs/cli/eval/)。

## 相关文档

- [安装](/zh/docs/install/) — 环境要求与启动
- [性能测试](/zh/docs/performance/) — 并发压测与阈值探测
- [性能核心指标](/zh/docs/performance/metrics/) — perf 输出指标口径
- [概述](/zh/docs/accuracy/) — 三模式评测
- [精度核心指标](/zh/docs/accuracy/metrics/) — eval 输出指标口径
- [数据（Datas）](/zh/docs/data/) — 任务产物的查看与导入
